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

Opening a project from a script is not enough. The next question is whether the editor process is the one you think it is: which project, which pid, whether the log is moving, whether Autowork passed. Clicking the window does not answer that in CI, and it does not answer it from a second tool on the same machine.

`modules/remote_control` is that check. `RemoteControlServer` is a small HTTP server. The usual client is `blazium-cli remote`. Anything that can send HTTP to loopback can call the same routes. The route table, the exec names, and JustAMCP are in [Drive the editor](../remote-control-and-mcp/remote-control-and-mcp.md). This page is why the server exists and how far it is allowed to go.

## Why it stays on loopback

The default bind is `127.0.0.1:6508`. It is not a public API and it is not the agent protocol. JustAMCP is a second server, port 6506 in the editor, for MCP tools. Remote control can report MCP status. It does not speak MCP.

`blazium/remote_control/allow_eval` and `allow_runtime` default to false. Eval runs GDScript or Luau in the editor process. Leaving it off is the shipped default. A token, when set, is `Authorization: Bearer` or `X-Remote-Control-Token`. `bind_address` can be changed. Pointing it at a LAN address without a token exposes every route, including eval if you turned that on.

Hub uses the same pattern on a different port. Hub listens on **39218**. The token file is `hub_remote.json`. That file is not the editor token. The Games launcher is port **39220**. Mixing those files fails closed or talks to the wrong process.

## How it gets turned on

The server is off until something enables it.

| Switch | Default |
|---|---|
| `blazium/remote_control/server_enabled` | `false` |
| `--enable-remote-control` | off |
| `blazium-cli open` / `load` | on, because `remote.enable_on_open` defaults to true |

`blazium-cli run` starts the game and does not enable this server. After `GET /v1/health`, `open` and `load` assign a 6-character instance id with `POST /v1/instance`. Two editors: the newest is the default, and the CLI warns unless you pass `--instance` or `--project`.

```text
blazium-cli open ./MyProject
blazium-cli remote status --format json
blazium-cli remote doctor
```

`remote doctor` is the config check. `remote autowork run --wait` runs the in-engine test suite through the same server. Headless Autowork does not need the server: `blazium --headless --path . -s run_tests.gd`.

## Status

Shipped on `blazium-dev`. Tests: [remote_control_module_tests](https://github.com/blazium-games/remote_control_module_tests). The module does not add a cloud relay, a second machine, or an auth scheme beyond the bearer token. CLI prefs for host, port, and token are `BLAZIUM_REMOTE_HOST`, `BLAZIUM_REMOTE_PORT`, `BLAZIUM_REMOTE_TOKEN`, and `%APPDATA%\blazium\cli.json` or `~/.config/blazium/cli.json`.

Turn later opens off with `blazium-cli remote config set enable-on-open false`.

The CLI that calls this server is [Blazium Hub & Blazium CLI](../blazium-hub-and-cli/blazium-hub-and-cli.md). Engine docs: [docs.blazium.app](https://docs.blazium.app).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
