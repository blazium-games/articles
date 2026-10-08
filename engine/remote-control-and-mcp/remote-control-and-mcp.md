---
title: "Drive the editor: CLI remote and MCP"
description: "Two doors into one editor: blazium-cli Remote is localhost JSON, JustAMCP is MCP for agents, and Autowork is how both prove they work."
cover: "assets/cover.png"
slug: "remote-control-and-mcp"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Three tools, three jobs. Do not collapse them. The HTTP server was added so the CLI and CI can check health, logs, play state, snapshots, and Autowork without clicking the window. SCons `hub_register=yes` registers editor builds with Hub after the build, through `blazium-cli`, not at runtime. Blazium Games used this in-house to validate editor automation.

## Status

`modules/remote_control`, `modules/justamcp`, and Autowork are on `blazium-dev`. Remote control defaults to off in Project Settings and comes up when `blazium-cli open` or `load` passes `--enable-remote-control` (`remote.enable_on_open` defaults to true). JustAMCP stays off until `blazium/justamcp/server_enabled` or `--enable-mcp`. `blazium-cli remote config set enable-mcp-on-load true` is the CLI switch for that.

Neither server is a cloud relay. Default binds are loopback. Remote control is port **6508**. Editor MCP is port **6506**. A game export port of `0` means editor port + 1, which is **6507**. Pointing the CLI at 6507 does not reach remote control.

The bind stays on `127.0.0.1` because the routes include play, snapshots, and eval. `allow_eval` defaults to false. Eval runs GDScript or Luau in the editor process. A token, when set, is `Authorization: Bearer` or `X-Remote-Control-Token`.

## First check

```text
blazium-cli open ./MyProject
blazium-cli remote status --format json
blazium-cli remote doctor
blazium-cli remote exec ping
```

`open` waits until `GET /v1/health` responds, then `POST /v1/instance` stores a 6-character id. `status` prints project, pid, and that id. One editor is selected for you. Two editors: the newest is the default, and the CLI warns unless `--quiet`. Select with `--instance` or `--project`.

`remote eval-gdscript` returns nothing useful until `blazium/remote_control/allow_eval` is true. That setting defaults to false.

![Autowork, remote_control, JustAMCP](assets/automation-three.png)

## remote_control

Localhost JSON over HTTP, routes under `/v1/`. Default bind is `127.0.0.1:6508`. Port 6507 is the game JustAMCP default (editor MCP is 6506, and a game port of 0 means editor port + 1). Do not point the CLI at 6507 and expect remote control.

Enable with Project Settings `blazium/remote_control/server_enabled` (default `false`) or `--enable-remote-control`. Port: `--remote-control-port` or `blazium/remote_control/server_port`. Token: `--remote-control-token` or `blazium/remote_control/token`. Bind: `blazium/remote_control/bind_address` (default `127.0.0.1`).

`blazium/remote_control/allow_eval` defaults to false. `blazium/remote_control/allow_runtime` defaults to false. `remote eval` does nothing useful until eval is allowed. A token, when set, is `Authorization: Bearer` or the `X-Remote-Control-Token` header.

The class is `RemoteControlServer`. Routes registered in `remote_control_server.cpp`:

| Route | Job |
|---|---|
| `GET /v1/health` | Liveness |
| `GET /v1/status` | Project, pid, instance id |
| `POST /v1/instance` | Assign the short instance id |
| `GET /v1/commands` | What `exec` accepts |
| `POST /v1/exec` | Built-in commands |
| `POST /v1/eval` | Expression, if `allow_eval` |
| `GET /v1/logs` | Engine log |

Built-in exec names include `play_main_scene`, `play_current_scene`, `stop_playing`, `pause_playing`, `resume_playing`, `play_status`, `snapshot_editor`, `snapshot_scene`, `get_logs`, `debugger_info`, `autowork_run`, and `mcp_status`. Snapshots return a PNG as `png_base64`.

## CLI is the client

```text
blazium-cli remote status --format json
blazium-cli remote exec ping
blazium-cli remote eval-gdscript "2 + 2"
blazium-cli remote logs --since 0 --limit 200
blazium-cli remote autowork run --wait
blazium-cli remote doctor
```

`open` and `load` start remote control by default (`remote.enable_on_open`) and assign a 6-character instance id after `/v1/health`. One editor: it is selected for you. Two editors: the newest is the default, and you pass `--instance` or `--project` to pick. Env: `BLAZIUM_REMOTE_HOST`, `BLAZIUM_REMOTE_PORT`, `BLAZIUM_REMOTE_TOKEN`.

![remote --help](assets/cli-remote-help.svg)
<!-- ASCIINEMA: assets/cli-remote-help.cast | blazium-cli remote --help -->

`blazium-cli remote config set enable-mcp-on-load true` turns JustAMCP on when the CLI loads a project.

## JustAMCP

Native MCP server in the editor (`modules/justamcp`). Streamable HTTP on `POST /mcp`, `GET /mcp`, and `DELETE /mcp`, plus the legacy `/sse` and `/message` routes and the OAuth discovery paths. `JustAMCPRuntime` is the object that stays up across scene changes.

Editor settings: `blazium/justamcp/server_enabled`, `blazium/justamcp/server_port` (default **6506**), `blazium/justamcp/project_mcp_dir` (default `res://mcp`). Game export: `blazium/justamcp/export_port` (default **0**, which becomes 6507). CLI: `--enable-mcp`, `--mcp-port`, `--mcp-client-id`, `--mcp-client-secret`.

Tool categories include editor, scene, script, resource, docs, autowork, export, and runtime. Names you will see in tests and guides: `blazium_get_project_info`, `blazium_scene_tree_dump`, `blazium_logs_read`, `docs_list_classes`, `blazium_autowork_run_all_tests`. Asset tags and semantic search are `blazium_tags_*` and `semantic_search` / `blazium_semantic_search`. Prompt `blazium_asset_tagging_workflow` is the tagging walk.

![JustAMCP settings](assets/mcp-settings.png)

![MCP prompts / tools](assets/mcp-prompts.png)

## Two `blazium://` owners

| Owner | Example |
|---|---|
| CLI / Hub (OS protocol) | `blazium://open?path=C:\game` |
| JustAMCP (MCP resource) | `blazium://scene/…`, `blazium://docs/…`, `blazium://tags/dictionary` |

## Autowork

`Autowork` is the in-engine test node: directories of test scripts, asserts, spies, and a JSON or JUnit dump. Run it from the editor panel, headless, or through remote control:

```text
blazium --headless --path . -s run_tests.gd
blazium-cli remote autowork run --wait
```

Hub's repo runs that headless entry in CI. Remote control's `autowork_run` and JustAMCP's autowork tools call the same module. A failing assert in the panel and a green CLI run are the same suite.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
