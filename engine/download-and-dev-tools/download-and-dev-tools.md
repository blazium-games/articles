---
title: "Download Blazium and the dev tools"
description: "Website download pages, Hub installer, CLI, GitHub Actions, and the Docker web template, and which one you actually need."
cover: "assets/cover.png"
slug: "download-and-dev-tools"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

## Why we built it

The engine README says official binaries are on [blazium.app/download](https://blazium.app/download). The CLI and Hub READMEs point dev tools at [blazium.app/dev-tools](https://blazium.app/dev-tools). Hub's installer is the path that also lays down `blazium-cli` and the crash sidecar. The CLI is also published on its own, for machines that should not run Hub. The CDN catalogs in those READMEs (`cli.json`, Hub installers, `crash_reporter.json`, `toolchain.json`) are what those downloads resolve to.

## What Blazium Games uses it for

The download pages, Hub, the CLI, the crash reporter, and the CDN were built for the Blazium Engine and this ecosystem. Release CI publishes the catalogs. Hub only fetches `https://cdn.blazium.app`. That is how the Hub binary, which is built from `blazium_4.8`, installs editor builds for the line you pick. Internal game builds use the same CDN downloads the public gets. The store is not this page. Store uploads are `chauffeur`.

## What other projects get

The same pages. Published Hub and CLI binaries are Linux and Windows. There is no macOS installer in Hub's `packaging/` tree, and no Flatpak. [blazium#428](https://github.com/blazium-games/blazium/issues/428) asks for one.

If you make games, install [Hub](../blazium-hub/blazium-hub.md). If you already live in a terminal or CI, install [CLI](../blazium-cli/blazium-cli.md). Both can be found on the [website](https://blazium.app).

## Status

Published Hub installers and CLI binaries are Linux and Windows. Hub packaging in [blazium-hub](https://github.com/blazium-games/blazium-hub) is `packaging/windows` and `packaging/linux`. There is no macOS installer in that tree. A CLI built locally on macOS can still install a macOS editor. CI does not publish that CLI binary.

There is no official Flatpak or Flathub package. [blazium#428](https://github.com/blazium-games/blazium/issues/428) asks for one. It is not a button on the download page.

Hub's own executable is built from engine branch `blazium_4.8`. The editor zips on [blazium.app/download](https://blazium.app/download) are the product line you install, Blazium `0.6.x` (Godot 4.3 compatible, `blazium-dev`). Engine docs: [docs.blazium.app](https://docs.blazium.app). Dev tools index: [blazium.app/dev-tools](https://blazium.app/dev-tools).

![Stack map](assets/ecosystem-map.png)

## Hub

Windows Inno, Linux `.deb`. The installer also installs the CLI and the crash sidecar, so you do not download those separately. Start here: [https://blazium.app/dev-tools/download?tool=hub](https://blazium.app/dev-tools/download?tool=hub)

That bundle is the desktop path. Hub's own CI builds the Hub executable from engine branch `blazium_4.8`. The editors it installs are the public CDN builds.

## CLI

GitHub Releases, npm (`@blazium-engine/cli`), the CDN manifest `https://cdn.blazium.app/cli/cli.json`, or the Hub bundle above. Direct page: [https://blazium.app/dev-tools/download?tool=cli](https://blazium.app/dev-tools/download?tool=cli)

![blazium-cli version](assets/cli-version.svg)
<!-- ASCIINEMA: assets/cli-version.cast | blazium-cli version -->

## Editor builds

[https://blazium.app/download](https://blazium.app/download)

The download page is the editor itself (prebuilt archives, package-manager commands, and the same bits over other channels). Those zips are what `blazium-cli install` fetches from `cdn.blazium.app`. You can unpack one by hand. The CLI is what records it in `hub.json` so Hub and `blazium-cli open` can find it.

The product version on that page is Blazium `0.6.x`. Godot compatibility for this line is 4.3.2. Export templates follow the Blazium version, not a `4.3.2.stable` folder. See [Export templates and the CDN](../export-templates-and-cdn/export-templates-and-cdn.md).

## Dev tools

[https://blazium.app/dev-tools](https://blazium.app/dev-tools)

| Tool | Where it lives | When |
|---|---|---|
| Hub | installer, `{autopf}\Blazium\Engine` | Making games on a desktop |
| CLI | [blazium-cli](https://github.com/blazium-games/blazium-cli) | Scripts, CI, `blazium://` |
| Docker web template | [docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template) | Host a web export, including Discord activities |
| setup-blazium-cli | [setup-blazium-cli](https://github.com/blazium-games/setup-blazium-cli) | Put CLI on a runner |
| setup-blazium-engine | [setup-blazium-engine](https://github.com/blazium-games/setup-blazium-engine) | Install an editor on a runner |
| export-blazium-game | [export-blazium-game](https://github.com/blazium-games/export-blazium-game) | Export a project |
| deploy-blazium-game | [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game) | Push a built artifact |
| Toolchain | [blazium-toolchain](https://github.com/blazium-games/blazium-toolchain) | PS1, PS2, N64, Interactive DVD |

The four Actions are separate repositories. They are not a `github_actions/` folder in the articles checkout. Article: [GitHub Actions for Blazium](../github-actions-for-blazium/github-actions-for-blazium.md).

![GitHub Actions flow](assets/github-actions-flow.png)

## Pick one path

| You | Install |
|---|---|
| Making a game on a PC | Hub (CLI comes with it) |
| Scripting installs or opening projects | CLI |
| GitHub CI | `setup-blazium-cli` or `setup-blazium-engine`, then export or Autowork |
| Discord activity or YouTube Playable | `Web` export + [Docker web export](../docker-web-export/docker-web-export.md) |
| A console or Interactive DVD build | [Toolchain](../blazium-toolchain/blazium-toolchain.md) |

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
