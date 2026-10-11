---
title: "Streaming tools in Blazium"
description: "Twitch, Kick, IRC, Crowd Control, and OBS are separate modules. Nothing wires them together for you."
cover: "assets/cover.png"
slug: "streaming-stack"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Streaming tools in Blazium

### Chat, effects, and the broadcast are three sockets

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

Godot does not ship a Twitch client, a Kick client, or an OBS websocket. We added them because a live game is a pile of HTTP and sockets that every project was binding by hand. They do not share a base class. You wire them.

We used `TwitchAPI`, `KickAPI`, IRC, Crowd Control, and `OBSClient` in-house to validate those clients. That pass does not name a channel or a shipped overlay. Hangman's public releases are Steam, Discord, Google Play, and the Apple App Store, not a claim that the Steam build is an OBS scene. Demon Lord: Clicker is a Steam live-ops validation story; it is not this streaming stack.

![Twitch, Kick, IRC, then Crowd Control, then the game, then OBS](assets/streaming-stack.png)

## What is in the tree

`twitchapi`, `kickapi`, `ircclient`, `crowdcontrol`, and `obsclient` are modules on `blazium-dev`. Each has its own test repository on the org. There is no scene that connects all five, and no Blazium service that holds your tokens. Put tokens in a `.env` file and read them with `ENV` from `modules/dotenv` (`load_env_file`, typed getters, and related helpers). That file is plain text. It is not a security boundary.

`CrowdControl` and `OBSClient` are `Object` singletons, not `Node`. Both need `poll()` from `_process`. Crowd Control has no `trigger()` method. The viewer starts the effect on Crowd Control's side. The game answers.

| Need | Class | Module |
|---|---|---|
| Twitch Helix | `TwitchAPI` | `twitchapi` |
| Twitch chat | `TwitchIRCClient` / `TwitchIRCClientNode` | `ircclient` |
| Kick HTTP | `KickAPI` | `kickapi` |
| Generic IRC | `IRCClient` / `IRCClientNode` | `ircclient` |
| Viewer effects | `CrowdControl` | `crowdcontrol` |
| Scenes, record, stream | `OBSClient` | `obsclient` |

`TwitchIRCClient` does not inherit `IRCClient`. It is a parallel `RefCounted` with `connect_to_twitch(username, oauth_token, use_ssl=true)`. `TwitchAPI.configure(client_id, access_token)` is Helix and polls responses every physics frame. `KickAPI.configure(access_token)` is the Kick HTTP API.

## IRC and Twitch chat

`IRCClient` speaks RFC 1459, RFC 2812, and IRCv3. `connect_to_server(host, port, use_ssl, nick, username, realname, password="")` opens the socket. You must `poll()` regularly, or use `IRCClientNode` for automatic polling. SASL helpers include `enable_sasl_plain`, `enable_sasl_external`, and a SCRAM entry that currently falls back to PLAIN with a warning. Set TLS options before connecting with `use_ssl=true`.

```gdscript
var irc := IRCClient.new()
func _ready() -> void:
    irc.message_received.connect(_on_irc_message)
    var err := irc.connect_to_server("irc.libera.chat", 6697, true, "MyBot", "bot", "My Bot")
    if err != OK:
        push_error(err)

func _process(_delta: float) -> void:
    irc.poll()
```

![IRC session](assets/irc-session.png)

Twitch chat is the dedicated client:

```gdscript
var twitch_irc := TwitchIRCClient.new()
func _ready() -> void:
    ENV.load_env_file("res://.env")
    twitch_irc.connect_to_twitch(ENV.get_env("TWITCH_USER"), ENV.get_env("TWITCH_OAUTH"))
```

Helix stays on `TwitchAPI`. Example from the class reference: `TwitchAPI.configure(client_id, access_token)` then `TwitchAPI.get_users().get_users({"login": ["twitch"]})`, with `request_completed` / `request_failed` for results. Category getters include ads, analytics, bits, channel points, channels, chat, and more. Chat HTTP (send message, badges, emotes) is Helix; IRC is the firehose. Channel points redemptions arrive through Helix helpers such as `TwitchAPI.get_channel_points().get_custom_reward_redemption(...)`; they are not Crowd Control effects and they are not OBS scene changes until your game code says so.

## Kick HTTP

`KickAPI` is a singleton for Kick's developer public API. Configure with an access token, then use category request handlers such as `get_users()`. Connect `request_completed`, `request_failed`, and `rate_limit_warning`. There is no Kick IRC class in-tree parallel to `TwitchIRCClient`; if you need Kick chat beyond HTTP, that is outside these modules.

```gdscript
func _ready() -> void:
    ENV.load_env_file("res://.env")
    KickAPI.configure(ENV.get_env("KICK_ACCESS_TOKEN"))
    KickAPI.request_completed.connect(_on_kick)
    KickAPI.get_users().get_users({"username": ["streamer_name"]})
```

## Crowd Control (effects)

