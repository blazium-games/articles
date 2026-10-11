---
title: "Blazium Services"
description: "Login, lobby, and master-server clients live in blazium-sdk-module. Only the login host answers today."
cover: "assets/cover.png"
slug: "blazium-services"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Blazium Services

### Matchmaking clients that are not in the stock editor

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

Hangman needed a lobby that did not hand every player everyone else's IP. The clients for that are `LoginClient`, `LobbyClient`, `ScriptedLobbyClient`, and `MasterServerClient`. They are C++ nodes that inherit `BlaziumClient`. They are not registered in a stock `blazium-dev` editor.

They live in [blazium-sdk-module](https://github.com/blazium-games/blazium-sdk-module). The module's last merge on that tree is 4 September 2025. A stock 0.6 editor does not show those classes in the Create dialog. GDScript templates under `modules/gdscript/editor/script_templates/` still use the names (`LoginClient/default.gd`, `LobbyClient/default.gd`, `ScriptedLobbyClient/default.gd`). Those templates do not run until you compile the SDK in as a custom module. Discord embed, YouTube Playables, JWT, `.env`, and CSV now also have in-tree engine modules (`socialexports`, `jwttool`, `dotenv`, `dotcsv`), although the older SDK still registers its copies. The lobby stack remains SDK-only.

Hangman itself is the proof that this stack is real game code: the example project autoloads `GlobalLobbyClient` from `lobby_client.tscn`, extends `LobbyClient`, and drives match state through lobby data and `notify_lobby`. That project still requires an SDK build. Shipping Hangman on Steam, Discord, Google Play, and the Apple App Store validated export and store upload; it does not put `LobbyClient` into the official editor zip.

![Service clients and the hosts they name](assets/services-hosts.png)

## What is actually up

Checked on 11 October 2026:

| Client | Default in the SDK | DNS / HTTP |
|---|---|---|
| `LoginClient` | host `login.blazium.app` | Resolves. `https://login.blazium.app/` returns `{"status":"ok","success":true}` |
| `LobbyClient` | `wss://lobby.blazium.app/connect` | Does not resolve |
| `ScriptedLobbyClient` | `wss://scriptedlobby.blazium.app/connect` | Does not resolve |
| `MasterServerClient` | `https://masterserver.blazium.app/api/v1` | Does not resolve |

The login client stores the host without a scheme. It adds `wss://` for the socket (`/connect`) and `https://` for HTTP (`/api/v1/connect`, `/api/v1/auth`, `/api/v1/steam/auth`, `/api/v1/private/profile`). An older Hangman inspector showed `wss://login.blazium.app/connect` typed into the Server URL field. That is a scene value, not the current source default of `login.blazium.app`.

Inside a Discord activity the same clients rewrite the host to `{client_id}.discordsays.com/.proxy/` plus a path (`blazium/login`, `blazium/lobby/connect`, `blazium/scriptedlobby/connect`, or `blazium/masterserver/api/v1`). That rewrite is in the SDK constructors and `discord_embedded_app/path` setters. It is not something `DiscordEmbeddedAppClient` in the engine does by itself.

`POGRClient` is also in the SDK. It posts to `https://api.pogr.io/v1/intake`. That is a third-party intake URL, not a Blazium host. Methods are `init`, `end`, `data`, `event`, `logs`, `metrics`, and `monitor`.

## Login, then a room

`LoginClient` needs a non-empty alphanumeric `game_id` before `connect_to_server`. The documented flow is: connect, then `request_login_info(login_type)`, open the URL from `LoginURLResult.login_url`, and keep the JWT from `received_jwt` (payload: `jwt`, `type`, `access_token`). `request_auth`, `request_auth_id`, `request_steam_auth`, and `verify_jwt_token` cover the rest of that surface. Do not print live tokens.

The engine's own `JWT` / `JWTBuilder` / `DecodedJWT` classes, in `modules/jwttool`, are what you use to build and check tokens in game code. They are not this login node. The SDK still carries an older `jwt.cpp` / `jwt.h` pair; the class reference you want for new work is the engine module.

```gdscript
extends LoginClient

func _ready() -> void:
    received_jwt.connect(_on_jwt)
    game_id = "hangman"
    var connect_res: LoginConnectResult = await connect_to_server().finished
    if connect_res.has_error():
        push_error(connect_res.error)
        return
    var login_res: LoginURLResult = await request_login_info("discord").finished
    if login_res.has_error():
        push_error(login_res.error)
        return
    OS.shell_open(login_res.login_url)

func _on_jwt(jwt: String, type: String, access_token: String) -> void:
    # Store jwt yourself. Do not log it.
    pass
```

That pattern matches the editor script template. Steam's path on the same node is `request_steam_auth(auth_id, steam_ticket)`, which POSTs to `/api/v1/steam/auth/{auth_id}`.

## LobbyClient

`LobbyClient.connect_to_server` opens the websocket. On success you get `connected_to_server` with a peer and a reconnection token. Store the token yourself. The node does not write `user://` for you. Hangman's `lobby_client.gd` loads and saves `user://blazium.cfg` under the `LobbyClient` section; the script template does the same.

```gdscript
extends LobbyClient

func _ready() -> void:
    var config := ConfigFile.new()
    config.load("user://blazium.cfg")
    reconnection_token = config.get_value("LobbyClient", "reconnection_token", "")
    connected_to_server.connect(_on_connected)
    var res: LobbyResult = await connect_to_server().finished
    if res.has_error():
        push_error(res.error)

func _on_connected(_peer: LobbyPeer, new_token: String) -> void:
    var config := ConfigFile.new()
    config.set_value("LobbyClient", "reconnection_token", new_token)
    config.save("user://blazium.cfg")
```

Once connected: `create_lobby`, `join_lobby`, `quick_join`, `list_lobbies`, `leave_lobby`, `kick_peer`, `set_lobby_ready`, `set_lobby_sealed`, tag and data helpers, `send_chat_message`, `notify_lobby`, and `notify_peer`. Members `peer`, `peers`, `lobby`, `host_data`, and `peer_data` update as the room changes. Peers in the lobby are lobby peers. Their game-traffic addresses are not what this socket is for.

Hangman's host keeps the secret word in private lobby data (`add_lobby_data({"word": ...}, true)`), public guessed state in lobby data, and letter guesses through `notify_lobby({"command": "guess", "letter": letter})`. That is authoritative-enough for a party game without an ENet mesh for the puzzle itself.

## ScriptedLobbyClient

`ScriptedLobbyClient` is the authoritative variant. Default URL is `wss://scriptedlobby.blazium.app/connect`. Discord path default is `blazium/scriptedlobby/connect`. Compared with `LobbyClient`, the host cannot set arbitrary data or notify on peer disconnect the same way, and `received_lobby_data` omits the `is_private` parameter. Server-side work goes through `lobby_call(method, args)`.

Lobby server notes in [lobby-template](https://github.com/blazium-games/lobby-template) describe a `lobby_service` binary, `config.ini`, `games.ini`, and Lua, AngelScript, or relay backends. That repository is documentation and a demo project. It is not a public hostname. Point `server_url` at a host you run.

## MasterServerClient

`MasterServerClient` registers and lists dedicated servers against whatever `server_url` you set. The methods are `create_game`, `update_game`, and `recent_games`. They take or return `GameServerInfo` (`game_name`, `description`, `ip_address`, `port`, `players`, `max_players`, `version`, and `id` after create). Under the hood create POSTs to `{server_url}/server/create`. The hostname baked as the default does not resolve, so set the URL to a server you run.

```gdscript
@export var master: MasterServerClient

func register_server() -> void:
    var info := GameServerInfo.new()
    info.game_name = "hangman-ds"
    info.ip_address = "203.0.113.10"
    info.port = 7777
    info.max_players = 8
    info.version = "1.0.0"
    var res: MasterServerResult = await master.create_game(info).finished
    if res.has_error():
        push_error(res.error)
```

## Discord proxy rewrite

When `DiscordEmbeddedAppClient.static_is_discord_environment()` is true, leaving the default URL makes the SDK rewrite to the activity proxy. Override with `discord_embedded_app/path` if your Discord URL mapping uses a different suffix. The engine's embed client does not perform that rewrite for you; the SDK clients do. Host the web export with [docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template) so Nginx answers `/.proxy/` with COOP/COEP.

![Identity pieces around login and lobby](assets/identity-flow.png)

## Where this sits next to ENet

![Networking layers](assets/networking-layers.png)

Lobby traffic is HTTP and WebSocket. World simulation stays on `enet_server` or MultiplayerAPI's ENet peer. Do not put ticks on the lobby node. Use the lobby to form a room, exchange readiness and small dictionaries, then hand simulation to ENet (or keep puzzle state in lobby data if the game is small enough, as Hangman does).

The engine's `Discord.create_or_join_lobby` is a Discord Social SDK lobby. It is a different object from `LobbyClient`. Mixing the names in one sentence is how people wire the wrong socket.

## Edge cases

- Missing `game_id` fails connection. Keep it alphanumeric.
- Reconnection tokens are opaque strings. Clearing them (`reconnection_token = ""`) before disconnect is how Hangman's settings force a fresh peer.
- Discord path overrides only matter inside the embed environment; outside Discord the baked `*.blazium.app` defaults apply.
- `ScriptedLobbyClient.lobby_call` is how authoritative server methods run; calling host-only data setters from the non-authoritative mental model will not match the scripted service rules.
- `MasterServerClient` HTTP paths are under the `server_url` you set; the default host does not resolve, so a forgotten override looks like DNS failure, not a GDScript bug.
- Do not log JWTs from `received_jwt`.

## What you compile, and what is missing

Drop the SDK in as a Godot/Blazium custom module and build. `can_build` in the SDK's `config.py` returns true on every platform the file sees. That does not mean the official editor zip already contains it. If `LobbyClient` is missing from the Create dialog, you are on a stock `blazium-dev` build. Script templates for these classes ship in the engine tree anyway, which is confusing until you know the registration lives in the SDK.

Class reference pages for these nodes are not on `docs.blazium.app` today (the LobbyClient page 404s). Read the XML under `doc_classes/` in the SDK repo. The older `services-docs` repository is thin and does not replace that class XML. Only `login.blazium.app` answers among the baked Blazium service hosts. Lobby, scripted lobby, and master server require your own deployment or a URL you control.

## Links

- SDK module: https://github.com/blazium-games/blazium-sdk-module
- Lobby server notes: https://github.com/blazium-games/lobby-template
- Login host: https://login.blazium.app/
- Example Hangman: https://github.com/blazium-games/example-game-hangman
- Web host template: https://github.com/blazium-games/docker-webbuild-template
- Engine: https://github.com/blazium-games/blazium
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
