---
title: "Identity, Steam, and Xbox"
description: "Tickets and OAuth become JWTs. Steamworks and Microsoft GDK are the store clients."
cover: "assets/cover.png"
slug: "online-identity-and-stores"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

A store ticket or an OAuth code is not a session. Turn it into a JWT, then hand that to Lobby or your backend.

![Identity flow](assets/identity-flow.png)

![JWT issue, kid, verify, grant or reject](assets/jwt-validate.png)

## JWT

Classes: `JWT`, `JWTBuilder`, `DecodedJWT`. HS256 and RS256. `kid`, expiry, revocation.

```gdscript
var token := JWTBuilder.new() \
    .with_issuer("login.blazium.app") \
    .with_subject(user_id) \
    .with_expires_at(Time.get_unix_time_from_system() + 3600) \
    .sign_hs256(secret)

var decoded: DecodedJWT = JWT.decode(token)
if not decoded.is_valid():
    return
```

![Granting access](assets/granting-access.gif)

Login Service walk: [Blazium Services](../blazium-services/blazium-services.md). Do not re-implement matchmaking here.

## Steam

Native `Steam` singleton. GodotSteam was removed in 0.5.246. `features.json` on the website still mentions GodotSteam. That page is wrong.

```gdscript
func _ready() -> void:
    if not Steam.initialize(480):
        push_warning("Steam unavailable")
        return
    var ticket := Steam.get_auth_session_ticket()
    var jwt := await MyBackend.authenticate_steam(ticket)
```

`480` is Spacewar, Steam's test app. Use your app id in production. Achievements, stats, inventory, web tickets, `authenticate_with_server` are the day-one surface.

<!-- CAPTURE: assets/steam-overlay.png | Game | Steam overlay over a running Blazium game -->
<!-- CAPTURE: assets/steam-achievement.gif | Game | Achievement unlock -->
<!-- CAPTURE: assets/cover.png | Game | Overlay plus JWT decode, 16:9 -->

## GDK / Xbox

Code lives in `xbox_module`. Export class `EditorExportPlatformXbox`. **Off by default.** Enable with `module_xbox_module_enabled=yes` and a GDK install. What ships today is PC GDK + XSAPI (achievements, presence, leaderboards) plus `MicrosoftGame.config` packaging. This article does not claim a retail Xbox kit pipeline.

![GDK / Xbox export tooling](assets/gdk-export.png)

<!-- CAPTURE: assets/gdk-off-by-default.png | Editor or docs | Export preset with a caption that the module is default off -->
<!-- CAPTURE: assets/version-info.png | Editor | Engine.get_version_info() showing Godot and Blazium lines -->

`LIVE_TESTS=1` turns on signed-in Xbox Live tests. Packaging smoke tests run without credentials.

If you cannot show a packaged Xbox build, keep the still at the PC export preset and say so in the caption.
