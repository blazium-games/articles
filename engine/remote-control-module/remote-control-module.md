---
title: "The Remote Control module"
description: >-
    Remote Control lets the CLI and tools talk to a running Blazium editor for status, commands, and logs.
cover: "assets/cover.png"
slug: "remote-control-module"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---
# The Remote Control Module

A new **Remote Control** module has been added to the Blazium Game Engine, allowing external tools to talk to
a running editor, or when explicitly enabled, a running game.
It exposes a lightweight local HTTP server that other applications, most notably the 
[Blazium CLI](../blazium-hub-and-cli/blazium-hub-and-cli.md),
can use to query status, execute commands, evaluate expressions, inspect logs, and drive editor
workflows without needing to interact with the UI directly.

<!-- image showing.. idk -->

At the centre of the module is **RemoteControlServer**, a singleton that listens on a configurable
local port (default to `127.0.0.1:6507`).
Requests can be protected with an optional token.
The server supports status queries, command execution through a registry of built-in actions,
expression evaluation (GDScript by default, with optional Luau support),
log and error retrieval, debugger information, and integration with
[Autowork](../autowork-testing-framework/autowork-testing-framework.md) jobs.
Evaluation is disabled by default and blocked from dangerous operations for safety.

<!-- image showing remote control project settings -->

The module is available in editor builds and in Hub-capable export templates.
It can be enabled via Project Settings or the command-line flag.
Additional settings control the port, bind address, authentication token, and whether evaluation is allowed.

## Using Remote Control with Blazium CLI

[Blazium CLI](../blazium-hub-and-cli/blazium-hub-and-cli.md) provides a convenient `remote`
command that communicates with any running editor that has the module enabled.
Typical usage includes:

```bash
blazium-cli remote status --format json
blazium-cli remote instances
blazium-cli remote list
blazium-cli remote eval "2 + 2"
blazium-cli remote eval-lua "1 + 1"
blazium-cli remote logs --since 0 --limit 200
blazium-cli remote errors --limit 100
blazium-cli remote debugger info
blazium-cli remote autowork run --wait
blazium-cli remote autowork results
blazium-cli remote --instance AB3K7M status
blazium-cli remote --project ./MyProject status
blazium-cli remote config set enable-mcp-on-load true
```

## Documentation & Next Steps

The module is available in the [latest nightly of Blazium](https://blazium.app/download)
and a dedicated tests project is available at
[remote_control_module_tests](https://github.com/blazium-games/remote_control_module_tests).

The Remote Control module form a practical bridge between the editor and external tooling,
making it easier to automate checks, inspect running sessions, and integrate Blazium into
larger development workflows.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**