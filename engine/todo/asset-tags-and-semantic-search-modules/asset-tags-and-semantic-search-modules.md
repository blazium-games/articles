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

We did it this way because a tag database beside the project goes stale the moment someone copies the folder. `res://.blazium/asset_tags/tags.json` and `asset_index.json` travel with the project. Commit them if the tags are part of the game. They are not an editor cache.

Godot has no core module for this. Both of ours build only for the editor. A shipped player does not load them. `EditorExportAssetTags` can bake a sidecar at export time. That file is data. It is not the search module running in the game.

![The dock writes JSON. An agent reads it through MCP.](assets/tag-files.png)

![MCP is one consumer](assets/automation-three.png)

## What your agents can call

Enable JustAMCP (`blazium/justamcp/server_enabled`, or `--enable-mcp` from the CLI). The server is port 6506. Tag tools are named `blazium_tags_*`: list, add, remove, rename, set on an asset, find, search, unused, rescan, undo. Semantic tools are `semantic_search`, `semantic_find_similar`, `semantic_index_stats`, and `semantic_rebuild_index`. The prompt `blazium_asset_tagging_workflow` is the walk those tools expect.

That is the surface your agents use to organize, search, and maintain assets without leaving the editor. Search is those tools. It is not a raw read of a random resource path.

## What search is willing to do

The default backend is `lexical`. `embedding` and `hybrid` exist. The default embedding provider is `hash_vector`, which needs no network. `ngram` is local. `http` uses `blazium/semanticsearch/embedding_http_url` and falls back to `hash_vector` if the request fails. There is no Blazium-hosted embedding service. If you set `http`, the URL is yours.

HTTP work is deferred so startup stays responsive, and async search rejects the HTTP provider off the main thread. Changing backend or provider needs an editor restart. The index is `res://.blazium/semantic_index/index.json`.

`semanticsearch` does not build unless `assettags` does.

We validated the dock, the JSON, and the MCP tools in-house, including while Demon Lord: Clicker was exercising the 2D editor. That does not mean a shipped build of that game runs semantic search at runtime. The modules are editor-only.

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
