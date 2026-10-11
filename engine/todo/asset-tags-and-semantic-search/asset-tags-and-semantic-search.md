---
title: "Asset tags and search"
description: "Tag files in the project, bake a sidecar on export, and let an agent search them through JustAMCP."
cover: "assets/cover.png"
slug: "asset-tags-and-semantic-search"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Asset tags and search

### The dictionary lives in the project, not in a sidecar database

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

An agent that cannot find the tree texture will invent a path. We added asset tags so the dictionary is JSON in the project, the filesystem dock can edit it, and JustAMCP can search it. `semanticsearch` sits on top of that index. Both modules are editor-only. A shipped game does not load them.

Godot has no equivalent in core. We used the pair in-house, including on Demon Lord: Clicker while we were validating the 2D tools, to confirm the dock, the JSON, and the MCP tools stayed in sync. That is a validation pass. It does not mean a shipped player runs the search module.

![Tags are one thing an agent can call](assets/automation-three.png)

![Where the files live](assets/tag-files.png)

## Use it

1. Project Settings, tab **Asset Tags**. Add a name. The placeholder in the editor is `Environment.Nature.Tree`. Comment, rename, and remove are on that tab. **Cleanup Unused** drops dictionary names nothing references.
2. FileSystem dock, select the file, context menu **Edit Asset Tags...**. Apply writes the assignment. Multi-select applies only the tags you add or remove, to every selected file.
3. Commit `res://.blazium/asset_tags/tags.json` and `asset_index.json` if the tags belong to the project. They are not an editor cache.
4. For an agent, enable JustAMCP and call the tools below. Search goes through the semantic tools, not a raw file read.

`config.py` limits both modules to editor builds. `semanticsearch` does not build unless `assettags` does. `EditorExportAssetTags` can bake tag data into the export. That bake is a file the export plugin writes. It is not the editor module running in the player.

## Classes

`AssetTagManager` is the dictionary (add, rename, comment, batch, save). `AssetTagRegistry` is the path-to-tags index (`add_tags_to_asset`, `find_assets_by_tag`, `search_assets`). `AssetTagCoordinator` wraps a change so the filesystem dock can undo it. They are created in the editor init callback, not as `Engine` singletons you grab from gameplay code. `AssetTagRuntime` is registered so the export plugin can call `bake_tags_for_export` and `read_tags_for_export_bake`.

## Search

Backends that exist today are `lexical` (the default), `embedding`, and `hybrid`. Embedding providers are `hash_vector` (the default), `ngram`, and `http`. HTTP uses `blazium/semanticsearch/embedding_http_url` and falls back to `hash_vector` when the request fails. There is no hosted embedding service in the Blazium repos. If you set `http`, you bring the URL.

HTTP embedding is deferred off the startup path so the editor stays responsive. Async search rejects the HTTP provider off the main thread. Changing `backend` or `embedding_provider` needs an editor restart.

The index file is `res://.blazium/semantic_index/index.json`.

## MCP tools

JustAMCP exposes `blazium_tags_list`, `blazium_tags_add`, `blazium_tags_remove`, `blazium_tags_rename`, `blazium_tags_set_on_asset`, `blazium_tags_find_assets`, `blazium_tags_search_assets`, `blazium_tags_get_unused`, `blazium_tags_rescan`, and `blazium_tags_undo_last_change`, among the rest of the `blazium_tags_*` set. Semantic tools include `semantic_search`, `semantic_find_similar`, `semantic_index_stats`, and `semantic_rebuild_index`. The prompt `blazium_asset_tagging_workflow` is the tagging walk. Those tools are how your agents organize and search assets without leaving the editor.

The server listens on port 6506 when `blazium/justamcp/server_enabled` is on, or when the CLI passes `--enable-mcp`.

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
