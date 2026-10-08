---
title: "Identity, Steam, and Xbox"
description: "Tickets and OAuth become JSON Web Tokens. Steamworks and Microsoft GDK are the store clients."
cover: "assets/cover.png"
slug: "online-identity-and-stores"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

A store ticket or an OAuth code is not a session. Turn it into a JSON Web Token (JWT), then check it on your backend. The engine pieces on `blazium-dev` are `modules/jwttool`, `modules/steam`, `modules/discord_module`, and `modules/xbox_module`.

## Status

JWT, Steam, and Discord desktop auth are in the tree and build with the engine. `xbox_module` is off unless SCons gets `module_xbox_module_enabled=yes`. The stable script surface is `GDK` in the class reference (`initialize`, `shutdown`, `is_available`, `is_initialized`, `dispatch`). C++ getters for users, achievements, stats, leaderboards, store, and presence are in `modules/xbox_module/gdk/gdk.h`. Most of those sub-objects have no class-reference XML yet. Read the header before calling them. `EditorExportPlatformXbox` needs a GDK install on the machine. This is not a retail console-kit guide. Signed-in tests need `LIVE_TESTS=1`.

Steam on `blazium-dev` covers `initialize`, achievements, stats, inventory, workshop items, and `authenticate_with_server`. It does not expose Steam leaderboards. [blazium#807](https://github.com/blazium-games/blazium/issues/807) asks for `ISteamUserStats` leaderboard calls. That issue is open. The methods are not in `modules/steam`.

`LoginClient`, `LobbyClient`, and `MasterServerClient` are not registered. Script templates with those names are still under `modules/gdscript/editor/script_templates/` and will not run. GodotSteam was removed in 0.5.246. The published call list for achievements and inventory is the [Steam module](../steam-module/steam-module.md) article. Engine docs: [docs.blazium.app](https://docs.blazium.app).

![Identity flow](assets/identity-flow.png)

![JWT issue, kid, verify, grant or reject](assets/jwt-validate.png)

## JWT

`JWT` is the singleton. `JWTBuilder` constructs a token. `DecodedJWT` reads one. Algorithms documented on the class are HS256 and RS256. `kid` is the header key id. `JWT.validate_with_map` picks the key by that `kid`. Expiry is `set_expiration(seconds_from_now)` on the builder, and `is_expired` / `validate_timing(jwt, leeway_seconds)` on the way in. `revoke_jti` / `is_revoked` / `clear_revoked` are the in-process revocation list.

The builder example in `JWTBuilder.xml`:

```gdscript
var builder := JWTBuilder.new().set_issuer("auth.local").set_subject(user_id)
builder.set_algorithm("HS256")
builder.set_expiration(3600)
var token := builder.sign(secret)
var decoded := JWT.parse(token)
print(decoded.get_claim_as_string("sub"))
if decoded.is_expired():
    return
```

`sign` takes a `String` secret for HS256 or a `CryptoKey` for RS256. `JWT.create_jwt_timed` is deprecated. Use the builder.

![Granting access](assets/granting-access.gif)

This article does not stand up a login server. It is the token the game already has, and how Steam or Discord can exchange a platform ticket for one.

## Steam

Native `Steam` singleton in `modules/steam`. GodotSteam was removed in 0.5.246. `initialize(app_id)` returns an `Error`. `480` is Spacewar, Steam's test app id.

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
        print(result.get_jwt().length())
    Steam.cancel_auth_ticket(auth_ticket_handle)
```

`authenticate_with_server(url, ticket, app_id)` is the call that comes back as `SteamAuthResult` (`get_jwt()`, `get_steam_id()`, `get_persona()`, `is_success()`). `cancel_auth_ticket` drops a handle you no longer need. Achievements, stats, and inventory are the rest of the same singleton. The published walkthrough of those calls is the [Steam module](../steam-module/steam-module.md) article.

## Discord desktop login

Separate from an embedded activity. `Discord.initialize(client_id)` is the full OAuth path (friends, invites, server auth). `initialize_presence_only` is rich presence without that. `authenticate_with_server(url, access_token, client_id)` returns a `DiscordAuthResult` whose `get_jwt()` is the session your backend issued. `create_or_join_lobby(secret)` is a Discord SDK lobby, not a Blazium HTTP service.

Embedded activities use `DiscordEmbeddedAppClient` instead. See [Discord on Blazium](../discord-on-blazium/discord-on-blazium.md).

## GDK / Xbox

`xbox_module` is off unless you pass `module_xbox_module_enabled=yes`. The class reference singleton is `GDK` (`initialize(config)`, `shutdown`, `is_available`, `is_initialized`, `dispatch`). C++ also exposes getters for users, achievements, stats, leaderboards, store, presence, and related Xbox Live surfaces (`modules/xbox_module/gdk/gdk.h`). Those sub-objects are real. Most of them do not have class-reference XML yet, so treat `GDK.xml` as the stable surface and read the headers before you call further.

The export platform is `EditorExportPlatformXbox`. A GDK install has to be on the machine (`gdk_path`, or `GameDKCoreLatest` / `GameDKLatest`). This article does not describe a retail console kit.

![GDK / Xbox export tooling](assets/gdk-export.png)

Tests in the module can require `LIVE_TESTS=1` for signed-in Xbox Live calls. Packaging checks run without that.

## Networking that compiles

Matchmaking you can compile on `blazium-dev` is `ENetServer` / `ENetClient`, `SignalClient` plus `WebRTCEnetSession` in `games_enet_webrtc`, or `Discord.create_or_join_lobby`. The missing login and lobby classes are in Status. They are not a later section of this article.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
