---
title: "Blazium CLI"
description: "Install editors, register projects, fetch templates, self-update, and remote-control a running editor."
cover: "assets/cover.png"
slug: "blazium-cli"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

`blazium-cli` is the binary [Hub](../blazium-hub/blazium-hub.md) shells, CI calls, and Windows/Linux register for `blazium://`. It installs editors, keeps the project registry, fetches export templates, updates itself, talks to a running editor, and can deploy a finished build to Steam or itch.io. Blazium Games store uploads are a different tool (`chauffeur`), not this binary.

## Get it

Installing Hub is the path that also installs the CLI. The other paths are for machines that should not run Hub.

1. **Hub bundle.** Inno (Windows) and the `.deb` (Linux) put `blazium-cli` next to Hub and on `PATH`.
2. **npm.** `npm install -g @blazium-engine/cli` or `npx @blazium-engine/cli`. The optional packages are `@blazium-engine/cli-linux-x64`, `cli-linux-ia32`, `cli-win32-x64`, and `cli-win32-ia32`. If that package is present, nothing is downloaded from the CDN.
3. **GitHub Releases.** `blazium-cli-windows-x86_64.exe`, `blazium-cli-windows-x86_32.exe`, `blazium-cli-linux-x86_64`, `blazium-cli-linux-x86_32`. Published binaries are Linux and Windows. A CLI you build yourself on macOS can still install a macOS editor.
4. **CDN manifest.** `https://cdn.blazium.app/cli/cli.json`. Files live at `https://cdn.blazium.app/cli/{os}/{arch}/{version}/blazium-cli[.exe]`.

Local `go build` prints `0.0.0-dev` until CI stamps `data/cliBuild.txt`. Go 1.25 or later. `go test ./...` then `go build -o blazium-cli .`

![blazium-cli --help](assets/cli-help.svg)
<!-- ASCIINEMA: assets/cli-help.cast | blazium-cli --help -->

```text
asciinema play assets/cli-help.cast
```

## Install an editor

```text
blazium-cli install 0.6.725
blazium-cli install nightly --templates
blazium-cli install 0.6.751 --channel nightly
blazium-cli uninstall 0.6.725
```

Current `EditorInstallDir` puts editors in `{install-path}/{channel}/{version}`. Channels are `release`, `prerelease`, and `nightly`. An empty channel is treated as `release`. `--templates` also pulls the `.tpz` bundle for that version. See [Export templates and the CDN](../export-templates-and-cdn/export-templates-and-cdn.md).

The `editors` cast in this article is from an older CLI: that machine stored `0.6.725` directly under `Editors\`, with `channel:release` only as a field. New installs follow the channel directory.

![blazium-cli install-path](assets/cli-install-path.svg)
<!-- ASCIINEMA: assets/cli-install-path.cast | blazium-cli install-path -->

`blazium-cli install-path` prints the root. `blazium-cli install-path D:\Blazium\Editors` changes it. `--move` relocates editors that are already on disk.

## List and default

```text
blazium-cli editors
blazium-cli editors default
blazium-cli editors default --channel release --version latest
blazium-cli editors default 0.6.725
blazium-cli editors add C:\path\to\blazium.exe --version 0.6.725
blazium-cli install-path
```

Unset policy is **latest release** among installed editors. `default_editor_channel` is `release`, `prerelease`, or `nightly`. `default_editor_version` is `latest` or a concrete version. A hard pin (`editors default 0.6.725`) wins when that build is installed.

![blazium-cli editors](assets/cli-editors.svg)
<!-- ASCIINEMA: assets/cli-editors.cast | blazium-cli editors -->

![blazium-cli version](assets/cli-version.svg)
<!-- ASCIINEMA: assets/cli-version.cast | blazium-cli version -->

## Projects

```text
blazium-cli projects
blazium-cli projects add ./MyProject
blazium-cli projects remove MyProject
blazium-cli open ./MyProject
blazium-cli load ./MyProject
blazium-cli run ./MyProject
blazium-cli project-manager
```

`open` and `load` start the editor with `--editor --path`. They do not run the game. `load` also prints a project profile: JustAMCP, remote_control, editor_version, features.

Both attach remote control by default (`remote.enable_on_open`, default true). After `/v1/health` responds, the CLI assigns a 6-character instance id with `POST /v1/instance`.

`run` (alias `play`) starts the game with `--path` and without `--editor`. If `application/run/main_scene` is empty, the CLI returns a JSON error and does not start the binary. Remote control stays off for `run`.

`project-manager` starts the default editor with `--project-manager` and no project path.

Registry file: `%APPDATA%\blazium\hub.json` (Windows) or `~/.config/blazium/hub.json`.

## Templates

```text
blazium-cli install 0.6.725 --templates
blazium-cli templates list
blazium-cli templates download 0.6.725 --tpz
```

Templates are versioned as Blazium `0.6.x`, not Godot `4.3.2`. Metadata resolution order is in the [templates article](../export-templates-and-cdn/export-templates-and-cdn.md).

![templates --help](assets/cli-templates-help.svg)
<!-- ASCIINEMA: assets/cli-templates-help.cast | blazium-cli templates --help -->

## Upgrade

```text
blazium-cli upgrade --dry-run
blazium-cli upgrade
blazium-cli update check
blazium-cli update apply --product cli
blazium-cli update apply --product hub --install-root "C:\Program Files\Blazium"
blazium-cli update apply --product launcher --install-root "C:\Program Files\Blazium\Games"
```

`update apply` knows `cli`, `hub`, `crash_reporter`, and `launcher`. `--product launcher` installs BlaziumLauncher and, on Windows, starts setup with `/NOCLI` so an existing `blazium://` handler is left alone. Under Program Files, apply may raise a UAC prompt.

