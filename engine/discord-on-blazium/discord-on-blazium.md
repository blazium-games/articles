---
title: "Discord: Embedded Apps and Social SDK"
description: "Two jobs. Ship a game that runs inside Discord, or ship a desktop game with rich presence and invites."
cover: "assets/cover.png"
slug: "discord-on-blazium"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Pick a job first. The APIs are not interchangeable.

![Embedded App vs Social SDK](assets/discord-two-jobs.png)

| | Embedded App | Social SDK |
|---|---|---|
| Environment | Web, inside Discord | Desktop / mobile game |
| Class | `DiscordEmbeddedAppClient` | `Discord` singleton |
| Module | `socialexports` | `discord_module` |
| Export | Web + `blazium/discord_embed` | Ordinary desktop export |
| Services | Login / Lobby URL rewrite on `discordsays.com` | Optional Discord login to your backend |

## Embedded Apps

Hangman shipped this way. The node talks to the Discord Embedded App JavaScript SDK in the page. It activates only when it is actually on Discord.

Web export flag: `blazium/discord_embed`. Host with [Docker web export](../docker-web-export/docker-web-export.md) so `.proxy` paths rewrite. Discord admin: create an application, set URL mappings.

![DiscordEmbeddedAppClient in the tree](assets/embedded-nodes.png)

![Discord URL mappings](assets/discord-admin-map.png)

![LoginClient next to the embed node](assets/login-client-discord.png)

```gdscript
@export var discord: DiscordEmbeddedAppClient

func _ready() -> void:
    if not discord.is_discord_environment():
        return
    await discord.is_ready().finished
    var result := await discord.authorize("code", "", "none", ["identify"]).finished
    print(result.data.has("code"))
```

Send that code to [Login](../blazium-services/blazium-services.md). Lobby already knows the user.

![Authorize result](assets/discord-auth.png)

<!-- CAPTURE: assets/embedded-in-voice.mp4 | Discord | 15s activity running in voice -->
<!-- CAPTURE: assets/web-export-flags.png | Editor | Web export Discord embed checkbox -->

## Social SDK

`Discord` singleton. Two modes: lite rich presence, or full social (friends, invites, lobbies). App id from the Discord developer portal. This is not an Embedded App. It does not run inside Discord's web view.

```gdscript
func _ready() -> void:
    Discord.initialize(ENV.get_value("DISCORD_APP_ID"))
    Discord.set_rich_presence({
        "details": "In a match",
        "state": "Hangman",
    })
```

Confirm method names against the class reference before publish. The old module post used a `Discord` singleton; keep that.

<!-- CAPTURE: assets/rich-presence.png | Discord | Profile showing the running Blazium game -->
<!-- CAPTURE: assets/cover.png | Discord | Activity on the left, presence on the right, 16:9 -->

## Hosting

Embedded Apps need the Docker template and the URL map. Social SDK needs the Steam-or-desktop binary and the Discord client running. [Blazium Services](../blazium-services/blazium-services.md) sit under both if you want Login.