`CrowdControl` connects to Crowd Control's PubSub. Default URL for `connect_to_crowdcontrol` is `wss://pubsub.crowdcontrol.live/`. Register the game on the Crowd Control Developer Portal for an App ID and secret. Auth helpers include websocket and HTTP polling paths; `authentication_url_ready` carries the URL the streamer must open. Cache tokens with `get_auth_token` / `set_auth_token` and `refresh_token` when needed.

When a viewer buys or triggers an effect, `effect_requested` delivers a dictionary with `reqId`, `code`, and `parameters`. Apply the effect in your game, then answer:

```gdscript
func _process(_delta: float) -> void:
    CrowdControl.poll()

func _on_effect(effect_data: Dictionary) -> void:
    var req_id = effect_data.get("reqId")
    match effect_data.get("code"):
        "give_coins":
            # mutate game state, then:
            CrowdControl.respond_to_effect_instant(req_id, CrowdControl.STATUS_SUCCESS, "Coins given!")
        "invert_controls":
            CrowdControl.respond_to_effect_timed(req_id, CrowdControl.STATUS_TIMED_BEGIN, 30000, "Invert Controls started.")
```

You do not start the effect from the game. Instant versus timed is the response API. Closing the socket is `close()`.

## OBS (broadcast)

`OBSClient` speaks obs-websocket 5.x. `connect_to_obs(url, password="", event_subscriptions=2047)` returns an `Error` when the attempt starts. Call `poll()` until the handshake finishes. `get_connection_state` / `is_obs_connected` tell you the socket came up. `set_current_program_scene` switches the program scene. The class also covers inputs, filters, record, stream, replay buffer, studio mode, and `send_request` / `send_request_batch` for anything not wrapped.

```gdscript
func _ready() -> void:
    ENV.load_env_file("res://.env")
    var err := OBSClient.connect_to_obs("ws://localhost:4455", ENV.get_env("OBS_PASSWORD"))
    if err != OK:
        push_error(err)

func _process(_delta: float) -> void:
    OBSClient.poll()

func cut_to_alert() -> void:
    if OBSClient.is_obs_connected():
        OBSClient.set_current_program_scene("Alert")
```

![OBS connect](assets/obs-connect.png)

Record and stream controls (`get_record_status`, `get_stream_status`, pause/resume, replay buffer) sit on the same singleton. Use them when the game owns the broadcast machine. Do not assume a remote OBS over the public internet without your own tunnel; the default URL in docs is `ws://localhost:4455`.

## Wiring the three jobs

Keep the boundaries explicit:

1. **Chat / channel metadata** — `TwitchIRCClient` / `IRCClient` for messages; `TwitchAPI` / `KickAPI` for Helix-style HTTP.
2. **Viewer effects** — `CrowdControl` answers effects; it does not own chat or OBS.
3. **Broadcast** — `OBSClient` switches scenes, records, and streams; it does not parse Twitch chat.

A loop that is actually useful looks like this: Helix or IRC delivers a message, the game mutates something, Crowd Control may apply a paid effect on its own socket, then `OBSClient` changes a scene if you asked it to. Nothing in the engine does the middle step for you.

If you only need alerts on channel-point redemptions, you can skip Crowd Control entirely and drive OBS from Helix callbacks. If you only need paid chaos effects, you can skip OBS. The modules are independent on purpose so a failure on one socket does not take down the others.

## Tokens and dotenv

Load secrets with `ENV.load_env_file` (or the auto-load helpers) and read them with `ENV.get_env`, `get_env_int`, and the other typed getters. `get_missing_envs` is useful at boot. Pushing values into the OS environment is optional (`push` helpers in the same singleton). Treat `.env` as developer convenience on a stream PC, not as a vault.

## Edge cases and limits

- Forgetting `poll()` on Crowd Control or OBS looks like a dead socket.
- `TwitchIRCClient` is not a subclass of `IRCClient`; do not cast across them.
- Tokens in `.env` are local convenience. Rotate them like any secret that sat on disk.
- There is no unified "StreamingManager" type and no Blazium-hosted token vault.
- SASL SCRAM-SHA-256 on `IRCClient` currently falls back to PLAIN with a warning; prefer `enable_sasl_plain` or `enable_sasl_external` for production IRC.
- In-house validation covered the clients. It did not ship a branded overlay as a product claim.
- Hangman storefronts do not imply streaming integration in those builds.

Test repos referenced from the class XML include [obsclient_module_tests](https://github.com/blazium-games/obsclient_module_tests), [irc_module_tests](https://github.com/blazium-games/irc_module_tests), [twitchapi_module_tests](https://github.com/blazium-games/twitchapi_module_tests), [kickapi_module_tests](https://github.com/blazium-games/kickapi_module_tests), and [crowdcontrol_module_tests](https://github.com/blazium-games/crowdcontrol_module_tests).

## Links

- Engine: https://github.com/blazium-games/blazium
- OBS tests: https://github.com/blazium-games/obsclient_module_tests
- IRC tests: https://github.com/blazium-games/irc_module_tests
- Twitch tests: https://github.com/blazium-games/twitchapi_module_tests
- Kick tests: https://github.com/blazium-games/kickapi_module_tests
- Crowd Control tests: https://github.com/blazium-games/crowdcontrol_module_tests
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
