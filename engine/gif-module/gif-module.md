---
title: "GIF Module"
description: "Native GIF support in Blazium: decode, import, playback, encode, and MovieWriter."
cover: "assets/cover.png"
slug: "gif-module"
deployed: false
date: "2026-09-02"
author: "sshiiden"
hosts: []
---

# The GIF Module

## Why we built it

The commit that adds the module is "Add GIF module for reading, writing, and playing animated GIFs." A follow-up narrows the design: "Update implementation to only add GifTexture which can be used anywhere as a texture." `GIFTexture.xml` says the same thing: assign it to Sprite2D, Sprite3D, TextureRect, a material, or a shader uniform like any other `Texture2D`. A later editor commit keeps GIF capture from blocking the editor, in the same change that keeps Steam ticket polling and remote Autowork off the UI thread.

## What Blazium Games uses it for

Blazium Games used `GIFTexture` and `GIFRecorder` in-house to validate GIF import, playback, and capture, including capture that does not block the editor. That is a validation pass. It does not name a shipped title.

## What other projects get

The module is always built, in the editor and in export templates. A `.gif` import is a texture with its own playhead. `GIFRecorder` and `MovieWriterGIF` write one back out. Capture is not supposed to freeze the editor.

A `.gif` file is a texture with a clock, a disposal method, and a loop count. `modules/gif` is the native path: decode on import, play as a `Texture2D`, encode again from a viewport or from the engine movie recorder.

The module is always built. `config.py` returns true for both `can_build` and `is_enabled`. It is in the editor and in export templates. There is no separate GIF download on the CDN.

Drop a `.gif` in the filesystem dock. `ResourceImporterGIF` produces a `GIFTexture`. Assign it and set `play` and `loop`. `GIFRecorder.record_viewport(viewport, path, duration_sec, fps)` writes one back out. The C++ default fps is 12. This page is what the module is for and what it will not do.

## What landed

| Class | Job |
|---|---|
| `GIFTexture` | `Texture2D` with its own playhead. `resource_local_to_scene` defaults to true |
| `ResourceImporterGIF` | Drop a `.gif` in the filesystem dock |
| `ResourceImporterGIFFrames` | The same file as frames for a sprite sheet |
| `GIFRecorder` | Viewport, window, or screen back out to a `.gif` |
| `MovieWriterGIF` | The engine movie recorder, when the output path ends in `.gif` |

`GIFTexture.from_sprite_frames` and `to_sprite_frames` move a clip between this texture and `SpriteFrames`. `save_to_path` writes the encoded file. Delay on `add_source_frame` is in centiseconds.

```gdscript
var gif := GIFTexture.new()
var err := gif.load_from_path("res://ui/banner.gif")
if err != OK:
    push_error(err)
$Sprite2D.texture = gif
gif.play = true
```

Playback follows `netscape_loop_count` while `loop` is true. `autoplay_on_load` and importer `speed_scale` are set at import. Use Make Unique when two nodes in one scene must not share a playhead.

## Limits

Project Settings cap the decode and the capture:

| Key | Default |
|---|---|
| `blazium/gif/max_canvas_pixels` | `16777216` |
| `blazium/gif/max_frames` | `4096` |
| `blazium/gif/capture_hotkey` | `0` (off) |
| `blazium/gif/capture_source` | `0` Viewport, `1` Window |
| `blazium/gif/capture_output_dir` | `user://` |

A file over those caps is rejected. The hotkey is read on `process_frame` and toggles `GIFRecorder` only when it is not zero. A long full-screen capture hits `max_frames` and the encode fails. This is not a video codec. Short clips stay in the 10 to 15 fps range because that is what the caps and the file size allow.

`MovieWriterGIF` and `GIFRecorder` share the encoder. They are not the same API. The movie writer is the engine's built-in recorder pointed at a `.gif` path. `record_viewport` is the one-shot on a `SubViewport`.

## Status

Shipped on `blazium-dev`. No SCons flag turns it off. Tests live in [gif_module_tests](https://github.com/blazium-games/gif_module_tests). Nothing in the module registers a follow-up format (APNG, WebP animation). Those are not a queued target in this tree.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
