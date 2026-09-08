---
title: "Asset Tags & Semantic Search Modules"
description: >-
    A modern, agent-friendly asset management layer that remains fully under the
    control of the engine and the project’s own tag dictionary.
cover: "assets/cover.png"
slug: "asset-tags-and-semantic-search-modules"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---
# Asset Tags & Semantic Search

Introducing two closely related modules, **Asset Tags** and **Semantic Search**, that give projects a
structured way to organize and find assets.

Asset Tags provides a hierarchical tagging system, while Semantic Search builds a fast index over
those tags so both exact and similarity-based queries are quick and reliable.
The editor’s MCP server exposes both modules to AI agents, letting them organize, search, and
maintain assets without leaving the editor.

## The Asset Tags Module

The Asset Tags module maintains a project-wide tag dictionary and tracks which assets use which tags.

<!-- image showing the tag manager window -->

Tags are hierarchical (for example `character/enemy/boss`), and matching is parent-aware:
searching for `character` also returns assets tagged more specifically under that path.
Optional strict modes can reject unknown tags or invalid paths, and a configurable list of
file extensions determines what can be tagged.

<!-- image showing a tag search in the filesystem dock -->

Data is stored in sidecar files with recovery mechanisms for corrupted dictionaries, and batch operations keep the editor responsive while allowing atomic updates across multiple assets.

## The Semantic Search Module

Semantic Search builds a lightweight, persistent index over asset tags and metadata.
The index stays in sync with the Asset Tags registry through rebuilds or incremental updates,
ensuring both modules remain consistent.
This design keeps queries fast whether you’re looking for exact matches or similar assets.

## Integration with the editor MCP

JustAMCP, Blazium’s MCP server, exposes dedicated tool sets for both modules.
Agents can create and manage tag hierarchies, assign or remove tags from assets, run hierarchical
or similarity searches, generate unused-tag reports, and rebuild the index.

<!-- image showing the ai chat using the mcp -->

A ready-made workflow prompt is also available to guide agents through safe, step-by-step tagging.
Because the tools operate on the same live systems used by the editor UI, any changes an agent makes
appear immediately in the Asset Tags panel, FileSystem context menus, and active searches.
Tag updates automatically keep the semantic index consistent, or an explicit rebuild can be
triggered when needed.

## Next Steps

Both modules are available in the [latest nightly of Blazium](https://blazium.app/download).

Together with JustAMCP, Asset Tags and Semantic Search give projects a modern, agent-friendly
asset management layer that remains fully under the control of the engine and the project’s
own tag dictionary.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**