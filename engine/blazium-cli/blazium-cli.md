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

The same binary [Hub](../blazium-hub/blazium-hub.md) shells, CI uses, and Windows/Linux registers for `blazium://`.

## Get it

1. **Hub bundle.** The installer puts `blazium-cli` on PATH (or next to Hub).
2. **GitHub Releases.** `blazium-cli-windows-x86_64.exe` and the other OS/arch assets.
3. **CDN manifest.** `https://cdn.blazium.app/cli/cli.json`

Local builds print `0.0.0-dev` until CI stamps `data/cliBuild.txt`.

![blazium-cli --help](assets/cli-help.svg)
<!-- ASCIINEMA: assets/cli-help.cast | blazium-cli --help -->

```text
asciinema play assets/cli-help.cast
```

## Install an editor

```text
blazium-cli install 0.6.725
blazium-cli install nightly --templates
```

Editors land in `{install-path}/{channel}/{version}`. Channels: `release`, `prerelease`, `nightly`.

![blazium-cli install-path](assets/cli-install-path.svg)
<!-- ASCIINEMA: assets/cli-install-path.cast | blazium-cli install-path -->

<!-- ASCIINEMA: assets/cli-install.cast | blazium-cli install 0.6.725 -->
<!-- CAPTURE: record with: asciinema rec assets/cli-install.cast -->

## List and default

```text
blazium-cli editors
blazium-cli editors default
blazium-cli install-path
```

Unset policy is **latest release** among installed editors.

![blazium-cli editors](assets/cli-editors.svg)
<!-- ASCIINEMA: assets/cli-editors.cast | blazium-cli editors -->

![blazium-cli version](assets/cli-version.svg)
<!-- ASCIINEMA: assets/cli-version.cast | blazium-cli version -->

<!-- CAPTURE: assets/cover.png | Hub + terminal | Replace diagram cover with terminal next to Hub, editors output visible -->

## Projects

```text
blazium-cli projects
blazium-cli projects add ./MyProject
blazium-cli open ./MyProject
blazium-cli load ./MyProject
```

`open` launches the editor with a unique `remote_control` port and token (`remote.enable_on_open`, default true), waits for `/v1/health`, then assigns a 6-character instance id.

`load` also prints a project profile: JustAMCP, remote_control, editor_version, features.

Registry file: `%APPDATA%\blazium\hub.json` (Windows) or `~/.config/blazium/hub.json`.

<!-- CAPTURE: record asciinema rec for open, then a Hub/editor still of the window appearing -->
<!-- CAPTURE: assets/cli-open-editor.png | Editor | Editor window after blazium-cli open -->

## Templates

```text
blazium-cli install 0.6.725 --templates
blazium-cli templates list
```

Templates are versioned as Blazium `0.6.x`, not Godot `4.3.2`. Full story: [Export templates and the CDN](../export-templates-and-cdn/export-templates-and-cdn.md).

![templates --help](assets/cli-templates-help.svg)
<!-- ASCIINEMA: assets/cli-templates-help.cast | blazium-cli templates --help -->

## Upgrade

```text
blazium-cli upgrade --dry-run
blazium-cli upgrade
blazium-cli update check
blazium-cli update apply --product cli
```

Products `update apply` knows: `cli`, `hub`, `crash_reporter`. Under Program Files on Windows, apply may UAC.

![update --help](assets/cli-update-help.svg)
<!-- ASCIINEMA: assets/cli-update-help.cast | blazium-cli update --help -->

<!-- CAPTURE: assets/cli-uac.png | Windows | UAC prompt when upgrading a Program Files install -->

## Remote

Short table. The long form is [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).

| Command | Job |
|---|---|
| `remote status` | Health, instance id, project |
| `remote ping` / `remote exec` | Built-in commands |
| `remote eval` / `eval-gdscript` / `eval-lua` | Expressions |
| `remote logs` / `errors` | Engine log |
| `remote autowork run --wait` | Run Autowork |
| `remote snapshot editor` | PNG of the editor |
| `remote doctor` | Config check |

![remote --help](assets/cli-remote-help.svg)
<!-- ASCIINEMA: assets/cli-remote-help.cast | blazium-cli remote --help -->

Two live instances: newest is default. Pass `--instance <id>` or `--project <path>`.

## URI handler

OS installers point `blazium://` at this binary (`handle-uri`).

| URI | Action |
|---|---|
| `blazium://hub` | Focus Hub |
| `blazium://open?path=` | Open project |
| `blazium://load?path=` | Load with profile |
| `blazium://install?version=` | Install editor |
| `blazium://register?path=` | Register a local binary |

![handle-uri --help](assets/cli-handle-uri-help.svg)
<!-- ASCIINEMA: assets/cli-handle-uri-help.cast | blazium-cli handle-uri --help -->

<!-- CAPTURE: assets/cli-uri.gif | OS | Click blazium://hub from a doc, Hub focuses. Record the CLI side with asciinema. -->

## CI

[GitHub Actions for Blazium](../github-actions-for-blazium/github-actions-for-blazium.md) is `setup-blazium-cli` then this binary.

![Install flow](assets/install-flow.png)
