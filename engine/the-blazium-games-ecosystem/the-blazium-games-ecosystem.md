---
title: "The Blazium Games Ecosystem"
description: "How the engine, Hub, CLI, CDN, toolchain, and crash reporter fit together on the blazium-dev line."
cover: "assets/cover.png"
slug: "the-blazium-games-ecosystem"
deployed: false
date: "2026-09-08"
author: "sshiiden"
hosts: []
---

# The Blazium Games Ecosystem

Project Hangman needed more than an editor binary. It needed a place to download a known build, a way to open that project again next week, a crash dump that did not upload itself, and a web build Discord would actually load. Those needs turned into separate tools. They share a CDN and a CLI. They do not share one repo.

This article is the map of why each piece exists. The file-level walk is [The Blazium engine stack](../what-is-the-blazium-ecosystem/what-is-the-blazium-ecosystem.md). The engine line this describes is `blazium-dev` (Godot 4.3 compatible, product version `0.6.x`). Hub's own executable is built from `blazium_4.8`. Do not treat those as one branch.

## The engine

[Blazium](https://github.com/blazium-games/blazium) is the MIT editor and the export templates. Modules that matter for the rest of this page live in that tree on `blazium-dev`: crash reporter, analytics, remote control, JustAMCP, GIF, asset tags, Steam, Discord, the data-format modules, and Interactive DVD. If a class is not registered there, this article does not call it a feature.

## Crash reporter and analytics

We wanted dumps before we wanted charts. The crash reporter writes a Breakpad minidump and a JSON file, then a sidecar asks before anything is uploaded. Analytics is a second module on the same app id and build id, and it stays silent until consent is given. Hub CI bakes both at `https://crash.blazium.app` (`/v1/reports` and `/v1/events`).

[Crash Reporter & Analytics](../crash-reporter-and-analytics/crash-reporter-and-analytics.md).

## Hub and CLI

Hub is the window. The CLI is the program that installs editors, registers projects, and opens them. The Hub installer is also how most people get the CLI: one setup, three binaries (Hub, `blazium-cli`, crash sidecar). CI uses the CLI without Hub.

Deep links (`blazium://`) are registered to the CLI. Hub listens on loopback port 39218. The token file is `hub_remote.json`. Leave it alone.

[Blazium Hub & Blazium CLI](../blazium-hub-and-cli/blazium-hub-and-cli.md).

## CDN

`cdn.blazium.app` is the public bucket: editor zips, export templates, `cli.json`, Hub installers, the crash sidecar catalog, the toolchain catalog, and Hub News. Release CI fills it. Hub only reads that host. The CLI will also ask `blazium.app` for template metadata when the CDN manifests are missing.

Templates follow the Blazium version (`0.6.x`), not a Godot `4.3.2.stable` directory. [Export templates and the CDN](../export-templates-and-cdn/export-templates-and-cdn.md).

## Toolchain

Console compilers are GPL or otherwise not MIT. They live in [blazium-toolchain](https://github.com/blazium-games/blazium-toolchain), which the editor spawns for Interactive DVD and which you run yourself for PS1, PS2, and N64. `ps3` and `ps4` exit 2. They are not a hidden shipping target.

Web export is not part of that CLI. It is the editor preset `Web`, and optionally the Docker template when Discord needs `/.proxy/`. Windows screensaver and live wallpaper are engine export platforms (`screensaver`, `livewallpaper`), also not the toolchain.

[The Blazium Toolchain](../the-blazium-toolchain/the-blazium-toolchain.md).

## GitHub Actions

Four repositories, not a folder in this articles checkout:

- [setup-blazium-cli](https://github.com/blazium-games/setup-blazium-cli) at `v0.2.1`
- [setup-blazium-engine](https://github.com/blazium-games/setup-blazium-engine) at `v0.3.0`
- [export-blazium-game](https://github.com/blazium-games/export-blazium-game) at `v0.3.2`
- [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game) at `v0.0.2`

Pin the tag you intend to run. `version: latest` on setup-engine tracks the nightly channel. [GitHub Actions for Blazium](../github-actions-for-blazium/github-actions-for-blazium.md).

## What we did not ship as engine nodes

Lobby, scripted lobby, login, and master-server clients show up as GDScript templates under `modules/gdscript/editor/script_templates/`. The classes they extend are not registered in `blazium-dev`. Networking you can compile is ENet (`ENetServer`, `ENetClient`), the WebRTC signaling client (`SignalClient`, `WebRTCEnetSession` in `games_enet_webrtc`), and Discord's own `create_or_join_lobby`. The draft that describes the missing nodes is left as it was. Do not treat it as the API.

## Where to start

Install Hub if you are making a game on a desktop. Install the CLI if you are writing a script. Export `Web` and use the Docker template if the game has to run inside Discord. Read the crash article before you turn uploads on.

[blazium.app](https://blazium.app) · [Discord](https://blazium.app/chat)

---

- **[Discord](https://blazium.app/chat)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
