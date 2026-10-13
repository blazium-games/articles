---
title: 'Blazium Engine v0.6.927: The Final 4.3+ Release'
description: >-
  The last Blazium release on the 4.3+ line: GDScript traits, structs and
  @abstract, the JustAMCP editor MCP server, native Trenchbroom/Hammer map
  import, opt-in CrashReporter and Analytics, Steam Workshop and more. Next
  stop: the 4.8+ branch.
cover: assets/cover.jpg
changes: 'https://github.com/blazium-games/blazium/compare/v0.6.725...v0.6.927'
deployed: true
date: 2026-10-13
slug: blazium-engine-v06927-the-final-43-release
author: Bioblaze Payne
hosts:
  - name: IndieDB
    url: >-
      https://www.indiedb.com/engines/blazium-engine/news/blazium-engine-v06927-the-final-43-release
  - name: X
    url: 'https://x.com/BlaziumGames/status/2110041763385954656'
---
# Blazium Engine v0.6.927: The Final 4.3+ Release

![Blazium Engine](https://raw.githubusercontent.com/blazium-games/blazium/v0.6.927/logo.png)

*By Randolph Aarseth II, Co-Founder, Blazium Games ([blazium.games](https://blazium.games))*

**[v0.6.927](https://github.com/blazium-games/blazium/releases/tag/v0.6.927) is officially the last Blazium release on the 4.3+ line. Starting with the next release, Blazium moves to the 4.8+ branch.** This changelog covers everything after [v0.6.725](https://github.com/blazium-games/blazium/releases/tag/v0.6.725), up to and including v0.6.927 (July 16 – October 13, 2026).

**By the numbers:** 26 releases (3 stable: v0.6.817, v0.6.838 and v0.6.927, plus 23 nightlies), 202 commits, 74 merged pull requests, and 8 commit authors: 4 Blazium contributors (Bioblaze, TheKingScott, sshiiden, WhalesState) and 4 upstream Godot authors whose work was cherry-picked. Full diff: [v0.6.725...v0.6.927](https://github.com/blazium-games/blazium/compare/v0.6.725...v0.6.927).

---

## Highlights

- **GDScript traits, structs and `@abstract`.** GDScript now has a trait system and structs ([#792](https://github.com/blazium-games/blazium/pull/792)). Godot 4.5's abstract classes and methods are backported too ([#797](https://github.com/blazium-games/blazium/pull/797)).
- **JustAMCP, an MCP server built into the editor.** AI agents can drive the editor and running games over the Model Context Protocol. It ships with the full editor tool surface, sandboxing, undoable scene edits and support for both MCP spec eras ([#719](https://github.com/blazium-games/blazium/pull/719), [#746](https://github.com/blazium-games/blazium/pull/746), [#810](https://github.com/blazium-games/blazium/pull/810)).
- **Trenchbroom / Hammer map import.** Blazium's native map-import module adds Quake `.map` and Hammer VMF parsing, FGD configs, brush CSG and NetRadiant integration ([#715](https://github.com/blazium-games/blazium/pull/715)).
- **CrashReporter and Analytics, both opt-in.** Crash reporting uses Breakpad minidumps. Analytics has identity, consent and an HTTP queue. Both are keyed to an App ID and Build ID that are baked in at build time ([#748](https://github.com/blazium-games/blazium/pull/748), [#749](https://github.com/blazium-games/blazium/pull/749), [#751](https://github.com/blazium-games/blazium/pull/751), [#753](https://github.com/blazium-games/blazium/pull/753)).
- **Steam Workshop and obfuscation.** Steam Workshop (ISteamUGC) is now supported ([#812](https://github.com/blazium-games/blazium/pull/812)). A first-party obfuscation module adds identity seals, asset marks and HMAC-scrambled GDScript/Luau packs ([#794](https://github.com/blazium-games/blazium/pull/794), [#813](https://github.com/blazium-games/blazium/pull/813)).

---

## Scripting: GDScript and Luau

- **Traits and structs** were added to GDScript, along with the `GDScriptStruct` class reference and `PROPERTY_HINT_STRUCT` ([#792](https://github.com/blazium-games/blazium/pull/792)).
- **`@abstract` classes and methods**, with runtime checks that block instantiating an abstract class and a fix for the "inherit from abstract class" dialog ([#797](https://github.com/blazium-games/blazium/pull/797)). These are upstream cherry-picks; see the Godot section below.
- **Opt-in GDScript style guide** warnings ([#721](https://github.com/blazium-games/blazium/pull/721)).
- **Interpreter fixes:**
  - Integer division or modulo of INT64_MIN by -1 no longer crashes.
  - Short-circuiting logical operators no longer trigger the STANDALONE_EXPRESSION warning ([#726](https://github.com/blazium-games/blazium/pull/726)).
- **Missing-comma checks** were added ([#731](https://github.com/blazium-games/blazium/pull/731)).
- **Custom enumerations** are highlighted correctly again ([#739](https://github.com/blazium-games/blazium/pull/739)).
- **`ord()` is back** in GDScript ([#779](https://github.com/blazium-games/blazium/pull/779)).
- **Luau:** Add Child Node no longer returns a null child for global classes, editor analysis is fixed, and TextEdit gutter lines are fixed ([#724](https://github.com/blazium-games/blazium/pull/724)).

## Editor

- **Blazium module menus.** Each Blazium module screen now opens in its own window from a Blazium menu ([#816](https://github.com/blazium-games/blazium/pull/816)). The windows are set up before they appear and use the editor's panel color ([#827](https://github.com/blazium-games/blazium/pull/827)).
- **remote_control module.** The editor accepts non-blocking HTTP control from the CLI, including play and snapshot commands ([#732](https://github.com/blazium-games/blazium/pull/732)).
- **Hub flags.** New `hub_build` and `hub_register` flags, plus a bridge from JustAMCP to remote_control ([#742](https://github.com/blazium-games/blazium/pull/742)).
- **AssetTags and SemanticSearch** for project assets ([#719](https://github.com/blazium-games/blazium/pull/719)).
- **Editor-only navmesh export.** 2D and 3D navigation can be baked and written out for dedicated servers ([#775](https://github.com/blazium-games/blazium/pull/775)).
- **Project files.** `project.blazium` is now preferred, and `project.godot` is still accepted ([#743](https://github.com/blazium-games/blazium/pull/743)).
- **Startup errors.** Node3D `!is_inside_tree()` errors at editor startup are gone. VisualInstance3D skips transform updates until the node is in the tree ([#774](https://github.com/blazium-games/blazium/pull/774)).
- **Autowork testing.** Test discovery, JUnit output, CLI and port gaps are closed, so tests run without extra scripts ([#772](https://github.com/blazium-games/blazium/pull/772)).
- **Test cleanup.** Unit tests no longer leave `.tscn` or `.blazium` files in the engine tree ([#773](https://github.com/blazium-games/blazium/pull/773)).

## JustAMCP (Model Context Protocol)

- **Initial integration** ([#719](https://github.com/blazium-games/blazium/pull/719)).
- **Connectivity:**
  - Streamable HTTP connectivity and Output spam are fixed ([#728](https://github.com/blazium-games/blazium/pull/728)).
  - Port 6506 really binds now, and a failed bind fails loudly ([#747](https://github.com/blazium-games/blazium/pull/747)).
  - The CLI `--mcp-port` and Editor Settings stay in sync ([#757](https://github.com/blazium-games/blazium/pull/757)).
- **Spec support.** MCP 2026-07-28 is served statelessly, alongside Cursor 2025-11-25 sessions, with capabilities gated per spec era ([#746](https://github.com/blazium-games/blazium/pull/746)).
- **Tool surface:**
  - Section toggles now act as a tools/list budget instead of hiding tools ([#750](https://github.com/blazium-games/blazium/pull/750)).
  - Sandboxed native tools close the gaps relative to Godot agents ([#758](https://github.com/blazium-games/blazium/pull/758)).
  - The full editor surface is exposed, and headless calls stay inside the project ([#810](https://github.com/blazium-games/blazium/pull/810), [#814](https://github.com/blazium-games/blazium/pull/814)).
  - Tools are initialized in shipping editors, and tiled import is fixed ([#829](https://github.com/blazium-games/blazium/pull/829)).
- **Client host.** A sterilized Streamable HTTP MCP client host was added ([#759](https://github.com/blazium-games/blazium/pull/759)).
- **Runtime MCP in exports.** Exported games can opt in to their own MCP server, using the game port +1 and project-owned tools ([#768](https://github.com/blazium-games/blazium/pull/768)).
- **Reliability:**
  - Sessions are isolated, and the verification tools go deeper ([#819](https://github.com/blazium-games/blazium/pull/819)).
  - Calls return modern MCP results, and the editor stays responsive while an agent drives it ([#822](https://github.com/blazium-games/blazium/pull/822)).
  - Scene edits can be undone without stalling the editor or flooding the log ([#824](https://github.com/blazium-games/blazium/pull/824)).
  - Cancel/dispatch no longer double-frees queue entries ([#774](https://github.com/blazium-games/blazium/pull/774)).
  - Listen streams for MCP 2026-07-28 stay alive and deliver tool results ([dce25da](https://github.com/blazium-games/blazium/commit/dce25da06105bd1b3ec0f0ff211d7b4bb466f611)).
- **Editor console.** Array editor-settings warnings no longer appear on load ([#744](https://github.com/blazium-games/blazium/pull/744)).

## 2D, 3D and Content

- **Sprite2D `mask_parent`** ([#720](https://github.com/blazium-games/blazium/pull/720)).
- **GIF module.** A `GIFTexture` that works anywhere a texture does, with autoplay on load and more import options. It also fixes compressed-texture errors in `Sprite2D.is_pixel_opaque` ([#752](https://github.com/blazium-games/blazium/pull/752)).
- **Trenchbroom map import** covers Quake `.map` and Hammer VMF, including displacements, overlays, patches and instances. It also adds FGD point classes, an editor plugin and doctests ([#715](https://github.com/blazium-games/blazium/pull/715)).
- **dddbrowser module** for exporting and previewing DDD pages ([#725](https://github.com/blazium-games/blazium/pull/725)).
- **InterDVD** scene authoring, with export through blazium-toolchain ([#764](https://github.com/blazium-games/blazium/pull/764)).

## Blazium Services and Modules

- **CrashReporter.** Opt-in, using Breakpad minidumps ([#748](https://github.com/blazium-games/blazium/pull/748)).
- **Analytics.** Opt-in, with identity, consent and an HTTP queue ([#749](https://github.com/blazium-games/blazium/pull/749)).
- **App identity:**
  - Both services identify the app by a shared App ID and Build ID ([#751](https://github.com/blazium-games/blazium/pull/751)).
  - The editor's App ID, Build ID and analytics URL are baked in at build time and can't be changed at runtime ([#753](https://github.com/blazium-games/blazium/pull/753)).
  - Optional template identity is locked at bake time, and the sidecar file is found next to the game ([#754](https://github.com/blazium-games/blazium/pull/754)).
- **ColdStorage.** An editor VCS module ([#737](https://github.com/blazium-games/blazium/pull/737)).
- **Obfuscation module:**
  - Identity seals, asset marks, comment-lattice evidence, and HMAC-scrambled GDScript/Luau packs ([#794](https://github.com/blazium-games/blazium/pull/794)).
  - Exports built with `scramble_names` now load, and renaming is safe ([#813](https://github.com/blazium-games/blazium/pull/813)).
- **Steam Workshop** (ISteamUGC) support ([#812](https://github.com/blazium-games/blazium/pull/812)).
- **TownSDK.** An FPS client with game-type switching, username auth, look movement, fire/shot/health/death/respawn, pickup/equip/use/reload, crafting, dropping items, interaction and admin_bank ([#776](https://github.com/blazium-games/blazium/pull/776)). It also advertises the VoIP host from HELLO_ACK ([#784](https://github.com/blazium-games/blazium/pull/784)) and supports moving items in grid inventories ([#785](https://github.com/blazium-games/blazium/pull/785)).
- **Warcry.** An Opus voice client with an editor admin dock ([#777](https://github.com/blazium-games/blazium/pull/777)). Follow-up work covers:
  - stereo downlink ([#780](https://github.com/blazium-games/blazium/pull/780))
  - decoder fallback and safe swapping ([#786](https://github.com/blazium-games/blazium/pull/786), [#787](https://github.com/blazium-games/blazium/pull/787), [#789](https://github.com/blazium-games/blazium/pull/789))
  - dropping voice from users or channels that are gone ([#790](https://github.com/blazium-games/blazium/pull/790))
  - applying full SERVER_STATE arrays and clearing the roster on disconnect ([#791](https://github.com/blazium-games/blazium/pull/791))
- **4.8 only.** Warcry, TownSDK and ColdStorage were later removed from the 4.3 line and kept on the 4.8 branch ([#804](https://github.com/blazium-games/blazium/pull/804)).

## Networking

- **ENetServer.** A buffer overflow is fixed ([#717](https://github.com/blazium-games/blazium/pull/717)).
- **games_enet_webrtc.** A new module runs ENet over WebRTC. It is off by default ([#769](https://github.com/blazium-games/blazium/pull/769)).

## Platforms and Export

- **Windows:**
  - Live wallpaper module ([#765](https://github.com/blazium-games/blazium/pull/765)).
  - Screensaver module ([#766](https://github.com/blazium-games/blazium/pull/766)).
  - Double-clicking the tray icon restores the window ([#773](https://github.com/blazium-games/blazium/pull/773)).
- **Device autorun,** plus fixes to export consumers ([#767](https://github.com/blazium-games/blazium/pull/767)).
- **Hiding the main window.** A project setting allows it on Windows, Linux and macOS ([#770](https://github.com/blazium-games/blazium/pull/770)).
- **OS packaging.** Branding is fixed, Wayland desktop icons match correctly, and the desktop files and Windows installer rename are documented ([#743](https://github.com/blazium-games/blazium/pull/743)).
- **Archives.** Web template ZIPs and the Steam icon pack are now built with 7z ([#730](https://github.com/blazium-games/blazium/pull/730)).

## CI and Build

- **Nightly versioning.** `update_version_from_git.py` and an SCons `update_version_from_git` flag set nightly versions from git tags ([#729](https://github.com/blazium-games/blazium/pull/729), [#742](https://github.com/blazium-games/blazium/pull/742)).
- **Breakpad build fixes.** The web editor's timeval and missing compat headers are fixed ([#755](https://github.com/blazium-games/blazium/pull/755)). Linux x86_32 assembles, the crash reporter stays off web and mobile, and flaky D3D12 SDK downloads are retried ([#756](https://github.com/blazium-games/blazium/pull/756)).
- **Xbox CI.** The Windows Xbox MSVC job no longer starves the hosted runner, and it stays on windows-latest so the Gaming GDK is available ([#771](https://github.com/blazium-games/blazium/pull/771)).
- **Upstream sync job.** A daily job cherry-picks new commits from godotengine/godot master into `blazium_4.8`. It has a manual dry-run option and compares against upstream master, not the fork's own master. It also skips patches already on the branch and reads skip SHAs from a list file ([#781](https://github.com/blazium-games/blazium/pull/781), [#782](https://github.com/blazium-games/blazium/pull/782), [#783](https://github.com/blazium-games/blazium/pull/783), [#800](https://github.com/blazium-games/blazium/pull/800)).

## Docs

- **Class references** were synced with `--doctool` output for the new modules, including Analytics, CrashReporter, GIFTexture, TownSDK, Warcry and JustAMCP.
- **Project documentation** now describes both engine lines and keeps Blazium Games separate as its own product ([712c1e3](https://github.com/blazium-games/blazium/commit/712c1e3a0)).

## Upstream Godot Cherry-picks

- [Windows] Intel Gen9.5 (Kaby Lake) GPUs added to the ANGLE blocklist, by bruvzg ([#722](https://github.com/blazium-games/blazium/pull/722)).
- GDScript: `ord()` re-added, by dalexeev ([#779](https://github.com/blazium-games/blazium/pull/779)).
- GDScript abstract classes and the `@abstract` annotation, by aaronfranke. Abstract methods and runtime instantiation checks, by dalexeev. The inherit-from-abstract dialog fix, by IphStich ([#797](https://github.com/blazium-games/blazium/pull/797)).

---

Release downloads: [github.com/blazium-games/blazium/releases/tag/v0.6.927](https://github.com/blazium-games/blazium/releases/tag/v0.6.927). Next up is Blazium on 4.8+. Follow along at [blazium.games](https://blazium.games).
