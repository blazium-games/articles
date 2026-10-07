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

The GIF module (`modules/gif`) is always built. `config.py` returns true for both `can_build` and `is_enabled`. It covers decoding, resource import, runtime playback, encoding, recording, and a MovieWriter.

At the center is **GIFTexture**, a `Texture2D` that stores the decoded frames and its own playback state. Importing a `.gif` produces a GIFTexture. Assign it to Sprite2D, Sprite3D, TextureRect, a material, or a shader uniform the same way you assign any other texture.

`Resource.resource_local_to_scene` is on by default, so each scene instance has its own playhead. Use Make Unique when two nodes in the same scene must play independently. Looping follows `netscape_loop_count` while `loop` is true. Playback starts on load when `autoplay_on_load` is true. `speed_scale` on the importer can run the clip faster, slower, or in reverse.

```gdscript
var gif := GIFTexture.new()
var err := gif.load_from_path("res://ui/banner.gif")
if err != OK:
    push_error(err)
$Sprite2D.texture = gif
gif.play = true
```

`from_sprite_frames` builds a GIFTexture from a SpriteFrames animation. `to_sprite_frames` goes the other way. `add_source_frame(image, delay_cs, disposal, position)` appends a raw frame. Delay is in centiseconds. `bake_frames` composites disposal, offsets, and transparency into full-canvas frames. `save_to_path` / `save_to_buffer` encode.

Importer options on `ResourceImporterGIF` include `autoplay_on_load`, `bake_compress`, `bake_storage`, `display_mode`, `dither`, `loop_count`, and `speed_scale`. `ResourceImporterGIFFrames` is the sprite-sheet style import.

## Limits

Project Settings, registered in `register_types.cpp`:

| Key | Default |
|---|---|
| `blazium/gif/max_canvas_pixels` | `16777216` |
| `blazium/gif/max_frames` | `4096` |
| `blazium/gif/capture_hotkey` | `0` (off) |
| `blazium/gif/capture_source` | `0` (Viewport; `1` is Window) |
| `blazium/gif/capture_output_dir` | `user://` |

A file over those caps is rejected. The hotkey is read on `process_frame` and toggles `GIFRecorder` when it is not zero.

## MovieWriter

`MovieWriterGIF` is a MovieWriter. Point the engine's movie recorder at a `.gif` path and the writer emits an animated GIF. That path does not use the `GIFRecorder` API. It uses the same encode path the rest of the module uses.

## Recording

**GIFRecorder** captures a viewport, the main window, or the screen. `record_viewport(viewport, path, duration_sec, fps)` is the one-shot. The default fps in the C++ signature is 12. Manual control is `start_viewport`, `start_window`, `start_screen`, `add_frame`, `stop`, and `save`. Properties: `dither`, `fps`, `loop_count`, `max_frames`, `max_size`, `paused`.

```gdscript
var err := GIFRecorder.record_viewport($SubViewport, "user://clip.gif", 4.0, 12)
if err != OK:
    push_error(err)
```

It works in the editor and in exported templates, because the module is not editor-only.

The field-level walk of import versus record is in [GIF import and recording](../gif-texture-and-recorder/gif-texture-and-recorder.md). Tests: [gif_module_tests](https://github.com/blazium-games/gif_module_tests).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
