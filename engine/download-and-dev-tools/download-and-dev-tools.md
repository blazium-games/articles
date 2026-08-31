---
title: "Download Blazium and the dev tools"
description: "Website download tabs, Hub installer, CLI, GitHub Actions, and the Docker web template, and which one you actually need."
cover: "assets/cover.png"
slug: "download-and-dev-tools"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

If you make games, install [Hub](../blazium-hub/blazium-hub.md). If you already live in a terminal or CI, install [CLI](../blazium-cli/blazium-cli.md). The website is how you find both.

![Stack map](assets/ecosystem-map.png)

## Hub

Windows Inno, Linux `.deb`. Bundles CLI and the crash sidecar. Start here: [https://blazium.app/dev-tools/download?tool=hub](https://blazium.app/dev-tools/download?tool=hub)

The Hub card is missing from `blazium.app/data/dev_tools.json` today. The URL above still works. Add the card before you screenshot the page, or the still will lie.

<!-- CAPTURE: assets/dev-tools-hub-download.png | Website | /dev-tools/download?tool=hub dropdown -->
<!-- CAPTURE: assets/cover.png | Website | Replace with download page, prebuilt tab, 16:9 -->

## CLI

GitHub Releases, or `https://cdn.blazium.app/cli/cli.json`, or the Hub bundle.

![blazium-cli version](assets/cli-version.svg)
<!-- ASCIINEMA: assets/cli-version.cast | blazium-cli version -->

## Website tabs

[https://blazium.app/download](https://blazium.app/download)

| Tab | What it is |
|---|---|
| Prebuilt binaries | Editor zips by OS / arch / C# |
| Package managers | Pacman, Chocolatey |
| Torrents | Same builds |
| Stores | Listed digital stores |

OS list on the site: Windows, Linux, macOS, Android, Horizon OS, PICO OS, Web. Arch: x86_64, x86_32, ARM64, ARM32. C# with or without Mono.

<!-- CAPTURE: assets/download-prebuilt.png | Website | OS / arch / C# selectors -->
<!-- CAPTURE: assets/download-pkg.png | Website | Pacman / Chocolatey commands -->
<!-- CAPTURE: assets/blazium-app-home.png | Website | Home -->

## Dev-tools page

[https://blazium.app/dev-tools](https://blazium.app/dev-tools)

| Tool | Repo / URL | When |
|---|---|---|
| Hub | installer | Making games on a desktop |
| CLI | `blazium-games/blazium-cli` | Scripts, CI, `blazium://` |
| Docker web template | `blazium-games/docker-webbuild-template` | Host a web export, including Discord activities |
| setup-blazium-cli | `github_actions/setup-blazium-cli` | Put CLI on a runner |
| setup-blazium-engine | `github_actions/setup-blazium-engine` | Install an editor on a runner |
| export-blazium-game | `github_actions/export-blazium-game` | Export a project |
| deploy-blazium-game | `github_actions/deploy-blazium-game` | Push a built artifact to a store |

Those four Actions live in this ecosystem checkout under `github_actions/`. Article: [GitHub Actions for Blazium](../github-actions-for-blazium/github-actions-for-blazium.md).

![GitHub Actions flow](assets/github-actions-flow.png)

<!-- CAPTURE: assets/dev-tools.png | Website | Dev-tools cards after Hub is on the page -->

## Pick one path

| You | Install |
|---|---|
| Making a game on a PC | Hub |
| Scripting installs / opening projects | CLI |
| GitHub CI | setup-blazium-cli + setup-blazium-engine, then export / Autowork |
| Discord activity or YouTube Playable | Web export + [Docker web export](../docker-web-export/docker-web-export.md) |
