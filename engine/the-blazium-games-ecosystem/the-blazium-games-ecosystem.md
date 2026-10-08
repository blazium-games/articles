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

## Why this map exists

The engine README groups what Blazium adds on top of Godot: editor and agent tools, store and platform modules, data modules, live-ops modules, and the older-console path that uses the toolchain. The tool READMEs then split that into separate repos (engine, CLI, Hub, crash sidecar, toolchain) that share `cdn.blazium.app`. Hub, the CLI, the crash reporter, and the CDN were built for the Blazium Engine and this ecosystem. Analytics and the in-game bug reporter were built for our games: the example Hangman game and Demon Lord: Clicker. The [2025 community update](../blazium-community-update-goodbye-2025-lets-conquer-2026/blazium-community-update-goodbye-2025-lets-conquer-2026.md) lists the CLI, the deployment framework, the GitHub Actions, and Hangman as work from that year. The [Discord deploy article](../blazium-deploy-games-on-discord/blazium-deploy-games-on-discord.md) is where the embed work is tied to Hangman running in Discord voice chat. Hangman has since shipped as a Discord app.

## What Blazium Games uses it for

Hub, the CLI, the crash reporter, and the CDN were built for the engine and this ecosystem. Blazium Games reads incoming crash reports to find engine issues and ships patches for those crashes. Analytics, and the in-game bug reporter, were built for the example Hangman game and Demon Lord: Clicker. In Demon Lord: Clicker the bug reporter sends a description, a screenshot, logs, and session details to our backend, with account IDs and PC usernames stripped. The backend links those reports to GitHub issues. That is not the minidump, and it is not a claim about how analytics events are used.

Hangman is our example game, not a commercial title. It shipped on Steam, Discord (as an Embedded App), Google Play, and the Apple App Store. That release is how store export and deploy were checked end to end. It does not say which module each store build called. Internal game builds use the same CDN downloads and export templates the public gets.

Hub CI still bakes crash and analytics endpoints for the Hub binary. The Hub installer can place BlaziumLauncher for the store, while store uploads stay in `chauffeur`. Steam and itch deploys go through `blazium-cli`, not through the store uploader. Interactive DVD export spawns `blazium-toolchain`. The engine README is explicit that the store and the engine are not the same product. A Made with Blazium shelf and an AssetLib URL are the bridges it names. The other modules (GIF, asset tags, remote control, the toolchain, streaming, data formats, Steam, Discord desktop, GDK, JWT) were used in-house to validate the behavior each one implements. That validation is not a list of shipped titles.

## What other projects get

The same CDN catalogs, the same CLI commands, and the same modules on `blazium-dev`. A game does not have to use the Blazium Games store. A store listing does not have to be made with the engine.

This article is the map of why each piece exists. The file-level walk is [The Blazium engine stack](../what-is-the-blazium-ecosystem/what-is-the-blazium-ecosystem.md). The engine line this describes is `blazium-dev` (Godot 4.3 compatible, product version `0.6.x`). Hub's own executable is built from `blazium_4.8`. Do not treat those as one branch.

## The engine

[Blazium](https://github.com/blazium-games/blazium) is the MIT editor and the export templates. Modules that matter for the rest of this page live in that tree on `blazium-dev`: crash reporter, analytics, remote control, JustAMCP, GIF, asset tags, Steam, Discord, the data-format modules, and Interactive DVD. If a class is not registered there, this article does not call it a feature.

## Crash reporter and analytics

The crash reporter writes a Breakpad minidump and a JSON file, then a sidecar asks before anything is uploaded. Analytics is a second module on the same app id and a build id, and it stays silent until consent is given. Hub CI bakes both at `https://crash.blazium.app` (`/v1/reports` and `/v1/events`). The commits that add them are quoted in [Crash Reporter & Analytics](../crash-reporter-and-analytics/crash-reporter-and-analytics.md).

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

## What is not an engine node on this line

Lobby, scripted lobby, login, and master-server clients show up as GDScript templates under `modules/gdscript/editor/script_templates/`. The classes they extend are not registered on `blazium-dev`. Networking you can compile is ENet (`ENetServer`, `ENetClient`), the WebRTC signaling client (`SignalClient`, `WebRTCEnetSession` in `games_enet_webrtc`), and Discord's own `create_or_join_lobby`. The services draft that names those missing nodes is unchanged. It is not the API.

Other gaps that are explicit in the repos, not dates:

- Crash reporting compiles on Windows and Linux/BSD only.
- Hub installers and published CLI binaries are Linux and Windows. [blazium#428](https://github.com/blazium-games/blazium/issues/428) asks for a Flatpak. There is no package yet.
- `ps3` and `ps4` in the toolchain exit `2`.
- The Steam module has no leaderboard methods. [blazium#807](https://github.com/blazium-games/blazium/issues/807) asks for them.
- The Hub project card has a version control in the scene. Open does not read it.

Engine docs: [docs.blazium.app](https://docs.blazium.app). Downloads: [blazium.app](https://blazium.app).

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
