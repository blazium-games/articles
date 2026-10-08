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

Import a gif onto a sprite. Record a viewport, a window, or the screen back out to a gif. `modules/gif` is how those two directions work. Why the module is a `Texture2D` is in [GIF Module](../gif-module/gif-module.md).

## Status

The module is always built on `blazium-dev`. `can_build` and `is_enabled` both return true. It runs in the editor and in exported games. There is no CDN package for it. Why it is one module, and what it will not grow into, is [GIF Module](../gif-module/gif-module.md).

## Import a file

1. Copy `coin.gif` into the project.
2. The dock runs `ResourceImporterGIF` and produces a `GIFTexture`. `ResourceImporterGIFFrames` is the importer that splits the file into frames instead.
3. Assign the texture to `Sprite2D`, `TextureRect`, or any other `Texture2D` slot.
4. Set `play` and `loop`. `resource_local_to_scene` defaults to true, so each scene instance has its own playhead. Use Make Unique when two nodes in the same scene must not share one.

Importer options include `autoplay_on_load`, `loop_count`, `speed_scale`, `dither`, `display_mode`, `bake_compress`, and `bake_storage`. Canvas and frame caps are `blazium/gif/max_canvas_pixels` (16777216) and `blazium/gif/max_frames` (4096). Over the cap, import fails.

## Playback

`GIFTexture` is a `Texture2D`. `play`, `loop`, and `current_frame` control the instance. `speed_scale` is an importer option. `get_frame_count`, `get_frame_delay`, and `get_frame_delay_sec` read one frame. `get_active_texture(frame)` is the composited texture. Delay on `add_source_frame` is in centiseconds.

```gdscript
var gif: GIFTexture = load("res://sprites/coin.gif")
$Sprite2D.texture = gif
gif.play = true
gif.loop = true
```

`GIFTexture.from_sprite_frames(frames, &"default")` builds a gif from an existing SpriteFrames animation. `to_sprite_frames()` goes back. `save_to_path` writes the encoded file.

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

`MovieWriterGIF` registers GIF as a movie-writer target. Use it when you want the engine's built-in movie recorder to write a `.gif` without calling `GIFRecorder`. Keep the fps in the 10 to 15 range and keep the clip short. A long full-screen capture will hit `max_frames` or `max_canvas_pixels` and fail the encode.

Class reference and the why-we-added-it writeup: [GIF Module](../gif-module/gif-module.md). Tests: [gif_module_tests](https://github.com/blazium-games/gif_module_tests).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
