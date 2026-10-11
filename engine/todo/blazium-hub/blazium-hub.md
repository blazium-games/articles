---
title: "Blazium Hub"
description: "The desktop window over blazium-cli: projects, editor installs, News, and settings. The CLI does the mutations."
cover: "assets/cover.png"
slug: "blazium-hub"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Blazium Hub

### A launcher that does not download editors itself

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

Godot's project manager lives inside the editor binary. That is a fine place for it when one build is the product. We ship three channels, two engine lines, and a crash sidecar, and we wanted a window that could install any of those editors without becoming a second copy of the engine. Hub is that window. It lists projects, asks the CDN what is published, and hands every install, uninstall, and open to [blazium-cli](https://github.com/blazium-games/blazium-cli).

The installer is also how most people get the CLI. Windows Setup and the Linux package put Hub, `blazium-cli`, and `crash_reporter` on disk together, and they register `blazium://` to the CLI. A terminal or a CI job can skip Hub. A desktop machine should not have to.

![Install flow: installer, on-disk trio, blazium://, Hub remote, Editors, Open](assets/install-flow.png)

## Why the window is thin

Hub's own executable is a 2D project. CI builds it from the engine branch `blazium_4.8`, with a short module set that includes GDScript, `httpserver`, `remote_control`, `crash_reporter`, and `analytics`, and it bakes `editor_app_id=blazium-hub`. That binary is the launcher. It is not the editor you install from the Editors tab.

The allowlist is deliberate. Hub enables `gl_compatibility`, low processor mode, and no XR. The shipped template sets `disable_3d=yes`, `vulkan=no`, `openxr=no`, `d3d12=no`, `optimize=size`, and `lto=full`. There is no Mono, Luau, or JustAMCP in that binary. Autowork tests still download a published nightly Linux editor that has Luau; the Hub product binary itself does not.

The editors on the CDN are the `0.6.x` line from `blazium-dev`, which tracks Godot 4.3. As of 11 October 2026 the release catalog points at [0.6.838](https://cdn.blazium.app/catalog/versions/release/latest.json) and the nightly catalog points at 0.6.924. Hub never calls Cerebro, our internal build service. `CdnClient` only accepts `cdn.blazium.app`.

Published installers exist for Windows and Linux. There is no macOS Hub package in [blazium-hub](https://github.com/blazium-games/blazium-hub) `packaging/`. A CLI you compile yourself on macOS can still install a macOS editor. There is no official Flatpak. [blazium#428](https://github.com/blazium-games/blazium/issues/428) asks for one. It is an open request, not a download.

Windows uses Inno Setup, machine-wide under `{autopf}\Blazium`, and it requires admin. `BlaziumHub.exe` lands in `{autopf}\Blazium\Engine`. The CLI and the crash sidecar stay in `{autopf}\Blazium`. The protocol registration runs `blazium-cli.exe handle-uri`, not Hub. An optional installer task can download the Games launcher into `{autopf}\Blazium\Games`. Linux is an nfpm `.deb` that registers `x-scheme-handler/blazium` the same way.

## Projects

Hub imports a project by scanning a folder for `project.godot`. Opening that card runs `blazium-cli open`. Run on the card runs `blazium-cli run` / `play`. Favorite pins the card. Remove takes it off the list with `blazium-cli projects remove`.

The project card draws a version dropdown (`BlaziumVersionButton`). Nothing fills it, and the open path does not read it. `projects_view.gd` calls `HubCli.open_project_async(path)` and stops there. Until that call passes a version, Open is the CLI default. Set the default with `blazium-cli editors default` if you need a pin. The button on the card does not do it. Treat the control as unfinished UI.

The Projects tab can also download starters. Hub asks the CLI for `starters list`, then `starters download <name> -dir <folder>`. The catalog is `https://cdn.blazium.app/starters/starters.json`. That path creates a new project tree; it is not an export-template install.

Hub and the CLI share one registry: `%APPDATA%\blazium\hub.json` on Windows, `~/.config/blazium/hub.json` elsewhere.

![Hub's four tabs](assets/hub-tabs.png)

## Editors

The channel dropdown is `release`, `prerelease`, and `nightly`. The installed list comes from the CLI registry. The available list is the CDN catalog for that channel. Install, Uninstall, and Refresh shell the CLI, and the log under the tab is that process's output.

Current CLI builds put editors in `{install-path}/{channel}/{version}`. In one recorded session the install root was `C:\Users\Bioblaze\AppData\Local\Blazium\Editors` and the resolved default was `0.6.725`, stored directly under `Editors\` with the channel only as a field. That is the layout of the CLI that was recorded. New installs insert `release`, `prerelease`, or `nightly` between the root and the version. Change the root with `blazium-cli install-path`, or from Settings, which calls the same command.

If you never set a default, the CLI picks the latest installed editor on the `release` channel.

When Hub launches an editor it can forward analytics consent and a crash-reporter path. If you declined data collection, Hub passes `--no-crash-reporter`. Those flags are CLI arguments on the open/run path; they are not a second install mechanism.

## News

Hub fetches `https://cdn.blazium.app/articles/rss.xml`, then `meta.json` and `content.bbcode` for the slug you open. External host entries, IndieDB and the rest, show up as links. BBCode is allowlisted before it is drawn. Cover URLs that are not on the CDN host are dropped. A post shows up there after `deployed` is set and the publish workflow has uploaded it. Parsed items are cached under `user://news-cache.json` so a cold open still has something to show.

CDN responses, News links, `blazium://` targets, and CLI JSON all go through the same checks: HTTPS for external opens, size caps on CDN bodies, and loopback-only for remote control even if a config file has been edited.

## Settings and the tray

Settings stores the two paths the CLI needs:

- CLI path. Hub will not install or open anything until this points at `blazium-cli`. Unsafe paths are rejected before they are stored.
- Editor install path. This is the root passed to `blazium-cli install-path`, not one editor binary.

On Windows, close-to-tray hides the window instead of quitting. Check for updates covers Hub plus the bundled CLI, crash sidecar, and toolchain. The update queue order is hub, cli, crash_reporter, toolchain, editor, templates. While a Hub update is outstanding, standalone CLI and crash-reporter prompts are suppressed, because Hub ships those binaries. Toolchain is not bundled with Hub, so it still prompts on its own. Under Program Files, `blazium-cli update apply` may raise a UAC prompt. The CLI can also apply `launcher`. Hub's own update queue does not prompt for the Games launcher.

The log under Settings can be copied or cleared. It is the same stream as the Editors tab console.

The Windows tray can show Hub, open a recent project, or quit. Recent projects are the same registry as the Projects tab, so a favorite you set in the window is the one the tray lists first. Single-instance IPC only accepts `SHOW` or `blazium:` messages; everything else is rejected.

## Deep links

The CLI is the OS protocol handler. Hub listens on loopback port **39218**. The installers write `hub_remote.json` (a token plus that port). Do not edit that file. A bad token or a non-loopback host fails closed: Hub forces the bind back to loopback.

Load order is the user file (`%APPDATA%\blazium\hub_remote.json` or `~/.config/blazium/hub_remote.json`), then the machine file (`%ProgramData%\blazium\hub_remote.json` or `/etc/blazium/hub_remote.json`). `blazium-cli hub-remote ensure` creates a missing file and does not rotate a token that is already valid. Windows Setup prefers the CLI ensure path, then falls back to `BlaziumHub --headless --ensure-hub-remote`. Linux postinst does the same against `/etc/blazium/hub_remote.json`; a failure there does not fail package configure.

| URI | Action |
|---|---|
| `blazium://hub` | Focus Hub |
| `blazium://open?path=` | Open a project in the editor |
| `blazium://load?path=` | Open a project and print the full profile |
| `blazium://project/<encoded-path>` | Shorthand for open |
| `blazium://install?version=` | Download that editor |
| `blazium://register?path=` | Register a local editor binary |

`blazium://install/<uuid>`, `blazium://game/<uuid>`, and `blazium://buy/<uuid>` go to the Games launcher on port **39220**. They do not install an editor. The Blazium Games store is a different product from this launcher. Store uploads can go through `blazium-cli games` (the command is also named `chauffeur`) or through the standalone games CLI. Steam and itch uploads are `blazium-cli deploy`.

JustAMCP, the editor MCP server, also uses `blazium://` for resources such as `blazium://scene/…` and `blazium://tags/dictionary`. That is a different owner of the same scheme. The OS handler is still the CLI. JustAMCP listens on port 6506. The editor remote-control server is `127.0.0.1:6508`.

Hub's crash bake posts to `https://crash.blazium.app/v1/reports`. The sidecar still asks before anything is uploaded.

## What you should expect from the UI

Hub is a state and workflow surface: which projects you have, which editors are installed, which news posts are unread, whether close-to-tray is on. It is not a second downloader. If the CLI path is wrong, every Install and Open fails in the console under the tab. If the CDN is reachable and the CLI is not, News still loads and Editors still show available builds, but Install stays broken until Settings points at a real binary.

## Links

- Download Hub: https://blazium.app/dev-tools
- Blazium Hub: https://github.com/blazium-games/blazium-hub
- Blazium CLI: https://github.com/blazium-games/blazium-cli
- Editor downloads: https://blazium.app/download
- Release catalog: https://cdn.blazium.app/catalog/versions/release/latest.json
- Starters catalog: https://cdn.blazium.app/starters/starters.json
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
