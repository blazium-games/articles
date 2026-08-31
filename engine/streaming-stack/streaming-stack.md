---
title: "Streaming tools in Blazium"
description: "Twitch, Kick, IRC, Crowd Control, and OBS as one live-ops path, not five module posts."
cover: "assets/cover.png"
slug: "streaming-stack"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Chat in. The game mutates. OBS cuts. Five modules, one path.

![Twitch / Kick / IRC → Crowd Control → game → OBS](assets/streaming-stack.png)

## Chat inputs

| Need | Class | Module |
|---|---|---|
| Twitch identity, clips, subs | `TwitchAPI` / `TwitchHttpClient` | `twitchapi` |
| Twitch chat messages now | `TwitchIRCClient` / `IRCClientNode` | `ircclient` |
| Kick | `KickAPI` | `kickapi` |
| Generic IRC | `IRCClientNode` | `ircclient` |

Helix is HTTP. IRC is a socket. Do not poll Helix for every chat line.

![IRC session log](assets/irc-session.png)

<!-- CAPTURE: recrop irc-session.png if the log is stale. Prefer a new capture from a real channel. -->

## Crowd Control

Viewer buys or votes an effect. Native `CrowdControl*` classes, editor effect packs, HTTP/WebSocket to Crowd Control.

<!-- CAPTURE: assets/crowd-control-pack.png | Editor | Effect pack inspector -->

## OBS

`OBSClient`, obs-websocket 5.x. Scenes, stream/record, studio mode.

![OBS connection](assets/obs-connect.png)

## One overlay

Chat command `!boom` spawns an effect and cuts OBS to scene `Alert`. Tokens live in `.env`. See [ENV, INI, and CSV](../data-formats/data-formats.md).

```gdscript
extends Node

@onready var irc: IRCClientNode = $IRCClientNode
@onready var obs: OBSClient = $OBSClient
@onready var cc: CrowdControl = CrowdControl

func _ready() -> void:
    irc.message_received.connect(_on_chat)
    obs.connect_to_host(ENV.get_value("OBS_HOST"), int(ENV.get_value("OBS_PORT")), ENV.get_value("OBS_PASSWORD"))

func _on_chat(nick: String, text: String) -> void:
    if text.strip_edges() != "!boom":
        return
    cc.trigger("explosion")
    obs.set_current_program_scene("Alert")
```

Class names for Crowd Control and IRC signals must match the build you ship. If a signal was renamed, fix this sample against the class reference before `deployed: true`.

<!-- CAPTURE: assets/chat-to-obs.gif | Game + OBS | Command in chat, in-game effect, OBS scene cut. Master mp4 15s. -->
<!-- CAPTURE: assets/cover.png | OBS + game + chat | Replace diagram cover -->
