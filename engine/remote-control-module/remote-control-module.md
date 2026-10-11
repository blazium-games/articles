---
title: "Why the editor has a localhost HTTP server"
description: "remote_control lets the CLI and CI query a running editor. Eval stays off. JustAMCP is a different port."
cover: "assets/cover.png"
slug: "remote-control-module"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Why the editor has a localhost HTTP server

### Scripts should not have to click the window

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

The commit that added `modules/remote_control` says it is CLI-to-editor HTTP control. A follow-up made exec and eval non-blocking: they are deferred onto the main thread, and play, pause, stop, and a PNG snapshot are built-in commands. Another commit keeps privileged exec and eval off by default. The test-runner side of the same idea is Autowork, so a headless job can run tests without a driver script glued on beside the editor.

Godot does not ship this server. We needed it because Hub and CI both have to open a project and know that the editor is actually up. Clicking is not a protocol.

![Three ways to drive the editor](assets/automation-three.png)

![Ports](assets/editor-ports.png)

## What is on by default

Almost nothing. `blazium/remote_control/server_enabled` is false. `allow_eval` is false. `allow_runtime` is false. The bind is `127.0.0.1` and the port is **6508**, because the routes include play, snapshots, and eval. A token, when set, is `Authorization: Bearer` or `X-Remote-Control-Token`.

`blazium-cli open` turns the server on, because `remote.enable_on_open` defaults to true. After `GET /v1/health` the CLI posts `/v1/instance` and stores a 6-character id. That is how a later `remote status` knows which editor it is talking to. Two editors: the newest is the default, and the CLI warns unless you pass `--quiet`.

Eval runs GDScript or Luau inside the editor process. Leave it off unless you meant to type code into a running editor from a shell.

Export templates do not include the module unless the build was made with `hub_build=yes`. Hub itself is one of those builds. A game you export for players is not, unless you asked for that flag.

## The other port

JustAMCP is the MCP server, default port **6506**. A game export port of 0 means 6507. `blazium-cli remote` does not speak MCP. Pointing it at 6507 will not run `remote exec`. `mcp_status` on the remote-control server is how you ask whether the MCP server is up. It is not a proxy to it.

`blazium://` as an OS protocol is the CLI. `blazium://scene/…` inside JustAMCP is a resource URI. Same scheme, two owners.

SCons `hub_register=yes` calls `blazium-cli` after a build to register that editor with Hub. That is not the HTTP server. It does not run while you are editing.

We used remote control in-house for health checks, play commands, snapshots, and Autowork in CI. That is the job. It is not a cloud relay, and it is not a multiplayer API.

## Links

- Module: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/remote_control
- JustAMCP: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/justamcp
- CLI: https://github.com/blazium-games/blazium-cli
- Tests: https://github.com/blazium-games/remote_control_module_tests
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
