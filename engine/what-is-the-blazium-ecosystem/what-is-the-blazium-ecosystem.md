---
title: "The Blazium engine stack"
description: "How the website, CDN, Hub, CLI, editor, and crash sidecar fit together."
cover: "assets/cover.png"
slug: "what-is-the-blazium-ecosystem"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# The Blazium engine stack

### One CDN, a thin launcher, and an editor that is not the launcher

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

You install Hub. Hub asks the CLI to fetch an editor from the CDN. The editor is the engine. News in Hub reads `https://cdn.blazium.app/articles/rss.xml` after a post is marked deployed and the publish workflow has uploaded it.

We split it this way because a full engine deploy should not depend on one person's laptop, and a download should not depend on GitHub being healthy. The website, Hub, and the CLI read `cdn.blazium.app`. The editor's export-template manager still asks `blazium.app` for a mirror list, and that live list points at the GitHub release pack. The CDN copy is what the CLI downloads, and it is what the site code is moving the editor toward.

![The Blazium engine stack](assets/ecosystem-map.png)

| Box | Job |
|---|---|
| [blazium.app](https://blazium.app) | Download pages and docs |
| cdn.blazium.app | Editor builds, export templates, CLI, crash sidecar, toolchain catalog, Hub News |
| Hub | Projects, Editors, News, Settings. Shells the CLI |
| CLI | Installs editors, registers projects, handles `blazium://` |
| Editor | Blazium `0.6.x` on `blazium-dev` (Godot 4.3 compatible) |
| Crash sidecar | Shows the dump. Uploads only after you confirm |
| Cerebro | Internal. Release CI publishes catalogs. Hub never calls it |

![One product, several repositories](assets/repo-split.png)

There is a second engine line, `blazium_4.8`, which tracks Godot 4.8. Hub's own executable, the crash sidecar builds, and the skills tooling track that branch. The editors you install from the CDN are `0.6.x` from `blazium-dev`. As of 11 October 2026 the release catalog is [0.6.838](https://cdn.blazium.app/catalog/versions/release/latest.json) and nightly is 0.6.924. There is no `0.8` build on the CDN yet. CI policy maps 0.8 and 0.9 to the 4.8 line when those versions exist. They do not exist as downloads today.

Published Hub and CLI binaries are Linux and Windows. There is no Flatpak. [blazium#428](https://github.com/blazium-games/blazium/issues/428) is the open request. The store at [blazium.games](https://blazium.games) is a different product. Uploads there go through `blazium-cli games` or the standalone games CLI, not through `blazium-cli deploy`. Steam and itch are `deploy`.

## Two version numbers

![Godot 4.3 line versus Blazium 0.6.x](assets/dual-version.png)

Godot compatibility for `blazium-dev` is 4.3. The product you download is Blazium `0.6.x`. Export templates install under the Blazium version and channel, such as `0.6.838.release`, not `4.3.2.stable`. Mixing those folders is the usual "templates missing" failure. Godot's own mirror list uses `4.x.y.stable` and points at `downloads.godotengine.org`.

## The walk

1. Get Hub from [the dev-tools download](https://blazium.app/dev-tools/download?tool=hub). Windows is Inno, machine-wide, admin. Linux is a `.deb`. The installer also lays down `blazium-cli` and `crash_reporter`.
2. Hub opens with four tabs.

![Hub tabs](assets/hub-tabs.png)

3. Editors tab. Channel `release`, `prerelease`, or `nightly`. Install. The CLI downloads from `cdn.blazium.app` into `{install-path}/{channel}/{version}`.
4. Projects tab. Add a `project.godot`, or scan a folder. Open runs `blazium-cli open`. The version dropdown on the card is drawn and not read. Open uses the CLI default until that is wired.
5. The editor starts with remote control on port **6508** unless `enable_on_open` is off, so `blazium-cli remote` can reach it. JustAMCP, if you enable it, is port **6506**.

![blazium-cli editors](assets/cli-editors.svg)

```text
asciinema play assets/cli-editors.cast
```

## What else is in the editor

Crash reports: the engine writes a minidump and a JSON file. The sidecar asks. Nothing leaves the machine until Send. Editor builds do not HTTP-upload. We read the reports that are sent and patch the engine from them. Analytics is a separate opt-in queue on `/v1/events`. It is not the patch input.

The toolchain is GPL-3.0-or-later so GCC and the console SDKs stay out of the MIT editor. The editor spawns it for Interactive DVD. PS1, PS2, and N64 are terminal commands in that binary. `ps3` and `ps4` exit 2. They are reserved names, not a ship date.

A web export is the preset named `Web`. [docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template) is Nginx for that folder, including Discord's `/.proxy/` path. It is not a toolchain target and it is not the web editor.

`LobbyClient` and `LoginClient` are not registered on `blazium-dev`. They live in [blazium-sdk-module](https://github.com/blazium-games/blazium-sdk-module). `login.blazium.app` answers. The lobby and master-server hostnames in that SDK do not resolve. Game traffic that does compile in the engine is ENet and the Discord Social SDK lobby, which is a different object.

Multiplayer, GIF textures, asset tags, and the streaming clients (Twitch, Kick, IRC, Crowd Control, OBS) are modules in the editor repo. Tags and semantic search are editor-only. GIF is always built.

## Two meanings of blazium://

| Who | Example | Job |
|---|---|---|
| OS / CLI | `blazium://open?path=` | Open a project. Hub's remote port is **39218** |
| JustAMCP | `blazium://scene/…`, `blazium://tags/dictionary` | MCP resource inside the editor |

Same scheme. Two owners. The OS handler is the CLI.

## Links

- Download: https://blazium.app/download
- Dev tools: https://blazium.app/dev-tools
- Engine: https://github.com/blazium-games/blazium
- Hub: https://github.com/blazium-games/blazium-hub
- CLI: https://github.com/blazium-games/blazium-cli
- CDN release pointer: https://cdn.blazium.app/catalog/versions/release/latest.json
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
