---
title: "The Remote Control module"
description: "A local HTTP server so the CLI and other tools can query a running editor without driving the UI."
cover: "assets/cover.png"
slug: "remote-control-module"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---

# The Remote Control Module

We needed the CLI to open a project and then prove the editor was actually up: health, logs, a screenshot, a test run. Clicking the window does not survive CI, and it does not survive a second machine. The Remote Control module is that socket.

It is `modules/remote_control` on `blazium-dev`. `RemoteControlServer` is a small HTTP server. The usual client is [Blazium CLI](../blazium-hub-and-cli/blazium-hub-and-cli.md) (`blazium-cli remote`). Anything else that can send HTTP to loopback can use the same routes. The server is off until you enable it.

## Why it is local

The default bind is `127.0.0.1:6508`. It is not a public API. `blazium/remote_control/bind_address` can be changed, and you should not point it at a LAN address unless you also set a token and you understand that `allow_eval` can run code. `allow_eval` and `allow_runtime` both default to false. Token auth is `Authorization: Bearer <token>` or `X-Remote-Control-Token`.

Hub uses the same idea on a different port. Hub listens on **39218** with `hub_remote.json`. That file is not the editor token. Do not mix them.

## Turn it on

Project Settings:

| Key | Default |
|---|---|
| `blazium/remote_control/server_enabled` | `false` |
| `blazium/remote_control/server_port` | `6508` |
| `blazium/remote_control/bind_address` | `127.0.0.1` |
| `blazium/remote_control/token` | empty |
| `blazium/remote_control/allow_eval` | `false` |
| `blazium/remote_control/allow_runtime` | `false` |

Or start the editor with `--enable-remote-control`, `--remote-control-port=<port>`, and `--remote-control-token=<token>`.

`blazium-cli open` and `blazium-cli load` pass those flags for you when `remote.enable_on_open` is true (the default). After `GET /v1/health` succeeds, the CLI `POST`s `/v1/instance` and stores a 6-character id. `blazium-cli run` starts the game and does not enable this server.

## What you can ask

| Route | Use |
|---|---|
| `GET /v1/health` | Is the process listening? |
| `GET /v1/status` | Project, pid, instance id |
| `GET /v1/commands` | Built-in command names |
| `POST /v1/exec` | Run one of those commands |
| `POST /v1/eval` | GDScript or Luau, only if eval is allowed |
| `GET /v1/logs` | Log lines |

Commands worth knowing: `play_main_scene`, `play_current_scene`, `stop_playing`, `pause_playing`, `play_status`, `snapshot_editor`, `snapshot_scene`, `autowork_run`, `mcp_status`. A snapshot comes back as `png_base64`.

```text
blazium-cli remote status --format json
blazium-cli remote exec ping
blazium-cli remote autowork run --wait
blazium-cli remote doctor
```

Two editors at once: `--instance <id>` or `--project <path>`. The newest instance is the default, and the CLI warns you.

JustAMCP is a second server (port 6506 in the editor) for agent tools. Remote control can report MCP status. It is not the MCP server. The split is written up in [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md).

Tests: [remote_control_module_tests](https://github.com/blazium-games/remote_control_module_tests).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
