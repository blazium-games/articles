---
title: "The Blazium Toolchain"
description: >-
    A focused CLI that fetches the right compilers and tools so you can build,
    test, and package projects for PlayStation, PlayStation 2, Nintendo 64,
    and Interactive DVD without the usual setup headaches.
cover: "assets/cover.png"
slug: "the-blazium-toolchain"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---
# Blazium Toolchain

The **Blazium Toolchain** downloads the necessary compilers and supporting
software into a local cache,
keeps everything organized, and gives you clear commands to build, run, and package your projects.
It works side-by-side with the Blazium editor and is designed to stay out of the way once the
environment is ready.

## Supported Platforms

The toolchain currently focuses on four targets:

- **PlayStation (PS1)**:
compile, test in an emulator, and create disc images
- **PlayStation 2 (PS2)**:
build executables, run them, and produce ISO or CHD files
- **Nintendo 64 (N64)**:
produce ready-to-run ROM files with options for resolution, memory, and extras
- **Interactive DVD**:
master properly structured discs that include video folders and optional extra files

Each platform offers different setup profiles so you only install what you actually need.

Platform identifiers for **PlayStation 3** and **PlayStation 4** are already reserved,
so future export and build support can slot in without breaking existing workflows.

## Building and Testing

You can start from included sample projects or point the toolchain at your own source folders.
Extra files can be overlaid on top of the base project, and the fully resolved source tree can be
exported for inspection or further editing.
Once built, programs can be launched in the appropriate emulator, headless for automated checks or
with a full window when you want to see the result.
Finished work can be packaged into the correct format, executable, ISO, ROM, or CHD, ready for
distribution or real hardware.

## Documentation & Next Steps

<!-- https://github.com/blazium-games/blazium-toolchain -->

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**