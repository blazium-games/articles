---
title: "The Blazium engine stack"
description: "How website, Hub, CLI, CDN, editor, and crash reports fit together, from download to a running project."
cover: "assets/cover.png"
slug: "what-is-the-blazium-ecosystem"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

You install Hub. Hub asks CLI to fetch an editor from the CDN. The editor is the engine. The News tab in Hub is this articles repo.

That is the whole stack. Everything else hangs off those four pieces.

## The map

![The Blazium engine stack: website, CDN, Hub, CLI, editor, crash sidecar. Cerebro is internal.](assets/ecosystem-map.png)

| Box | Job |
|---|---|
| blazium.app | Download pages, docs, changelog |
| cdn.blazium.app | Editor builds, export templates, CLI, Hub installers, crash sidecar, Hub News |
| Hub | Desktop launcher: Projects, Editors, News, Settings |
| CLI | The binary Hub shells. Also the OS handler for `blazium://` |
| Editor | Blazium 0.6.x. Speaks `remote_control` so CLI can talk to it |
| Crash sidecar | Shows the dump. Uploads only after you confirm |
| Cerebro | Internal. CI publishes catalogs here. Hub never calls it at runtime |

## Two version numbers

![Godot compatibility line 4.3.2 vs Blazium product line 0.6.x](assets/dual-version.png)

Godot compatibility is `4.3.2` stable. The product you download is Blazium `0.6.x` (current release: `0.6.725`). Export templates install under the Blazium version folder, not `4.3.2.stable`. Mixing those two numbers is the usual "templates missing" failure.

## The walk

1. Get Hub from [blazium.app](https://blazium.app/download) or the installer on `/dev-tools`. Windows is Inno (machine-wide). Linux is a `.deb`.
2. Hub opens with four tabs.

![Hub tabs: Projects, Editors, News, Settings](assets/hub-tabs.png)

<!-- CAPTURE: assets/blazium-app-home.png | Website | blazium.app home or download tab -->
<!-- CAPTURE: assets/hub-annotated.png | Hub | Live window with the four tabs labeled -->

3. Editors tab. Channel `release` or `nightly`. Install. CLI downloads from `cdn.blazium.app` into `%LOCALAPPDATA%\Blazium\Editors\{version}` (Windows).
4. Projects tab. Add a `project.godot`, or Scan a folder. Open.
5. The editor starts with `remote_control` enabled so `blazium-cli remote` can reach it.

<!-- CAPTURE: assets/first-run.gif | Hub | 20-30s: Hub open, install an editor, open a project. Master as mp4, publish gif. -->

Replay the CLI side of that walk locally:

```text
asciinema play assets/cli-editors.cast
```

![blazium-cli editors, recorded with asciinema](assets/cli-editors.svg)
<!-- ASCIINEMA: assets/cli-editors.cast | blazium-cli editors -->

## The other pieces, one sentence each

- **Crash sidecar.** The engine writes a minidump. A small UI asks you. Nothing leaves the machine until Send. See [Crash reports](../crash-reporter/crash-reporter.md).
- **Blazium Services.** `LobbyClient`, `ScriptedLobbyClient`, `LoginClient`, `MasterServerClient` talk HTTP/WebSocket to hosted (or self-hosted) services. See [Blazium Services](../blazium-services/blazium-services.md).
- **CLI remote and MCP.** Localhost JSON for scripts. Model Context Protocol for agents. Autowork is how both prove they work. See [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).
- **Toolchain.** A GPLv3 sidecar the editor spawns for PS1 and Interactive DVD. Never merged into `blazium.git`. See [Console toolchain](../blazium-toolchain/blazium-toolchain.md).

## Two meanings of `blazium://`

| Who | Example | Job |
|---|---|---|
| OS / CLI | `blazium://open?path=…` | Open Hub or a project |
| JustAMCP | `blazium://scene/…` | MCP resource inside the editor |

Same scheme. Two owners. Do not mix them in copy or in tools.

## License split

The engine is MIT. `blazium-toolchain` is GPL-3.0-or-later so it can fetch GCC and SDK zips. The editor only spawns that binary.

## Next

- [Blazium Hub](../blazium-hub/blazium-hub.md)
- [Blazium CLI](../blazium-cli/blazium-cli.md)
- [Crash reports](../crash-reporter/crash-reporter.md)
- [Download and dev tools](../download-and-dev-tools/download-and-dev-tools.md)
