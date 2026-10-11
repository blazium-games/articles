---
title: "Why asset tags live in the project"
description: "The tag dictionary is JSON under res://.blazium. Editor-only modules expose it to the dock and to your agents through JustAMCP."
cover: "assets/cover.png"
slug: "asset-tags-and-semantic-search-modules"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Why asset tags live in the project

### Agents search the files you committed, not a database that drifted

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

The commit that added asset tags, semantic search, and the JustAMCP tools lists the pieces: a filesystem **Edit Asset Tags** action, a Project Settings **Asset Tags** tab, a search bridge, MCP tools, and deferred prune plus HTTP embedding so editor startup stays responsive. The 0.6.725 notes describe JustAMCP as the editor MCP server agents use to create and modify a project. Tags are one of the tool sets on that server.

We did it this way because a tag database beside the project goes stale the moment someone copies the folder. `res://.blazium/asset_tags/tags.json` and `asset_index.json` travel with the project. Commit them if the tags are part of the game. They are not an editor cache. The semantic index under `res://.blazium/semantic_index/` is rebuildable from tags and asset metadata; the dictionary and asset index are the durable inputs you should review in git.

Godot has no core module for this. Both of ours build only for the editor. A shipped player does not load them. `EditorExportAssetTags` can bake a sidecar at export time. That file is data. It is not the search module running in the game.

![The dock writes JSON. An agent reads it through MCP.](assets/tag-files.png)

![MCP is one consumer](assets/automation-three.png)

## Storage layout

`AssetTagStorage::get_storage_dir()` returns `res://.blazium/asset_tags`. Inside that directory:

| File / dir | Role |
|---|---|
| `tags.json` | Dictionary: tag names, comments, redirects |
| `asset_index.json` | Path → tag list |
| dirty sidecars under the index dirty dir | Per-path merges before compact |

Writes go through atomic helpers with rollback backups. Corrupt dictionary or index files are quarantined rather than silently trusted. `commit_dictionary_and_index` updates both payloads together when a coordinated mutation needs that guarantee. `AssetTagSerializer` is the JSON shape; `AssetTagSidecarIO` encodes per-path dirty names and applies them on load.

`AssetTagRuntime` keeps a process cache of the index for export bake and dirty-sidecar refresh. `invalidate_cache` / `notify_sidecar_dirty` keep that cache honest when the editor mutates storage.

## Indexing and reverse lookup

`AssetTagRegistry` owns the in-memory `asset_index` map and a reverse lookup from tag → paths. Mutations (`set_tags_for_asset`, `add_tags_to_asset`, `remove_tags_from_asset`, `rename_asset_path`, `apply_tag_rename`, `apply_tag_remove`) snapshot the index, apply, rebuild reverse entries, and persist. Batches (`begin_batch` / `commit_batch` / `abort_batch`) nest so MCP batch assign and UI multi-select do not rewrite the full file for every path.

Prune is deferred. `schedule_prune_removed_paths` debounces a scan that drops index entries whose files no longer exist. That keeps editor startup off the filesystem walk. `rescan` rebuilds reverse lookup from the current index and saves.

Hierarchy lives in `AssetTagHierarchy`: prefix match, rename remap, dedup. Strictness knobs are Project Settings only (`blazium/assettags/strict_paths`, `strict_tags`, `taggable_extensions`); the dictionary UI itself is the Project Settings **Asset Tags** tab, not a separate settings dump of tag names.

## Semantic index architecture

`semanticsearch` declares a hard dependency on `assettags` in `config.py`. It does not build for export templates. The semantic store is `res://.blazium/semantic_index/index.json`.

`SemanticSearchBackendFactory` picks `lexical`, `embedding`, or `hybrid`. Embedding providers are `hash_vector`, `ngram`, and `http`. Session backends are invalidated when settings change; `backend` and `embedding_provider` require an editor restart. HTTP embedding stays locked until the first project scan finishes, then unlocks deferred so startup does not block on a network round-trip. Failed or unavailable HTTP calls fall back to `hash_vector` and mark `used_fallback`.

Async workers:

