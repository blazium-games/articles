---
title: "Blazium Hub & Blazium CLI"
description: "Why Hub and the CLI exist, and how the installer makes the CLI the easy path."
cover: "assets/cover.png"
slug: "blazium-hub-and-cli"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---

# Blazium Hub & Blazium CLI

## Why we built it

The CLI README describes the job: install editors, keep a project registry, update the binary, remote-control a running editor, and deploy to Steam or itch.io. The Hub README describes the window on top of that: browse CDN catalogs, and send install, open, and project changes through the CLI, including `blazium://` links. In 2025 Blazium also shipped the CLI, an open-source deployment framework, and GitHub Actions, next to the example Hangman game. That list does not say Hangman is why the CLI exists.

## What Blazium Games uses it for

Hub and the CLI were built for the Blazium Engine and the ecosystem around it. They are how editors get installed, projects get opened, and `blazium://` links get handled. They were not built as the Blazium Games store client.

Hub's installer can download BlaziumLauncher into `{autopf}\Blazium\Games`. Store links go to that launcher, not to Hub. Uploads to the Blazium Games store stay in `chauffeur` (`@blazium-games/cli`), documented at [docs.blazium.games](https://docs.blazium.games). The CLI's own deploy path is Steam and itch.io. `deploy-blazium-game` marks those two reusable workflows deprecated in favor of `blazium-cli deploy steam` and `blazium-cli deploy itch`.

Our example game, Hangman, shipped on Steam, Discord, Google Play, and the Apple App Store. That release is how export and deploy were checked end to end. It does not say which CLI flags or Action inputs each store build used.

## What other projects get

The same installer lays down Hub, `blazium-cli`, and the crash sidecar. The same commands run in a terminal and in `setup-blazium-engine`. A project registry in `hub.json` is shared by Hub and the CLI, so a project added in one shows up in the other.

**Blazium Hub** is the window. **Blazium CLI** is the program that installs, registers, and launches. Hub is a front end for the CLI. The CLI also runs on its own, which is what scripts and GitHub Actions call.

## Why the installer bundles the CLI

Downloading Hub is the install path that also installs the CLI. The Windows Inno setup and the Linux `.deb` put three binaries down together: Hub, `blazium-cli`, and the crash sidecar. You do not hunt for a second download to get a working `PATH` entry. That is the point of the bundle. People who already live in a terminal can still take the CLI alone from npm (`@blazium-engine/cli`), GitHub Releases, or `https://cdn.blazium.app/cli/cli.json`.

Hub: [blazium.app/dev-tools/download?tool=hub](https://blazium.app/dev-tools/download?tool=hub)

CLI only: [blazium.app/dev-tools/download?tool=cli](https://blazium.app/dev-tools/download?tool=cli)

## What Hub is for

Hub lists projects and editor builds in one window. Scan a folder for `project.godot`. Favorite pins a card. Remove drops it from the registry. The card scene has a version `OptionButton`. The open path is still `HubCli.open_project_async(path)`, so that control is not consulted. There is no Hub issue that schedules wiring it. The editor you get is the CLI default until you run `blazium-cli editors default`. Custom local binaries show up after `blazium-cli editors add`.

The News tab reads `https://cdn.blazium.app/articles/rss.xml` and renders the post in the window. You do not need a browser to see what shipped.

Everything that changes disk goes through the CLI. Hub and the CLI share `%APPDATA%\blazium\hub.json` (or `~/.config/blazium/hub.json`). If the registry is right in one, it is right in the other.

The window has four tabs: Projects, Editors, News, and Settings. On Windows a tray icon stays up after you close the window. Hub listens on loopback port 39218. The token file is `hub_remote.json`. Leave it alone.

## What the CLI is for

The CLI downloads editor builds and export templates, registers projects, and opens them. Channels are `release`, `prerelease`, and `nightly`. A version lives at `{install-path}/{channel}/{version}`.

```text
blazium-cli install 0.6.725 --templates
blazium-cli projects add ./MyProject
blazium-cli open ./MyProject
```

`open` starts the editor and, by default, turns on remote control so a later `blazium-cli remote` command can reach that window. `run` starts the game instead, and leaves remote control off.

Deep links use the `blazium://` scheme. The OS handler is the CLI, not Hub. `blazium://open?path=` opens a project. `blazium://install?version=` installs an editor. `blazium://hub` focuses Hub over the loopback port the installer wrote into `hub_remote.json`. Leave that file alone.

When the editor was built with the Remote Control module, `blazium-cli remote` can query status, run a command, read logs, and kick Autowork without clicking the UI. The editor listens on `127.0.0.1:6508`. `allow_eval` defaults to false. Usual calls are `blazium-cli remote status`, `remote exec`, `remote logs`, and `remote autowork run --wait`. Blazium Games used that path in-house to validate editor automation.

Other commands on the same binary: `editors`, `templates`, `update apply --product cli|hub|crash_reporter|launcher`, `deploy steam`, and `deploy itch`.

## Why both

Hub is how a person picks a version and a project. The CLI is how that choice is repeatable: the same flags in a terminal, in a deep link, and in `setup-blazium-engine`. We did not want a launcher that hides a private install format. If Hub can do it, the CLI command is the thing that happened.

## What is actually shipping

Published CLI binaries and the Hub installers are Linux and Windows. A macOS CLI binary is not in the release set. You can still build the CLI on macOS and have it install a macOS editor. There is no official Flatpak. [blazium#428](https://github.com/blazium-games/blazium/issues/428) asks for one.

Hub's window is built from `blazium_4.8`. The editors it downloads are the CDN `0.6.x` builds from the `blazium-dev` line. Remote control inside those editors is port 6508. Hub's own loopback port is 39218. They are not the same server.

Engine docs: [docs.blazium.app](https://docs.blazium.app). CLI repo: [blazium-cli](https://github.com/blazium-games/blazium-cli). Hub repo: [blazium-hub](https://github.com/blazium-games/blazium-hub).

## Next steps

The pieces a download touches are [blazium.app](https://blazium.app), `cdn.blazium.app`, Hub, the CLI, and the `0.6.x` editor on `blazium-dev`. Hub's own executable is built from `blazium_4.8`.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
