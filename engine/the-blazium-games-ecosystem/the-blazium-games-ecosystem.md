---
title: "Why the Blazium tools are separate repositories"
description: "The editor is MIT. Hub, the CLI, the crash sidecar, and the toolchain are separate repos that share one CDN."
cover: "assets/cover.png"
slug: "the-blazium-games-ecosystem"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Why the Blazium tools are separate repositories

### The editor should not have to be the download server

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

The engine README groups what Blazium adds on top of Godot: editor and agent tools, store and platform modules, data modules, live-ops modules, and the older-console path. Those features do not all belong in one git tree. The editor is MIT and is the thing you ship a game with. The CLI installs that editor. Hub is a window over the CLI. The crash sidecar asks before a dump is uploaded. The toolchain is GPL-3.0-or-later because the compilers it fetches are not MIT. Putting GCC into `blazium.git` would have been the mistake the split exists to avoid.

They share `cdn.blazium.app` so a download does not depend on GitHub. The website, Hub, and the CLI read that host. The editor's template manager still uses the GitHub release pack, because the live mirror list has not switched over to the CDN entry in `details.json` yet.

![Repositories around the editor](assets/repo-split.png)

![What talks to what](assets/ecosystem-map.png)

## What we actually use them for

Hub, the CLI, the CDN, and the crash reporter exist for the engine. We read crash reports that are sent and we patch the engine from them. Analytics is a separate opt-in queue. It is not the patch input.

Hangman is the example game. It shipped on Steam, as a Discord Embedded App, on Google Play, and on the Apple App Store. The Discord embed work started so that game could run inside a voice channel. Those four storefronts are how export and deploy were checked. Demon Lord: Clicker was built in part to validate the newer tools, modules, and the 2D side.

In 2025 we also shipped the CLI, the deploy commands, and the GitHub Actions. The actions are four repositories: setup-blazium-cli, setup-blazium-engine, export-blazium-game, and deploy-blazium-game. Steam and itch reusable workflows in the deploy repo are deprecated in favor of `blazium-cli deploy`.

## Two lines, on purpose

`blazium-dev` is the Godot 4.3 line. The editors on the CDN are `0.6.x` from that branch. As of 11 October 2026, release is 0.6.838 and nightly is 0.6.924. `blazium_4.8` is the Godot 4.8 line. Hub's executable and the crash sidecar builds track it. There is no 0.8 download on the CDN yet. CI knows how to map 0.8 and 0.9 onto that line when those versions exist.

The store at [blazium.games](https://blazium.games) is not the engine and not Hub. A game on the store does not have to be made with Blazium. Uploads are `blazium-cli games` or the standalone games CLI.

`LobbyClient` is not in the engine tree. It is in [blazium-sdk-module](https://github.com/blazium-games/blazium-sdk-module). `login.blazium.app` answers. The lobby hostname that SDK defaults to does not resolve. Web export hosting for a Discord activity is [docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template), which is Nginx, not the web editor.

There is a public board at the [Blazium Community Roadmap](https://github.com/orgs/blazium-games/projects/1). I did not find a single TODO file in the Hub, CLI, or toolchain repos that lists the rest of this as a dated plan. Reserved names in code are the honest "not yet": `ps3` and `ps4` exit 2, Steam leaderboards are [issue 807](https://github.com/blazium-games/blazium/issues/807), and the project-card version dropdown in Hub is drawn and not read.

## Links

- Engine: https://github.com/blazium-games/blazium
- Hub: https://github.com/blazium-games/blazium-hub
- CLI: https://github.com/blazium-games/blazium-cli
- CDN release pointer: https://cdn.blazium.app/catalog/versions/release/latest.json
- Download: https://blazium.app/download
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
