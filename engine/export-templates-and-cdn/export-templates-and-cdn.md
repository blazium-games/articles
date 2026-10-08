---
title: "Export templates and the CDN"
description: "Templates are versioned as Blazium 0.6.x, not Godot 4.3.2. How the CLI and the editor fetch them."
cover: "assets/cover.png"
slug: "export-templates-and-cdn"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Blazium on the `blazium-dev` line is a Godot 4.3.2-compatible engine with its own version number, currently in the `0.6.x` range. Export templates are stored under that Blazium version. They are not stored under a `4.3.2.stable` folder. If you copied a Godot template layout by hand, the export dialog will say the templates are missing even though the files are on disk.

## Status

Release CI publishes editor zips and template bundles to `cdn.blazium.app`. Hub, at runtime, only reads that host. The CLI falls through to `GET /api/v1/templates/{deploy_type}/{version}` on `https://blazium.app` when `template_files.json`, `templates.json`, and `details.json` are all missing. Override that API base with `BLAZIUM_CEREBRO_URL`. Hub does not call it.

Mono is a second `.tpz` when you pass `--mono` or `download_mono` in CI. It is not a different version number. Web, Discord embed, and YouTube Playables flags live on the export preset named `Web`, not in a separate template product.

Install templates for the same Blazium version as the editor you are running. `blazium-cli install 0.6.725 --templates` is the command that does both. The editor Export Template Manager keys off the running editor's Blazium version, so a nightly editor will not use a release template directory.

![Two version numbers](assets/dual-version.png)

## What a template is

Each platform has `template_debug` and `template_release`. Mono builds are a second `.tpz` when you pass `--mono`. The web preset (`Web`) can also emit a Discord embed script and a YouTube Playables script, and it can gzip the WASM. Those flags live on the export preset, not in a separate template product. See [Discord on Blazium](../discord-on-blazium/discord-on-blazium.md).

## CLI

```text
blazium-cli install 0.6.725 --templates
blazium-cli templates list
blazium-cli templates download 0.6.725 --tpz
```

`install --templates` uses the CDN `.tpz` bundle. Individual file helpers resolve metadata in this order (from the CLI README):

1. `https://cdn.blazium.app/{channel}/{version}/template_files.json`
2. `…/templates.json` (legacy per-file list, or a `{base,mono}` bundle)
3. `…/details.json` (the export template manager bundle)
4. `GET /api/v1/templates/{deploy_type}/{version}` on `https://blazium.app`

Override the API base with `BLAZIUM_CEREBRO_URL`. The CLI calls that API. Hub does not.

On Unix, including macOS, the install root the CLI reports is `~/.local/share/blazium/export_templates`. On Windows it is under `%LOCALAPPDATA%\Blazium\export_templates`. Files land in a versioned subdirectory.

![templates --help](assets/cli-templates-help.svg)
<!-- ASCIINEMA: assets/cli-templates-help.cast | blazium-cli templates --help -->

## Editor

The Export Template Manager and the Export dialog both key off the running editor's Blazium version. Web preset checkboxes:

- `blazium/discord_embed/enabled` (and `blazium/discord_embed/autodetect`)
- `blazium/youtube_playable/enabled`
- `blazium/export_gzip_compressed_wasm/enabled`

`get_name()` for that platform is `Web`. A workflow `platform-name` has to match the preset name in `export_presets.cfg`, so the string is `Web`, not a menu label.

## CDN layout

![cdn.blazium.app tree](assets/cdn-tree.png)

| Prefix | Contents |
|---|---|
| `/{channel}/{version}/` | Editor builds and templates (`template_files.json`, `templates.json`, `details.json`) |
| `/cli/` | CLI binaries and `cli.json` |
| `/hub/` | Hub installers |
| `/crash_reporter/` | Sidecar catalog `crash_reporter.json` |
| `/toolchain/` | `toolchain.json` |
| `/articles/` | Hub News (`rss.xml`, bbcode, assets) |
| `/catalog/versions/` | `nightly.json`, `release.json`, and `latest.json` |

Release CI publishes those objects into the bucket. Hub, at runtime, only reads `cdn.blazium.app`. It does not call the Cerebro API. The CLI is the tool that falls through to `GET /api/v1/templates/...` when the three CDN manifests are missing.

## One export

Install templates for the same Blazium version as the editor, then export. If the editor is `0.6.725` and the only templates on disk are under a Godot `4.3.2` path, start over with `blazium-cli install 0.6.725 --templates`.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
