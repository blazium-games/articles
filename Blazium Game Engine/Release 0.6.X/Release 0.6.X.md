---
title: "Blazium Engine Release 0.6.X"
description: "The last 4.3 based version that will become the future LTS after the coming 4.6 based release."
cover: "assets/cover.jpg"
---

<!--
https://github.com/blazium-games/blazium/commits/blazium-dev/?since=2025-05-04&until=2026-03-30
-->

# Blazium Engine Release 0.6.X

Last 4.3 based release, will be future LTS version after the nex (4.6 based) release.
Big new features have been added, which justified setting up
[our documentation website](https://docs.blazium.app).

## New Features

### Autowork Unit Testing Module
![](assets/temp_autowork.png)

### HTTP Server Module
![](assets/http.jpg)

### SocketIO Module
![](assets/socketio.jpg)

### IRC Client Module
![](assets/irc.jpg)

### ENet Module
![](assets/enet.jpg)
<!--
Godot's implementation is limiting, this is a generalized implementation
-->

### CrowdControl Module
![](assets/crowdcontrol.jpg)

### Twitch API Module
![](assets/twitchapi.jpg)

### Kick API Module
![](assets/kickapi.jpg)

### OBS Client Module
![](assets/obs.jpg)

### Alternative scrollbar style
![](assets/scroll.jpg)
Option to make the editor's scrollbars thicker, making them easier to grab.

[By Tekisasu-JohnK](https://github.com/blazium-games/blazium/pull/584)

### QTerminal Support
Added QTerminal as supported terminal emulator for linux.

[By MisterPuma80](https://github.com/blazium-games/blazium/pull/602)

## Removals

### GodotSteam Module
Problems with implemention

### Six-Way Volumetric Lighting Material
Problems with implemention in the engine codebase

The Godot shader implementation can still be found at
[TheAenema/Godot-Six-Way-Volumetric-Shader](https://github.com/TheAenema/Godot-Six-Way-Volumetric-Shader).

## Download

[Download the latest release on blazium.app](https://blazium.app/download)

The complete list of changes can be found at the [changelog page](https://blazium.app/changelog?v=release_0.6.X).
