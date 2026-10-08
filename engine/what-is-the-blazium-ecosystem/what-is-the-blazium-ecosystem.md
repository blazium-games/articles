---
title: "The Blazium engine stack"
description: "How the website, Hub, CLI, CDN, editor, and crash reports fit together, from download to a running project."
cover: "assets/cover.png"
slug: "what-is-the-blazium-ecosystem"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

You install Hub. Hub asks the CLI to fetch an editor from the CDN. The editor is the engine. The News tab in Hub is this articles repo, once an article is marked deployed and published.

Hub, the CLI, the crash reporter, and the CDN were built for the Blazium Engine and this ecosystem. Internal game builds use the same CDN downloads and export templates the public gets. Analytics and the in-game bug reporter were built for our example Hangman game and for Demon Lord: Clicker. Hangman shipped on Steam, Discord (as an Embedded App), Google Play, and the Apple App Store. Crash reports that are sent are read to find engine issues and to ship patches for those crashes. The longer map is [The Blazium Games Ecosystem](../the-blazium-games-ecosystem/the-blazium-games-ecosystem.md).

That is the stack people touch. Everything else is a module inside the editor, or a separate repo the CLI and the editor know how to call.

## The map

![The Blazium engine stack: website, CDN, Hub, CLI, editor, crash sidecar. Cerebro is internal.](assets/ecosystem-map.png)

| Box | Job |
|---|---|
| [blazium.app](https://blazium.app) | Download pages, docs, changelog |
| cdn.blazium.app | Editor builds, export templates, CLI, Hub installers, crash sidecar, toolchain catalog, Hub News |
| Hub | Desktop launcher: Projects, Editors, News, Settings. Shells the CLI |
| CLI | Installs editors, registers projects, handles `blazium://` |
| Editor | Blazium `0.6.x` on the `blazium-dev` line (Godot 4.3 compatible). Speaks remote control so the CLI can talk to it |
| Crash sidecar | Shows the dump. Uploads only after you confirm |
| Cerebro | Internal. Release CI publishes catalogs. Hub never calls it. The CLI can, for template metadata, via `BLAZIUM_CEREBRO_URL` |

There is a second engine line, `blazium_4.8`. Hub's own executable is built from that branch. The editors you install from the CDN are whatever channel you picked. This article stays on what `blazium-dev` and the tool repos actually contain.

Published Hub and CLI binaries are Linux and Windows. There is no Flatpak in the download set. [blazium#428](https://github.com/blazium-games/blazium/issues/428) is the open request. Engine docs are [docs.blazium.app](https://docs.blazium.app). The store at [blazium.games](https://blazium.games) is a different product. Uploads there go through `chauffeur`, documented at [docs.blazium.games](https://docs.blazium.games), not through `blazium-cli deploy`.

## Two version numbers

![Godot compatibility line 4.3.2 vs Blazium product line 0.6.x](assets/dual-version.png)

Godot compatibility for `blazium-dev` is 4.3.2. The product you download is Blazium `0.6.x`. A recorded CLI session on one machine showed default editor `0.6.725` under `C:\Users\Bioblaze\AppData\Local\Blazium\Editors`. Export templates install under the Blazium version, not `4.3.2.stable`. Mixing those folders is the usual "templates missing" failure.

## The walk

1. Get Hub from the [dev-tools download page](https://blazium.app/dev-tools/download?tool=hub). Windows is Inno, machine-wide, admin. Linux is a `.deb`. The installer also lays down `blazium-cli` and `crash_reporter`.
2. Hub opens with four tabs.

![Hub tabs: Projects, Editors, News, Settings](assets/hub-tabs.png)

3. Editors tab. Channel `release`, `prerelease`, or `nightly`. Install. The CLI downloads from `cdn.blazium.app` into `{install-path}/{channel}/{version}`.
4. Projects tab. Add a `project.godot`, or scan a folder. Open runs `blazium-cli open`.
5. The editor starts with remote control on port **6508** (unless you turned `enable-on-open` off), so `blazium-cli remote` can reach it.

Replay the CLI side locally:

```text
asciinema play assets/cli-editors.cast
```

![blazium-cli editors, recorded with asciinema](assets/cli-editors.svg)
<!-- ASCIINEMA: assets/cli-editors.cast | blazium-cli editors -->

## The other pieces

- **Crash sidecar.** The engine writes a minidump and a JSON file. A small UI asks you. Nothing leaves the machine until Send. Editor HTTP upload is not implemented. See [Crash reports](../crash-reporter/crash-reporter.md).
- **Analytics.** Off until consent is given. Same app id and build id as crash reports. See [Opt-in analytics](../analytics-opt-in/analytics-opt-in.md).
- **CLI remote and MCP.** Localhost JSON for scripts on port 6508. JustAMCP for agents on port 6506. Autowork is the test runner both can start. See [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).
- **Toolchain.** A GPL-3.0 CLI. The editor spawns it for Interactive DVD (`export/inter_dvd/toolchain`). PS1, PS2, and N64 are terminal commands in that same binary. Compilers are not in `blazium.git`. See [Console toolchain](../blazium-toolchain/blazium-toolchain.md).
- **Web.** A normal editor preset named `Web`, plus the [Docker template](../docker-web-export/docker-web-export.md) if you need Discord `.proxy` paths. Web is not a toolchain target.
- **Multiplayer that compiles on `blazium-dev`.** `ENetServer` / `ENetClient`, WebRTC signaling (`SignalClient`, `WebRTCEnetSession`), and `Discord.create_or_join_lobby`. `LobbyClient`, `LoginClient`, and `MasterServerClient` are not registered classes in this tree. Script templates with those names are still in the editor template folder. They do not run.

## Two meanings of `blazium://`

| Who | Example | Job |
|---|---|---|
| OS / CLI | `blazium://open?path=` | Open Hub or a project. Hub's remote port is **39218** |
| JustAMCP | `blazium://scene/…`, `blazium://tags/dictionary` | MCP resource inside the editor |

Same scheme. Two owners.

## License split

The engine is MIT. `blazium-toolchain` is GPL-3.0-or-later so it can fetch GCC and the console SDKs. The editor process stays MIT and only executes that binary. Fetching the SDK into the engine repo would be the thing the split exists to avoid.

## Next

- [Blazium Hub](../blazium-hub/blazium-hub.md)
- [Blazium CLI](../blazium-cli/blazium-cli.md)
- [Crash reports](../crash-reporter/crash-reporter.md)
- [Download and dev tools](../download-and-dev-tools/download-and-dev-tools.md)

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