![update --help](assets/cli-update-help.svg)
<!-- ASCIINEMA: assets/cli-update-help.cast | blazium-cli update --help -->

## Remote

Short table. The long form is [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md). The editor module listens on `127.0.0.1:6508` by default, not 6507 (that port is the game JustAMCP default).

| Command | Job |
|---|---|
| `remote status` | Health, instance id, project |
| `remote ping` / `remote exec` | Built-in commands |
| `remote eval` / `eval-gdscript` / `eval-lua` | Expressions (`allow_eval` must be on) |
| `remote logs` / `errors` | Engine log |
| `remote autowork run --wait` | Run Autowork |
| `remote snapshot editor` | PNG of the editor |
| `remote doctor` | Config check |

![remote --help](assets/cli-remote-help.svg)
<!-- ASCIINEMA: assets/cli-remote-help.cast | blazium-cli remote --help -->

One live instance is used automatically. Two or more: the newest is the default, and the CLI prints a warning unless you pass `--quiet`. Select with `--instance <id>` or `--project <path>`.

Env overrides: `BLAZIUM_REMOTE_HOST`, `BLAZIUM_REMOTE_PORT`, `BLAZIUM_REMOTE_TOKEN`. CLI prefs live in `%APPDATA%\blazium\cli.json` or `~/.config/blazium/cli.json`.

Turn remote off for later opens with `blazium-cli remote config set enable-on-open false`.

## URI handler

OS installers point `blazium://` at this binary (`handle-uri`).

| URI | Action |
|---|---|
| `blazium://hub` | Focus Hub on port 39218 |
| `blazium://open?path=` | Open project |
| `blazium://load?path=` | Open project and print the profile |
| `blazium://install?version=` | Install editor |
| `blazium://register?path=` | Register a local binary |
| `blazium://game/<uuid>` | Forward to the Games launcher (port 39220) |

![handle-uri --help](assets/cli-handle-uri-help.svg)
<!-- ASCIINEMA: assets/cli-handle-uri-help.cast | blazium-cli handle-uri --help -->

`blazium-cli hub-remote ensure` writes `hub_remote.json` if neither the user file nor the machine file is valid. It does not rotate a valid token. Do not hand-edit that file.

## Deploy

Steam and itch.io deploys live in this CLI. Optional `blazium-deploy.yml` next to the game. Secrets come from flags, then the YAML, then `BLAZIUM_*` env.

```text
blazium-cli deploy tools status
blazium-cli deploy steam upload --dry-run
blazium-cli deploy itch push ./build --target user/game:windows
```

Steam Guard setup is interactive. Do not run `deploy steam guard setup` on a CI runner. itch.io push uses butler as a Go module. It does not download broth.

## CI

[GitHub Actions for Blazium](../github-actions-for-blazium/github-actions-for-blazium.md) starts with `setup-blazium-cli`, then this binary.

![Install flow](assets/install-flow.png)

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
