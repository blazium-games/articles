---
title: "Blazium Hub"
description: "Desktop launcher: projects, editor installs, News, settings. CLI does the mutations."
cover: "assets/cover.png"
slug: "blazium-hub"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Hub is a 2D Blazium app. It does not download editors. It shells [blazium-cli](../blazium-cli/blazium-cli.md). The installer puts three things on disk: Hub, CLI, and the crash sidecar.

![Install flow: installer, on-disk trio, blazium://, Hub remote, Editors, Open](assets/install-flow.png)

Windows: Inno Setup, machine-wide `{autopf}\Blazium`, admin required. Linux: `.deb`. Both register `blazium://` to CLI, not to Hub.

## Projects

Add a `project.godot`. Scan a folder. Open runs `blazium-cli open`. Remove unregisters. Favorite pins a card. A version option pins which installed editor opens that project.

<!-- CAPTURE: assets/projects-empty.png | Hub | Empty Projects tab, Add and Scan visible -->
<!-- CAPTURE: assets/projects-populated.png | Hub | 3+ project cards, one favorited -->
<!-- CAPTURE: assets/project-card-menu.png | Hub | Card overflow: remove, version pin -->
<!-- CAPTURE: assets/cover.png | Hub | Replace diagram cover with Projects tab, populated, 16:9 -->

## Editors

Channel dropdown: `release`, `prerelease`, `nightly`. Installed list comes from CLI (`%APPDATA%\blazium\hub.json`). Available list comes from `cdn.blazium.app` only. Install / Uninstall / Refresh. A log console at the bottom of the tab.

![Hub's four tabs](assets/hub-tabs.png)

<!-- CAPTURE: assets/editors-nightly.png | Hub | Editors tab, channel nightly, Installed and Available lists -->
<!-- CAPTURE: assets/editors-install.gif | Hub | Click Install, log lines, row moves to Installed -->

On this machine the CLI currently reports a default of `0.6.725` under `C:\Users\Bioblaze\AppData\Local\Blazium\Editors`.

## News

Hub fetches `https://cdn.blazium.app/articles/rss.xml`, then `meta.json` and `content.bbcode` for the opened slug. External `hosts` (IndieDB, itch) show as links. BBCode is allowlisted before display. This article, once `deployed: true`, is what News lists.

<!-- CAPTURE: assets/news-list.png | Hub | News list -->
<!-- CAPTURE: assets/news-open.png | Hub | Opened article, IndieDB host chip visible -->

## Settings

CLI path, editor install path, Windows close-to-tray, Check for updates, log copy/clear.

<!-- CAPTURE: assets/settings.png | Hub | Settings: CLI path, install path, tray checkbox -->

## Tray (Windows)

Show Hub, recent projects, Quit. Optional hide-on-close.

<!-- CAPTURE: assets/tray.png | Hub | Windows tray menu -->

## Deep links

CLI is the OS protocol handler. Hub listens on loopback port **39218**. `hub_remote.json` is a shared token file. Installers create it. Do not hand-edit it.

| URI | Action |
|---|---|
| `blazium://hub` | Focus Hub |
| `blazium://open?path=…` | Open / focus a project |
| `blazium://load?path=…` | Load with full profile |
| `blazium://project/<encoded-path>` | Shorthand open |
| `blazium://install?version=…` | Download that editor |
| `blazium://register?path=…` | Register a local editor binary |

JustAMCP also uses `blazium://scene/…` inside the editor. That is not this table. See [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).

## Updates

A Hub update covers Hub plus the bundled CLI and crash sidecar.

<!-- CAPTURE: assets/hub-update.png | Hub | Update confirmation dialog -->
<!-- CAPTURE: assets/installer-finish.png | Windows Inno | Finish page: launch Hub / visit blazium.app -->

## Next

[The stack](../what-is-the-blazium-ecosystem/what-is-the-blazium-ecosystem.md) · [CLI](../blazium-cli/blazium-cli.md) · [Crash reports](../crash-reporter/crash-reporter.md)
