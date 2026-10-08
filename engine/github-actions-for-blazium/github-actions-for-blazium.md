---
title: "GitHub Actions for Blazium"
description: "setup-blazium-cli, setup-blazium-engine, export-blazium-game, and deploy-blazium-game: install the tools in CI and ship a build."
cover: "assets/cover.png"
slug: "github-actions-for-blazium"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Four Actions. Each one is its own repository under [blazium-games](https://github.com/blazium-games). CI talks to the CDN through [blazium-cli](../blazium-cli/blazium-cli.md).

## Status

Pin the tag you intend to run. Current tags: `setup-blazium-cli@v0.2.1`, `setup-blazium-engine@v0.3.0` (that composite calls `setup-blazium-cli@v0.2.1`), `export-blazium-game@v0.3.2`, `deploy-blazium-game@v0.0.2`. Older README examples still say `blazium-engine/export-blazium-game@master`. That org name is not the repository.

`setup-blazium-engine` input `version: latest` tracks the nightly channel. `latest-release` is the release channel. Writing `latest` when you wanted a release build installs a nightly.

Steam and itch.io reusable workflows in deploy-blazium-game are marked deprecated. The replacement in that README is `blazium-cli deploy steam` and `blazium-cli deploy itch`. Docker, Play, iOS, and macOS workflows in the repo are unchanged. `deploy steam guard setup` is interactive. Do not put it in a job.

![setup-cli, then setup-engine, then export, then deploy](assets/github-actions-flow.png)

| Action | Repository | Job |
|---|---|---|
| Setup Blazium CLI | `blazium-games/setup-blazium-cli` | Download CLI from `cdn.blazium.app/cli/cli.json` and put it on `PATH` |
| Setup Blazium Engine | `blazium-games/setup-blazium-engine` | `blazium-cli install`, optional templates |
| Export Blazium Game | `blazium-games/export-blazium-game` | Export a project. `platform-name` must match an editor export preset |
| Deploy Blazium Game | `blazium-games/deploy-blazium-game` | Push an already-exported artifact |

Use the tags in Status, or a newer one you have read. The action list below is the job each repo does.

![blazium-cli --help](assets/cli-help.svg)
<!-- ASCIINEMA: assets/cli-help.cast | blazium-cli --help -->

## Minimal workflow

```yml
name: export
on: [push]
jobs:
  linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: blazium-games/setup-blazium-engine@v0.3.0
        with:
          version: latest-release
          download_template: true
      - name: Autowork
        run: "${BLAZIUM_EDITOR} --headless --path . -s run_tests.gd"
      - uses: blazium-games/export-blazium-game@v0.3.2
        with:
          blazium-version: latest-release
          game-name: MyGame
          platform-name: Linux x86_64
```

`setup-blazium-engine` calls `setup-blazium-cli` for you. After a successful install it exports `BLAZIUM_EDITOR`, `BLAZIUM_INSTALLED_VERSION`, and `BLAZIUM_TEMPLATE`.

## Version input

`setup-blazium-engine` `version` (default `latest`):

| Input | Meaning |
|---|---|
| `0.6.725` | That release |
| `latest-release` | Highest version on the release channel |
| `nightly`, `latest`, `latest-nightly` | Nightly channel. `latest` tracks nightly |
| `0.6.751-nightly` | That nightly |
| `latest-0.6` | Highest 0.6.x across nightly and release |
| `latest-release-0.6` | Highest 0.6.x on release |
| `lts` | LTS alias handled by the CLI |

If you wanted a release and you wrote `latest`, you get a nightly. Same version trap as [export templates](../export-templates-and-cdn/export-templates-and-cdn.md): Blazium `0.6.x`, not Godot `4.3.2`.

Other inputs: `download_template` (default `false`), `download_mono`, `platform`, `arch`, `use-cache`, `cli-version`. The cache key includes the resolved version, platform, arch, and whether Mono was requested.

CLI only:

```yml
- uses: blazium-games/setup-blazium-cli@v0.2.1
- run: blazium-cli install 0.6.725 --templates --json --quiet
```

Empty `version` on setup-cli uses `.latest` from `cli.json`. The action verifies SHA-256 when the manifest has one. Host arch is preferred. It falls back to `x86_64` when the CDN has no build for the runner arch.

## Export

`platform-name` must match the export preset name in the editor. Examples from the engine: `Web` (`EditorExportPlatformWeb.get_name()`), plus the desktop preset names in your `export_presets.cfg` (`Linux x86_64`, `Windows Desktop x86_64`, and the rest). The action rewrites `export_presets.cfg`. Apple and Android signing secrets stay empty until you export a store build. Steam uses `store-name: steam` plus `steam-app-id`.

## Deploy

Deploy runs on an artifact from export. Targets in the deploy README: Docker registry, itch.io, Play Store, iOS App Store, macOS App Store, Steam. See Status for which of those workflows are deprecated.

Do not paste secrets into the workflow file in a way that lands in the log. The kinds are Apple certificates, an Android keystore, a butler API key, a Docker token, and Steam publisher credentials.

A cache hit on `setup-blazium-engine` is keyed by resolved version, platform, arch, and whether Mono was requested. Changing only the game source does not invalidate that cache. The editor binary is what the cache holds.

## Autowork in CI

```text
"$BLAZIUM_EDITOR" --headless --path . -s run_tests.gd
```

Or, if an editor is already up with remote control: `blazium-cli remote autowork run --wait`. See [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
