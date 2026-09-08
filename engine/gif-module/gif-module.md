---
title: "GIF Module"
description: >-
    Native GIF support in the Blazium Game Engine with decoding, resource import, playback and recording.
cover: "assets/cover.png"
slug: "gif-module"
deployed: false
date: "2026-09-02"
author: "sshiiden"
hosts: []
---
# The GIF Module

The new **GIF module** adds native support for animated GIFs in Blazium, covering decoding, resource import, runtime playback, encoding, recording, and MovieWriter integration.

<!-- image showing a gif being added in the 2d viewport -->

At the core of the module is **GIFTexture**, a self-contained `Texture2D` subclass that stores both
the decoded frame data and its own playback state.
You can import a `.gif` file and use it directly with Sprite2D, Sprite3D, TextureRect, materials, or
shader uniforms just like any other texture.

Playback starts automatically, supports looping and speed control (including reverse),
and runs independently for each instance in a scene.
You can also convert between GIFTexture and SpriteFrames, or build a GIF from individual images.

## MovieWriter Support

GIF is now a supported format for the engine’s built-in movie recorder.
Simply choose a `.gif` path when recording and the engine will export an animated GIF automatically.

<!-- image showing a .gif path being set for moviewriter -->

## Recording a GIF

**GIFRecorder** lets you capture gameplay or the editor as an animated GIF.
You can record a viewport, the main window, or the entire screen.
Capture can be timed or started and stopped manually.
A configurable hotkey in Project Settings makes it easy to record and save clips during play.

<!-- image showing a gif being recorded by shortcut -->

## Documentation & Next Steps

The module is available in the [latest nightly of Blazium](https://blazium.app/download)
and a dedicated test project is available at
[gif_module_tests](https://github.com/blazium-games/gif_module_tests).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**