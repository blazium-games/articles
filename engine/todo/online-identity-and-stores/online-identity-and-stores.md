---
title: "Identity, Steam, and Xbox"
description: "Steam tickets and Discord OAuth become JSON Web Tokens. GDK is in the tree and off unless you build it."
cover: "assets/cover.png"
slug: "online-identity-and-stores"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Identity, Steam, and Xbox

### A platform ticket is not a session

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

GodotSteam left the tree in 0.5.246. We replaced the pieces we actually ship with: achievements, stats, inventory, workshop items, and a web API ticket the game can exchange with a backend. The Discord Social SDK covers desktop presence and invites. Microsoft GDK is in the tree for Xbox-shaped export, and it does not build unless you turn it on. Tokens are JSON Web Tokens (JWTs), built and checked in the engine.

Hangman shipped on Steam, Discord, Google Play, and the Apple App Store. That is how export and store upload were checked end to end. It does not mean every one of those builds called `Steam.initialize` or `GDK.initialize`. Demon Lord: Clicker is the later live-ops proof on Steam inventory, server-saved runs, and Discord presence; treat that as validation of those modules under load, not as a second claim that Hangman exercised every auth path.

The Blazium Games store at [blazium.games](https://blazium.games) is a different product. A game on that store does not have to be made with this engine. Uploads there are `blazium-cli games` (alias `chauffeur`), not the Steam module and not `blazium-cli deploy`.

![Steam ticket or Discord OAuth, then a JWT](assets/identity-flow.png)

`LoginClient` and `LobbyClient` on that diagram are the SDK module, not classes in a stock `blazium-dev` editor. The engine path is `Steam.authenticate_with_server` and `Discord.authenticate_with_server`, both of which return a token your backend minted. The platform ticket or OAuth access token proves the player to your server. The JWT is the game session you issue after that proof.

## JWT

`modules/jwttool` registers `JWT`, `JWTBuilder`, and `DecodedJWT`. The class reference documents HS256 and RS256. `kid` is the header key id. `JWT.validate_with_map` picks the key by that `kid`. `JWT.validate_timing(jwt, leeway_seconds)` checks time claims. `revoke_jti`, `is_revoked`, and `clear_revoked` are an in-process list. They die with the process. `JWT.create_jwt_timed` is deprecated. Use the builder.

```gdscript
var builder := JWTBuilder.new().set_issuer("auth.local").set_subject(user_id)
builder.set_algorithm("HS256")
builder.set_expiration(3600)
var token := builder.sign(secret)
var decoded := JWT.parse(token)
if decoded.is_expired():
    return
var subject := decoded.get_claim_as_string("sub")
```

`sign` takes a `String` secret for HS256 or a `CryptoKey` for RS256. `JWT.decode` / `get_payload` without signature checks are for inspection only; the class reference says not to use them for authentication. Prefer `JWT.parse` and signature validation with the matching key.

![Issue, kid, verify](assets/jwt-validate.png)

![Granting access](assets/granting-access.gif)

## Steam

`modules/steam` loads the Steamworks library at runtime. Methods fail without crashing the editor when the library or the client is missing.

```gdscript
func _ready() -> void:
    if Steam.initialize(480) != OK:
        push_warning("Steam unavailable")
        return
    Steam.web_api_ticket_ready.connect(_on_ticket)
    Steam.request_web_api_ticket("blazium")

func _on_ticket(hex_ticket: String, auth_ticket_handle: int) -> void:
    var result := Steam.authenticate_with_server(backend_url, hex_ticket, 480)
    if result.is_success():
        var session_jwt := result.get_jwt()
        # Keep session_jwt. Length check only in debug logs if you must.
        print(session_jwt.length())
```

`480` is Spacewar, Steam's test app id. `request_web_api_ticket` emits `web_api_ticket_ready` (and `web_api_ticket_failed` on failure). `authenticate_with_server` is synchronous and returns `SteamAuthResult`.

What the engine actually POSTs is JSON `{"ticket": "<hex>", "app_id": <int>}` with `Content-Type: application/json`. What it requires back is JSON that includes a `jwt` string. Optional fields the client also applies when present include Steam id, persona, and `app_id`. That is the client parse contract. It is not a claim that Blazium hosts a public auth API with a richer schema. Point `backend_url` at your server. On success use `get_jwt`, `get_steam_id`, `get_persona`, `get_app_id`; on failure use `get_error_message` / `is_success`.

Achievements, stats, inventory, and workshop items are on this singleton. Leaderboards are not. [blazium#807](https://github.com/blazium-games/blazium/issues/807) asks for `ISteamUserStats` leaderboard calls. The issue is open. There is no leaderboard method in `modules/steam`.

Demon Lord: Clicker signs players in by exchanging a Steam ticket with its backend and keeps every item, chest, and reward as Steam inventory. That is why inventory landed in the module. Hangman's Steam store presence proved the export and upload path; do not read it as a claim that Hangman exercised inventory exchanges.

## Discord on the desktop

`Discord.initialize_presence_only(client_id)` is auth-less rich presence. `Discord.initialize(client_id)` is the OAuth path: friends, invites, and `authenticate_with_server`, which returns `DiscordAuthResult`. `get_jwt()` on that result is the token your backend minted, not Discord's access token.

The engine POSTs `{"access_token": "...", "client_id": ...}` and requires a `jwt` field in the JSON response. Same rule as Steam: your server, your session. Optional identity fields on that response are applied when present (`get_discord_id`, `get_username`, `get_client_id` on `DiscordAuthResult`). `create_or_join_lobby` is a Discord SDK lobby, not the Blazium lobby client.

```gdscript
func exchange_discord_session(backend_url: String, client_id: int) -> void:
    if Discord.get_auth_state() != Discord.AUTH_READY:
        return
    var result: DiscordAuthResult = Discord.authenticate_with_server(
        backend_url, Discord.get_access_token(), client_id
    )
    if not result.is_success():
        push_error(result.get_error_message())
        return
    var session_jwt := result.get_jwt()
```

The Embedded App client is a different module (`socialexports`) and a web export. It does not replace `initialize` in a desktop build. Hangman's Discord ship is the embed path. Desktop presence and OAuth are the Social SDK path.

## Xbox / GDK

`xbox_module` is present and `is_enabled` in `config.py` defaults to false. Turn it on with `module_xbox_module_enabled=yes`, on Windows, with the GDK installed. Without that define, `GDK.initialize` returns a `GDKResult` error with code `gdk_not_enabled`.

The script surface in the class reference is `GDK`: `initialize`, `shutdown`, `is_available`, `is_initialized`, `dispatch`. Access via `Engine.get_singleton("GDK")` as the XML describes. C++ getters for users, achievements, stats, leaderboards, store, and presence are in `modules/xbox_module/gdk/gdk.h`. Most of those sub-objects do not have class-reference XML yet. Read the header before calling them. Call `dispatch` each frame, or enable `gdk/runtime/embed_dispatch`.

`EditorExportPlatformXbox` needs a GDK install on the machine doing the export. This is not a retail console-kit or signed-in test guide.

![GDK export](assets/gdk-export.png)

## Platform ticket versus game session

| Piece | Proves | Lives in |
|---|---|---|
| Steam web API ticket | Player owns / runs the Steam app | `Steam.request_web_api_ticket` → hex ticket |
| Discord OAuth access token | Player authorized your Discord application | `Discord.get_access_token` after `initialize` |
| Discord Embedded App auth | Player is in the activity frame | `DiscordEmbeddedAppClient.authorize` / `authenticate` |
| JWT from your backend | Your game session | `SteamAuthResult.get_jwt` / `DiscordAuthResult.get_jwt` / `LoginClient.received_jwt` |

Do not treat the platform ticket as the session. Exchange it, then authorize game APIs with the JWT. Revocation lists in `JWT` are process-local; multi-instance revoke belongs on your server.

`LoginClient` in the SDK can also obtain a JWT via Discord login URL or Steam ticket against `login.blazium.app`. That is a separate client from `Steam.authenticate_with_server`. Stock editors do not register it.

## What Hangman and Demon Lord actually proved

Hangman proved export and store upload across Steam, Discord Embedded App, Google Play, and the Apple App Store. That is a shipping claim about packages and storefronts. It is not a claim that every package called `Steam.authenticate_with_server` or `GDK.initialize`.

Demon Lord: Clicker validated Steam inventory, ticket exchange against a game backend, achievements/stats surface, Discord presence, and 2D load after launch on Steam. Use that when you talk about live inventory auth. Do not flatten both games into one sentence that implies Hangman ran GDK.

## Edge cases and limits

- Steam methods no-op safely when the dynamic library is missing; still check return values.
- Empty URL or empty ticket/token produces an immediate `SteamAuthResult` / `DiscordAuthResult` error without a network call.
- Auth HTTP uses a blocking client with connect and body timeouts in the auth helper; call it off the critical render path if you care about hitching.
- Missing `jwt` in the HTTP JSON is a hard failure (`Auth response missing jwt`).
- GDK is Windows + enabled module + installed GDK. `is_available` is false in builds compiled without it.
- No Steam leaderboards until #807 lands.
- Blazium Games uploads are `blazium-cli games`, not these singletons.
- `LoginClient` JWT from `login.blazium.app` and `Steam.authenticate_with_server` JWT from your URL are different clients. Do not assume they share claim names.

## Links

- Steam module: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/steam
- JWT: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/jwttool
- Discord module: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/discord_module
- Leaderboards issue: https://github.com/blazium-games/blazium/issues/807
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
