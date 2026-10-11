---
title: "Why the console compilers are not in the engine"
description: "The editor stays MIT. blazium-toolchain is GPL-3.0-or-later and the editor only spawns it."
cover: "assets/cover.png"
slug: "the-blazium-toolchain"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Why the console compilers are not in the engine

### MIT for the editor, GPL for the binary that fetches GCC

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

The Blazium engine is MIT. No royalty, no seat fee. That only stays true if we do not merge in trees that are not MIT. GCC, PSn00bSDK, pcsx-redux, mkpsxiso, the ps2dev SDK, and libdragon are the compilers and kits a PS1, PS2, or N64 build needs. They live in [blazium-toolchain](https://github.com/blazium-games/blazium-toolchain), which is GPL-3.0-or-later, so it is allowed to fetch them. The editor looks up `blazium-toolchain` on `PATH` (or `export/inter_dvd/toolchain`, or `BLAZIUM_TOOLCHAIN`) and runs it. The process that stays MIT never links those libraries.

The engine README lists PS1, PS2, N64, and Interactive DVD as something Blazium adds, used with the toolchain. The code is narrower than that sentence. Interactive DVD has an export platform. The editor runs `blazium-toolchain interdvd iso` and `blazium-toolchain interdvd ffmpeg`. There is no PS1, PS2, or N64 `EditorExportPlatform`. Those are terminal commands after `setup`. Godot does not ship this toolchain either.

![The editor spawns the GPL binary](assets/mit-vs-gpl.png)

![What actually builds](assets/toolchain-targets.png)

![Editor discovers blazium-toolchain then runs interdvd setup, ffmpeg, or iso as a child process](assets/editor-spawns-cli.png)

## Two repositories on purpose

`blazium.git` is the MIT editor and runtime. `blazium-toolchain.git` is a separate Go program under GPL-3.0-or-later. The NOTICE file in the toolchain repo states the rule in one sentence: third-party toolchain components must never be merged into the MIT editor; the editor only spawns the CLI.

That is not a packaging convenience. It is the license boundary. If we copied mipsel-none-elf GCC or libdragon into `modules/`, the editor distribution would have to carry those licenses. Spawning an external binary keeps the editor tree MIT while still giving console authors a supported fetch-and-build path.

The MIT guest stubs (CMake/Makefile plus C++) are embedded inside the CLI. Compilers and SDKs are not. `setup` downloads them into a cache. `export-guest` writes the stub out. libpsn00b, ps2sdk, and libdragon link into the exported guest binary, not into the Blazium editor process.

## How the editor finds the binary

Interactive DVD is the only built-in export platform that talks to the CLI. Discovery order in `InterDVDToolchain::discover_binary` is:

1. Editor setting `export/inter_dvd/toolchain` (filled from the export preset option `inter_dvd/toolchain` when that path is set)
2. Environment variable `BLAZIUM_TOOLCHAIN`
3. `blazium-toolchain` (or `blazium-toolchain.exe` on Windows) on `PATH`

If the binary is missing, bake and ISO paths that need it fail with an explicit message: set `export/inter_dvd/toolchain`, set `BLAZIUM_TOOLCHAIN`, or put the binary on `PATH`. Dummy-VOB export that never calls FFmpeg can still succeed without the CLI. Scene bake and cell transcode call `interdvd setup` when encode is not ready, then `interdvd ffmpeg`.

`InterDVDIfoWriter::toolchain_iso_args` builds the argument vector the editor passes: `interdvd iso --dir … --out … [--meta … --write-meta …] --json`. The editor does not invent a second mastering protocol. It shells the same CLI a human would run.

## Process architecture

The editor never `dlopen`s GCC. It never links libdragon. For Interactive DVD it constructs an argument list and executes the child process. Stdout from the child is process status: one verb per line (`fetching`, `installing`, `skip`, `wrote`, `ready`, `error`). Failures are shaped so a pasted ticket includes kind, message, fix, command, host, version, and prefix. `--json` collapses the same fields into one object. There is no session log file.

Cache layout under `--prefix` / `BLAZIUM_TOOLCHAIN_PREFIX` (default `%LOCALAPPDATA%\Blazium\blazium-toolchain` on Windows, `~/.local/share/blazium-toolchain` elsewhere) is per platform:

```text
<prefix>/ps1/…   <prefix>/ps2/…   <prefix>/n64/…   <prefix>/interdvd/…   <prefix>/steam/…
```

Discovery inside the CLI is environment, then that prefix tree, then a portable copy next to the executable, then `PATH`. SHA-pinned downloads live in the embedded `pins.json`. Project knobs (timeouts, profiles, ISO labels, size gates, host search paths) live in `blazium-toolchain.yml` / `.blazium-toolchain.yml`. Changing a fetch URL or hash without updating `internal/embedfs/files/` breaks reproducibility; CONTRIBUTING documents that copy step.

## Third-party license map

`THIRDPARTY.md` is the authoritative table. Each fetched tree keeps its upstream license. Roles that matter for the boundary:

![Third-party components stay in the spawned toolchain or guest binary, not linked into the MIT editor](assets/third-party-licenses.png)

| Component | Role relative to the editor |
|---|---|
| This CLI (GPL-3.0-or-later) | Spawned process |
| mipsel / mips64 / ps2dev GCC | Spawned at `build`; never linked into the editor |
| PSn00bSDK / libpsn00b, PS2SDK, libdragon | Linked into the guest only |
| mkpsxiso, pcsx-redux, Ares, Project64, PCSX2, FFmpeg, chdman | Spawned tools |
| OpenBIOS | Cached for PS1 smoke; Sony BIOS is never fetched |
| MIT guest stubs | Embedded in the CLI; exported on demand |

Do not copy those trees into `blazium/` or link them into the editor. That sentence is in the toolchain repo for a reason.

## What "no mkisofs" means

Interactive DVD mastering writes ISO9660 and UDF 1.02 inside the Go process. It does not shell out to `mkisofs` or `oscdimg`. You do not install those tools. The folder you pass already has `VIDEO_TS/`. Language and region fields in the CLI's `disc.interdvd.json` are metadata for that JSON file and are not written into the IFO or UDF by the CLI ISO path. The engine's separate IFO authoring path has its own region, parental, menu, and audio options.

PS1 is a different command. `ps1 iso` uses mkpsxiso, which `ps1 setup` downloads into the toolchain cache. Saying the toolchain never calls an external ISO tool would be wrong. The Interactive DVD path is the one that does not.

SteamCMD is another supported platform in the same binary: `steam setup` caches Valve's tool for `blazium-cli deploy steam upload`. It does not log in and does not push builds. It is not a console compiler; it is another fetch-into-prefix helper that stays outside the MIT editor.

## What does not ship

`ps3` and `ps4` are reserved names. Commands exit `2`. Manifest status is `planned`. There is no date. Published binaries are Linux and Windows, x86_64 and x86_32. Catalog: `https://cdn.blazium.app/toolchain/toolchain.json`.

A macOS build of the CLI can master an Interactive DVD. PS1, PS2, and N64 setup and build exit `2` on that host. CI does not publish a macOS binary. CI does run `go test`, `go vet`, `ps2 build --out hello.elf`, and `n64 build --out hello.z64` on Ubuntu and Windows.

Sony BIOS images and N64 PIF dumps are never fetched. `C:\ultra` is ignored. Emulators are smoke validators (`ps1 run`, `ps2 run`, `n64 run`), not a substitute for hardware. Cook ABI numbers (`BLAZIUM_PS1_COOK_ABI`, `BLAZIUM_PS2_COOK_ABI`, `BLAZIUM_N64_COOK_ABI`) belong to the toolchain's guest interfaces and are not shared across platforms.

## Exit codes and report shape

The CLI treats stdout as process status, not a log stream. Exit `2` means a reserved platform (`ps3`, `ps4`) or a host that cannot compile that guest. Exit `3` means a required host tool is missing. Failures go through the report helpers so a pasted GitHub issue includes kind, message, suggested fix, command line, host triple, toolchain version, and prefix. `--json` collapses the same fields into one object. There is no rotating session log beside that stream.

![Toolchain exit codes: 0 ok, 1 usage, 2 planned or unsupported host, 3 missing tool, 4 fail](assets/exit-codes.png)

| Code | Meaning in this CLI |
|---|---|
| `0` | Success |
| `1` | Usage / unknown platform (also: no arguments prints help and exits `1`) |
| `2` | Planned platform (`ps3`, `ps4`) or host that cannot compile that guest |
| `3` | Required host tool missing, or offline when a fetch is required |
| `4` | Other failure after the command was understood |

That contract matters for the architecture story: the MIT editor only needs to spawn, read exit status, and surface the child’s text. It does not import the Go report package, and it does not need to understand every fetch URL in `pins.json`.

## Editor spawn workflow

Interactive DVD is the only in-tree export platform that shells the CLI. The practical sequence inside the editor is:

1. `InterDVDToolchain::discover_binary` resolves the path (preset / editor setting, then `BLAZIUM_TOOLCHAIN`, then `PATH`).
2. Scene bake or cell transcode that needs encode calls `interdvd setup` when status says encode is not ready.
3. Encode runs `interdvd ffmpeg` with the argument list the editor builds.
4. ISO export runs `interdvd iso` via `InterDVDIfoWriter::toolchain_iso_args` / `InterDVDToolchain::iso_args`: `--dir`, `--out`, optional `--meta` / `--write-meta`, and `--json`.

Dummy-VOB paths that never call FFmpeg can finish without the binary. ISO export and bake paths that need the CLI fail with an explicit missing-toolchain message instead of silently shelling `mkisofs`.

PS1, PS2, and N64 never enter that editor class. After `setup` on Windows or Linux you run `build`, `run`, `iso` / `rom`, and cook flags from a terminal. Cook ABI constants (`BLAZIUM_PS1_COOK_ABI`, `BLAZIUM_PS2_COOK_ABI`, `BLAZIUM_N64_COOK_ABI`) live in the toolchain guest code and are not shared across platforms. They are not an editor cooker on `blazium-dev`.

## Failure cases at the license boundary

| Failure | What it means | What to do |
|---|---|---|
| Editor reports toolchain not found | Discovery order found nothing | Set `export/inter_dvd/toolchain`, `BLAZIUM_TOOLCHAIN`, or `PATH` |
| `interdvd iso` asked for `mkisofs` | Wrong mental model | This path masters ISO9660+UDF inside the Go process |
| Language / region missing from IFO after CLI ISO | CLI meta fields stay in `disc.interdvd.json` | Use engine `InterDVDIfoWriter` authoring for IFO region/parental/menu/audio |
| `ps3` / `ps4` exit `2` | Reserved / planned | Do not treat as a ship date |
| macOS `ps1 setup` exit `2` | Console hosts are Windows/Linux | Use those hosts for compile; macOS can still master Interactive DVD from a local build |
| Guest links appear inside the editor binary | Someone vendored SDK trees | Keep compilers and SDKs in the toolchain cache / guest export only |

## Validation versus a shipped title

We used the CLI in-house to validate the four console-adjacent targets and the Interactive DVD editor path. That is not a shipped console title on a storefront. The architecture exists so the MIT editor can stay MIT while authors who need those compilers have one place to fetch them.

Guest cook flags (`--tim`, `--node`, `--luau`, and the rest) read paths you name. The CLI does not sandbox those paths. Treat them like any other build tool that trusts the working tree. Cook ABI constants (`BLAZIUM_PS1_COOK_ABI`, `BLAZIUM_PS2_COOK_ABI`, `BLAZIUM_N64_COOK_ABI`) version the toolchain's guest interfaces and are not shared across platforms—another reason the guest trees live beside the CLI instead of inside `blazium.git`.

## Commands the architecture implies

These are the verbs the split exists to keep outside the MIT editor process:

| Verb | Runs where | Notes |
|---|---|---|
| `ps1\|ps2\|n64 setup` | Terminal / CI | Fetches pinned compilers into the prefix |
| `ps1\|ps2\|n64 build` | Terminal / CI | Links guest stubs; not an `EditorExportPlatform` |
| `interdvd setup` / `ffmpeg` / `iso` | Editor spawn or terminal | Only Interactive DVD has an export platform |
| `steam setup` | Terminal | Caches SteamCMD for CLI deploy; no login |
| `ps3` / `ps4` | Anywhere | Exit `2`, status `planned` |

Catalog for published Linux and Windows binaries: `https://cdn.blazium.app/toolchain/toolchain.json`. CI in that repo runs `go test`, `go vet`, and sample `ps2` / `n64` builds on Ubuntu and Windows. It does not publish a macOS binary even though a local macOS build can master Interactive DVD.

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
