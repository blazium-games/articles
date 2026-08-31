---
title: "Asset tags and search"
description: "Tag resources in the filesystem dock, bake tags into exports, search them from the editor and from MCP."
cover: "assets/cover.png"
slug: "asset-tags-and-semantic-search"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Tag a resource once. Search it later from the dock or from an agent. Two modules: `assettags` (dictionary, sidecars, export bake) and `semanticsearch` (index JustAMCP uses).

![Automation: MCP is one consumer of tags](assets/automation-three.png)

## Tag a resource

Filesystem dock, context menu. Hierarchical names. `AssetTagManager` is the singleton: add, batch, persist. Editor-only module. Sidecar files travel with the resource.

<!-- CAPTURE: assets/tag-add.gif | Editor | Right-click a resource, add a tag, tag visible on the item -->
<!-- CAPTURE: assets/tag-inspector.png | Editor | Tag dictionary UI -->
<!-- CAPTURE: assets/cover.png | Editor | Dock with tags plus search results, 16:9 -->

## Bake

`AssetTagRuntime` writes tags into exported games so runtime code can still query them. If a tag only exists in the editor and never bakes, shipped builds will not see it.

## Search

`SemanticAssetIndex` builds a lexical (and embedding) index from tags and metadata. `find_similar`, filtered queries. Used by JustAMCP semantic tools.

<!-- CAPTURE: assets/semantic-search.gif | Editor | Type a query, ranked assets appear -->

## MCP

Resource URIs: `blazium://tags/…`, `blazium://semantic/…`. Same scheme collision as Hub's OS protocol. Agents talk to JustAMCP, not to `blazium://open`. See [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).
