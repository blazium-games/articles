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

Engine versions used to be a folder you unpacked yourself, and projects were a path you typed into a shortcut. That breaks as soon as two games need two builds, or a CI job needs the same layout as a laptop.

We built two tools for that. **Blazium Hub** is the window. **Blazium CLI** is the program that actually installs, registers, and launches. Hub is a front end for the CLI. The CLI also runs on its own, which is what scripts and GitHub Actions call.

## Why the installer bundles the CLI

Downloading Hub is the install path that also installs the CLI. The Windows Inno setup and the Linux `.deb` put three binaries down together: Hub, `blazium-cli`, and the crash sidecar. You do not hunt for a second download to get a working `PATH` entry. That is the point of the bundle. People who already live in a terminal can still take the CLI alone from npm (`@blazium-engine/cli`), GitHub Releases, or `https://cdn.blazium.app/cli/cli.json`.

Hub: [blazium.app/dev-tools/download?tool=hub](https://blazium.app/dev-tools/download?tool=hub)

CLI only: [blazium.app/dev-tools/download?tool=cli](https://blazium.app/dev-tools/download?tool=cli)

## What Hub is for

Hub lists projects and editor builds in one window. Scan a folder for `project.godot`. Favorite pins a card. Remove drops it from the registry. The card has a version control in the scene, and the open button still calls the CLI with the project path only, so the editor you get is the CLI default until you change that default. Custom local binaries show up after `blazium-cli editors add`.

The News tab reads `https://cdn.blazium.app/articles/rss.xml` and renders the article in the window. You do not need a browser to see what shipped.

Everything that changes disk goes through the CLI. Hub and the CLI share `%APPDATA%\blazium\hub.json` (or `~/.config/blazium/hub.json`). If the registry is right in one, it is right in the other.

The longer walk of tabs, the tray, and port 39218 is in [Blazium Hub](../blazium-hub/blazium-hub.md).

## What the CLI is for

The CLI downloads editor builds and export templates, registers projects, and opens them. Channels are `release`, `prerelease`, and `nightly`. A version lives at `{install-path}/{channel}/{version}`.

```text
blazium-cli install 0.6.725 --templates
blazium-cli projects add ./MyProject
blazium-cli open ./MyProject
```

`open` starts the editor and, by default, turns on remote control so a later `blazium-cli remote` command can reach that window. `run` starts the game instead, and leaves remote control off.

Deep links use the `blazium://` scheme. The OS handler is the CLI, not Hub. `blazium://open?path=` opens a project. `blazium://install?version=` installs an editor. `blazium://hub` focuses Hub over the loopback port the installer wrote into `hub_remote.json`. Leave that file alone.

When the editor was built with the Remote Control module, `blazium-cli remote` can query status, run a command, read logs, and kick Autowork without clicking the UI. Details: [The Remote Control module](../remote-control-module/remote-control-module.md).

Command reference: [Blazium CLI](../blazium-cli/blazium-cli.md).

## Why both

Hub is how a person picks a version and a project. The CLI is how that choice is repeatable: the same flags in a terminal, in a deep link, and in `setup-blazium-engine`. We did not want a launcher that hides a private install format. If Hub can do it, the CLI command is the thing that happened.

## Next steps

[The Blazium engine stack](../what-is-the-blazium-ecosystem/what-is-the-blazium-ecosystem.md) is the map of website, CDN, Hub, CLI, and the editor.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
