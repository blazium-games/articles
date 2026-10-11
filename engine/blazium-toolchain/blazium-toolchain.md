---
title: "Blazium console toolchain"
description: "A GPL-3.0 CLI the editor spawns for Interactive DVD. PS1, PS2, and N64 are terminal commands in the same binary."
cover: "assets/cover.png"
slug: "blazium-toolchain"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Blazium console toolchain

### The compilers stay out of the MIT editor

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

The Blazium engine stays under the MIT license. GCC, PSn00bSDK, pcsx-redux, the ps2dev toolchain, and libdragon are not MIT, and dropping those trees into `blazium.git` would drag their licenses onto the editor. [blazium-toolchain](https://github.com/blazium-games/blazium-toolchain) is GPL-3.0-or-later so it can fetch them. The editor looks up the binary and runs it. It does not vendor the compilers.

We used that split in-house to validate PS1, PS2, N64, and Interactive DVD exports. That validation is not a shipped console title. Godot does not ship an official PS1, PS2, or N64 toolchain. We do not pretend the editor has export platforms for those three. Only Interactive DVD has an export platform class. The others are commands you run yourself after `setup`.

![MIT engine spawns GPLv3 toolchain](assets/mit-vs-gpl.png)

![What the binary builds](assets/toolchain-targets.png)

## Install

Published binaries are Linux and Windows, x86_64 and x86_32. Catalog: `https://cdn.blazium.app/toolchain/toolchain.json` (latest 0.1.9 when this was checked). npm:

```text
npm install -g @blazium-engine/toolchain
```

Or build it. Go 1.23.8 or later.

```text
git clone https://github.com/blazium-games/blazium-toolchain.git
cd blazium-toolchain
go test ./...
go build -o blazium-toolchain ./cmd/blazium-toolchain
```

A local macOS build can master an Interactive DVD. PS1, PS2, and N64 setup and build exit `2` on that host. CI does not ship a macOS binary.

Cache: `%LOCALAPPDATA%\Blazium\blazium-toolchain` on Windows, `~/.local/share/blazium-toolchain` elsewhere. Override with `--prefix` or `BLAZIUM_TOOLCHAIN_PREFIX`. SHA pins live in the embedded `pins.json`.

Stdout is one verb per line (`fetching`, `installing`, `skip`, `wrote`, `ready`, `error`). Exit `2` means a reserved platform or a host that cannot compile. Exit `3` means a host tool is missing.

The editor preset key is `export/inter_dvd/toolchain`. Empty means `BLAZIUM_TOOLCHAIN`, then `PATH`. Dummy-VOB export works without the CLI. ISO export does not.

## PS1

| Profile | Contents |
|---|---|
| `compile` | gcc 12.3.0, PSn00bSDK 0.24, elf2x |
| `dev` | compile, plus OpenBIOS and the pcsx-redux CLI |
| `iso` | dev, plus mkpsxiso |

```text
blazium-toolchain ps1 setup --profile dev
blazium-toolchain ps1 build --out GAME.EXE --sample template
blazium-toolchain ps1 run --timeout 120s GAME.EXE
```

`--offline` skips the network. `ps1 run` is headless unless you pass `--ui`. `ps1 build` without `--src` uses the MIT guest stub embedded in the CLI. Sony BIOS images are not fetched. The PS1 ISO step uses mkpsxiso, which `setup` downloads. That is not the Interactive DVD path.

## PS2

`ps2` ships. It does not exit 2.

| Profile | Contents |
|---|---|
| `compile` | ps2dev EE gcc and the PS2SDK |
| `dev` | compile, plus your `PCSX2_EXE` (BIOS is not fetched) |
| `iso` | dev, plus `ps2 iso --dir TREE` |

```text
blazium-toolchain ps2 setup --profile compile
blazium-toolchain ps2 build --out hello.elf --sample cube
blazium-toolchain ps2 iso --dir ./tree --out game.iso
```

Set `PCSX2_EXE` before `ps2 run`. `ps2 chd` wraps an ISO with `chdman` when that tool is on `PATH`.

## N64

There is no ISO command. `n64 iso` is rejected. The product is a big-endian `.z64`.

| Profile | Contents |
|---|---|
| `compile` | libdragon preview: `N64_INST`, `mips64-elf-gcc`, `libdragon.a` |
| `dev` | compile, plus Ares and/or Project64 |
| `rom` | compile, plus `mkdfs` / `n64tool` |

```text
blazium-toolchain n64 setup --profile compile
blazium-toolchain n64 build --out hello.z64 --display 320
blazium-toolchain n64 run --emu ares --rdram 8 hello.z64
```

`--display` is `320` or `640`. `--rdram 8` is the Expansion Pak size. Samples include `helloworld`, `rdpqdemo`, `t3dquad`, and `ovldemo`. `C:\ultra` is ignored. PIF dumps are not fetched.

## Interactive DVD

```text
blazium-toolchain interdvd meta init --out disc.interdvd.json
blazium-toolchain interdvd iso --dir ./disc --out disc.iso --meta disc.interdvd.json
```

The folder must already contain `VIDEO_TS/`. `AUDIO_TS/` is optional. **No mkisofs** means this command writes ISO9660 and UDF 1.02 itself. It does not shell out to `mkisofs` or `oscdimg`. The engine's `InterDVDIfoWriter` documents the same limit: the argument list is `--dir`, `--out`, `--meta`, `--write-meta`, and `--json`.

`menu_language`, `audio_language`, `subtitle_language`, `region_mask`, and `parental_level` are stored in `disc.interdvd.json`. They are not written into the IFO.

`interdvd setup` can fetch a pinned FFmpeg on Windows and Linux. The editor's scene baker runs `blazium-toolchain interdvd ffmpeg` to encode a cell. If the CLI is missing, bake fails with "blazium-toolchain is not ready."

## Reserved

`ps3` and `ps4` are names the CLI accepts so scripts fail clearly. Every command exits `2`. They are not a shipping target, and there is no date on them.

Compilers are downloaded into the cache on `setup`. They are not inside the Go binary. The MIT guest sources are. `export-guest --out DIR` writes that stub. Third-party licenses are in `THIRDPARTY.md` in the toolchain repo. libpsn00b, ps2sdk, and libdragon link into the exported guest, not into the editor.

## Links

- Toolchain: https://github.com/blazium-games/blazium-toolchain
- Catalog: https://cdn.blazium.app/toolchain/toolchain.json
- Engine: https://github.com/blazium-games/blazium
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
