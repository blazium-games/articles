---
title: "Blazium console toolchain"
description: "A GPLv3 sidecar the editor spawns. Today: PS1 setup/build/run, and Interactive DVD mastering."
cover: "assets/cover.png"
slug: "blazium-toolchain"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

The engine stays MIT. This CLI is GPL-3.0-or-later so it can fetch GCC, PSn00bSDK, pcsx-redux, mkpsxiso, and OpenBIOS. The editor only spawns the binary. Never merge those trees into `blazium.git`.

![MIT engine spawns GPLv3 toolchain](assets/mit-vs-gpl.png)

## Install

```text
git clone https://github.com/blazium-games/blazium-toolchain.git
cd blazium-toolchain
go test ./...
go build -o blazium-toolchain.exe ./cmd/blazium-toolchain
```

Go 1.23.8 or later. Cache: `%LOCALAPPDATA%\Blazium\blazium-toolchain` (Windows), `~/.local/share/blazium-toolchain` elsewhere. Override with `--prefix` or `BLAZIUM_TOOLCHAIN_PREFIX`.

```text
blazium-toolchain --json version
blazium-toolchain --json list
```

<!-- ASCIINEMA: assets/toolchain-version.cast | blazium-toolchain --json version -->
<!-- CAPTURE: record after building the binary: asciinema rec assets/toolchain-version.cast -->

## PS1

| Profile | Contents |
|---|---|
| `compile` | gcc + PSn00bSDK 0.24 + elf2x |
| `dev` | compile + OpenBIOS + pcsx-redux CLI |
| `iso` | dev + mkpsxiso |

```text
blazium-toolchain ps1 setup --profile dev
blazium-toolchain ps1 env
blazium-toolchain ps1 status
blazium-toolchain ps1 build --out GAME.EXE --sample template
blazium-toolchain ps1 run --timeout 120s GAME.EXE
```

Host tools: Windows and Linux. Other hosts exit `2`. `--offline` never hits the network. `ps1 build` without `--src` installs the embedded MIT guest stub.

<!-- ASCIINEMA: assets/ps1-setup.cast | blazium-toolchain ps1 setup --profile compile --offline -->
<!-- CAPTURE: assets/ps1-run.mp4 | pcsx-redux | 20s: run GAME.EXE. Also record the CLI with asciinema. -->
<!-- CAPTURE: assets/cover.png | Emulator + terminal | Replace diagram cover -->

## Interactive DVD

```text
blazium-toolchain interdvd meta init --out disc.interdvd.json
blazium-toolchain interdvd iso --dir ./disc --out disc.iso --meta disc.interdvd.json
```

The folder must already contain `VIDEO_TS/` (optional `AUDIO_TS/`). No mkisofs. Extra PC files sit beside the video folders (`--extra`). Mastering works on macOS even though PS1 host tools do not.

<!-- CAPTURE: assets/interdvd.png | Terminal / explorer | ISO output listing -->

## Reserved

`ps2`, `ps3`, `ps4` ids exist. Commands exit `2`. Do not document them as shipping.

## Editor spawn

A third-party app (the editor) downloads this CLI and execs it. Users do not vendor compilers into the engine repo. Third-party licenses: `THIRDPARTY.md` in the toolchain tree.
