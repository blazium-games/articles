---
title: "GitHub Actions for Blazium"
description: "Four repositories: put the CLI on a runner, install an editor, export a preset, deploy an artifact. Pin the tag."
cover: "assets/cover.png"
slug: "github-actions-for-blazium"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# GitHub Actions for Blazium

### Pin the tag you mean to run

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

In 2025 we published the CLI, a deploy path, and a set of GitHub Actions next to Hangman. Hangman later shipped on Steam, Discord, Google Play, and the Apple App Store. Those storefronts are how export and deploy were checked. They do not mean each store build called the same workflow file.

The public actions are four repositories. They are not a folder in the engine. CI talks to the CDN through [blazium-cli](https://github.com/blazium-games/blazium-cli).

![setup-cli, then setup-engine, then export, then deploy](assets/github-actions-flow.png)

| Action | Tag to pin | Job |
|---|---|---|
| [setup-blazium-cli](https://github.com/blazium-games/setup-blazium-cli) | `v0.2.1` | Download the CLI from `cdn.blazium.app/cli/cli.json` and put it on `PATH` |
| [setup-blazium-engine](https://github.com/blazium-games/setup-blazium-engine) | `v0.3.0` | `blazium-cli install`, optional templates |
| [export-blazium-game](https://github.com/blazium-games/export-blazium-game) | `v0.3.2` | Export a preset |
| [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game) | `v0.0.2` | Push an already-exported artifact |

`v0.2.1` and `v0.3.0` are git tags. The latest GitHub Release objects for those two repos are older (`v0.2.0` and `v0.1.1`). Pin the tag the action README uses, not whatever the Releases page calls Latest, until you have read the newer tag. Older examples that say `blazium-engine/export-blazium-game@master` use the former organization path. The current export action also self-checks out that old path, which GitHub redirects today. Prefer `blazium-games/…` and a version tag in new workflows.

![Pin setup-blazium-cli v0.2.1, setup-blazium-engine v0.3.0, export-blazium-game v0.3.2, and deploy-blazium-game v0.0.2](assets/pinned-actions.png)

![blazium-cli --help](assets/cli-help.svg)

```text
asciinema play assets/cli-help.cast
```

## A workflow

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

`setup-blazium-engine` calls `setup-blazium-cli` for you. After a successful install it exports `BLAZIUM_EDITOR`, `BLAZIUM_EDITOR_BIN`, `BLAZIUM_INSTALLED_VERSION`, `BLAZIUM_INSTALL_PATH`, and `BLAZIUM_TEMPLATE`.

![setup-blazium-engine installs through blazium-cli, exports BLAZIUM_EDITOR and BLAZIUM_TEMPLATE, then export-blazium-game builds an artifact for a deploy workflow or blazium-cli deploy](assets/setup-then-export.png)

## setup-blazium-cli inputs

| Input | Default | Meaning |
|---|---|---|
| `version` | empty | CLI semver; empty uses `.latest` from the manifest |
| `manifest-url` | `https://cdn.blazium.app/cli/cli.json` | Override only if you host a mirror |
| `downloads-path` | `downloads` | Directory added to `PATH` |

The action resolves runner OS to `linux` / `windows` / `darwin`, prefers host arch, and falls back to `x86_64` when the preferred arch is missing from the manifest. It verifies SHA-256 when the manifest entry has one, then runs `blazium-cli --version`.

## Version input on setup-engine

`setup-blazium-engine` `version` defaults to `latest`.

| Input | Meaning |
|---|---|
| `0.6.838` | That release |
| `latest-release` | Highest version on the release channel |
| `nightly`, `latest`, `latest-nightly` | Nightly channel. `latest` is nightly |
| `0.6.924-nightly` | That nightly |
| `latest-0.6` | Highest 0.6.x across nightly and release |
| `latest-release-0.6` | Highest 0.6.x on release |
| `lts` / `latest-lts` | Passed through as install spec `lts` |

If you wanted a release and you wrote `latest`, you get a nightly. Templates install under the Blazium version, not Godot `4.3.2.stable`.

Other inputs: `download_editor` (default true), `download_template` (default false), `download_mono`, `platform`, `arch`, `use-cache`, `cli-version`, `bin-path` (default `bin`). The cache key includes the resolved version, platform, arch, and whether Mono was requested. Changing only the game source does not invalidate that cache. On a cache hit the action re-registers the binary with `blazium-cli editors add` and still fetches templates when `download_template` is true.

CLI only:

```yml
- uses: blazium-games/setup-blazium-cli@v0.2.1
- run: blazium-cli install 0.6.838 --templates --json --quiet
```

## Export: platform-name and secrets

`platform-name` must match the export preset name. The action rewrites `export_presets.cfg` from its own copy. Known mappings inside the action:

| `platform-name` | Artifact shape |
|---|---|
| `Windows Desktop x86_64` / `x86_32` / `arm64` / `arm32` | `.exe` |
| `Linux x86_64` / `x86_32` | `.x86_64` / `.x86_32` |
| `macOS` | `.app` |
| `iOS` | `.xcarchive` → `.ipa` |
| `Android` | `.aab` |
| `Web` | `index.html` under `build/` |

The web preset's `get_name()` is `Web`. Desktop names are whatever you keep in `export_presets.cfg`. Apple and Android signing secrets stay empty until you export a store build. Windows export on Linux installs Wine and rcedit and writes Godot editor settings for those paths. Android without a keystore does `--export-debug`; with a keystore it does `--export-release`.

Required inputs: `game-name`, `platform-name`. Optional: `blazium-version` (default `latest`), package ids, Apple/Android secret blobs, `steam-app-id` + `store-name: steam`, `base-game-version`, `use-cache`.

## Deploy

Deploy runs on an artifact from export. Workflows in [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game):

![Active deploy-docker, deploy-android, deploy-ios, and deploy-macos workflows versus deprecated deploy-steam and deploy-itchio that redirect to blazium-cli deploy](assets/deploy-matrix.png)

| Workflow | Status |
|---|---|
| `deploy-docker.yml` | Active. Expects artifact preset name `Web` |
| `deploy-android.yml` | Active (Play) |
| `deploy-ios.yml` | Active |
| `deploy-macos.yml` | Active |
| `deploy-steam.yml` | Deprecated → `blazium-cli deploy steam` |
| `deploy-itchio.yml` | Deprecated → `blazium-cli deploy itch` |

Docker call shape from the README:

```yml
deploy-docker:
  uses: blazium-games/deploy-blazium-game/.github/workflows/deploy-docker.yml@v0.0.2
  with:
    artifact-name: Web
    docker-registry: registry.digitalocean.com
    registry-path: org-name/image-name
  secrets:
    docker-username: ${{ secrets.DOCKER_USERNAME }}
    docker-token: ${{ secrets.DOCKER_TOKEN }}
```

That workflow clones the webbuild template, drops the artifact into `static/`, and build-pushes with tags `latest` and `${{ github.sha }}`.

Steam / itch from the CLI instead:

```text
blazium-cli deploy steam upload
blazium-cli deploy itch push ./build --target user/game:windows
```

Credentials: `BLAZIUM_STEAM_*`, `BLAZIUM_BUTLER_API_KEY`, or `blazium-deploy.yml`. `deploy steam guard setup` is interactive. Do not put it in a job.

Do not paste secrets into the workflow file in a way that lands in the log. The kinds are Apple certificates, an Android keystore, a butler API key, a Docker token, and Steam publisher credentials.

## Headless checks

Headless Autowork is `"$BLAZIUM_EDITOR" --headless --path . -s run_tests.gd`. If an editor is already up with remote control, `blazium-cli remote autowork run --wait` talks to `127.0.0.1:6508`. Eval stays off unless `blazium/remote_control/allow_eval` is set. Port 6507 is the game JustAMCP default. Do not point the CLI at it.

## Environment exports after setup-engine

| Variable | Meaning |
|---|---|
| `BLAZIUM_EDITOR` | PATH-facing editor binary for later steps |
| `BLAZIUM_EDITOR_BIN` | Absolute path inside the Hub install tree |
| `BLAZIUM_INSTALLED_VERSION` / `version_latest` | Concrete resolved version |
| `BLAZIUM_INSTALL_PATH` | Editors root from `blazium-cli install-path` |
| `BLAZIUM_TEMPLATE` | Export templates root |

Use `"${BLAZIUM_EDITOR}" --headless …` rather than assuming `Blazium` is already on `PATH` from a previous job. Each job that needs the editor should run setup again or restore the cache the action manages.

macOS CDN zips are universal and named `*_macos.zip`. When `platform` is `macos` and `arch` is empty, setup-engine sets arch to `macos` so the CLI can match that filename token. Nested `.zip` leftovers from older packages are extracted before the action exports `BLAZIUM_EDITOR`.

## Matrix export workflow

Desktop and web exports often share one workflow with a matrix. The export action README uses that shape: each matrix cell sets `platform-name` to a known preset string, and the job runs on a runner that can produce that artifact. Windows Desktop presets are commonly exported from `ubuntu-latest` because the action installs Wine and rcedit and writes the editor settings paths for them.

```yml
strategy:
  fail-fast: false
  matrix:
    include:
      - platform: Linux x86_64
        runner: ubuntu-latest
      - platform: Windows Desktop x86_64
        runner: ubuntu-latest
      - platform: Web
        runner: ubuntu-latest
jobs:
  export:
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v4
      - uses: blazium-games/setup-blazium-engine@v0.3.0
        with:
          version: latest-release
          download_template: true
      - uses: blazium-games/export-blazium-game@v0.3.2
        with:
          blazium-version: latest-release
          game-name: MyGame
          platform-name: ${{ matrix.platform }}
```

Keep `game-name` stable across cells so artifact names stay predictable for deploy jobs that download them. `fail-fast: false` matters when one preset needs signing secrets another cell does not; a missing Android keystore should not cancel a Linux binary that already passed.

## Failure cases

| Symptom | Likely cause | Fix |
|---|---|---|
| Editor looks like a nightly after you typed `latest` | `setup-blazium-engine` maps `latest` to the nightly channel | Use `latest-release` or an exact `0.6.x` |
| Export cannot find a preset | `platform-name` does not match the name the action wrote into `export_presets.cfg` | Use the table names above, or accept that the action overwrites your local cfg |
| Templates missing at export | `download_template` stayed false, or version channel folders do not match | Set `download_template: true` and keep Blazium version + channel aligned |
| Android built as debug | No keystore secrets on the job | Supply `secret-android-keystore-*` for `--export-release` |
| SHA-256 mismatch on CLI download | Manifest `sha256` does not match the file | Fail the job; do not skip verification. Check `manifest-url` and CDN health |
| macOS runner cannot find `blazium-cli` | Published CLI packs are Linux and Windows | Run CLI steps on Linux/Windows, or host a darwin entry on your mirror |
| Steam / itch reusable workflow surprises | `deploy-steam.yml` / `deploy-itchio.yml` are deprecated | Call `blazium-cli deploy steam upload` or `blazium-cli deploy itch push` |
| Autowork cannot reach the editor | Wrong port or eval disabled | Editor remote control is `127.0.0.1:6508`; do not use JustAMCP `6507` |

Headless Autowork in CI does not need a live remote session. Prefer `"${BLAZIUM_EDITOR}" --headless --path . -s run_tests.gd` in the same job that ran setup-engine. Reserve `blazium-cli remote autowork run --wait` for a machine that already has an editor with remote control up.

## Secrets and job isolation

Apple certificates, Android keystores, Docker tokens, butler keys, and Steam publisher credentials belong in GitHub Actions secrets or environment secrets, not in the workflow YAML body. Base64 keystore blobs still decode onto the runner disk for the export step; treat the workspace as sensitive until the job ends.

Each job that needs the editor should run `setup-blazium-engine` again or restore the action-managed cache. Environment variables from one job do not appear in another. Cache keys include resolved version, platform, arch, and Mono; changing only game source leaves that cache valid, which is what you want for export-only pushes.

For store deploys that moved to the CLI, install the CLI once (`setup-blazium-cli@v0.2.1` or via setup-engine), then run deploy commands with credentials from the environment (`BLAZIUM_STEAM_*`, `BLAZIUM_BUTLER_API_KEY`) or `blazium-deploy.yml`. Interactive Steam Guard setup stays off CI.

## CLI-only and deploy follow-ups

When you only need the CLI on a runner (no editor install), pin setup-cli alone:

```yml
- uses: blazium-games/setup-blazium-cli@v0.2.1
- run: blazium-cli --version
- run: blazium-cli deploy itch push ./build --target user/game:windows
```

Docker deploy still expects the export artifact preset name `Web`. The reusable workflow clones the webbuild template, drops the artifact into `static/`, and build-pushes with tags `latest` and `${{ github.sha }}`. Android, iOS, and macOS reusable workflows remain active in the same deploy repo for those storefronts; only Steam and itch were deprecated there in favor of CLI verbs.

Export action inputs that gate store builds: `game-name` and `platform-name` are required. Optional signing and store fields include package ids, Apple/Android secret blobs, and `steam-app-id` with `store-name: steam`. Leaving Android keystore secrets empty selects `--export-debug`; providing them selects `--export-release`. Do not paste those blobs into the workflow file body where they land in logs.

## Limits

- Pin tags. Floating `@master` and the wrong org name are how old Hangman snippets rot.
- `latest` on setup-engine is nightly on purpose.
- export-blazium-game still vendors its own `export_presets.cfg` into the job; treat that as part of the contract when you customize presets.
- Steam and itch reusable workflows remain in the deploy repo as deprecated files; new jobs should call the CLI.
- setup-cli may select `darwin` as a platform string, but published CLI builds are Linux and Windows. A macOS runner only succeeds if the manifest you pointed at actually has a darwin entry, or you bring your own binary.

## Links

- setup-blazium-cli: https://github.com/blazium-games/setup-blazium-cli
- setup-blazium-engine: https://github.com/blazium-games/setup-blazium-engine
- export-blazium-game: https://github.com/blazium-games/export-blazium-game
- deploy-blazium-game: https://github.com/blazium-games/deploy-blazium-game
- CLI: https://github.com/blazium-games/blazium-cli
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