- `SemanticAsyncSearchWorker` — job TTL from `blazium/semanticsearch/async_job_ttl_ms` (default 1800000). Rejects HTTP provider off the main thread.
- `SemanticAsyncEmbedWorker` — refresh/stale refresh; also refuses HTTP for async embed refresh. Concurrent job caps come from `max_concurrent_async_jobs` (default 8).

`SemanticAssetIndex` exposes filtered lexical search, embedding/hybrid search, similarity, stats (`configured_backend`, `effective_backend`, stale embedding counts), and rebuild. Rank fusion sits behind the hybrid path.

## What MCP sees

Enable JustAMCP (`blazium/justamcp/server_enabled`, or `--enable-mcp` from the CLI). The server is port 6506. Tag tools are registered as `blazium_` + short name (`blazium_tags_list`, `blazium_tags_add`, …). Mutating tools—including dictionary changes, asset assignments, batches, and comment updates—require elicitation unless `confirmed=true`. Semantic tools are `blazium_semantic_search`, `blazium_semantic_find_similar`, `blazium_semantic_index_stats`, `blazium_semantic_rebuild_index`, and the prefixed async enqueue/poll/cancel trio. Resource URIs under `blazium://tags/...` and `blazium://semantic/...` are read helpers; the prompt `blazium_asset_tagging_workflow` tells agents not to treat a raw `resources/read` as search.

That is the surface your agents use to organize, search, and maintain assets without leaving the editor. Search is those tools. It is not a raw read of a random resource path.

## Export bake vs runtime modules

`EditorExportAssetTags` calls `AssetTagRuntime.bake_tags_for_export`. The bake copies a temporary sidecar tree into the export output's `.blazium/asset_tags/`. `read_tags_for_export_bake` can read those files later. None of that loads `AssetTagManager`, `SemanticAssetIndex`, or JustAMCP into a shipped player. Editor-only `can_build` is the gate.

## Why this shape

A SQLite or LevelDB beside `.godot/` would be invisible to git, easy to omit from a zip, and useless to an agent that only sees the project tree. JSON under `res://.blazium` is reviewable, mergeable, and the same bytes the MCP tools mutate. Deferred prune and deferred HTTP unlock keep that choice from taxing editor open.

We validated the dock, the JSON, and the MCP tools in-house. Demon Lord: Clicker separately exercised the newer tools and 2D editor, but that does not mean the shipped game runs semantic search at runtime. These modules are editor-only.

## Persistence failure modes

Index writes can fail mid-batch. The storage layer keeps rollback backups for dictionary and index payloads, quarantines corrupt JSON instead of loading it as empty success, and can quarantine malformed dirty sidecars. `save_index_merge` and dirty-sidecar apply exist so a large project does not rewrite the entire `asset_index.json` for one path change. `compact_index_sidecars` folds dirties back into the main file when a full rewrite is cheap again.

Coordinator undo snapshots both dictionary and index so `blazium_tags_undo_last_change` / the dock undo path restore a consistent pair. That is why MCP mutations go through the coordinator when available rather than poking JSON on disk.

## Limits that are in the source

- No Blazium-hosted embedding endpoint.
- HTTP async search and async embed refresh are rejected; use lexical or a local provider for background jobs.
- Changing backend/provider needs restart.
- Export bake is data only; do not expect `blazium_semantic_search` in a player.
- Dirty sidecars exist so partial index writes survive crashes; compact clears them when the full index is rewritten.
- `assettags` / `semanticsearch` `can_build` is editor-only; there is no template SCons flag that smuggles them into a player.
- Tag tool schemas register under category `asset_tags_tools`; per-tool enable flags live in Editor Settings via the schema builder.
- Semantic tool schemas register under `semantic_search_tools`; async job TTL and concurrency are Project Settings, not MCP arguments.
- Runtime cache invalidation is mandatory after dictionary redirect changes; `AssetTagRegistry` hooks redirect updates to `AssetTagRuntime::invalidate_cache`.
- JustAMCP resource reads under `blazium://semantic/...` redirect agents toward `blazium_semantic_search` instead of treating search as a plain `resources/read`.
- Hybrid mode combines lexical and embedding ranks; if embeddings are stale, stats will show it before search quality collapses silently. Rebuild before blaming MCP.

## Links

- assettags: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/assettags
- semanticsearch: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/semanticsearch
- JustAMCP: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/justamcp
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
