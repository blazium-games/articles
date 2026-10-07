---
title: "GIF import and recording"
description: "GIFTexture plays animated GIFs. GIFRecorder captures a viewport, window, or screen."
cover: "assets/cover.png"
slug: "gif-texture-and-recorder"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Import a gif onto a sprite. Record a viewport, a window, or the screen back out to a gif. `modules/gif` is how those two directions work, including clips you drop into Hub News.

## Import

Drop a `.gif` into the project. The importer produces a `GIFTexture`. `ResourceImporterGIFFrames` is the path that turns a gif into frames for a sprite sheet.

`GIFTexture` is a `Texture2D`. Each instance keeps its own playhead (`resource_local_to_scene` defaults to true). `play`, `loop`, `current_frame`, and `speed_scale` (on the importer) control playback. `get_frame_count`, `get_frame_delay`, and `get_frame_delay_sec` read one frame. `get_active_texture(frame)` is the composited texture.

```gdscript
var gif: GIFTexture = load("res://sprites/coin.gif")
$Sprite2D.texture = gif
gif.play = true
gif.loop = true
```

`GIFTexture.from_sprite_frames(frames, &"default")` builds a gif from an existing SpriteFrames animation. `to_sprite_frames()` goes back. `save_to_path` writes the encoded file.

Canvas and frame caps are `blazium/gif/max_canvas_pixels` (16777216) and `blazium/gif/max_frames` (4096).

## Record

```gdscript
var err := GIFRecorder.record_viewport($SubViewport, "user://clip.gif", 4.0, 12)
if err != OK:
    push_error(err)
```

`record_viewport` takes the viewport, the output path, a duration in seconds, and an fps (the C++ default is 12). For a clip you start and stop yourself:

```gdscript
GIFRecorder.start_viewport($SubViewport, "user://clip.gif")
# later
GIFRecorder.stop()
GIFRecorder.save()
```

Also `start_window`, `start_screen`, and `add_frame`. `is_recording` and `paused` are the state. `dither`, `fps`, `loop_count`, `max_frames`, and `max_size` are the encode knobs.

A Project Settings hotkey toggles capture when `blazium/gif/capture_hotkey` is not zero. `blazium/gif/capture_source` is Viewport (`0`) or Window (`1`). Files go to `blazium/gif/capture_output_dir` (default `user://`).

This works in the editor and in an exported game. The module is not tools-only.

## Movie writer

`MovieWriterGIF` registers GIF as a movie-writer target. Use it when you want the engine's built-in movie recorder to write a `.gif` without calling `GIFRecorder`. Keep the fps in the 10 to 15 range for a Hub News loop, and keep the clip short. A long full-screen capture will hit `max_frames` or `max_canvas_pixels` and fail the encode.

Class reference and the why-we-added-it writeup: [GIF Module](../gif-module/gif-module.md). Tests: [gif_module_tests](https://github.com/blazium-games/gif_module_tests).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
