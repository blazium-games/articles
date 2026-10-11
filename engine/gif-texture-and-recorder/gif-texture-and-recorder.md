---
title: "GIF import and recording"
description: "GIFTexture plays an animated GIF as a Texture2D. GIFRecorder and MovieWriterGIF write one back out."
cover: "assets/cover.png"
slug: "gif-texture-and-recorder"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# GIF import and recording

### A texture with a clock, not a video codec

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

Godot will import an image. It will not treat an animated GIF as a `Texture2D` you can drop on a sprite. We kept hitting that while making 2D games, including Demon Lord: Clicker, which we built in part to validate the 2D side and the newer modules. `modules/gif` is the native path: decode on import, play as a texture, encode again from a viewport or from the engine movie recorder.

The module is always built. `can_build` and `is_enabled` both return true. It is in the editor and in export templates. There is no CDN package for it. It will not grow into a video codec. The encoder is a palette path. `MovieWriterGIF` ignores audio.

![GIF in, GIF out](assets/gif-pipeline.png)

## Import

Copy a `.gif` into the project. `ResourceImporterGIF` produces a `GIFTexture`. `ResourceImporterGIFFrames` splits the file into frames instead. Assign the texture to `Sprite2D`, `TextureRect`, a material, or a shader uniform. `GIFTexture` is a `Texture2D`.

`resource_local_to_scene` defaults to true, so each scene instance has its own playhead. Use Make Unique when two nodes in the same scene must not share one.

Importer options include `autoplay_on_load`, `loop_count`, `speed_scale`, `dither`, `display_mode`, `bake_compress`, and `bake_storage`. Canvas and frame caps are Project Settings: `blazium/gif/max_canvas_pixels` (default 16777216) and `blazium/gif/max_frames` (default 4096). Over the cap, import fails.

## Playback

`play` defaults to false. `loop` defaults to true. `autoplay_on_load` defaults to true. Netscape loop counts are honored.

```gdscript
var gif: GIFTexture = load("res://sprites/coin.gif")
$Sprite2D.texture = gif
gif.play = true
gif.loop = true
```

`get_frame_count`, `get_frame_delay`, and `get_frame_delay_sec` read one frame. `get_active_texture(frame)` is the composited texture. Delay on `add_source_frame` is in centiseconds.

`GIFTexture.from_sprite_frames(frames, &"default")` builds a GIF from an existing SpriteFrames animation. `to_sprite_frames()` goes back. `save_to_path` writes the encoded file.

## Record

```gdscript
var err := GIFRecorder.record_viewport($SubViewport, "user://clip.gif", 4.0, 12)
if err != OK:
    push_error(err)
```

`record_viewport` takes the viewport, the output path, a duration in seconds, and an fps. The C++ default fps is 12. For a clip you start and stop yourself, `start_viewport` then later `stop` and `save`. Also `start_window`, `start_screen`, and `add_frame`. `is_recording` and `paused` are the state. `dither`, `fps`, `loop_count`, `max_frames`, and `max_size` are the encode knobs.

A Project Settings hotkey toggles capture when `blazium/gif/capture_hotkey` is not zero. The default is zero, so nothing is bound until you set it. `blazium/gif/capture_source` is Viewport (`0`) or Window (`1`). Files go to `blazium/gif/capture_output_dir` (default `user://`).

Capture is deferred so it does not block the editor. The same idea shows up in the commit that keeps GIF capture, Steam ticket polling, and remote Autowork off the UI thread. This works in the editor and in an exported game. The module is not tools-only.

## Movie writer

`MovieWriterGIF` registers GIF as a movie-writer target. Use it when the engine's built-in movie recorder should write a `.gif` without calling `GIFRecorder`. Keep the fps in the 10 to 15 range and keep the clip short. A long full-screen capture hits `max_frames` or `max_canvas_pixels` and the encode fails. Audio frames are dropped.

Tests: [gif_module_tests](https://github.com/blazium-games/gif_module_tests).

## Links

- Module: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/gif
- Tests: https://github.com/blazium-games/gif_module_tests
- Engine: https://github.com/blazium-games/blazium
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
