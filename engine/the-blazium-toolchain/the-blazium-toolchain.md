---
title: "The Blazium Toolchain"
description: "Why console compilers live in a GPL sidecar instead of inside the MIT engine."
cover: "assets/cover.png"
slug: "the-blazium-toolchain"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---

# Blazium Toolchain

Console SDKs are large, GPL or otherwise incompatible with a single MIT tree, and they change on their own schedule. Putting GCC, PSn00bSDK, ps2dev, and libdragon inside `blazium.git` would force that license onto the editor. We did not want that.

The **Blazium Toolchain** is a separate CLI. It downloads the compilers into a local cache, which keeps everything organized, and it gives you commands to build, run, and package. The engine stays MIT. The CLI is GPL-3.0-or-later. The editor only spawns the binary.

Repo: [blazium-games/blazium-toolchain](https://github.com/blazium-games/blazium-toolchain).

## What it actually builds

| Platform | Status on the current CLI |
|---|---|
| PlayStation 1 | `ps1 setup`, `build`, `run`, `iso` |
| PlayStation 2 | `ps2 setup`, `build`, `run`, `iso`, `elf-info`, `chd` |
| Nintendo 64 | `n64 setup`, `build`, `run`, `rom`. No ISO. Output is `.z64` |
| Interactive DVD | `interdvd setup`, `ffmpeg`, `iso`. The editor export calls this |
| PlayStation 3, PlayStation 4 | Reserved. Exit code `2` |

Windows screensaver, live wallpaper, and web export are engine modules (`screensaver`, `livewallpaper`, `platform/web`). They are not this CLI.

## Why the editor spawns it

Interactive DVD export on `blazium-dev` is `EditorExportPlatformWindowsInterDVD`. Scene encode and ISO mastering run `blazium-toolchain`. The lookup is `export/inter_dvd/toolchain`, then `BLAZIUM_TOOLCHAIN`, then `PATH`. ISO mastering does not call mkisofs or oscdimg. The CLI writes ISO9660 and UDF 1.02 from a folder that already has `VIDEO_TS/`.

PS1, PS2, and N64 do not have editor export platforms in this tree. You run those commands in a terminal after `setup`. Profiles (`compile`, `dev`, `iso` or `rom`) decide how much to fetch. `--offline` refuses the network. `--prefix` is the cache root so two games do not share a half-upgraded SDK by accident.

## Install

```text
npm install -g @blazium-engine/toolchain
blazium-toolchain --json list
blazium-toolchain ps1 setup --profile compile
```

Go 1.23.8 or later if you build from source. Published binaries are Linux and Windows, x86_64 and x86_32. The command list, cache layout, and the exact fetch pins are in [Blazium console toolchain](../blazium-toolchain/blazium-toolchain.md).

## What we left out on purpose

The CLI does not download Sony BIOS images or an N64 PIF ROM. `ps2 run` expects `PCSX2_EXE`. `n64 run` can use Ares (fetched on Windows x64 for the `dev` profile) or `PROJECT64_EXE`. A missing emulator is a skip, not a silent substitute.

`ps3` and `ps4` exit `2`. That is a reserved id, not a milestone with a date. Windows screensaver, live wallpaper, and the `Web` export preset stay in the engine. They are not waiting on this CLI.

Published binaries are Linux and Windows. Interactive DVD mastering works on a macOS build of the CLI. PS1, PS2, and N64 setup and build do not, on that host.

That split is the whole design. The MIT editor can call a GPL tool. It does not become one. The command list is [Blazium console toolchain](../blazium-toolchain/blazium-toolchain.md). Engine docs: [docs.blazium.app](https://docs.blazium.app).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
