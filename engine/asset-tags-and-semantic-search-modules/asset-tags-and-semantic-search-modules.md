---
title: "Asset Tags & Semantic Search Modules"
description: "Two editor modules that keep a project's tag dictionary in the project, and let your AI agents search it."
cover: "assets/cover.png"
slug: "asset-tags-and-semantic-search-modules"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---

# Asset Tags & Semantic Search

## Why we built it

The commit "Add AssetTags, SemanticSearch, and JustAMCP MCP integration" lists the pieces: FileSystem **Edit Asset Tags**, a Project Settings **Asset Tags** tab, a semantic search bridge, JustAMCP tools, and deferred prune plus HTTP embedding "so editor startup stays responsive." The release notes for 0.6.725 describe JustAMCP as the editor MCP server agents use to create and modify a project. Asset tags are one of the tool sets on that server. The commit does not name a content pipeline or a game.

## What Blazium Games uses it for

No engine commit, README, or issue read for this pass names a Blazium Games project that commits `res://.blazium/asset_tags/`.

<!-- QUESTION FOR BIOBLAZE: Does a first-party project, an art pipeline, or Demon Lord: Clicker commit asset tags, or is the module only the editor and JustAMCP surface described in that commit? -->

## What other projects get

The dictionary is JSON in the project. The dock writes it. An agent calls `blazium_tags_*` and `blazium_semantic_search` on the same data. Search backends that ship are local (`lexical`, `hash_vector`, `ngram`) unless you set an HTTP URL yourself. A failed HTTP request falls back to `hash_vector`.

A project collects files faster than a folder tree can explain them. The two editor modules keep that explanation next to the files, in a format the editor and an agent can both read.

**Asset Tags** is the dictionary and the per-file assignments. **Semantic Search** is an index over those tags. Exact lookup and similarity lookup share that index. The editor's MCP server (JustAMCP) exposes both modules so your AI agents can organize, search, and maintain assets without leaving the editor.

Both exist on `blazium-dev`. Both build only when the target is the editor. Semantic Search refuses to build without Asset Tags. A running export does not include either module. `EditorExportAssetTags` bakes what the build needs at export time.

Search that ships today is local unless you point `blazium/semanticsearch/embedding_http_url` at a server you run. The `http` provider falls back to `hash_vector` on failure. There is no Blazium-hosted embedding endpoint in these repos. Changing backend or provider needs an editor restart. `scan_filesystem` defaults to false, so the index does not walk the project until that is on or an agent asks for a rebuild.

## What you edit

The filesystem dock context menu tags the resource under the cursor. The Project Settings "Asset Tags" tab is the dictionary: names, comments, renames. Storage is plain JSON in the project, not a hidden editor cache:

- `res://.blazium/asset_tags/tags.json`
- `res://.blazium/asset_tags/asset_index.json`

Commit those files if the tags are part of the project. `blazium/assettags/strict_tags` rejects a name that is not in the dictionary. `blazium/assettags/strict_paths` rejects a path that is not on disk. `blazium/assettags/taggable_extensions` is the extension list the dock will offer.

`AssetTagCoordinator` batches a change so undo works. The classes are editor objects. Gameplay code does not own them. On export, `EditorExportAssetTags` bakes the tags the build needs. The running game does not include the module.

## What search does

`SemanticAssetIndex` is what JustAMCP calls. The default backend is lexical: tag tokens, no network. Set `blazium/semanticsearch/backend` to `embedding` or `hybrid` when you want a vector. Providers are `hash_vector` (default, local), `ngram`, and `http`. An empty HTTP URL or a failed request falls back to `hash_vector`. Changing the backend or the provider requires an editor restart.

`scan_filesystem` defaults to false, so the index does not walk the project until you turn that on or an agent asks for a rebuild.

## What an agent can call

Your AI agents use the JustAMCP tools, not a private socket:

| Tool | Job |
|---|---|
| `blazium_tags_list` | Dictionary |
| `blazium_tags_set_on_asset` | Assign tags |
| `blazium_tags_find_assets` | Exact tag |
| `blazium_tags_search_assets` | Tag query |
| `semantic_search` / `blazium_semantic_search` | Index query |
| `blazium_asset_tagging_workflow` | Prompt that walks the steps |

`blazium://tags/dictionary` is the MCP resource for the same dictionary. The how-to with settings and limits is [Asset tags and search](../asset-tags-and-semantic-search/asset-tags-and-semantic-search.md). The server those tools sit on is [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).

## Why it stays in-engine

A sidecar database would drift from the files the moment someone renames a texture outside the tool. The dictionary is a JSON file beside the assets, the dock writes it, and the agent reads the same file through MCP. That is the whole loop.

The running game does not get the modules. Export baking is the only path into a build, and only for tags the export plugin wrote. HTTP embeddings are a URL you supply. There is no hosted index to wait on. The settings, the dock labels, and the failure cases are in [Asset tags and search](../asset-tags-and-semantic-search/asset-tags-and-semantic-search.md). Engine docs: [docs.blazium.app](https://docs.blazium.app).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
