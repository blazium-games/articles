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

A project collects files faster than a folder tree can explain them. We added two editor modules so the explanation lives next to the files, in a format the editor and your AI agents can both read.

**Asset Tags** is the dictionary and the per-file assignments. **Semantic Search** is an index over those tags. Exact lookup and similarity lookup share that index. The editor's MCP server (JustAMCP) exposes both modules so your AI agents can organize, search, and maintain assets without leaving the editor.

Both exist on `blazium-dev`. Both build only when the target is the editor. Semantic Search refuses to build without Asset Tags.

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

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
