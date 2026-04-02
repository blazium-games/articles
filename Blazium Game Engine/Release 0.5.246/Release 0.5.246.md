---
title: "Blazium Engine Release 0.5.246"  
description: "The final 4.3-based version, which will become the future LTS after the upcoming 4.6-based release."  
cover: "assets/cover.jpg"
changes: https://github.com/blazium-games/blazium/commits/blazium-dev/?since=2025-05-04&until=2026-04-01
---

# Blazium Engine Release 0.5.246

This marks the **last release based on Godot 4.3** and will serve as
the future **Long-Term Support (LTS)** version once the next 4.6-based release arrives.

Thanks to the significant number of new features, we’ve re-launched our
[official documentation](https://docs.blazium.app) to help you make the most of Blazium.

## New Features

### HTTP Server Module
![](../HTTP%20Server%20Module/assets/http_demo.gif)

A full-featured HTTP server with support for REST APIs, static file serving, and Server-Sent Events (SSE).

Learn more about the HTTP Server in the [dedicated article]().

### RCON Module
![](../RCON%20Module/assets/rcon_demo.gif)

Connect as a client to existing RCON-enabled servers or run your own RCON server inside a Blazium project.

Learn more in the [dedicated article]().

### IRC Client Module
![](../IRC%20Client%20Module/assets/irc_client_code.jpg)

Quick and simple IRC client integration for real-time chat in your games.

Learn more in the [dedicated article]().

### New ENet Module
![](../New%20ENet%20Module/assets/enet_server_code.jpg)

A more flexible and less restrictive ENet implementation compared to the default one.

Learn more in the [dedicated article]().

### SocketIO Client Module
![](../SocketIO%20Client%20Module/assets/socketio_connection.jpg)

Easily connect to and manage Socket.IO connections from your projects.

Learn more in the [dedicated article]().

### CrowdControl Module
![](../Crowd%20Control%20Module/assets/cc_code2.jpg)

Seamless Crowd Control integration, making it easy to add interactive chat and
viewer-driven events for streamers.

Learn more in the [dedicated article]().

### Twitch API Module
![](../TwitchAPI%20Module/assets/twitch_code.jpg)

Full Twitch API integration for your streaming and community features.

Learn more in the [dedicated article]().

### Kick API Module
![](../KickAPI%20Module/assets/kick_code.jpg)

Kick API integration for modern streaming platforms.

Learn more in the [dedicated article]().

### OBS Client Module
![](../OBS%20Client%20Module/assets/obs_code.jpg)

Control OBS Studio directly from within Blazium.

Learn more in the [dedicated article]().

### Alternative Scrollbar Style
![](assets/scroll_demo.gif)

Option to enable thicker editor scrollbars, making them much easier to grab and use.

**Contributed by [Tekisasu-JohnK](https://github.com/blazium-games/blazium/pull/584)**

### QTerminal Support
Added support for **QTerminal** as a supported terminal emulator on Linux.

**Contributed by [MisterPuma80](https://github.com/blazium-games/blazium/pull/602)**

## Removals

### GodotSteam Module Removed

After encountering issues with the existing integration of the
[GodotSteam gdextension](https://godotsteam.com) into the engine and considering
that it is maintained by a separate team, we decided to remove the GodotSteam module.

We plan to develop our own robust solution in the future.

### Six-Way Volumetric Lighting Material Removed

The original Godot shader implementation remains available here:  
[TheAenema/Godot-Six-Way-Volumetric-Shader](https://github.com/TheAenema/Godot-Six-Way-Volumetric-Shader).

## Download

[Download the latest release on blazium.app](https://blazium.app/download)

For the complete list of changes, see the [changelog](https://blazium.app/changelog?v=release_0.5.246).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
- **[Patreon](https://www.patreon.com/cw/Blazium)**
