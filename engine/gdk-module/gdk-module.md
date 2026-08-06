---
title: GDK Module
description: >-
  Microsoft's Game Development Kit straight into the editor, with export
  tooling, live services, and a test suite
cover: assets/cover.jpg
deployed: true
date: 2026-06-27
slug: gdk-module
author: TheKingScott
hosts:
  - name: IndieDB
    url: 'https://www.indiedb.com/engines/blazium-engine/news/gdk-module'
---
# Introducing the GDK Module

![](assets/cover.jpg)

The **GDK Module** is a working integration with Microsoft's Game Development Kit on PC.
It links the engine against GDK runtime libraries, wires in Xbox Services (XSAPI), and adds
a dedicated Xbox export platform with editor tooling. Shipping an Xbox title from Blazium
does not have to be a manual side quest.

## Key Features

- **GDK Runtime Integration**: The engine links against the GDK on PC using `Thunks.dll`, following Microsoft's custom-engine guidance for PC titles.
- **XSAPI Services**: Xbox Services API layer for achievements, presence, leaderboards, stats, and multiplayer activity.
- **Export Platform**: Dedicated Xbox export target with `MicrosoftGame.config` packaging support.
- **Editor Plugin**: GDK tooling lives inside the Blazium editor instead of bolted on from the outside.
- **Tiered Test Suite**: Packaging and toolchain smoke tests run without credentials; live Xbox Live tests gate on environment variables.

## Why Add the GDK Module to Your Blazium Project?

![](assets/gdk.jpg)

Xbox developers get a path from editor to packaged build without leaving the engine:

**For Games**
- **Platform services**: Achievements, stats, presence, and leaderboards through native XSAPI bindings.
- **Xbox export**: Package builds with the Xbox export preset and validated `MicrosoftGame.config`.
- **Sandbox testing**: Run tier-0 tests locally, then enable `LIVE_TESTS=1` for signed-in scenarios.

**For Studios**
- Validate GDK toolchain and packaging in CI without an Xbox dev kit for every check.
- Port existing Xbox sample test coverage through the dedicated test project.
- Keep PC GDK and export tooling in sync with engine updates.

## Documentation & Next Steps

The module is already available in the [latest nightly of Blazium](https://blazium.app/download)
with a dedicated test project. See
[xbox_module_tests](https://github.com/blazium-games/xbox_module_tests)
for validation examples.

The GDK module brings Microsoft's Game Development Kit straight into Blazium on PC.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine/articles)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
