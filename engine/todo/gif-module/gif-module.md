---
title: "Why the GIF module is a texture"
description: "GIFTexture is a Texture2D with a playhead. The recorder writes one back. It is not a video codec."
cover: "assets/cover.png"
slug: "gif-module"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Why the GIF module is a texture

### Drop it on a sprite. Do not expect a movie.

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

The commit that added `modules/gif` was for reading, writing, and playing animated GIFs. The follow-up narrowed it: the thing you assign is `GIFTexture`, and it can sit anywhere a `Texture2D` sits. Sprite2D, Sprite3D, TextureRect, a material, a shader uniform. Godot does not have that class. We wanted it because 2D games, including Demon Lord: Clicker, keep using GIFs as art, and importing them as a pile of loose frames was the workaround.

The class documentation states the model in one place: `GIFTexture` is the single resource for GIF content. It owns the decoded frame data and its playback state. Importing a `.gif` produces that resource. There is no separate animation object in the registered API for the tree we ship; the texture is the animation.

![Import, play, record](assets/gif-pipeline.png)

## Always on

`can_build` and `is_enabled` in `modules/gif/config.py` both return true. There is no SCons flag and no CDN package. The module registers at `MODULE_INITIALIZATION_LEVEL_SCENE` into the editor and into export templates. Alongside `GIFTexture` and `GIFRecorder` it installs `ImageLoaderGIF`, `ResourceFormatLoaderGIF`, `ResourceSaverGIF`, and `MovieWriterGIF`, so `.gif` round-trips through `Image`, `ResourceLoader` / `ResourceSaver`, and the movie-writer registry without a second plugin.

Registered classes from `get_doc_classes()`:

| Class | Role |
|---|---|
| `GIFTexture` | Animated `Texture2D` |
| `GIFRecorder` | Viewport / window / screen capture |
| `ResourceImporterGIF` | Default `.gif` → `GIFTexture` importer |
| `ResourceImporterGIFFrames` | Alternate importer → `SpriteFrames` |

`MovieWriterGIF` is also registered with `MovieWriter::add_writer` so the engine movie recorder can target `.gif`. It is not listed in the doc_classes array, but the writer is part of the module.

## Texture model

`GIFTexture` inherits `Texture2D`. Assign it like any other texture. Playback state lives on the resource:

| Member | Default | Meaning |
|---|---|---|
| `play` | `false` | Advances frames when true |
| `loop` | `true` | Honors `netscape_loop_count` while looping |
| `autoplay_on_load` | `true` | Starts on load / instance |
| `netscape_loop_count` | `0` | `0` = forever; `N` plays `N` times |
| `speed_scale` | `1.0` | Negative values play in reverse |
| `display_mode` | `DISPLAY_SOURCE` (`0`) | Or `DISPLAY_BAKED` (`1`) |
| `bake_storage` | `BAKE_GENERATE_ON_LOAD` (`1`) | Or `BAKE_STORE` (`0`) |
| `dither` | `true` | Used when encoding |
| `encode_optimize` | `true` | Transparency / frame differencing on encode; recorder captures force this false so each frame is a full opaque picture |

`resource_local_to_scene` is enabled in the constructor (`set_local_to_scene(true)`), so two scene instances do not share a playhead unless you want them to. Use Make Unique when two nodes in the same scene must diverge.

Disposal constants match the GIF spec: `DISPOSAL_NONE`, `DISPOSAL_DO_NOT_DISPOSE`, `DISPOSAL_RESTORE_BACKGROUND`, `DISPOSAL_RESTORE_PREVIOUS`. Source frames carry delay in centiseconds, disposal, and canvas offset via `add_source_frame`. `bake_frames` composites those into full-canvas baked frames. Signals: `frames_changed`, `rebaked`.

## Why not video

GIF is a palette format. The encoder quantizes. `MovieWriterGIF::write_frame` accepts audio pointers from the movie-writer interface and ignores them; the encode path only stores images. There is no audio track, no seeking API beyond `current_frame`, and no promise of RGBA fidelity after encode. That is the format. Treating it as a movie codec would lie about what the file can hold.

The same limit is why we expose `GIFTexture` as a texture and not as `VideoStream`. A sprite that loops a coin flip is the job. A cutscene with dialogue audio is not.

## Import path

`ResourceImporterGIF` is the default importer for `.gif`. Options mirror texture members: `autoplay_on_load`, `loop_count` (maps to `netscape_loop_count`), `speed_scale`, `dither`, `display_mode`, `bake_compress`, `bake_storage`.

`ResourceImporterGIFFrames` is the alternate Import As path. It decodes into a `SpriteFrames` animation named `default` for `AnimatedSprite2D` / `AnimationPlayer` workflows. The texture importer stays the default because the texture is the product we wanted on Sprite2D and materials.

`GIFTexture.from_sprite_frames` and `to_sprite_frames` exist so an animation you already authored as SpriteFrames can become a GIF and the reverse. `load_from_path` / `load_from_buffer` and `save_to_path` / `save_to_buffer` cover round trips without the Import dock.

## Caps and failure modes

Project Settings registered in `register_types.cpp`:

| Setting | Default | Range hint |
|---|---|---|
| `blazium/gif/max_canvas_pixels` | `16777216` | `65536`–`268435456` |
| `blazium/gif/max_frames` | `4096` | `1`–`65536` |
| `blazium/gif/capture_hotkey` | `0` | `0` = unbound |
| `blazium/gif/capture_source` | `0` (Viewport) | `0` Viewport, `1` Window |
| `blazium/gif/capture_output_dir` | `user://` | directory |

Over the canvas or frame cap, decode and import fail with `ERR_OUT_OF_MEMORY` and a message that names the setting. A long full-screen capture will hit one of those and stop. Keep clips short and stay near the recorder default of 12 fps (the practical 10–15 fps band for palette GIF).

`GIFRecorder.max_frames` defaults to `0`, which means “use `blazium/gif/max_frames`.” `max_size` defaults to `Vector2i(480, 270)` and downscales larger captures; `(0, 0)` disables scaling.

## Recorder and movie writer as the write side

`GIFRecorder` is the script-facing encoder for a viewport, the engine window, a display, or manually pushed `Image` frames. `MovieWriterGIF` is the engine movie-recorder target for the same format. Both share the palette encoder and the project caps. Capture works in the editor and in exported templates; the module is not tools-only.

`GIFTexture` itself is careful about threads: non-main-thread setup finishes through `call_deferred`, and several update paths check `Thread::is_main_thread()`. That is resource safety, not a claim that encode is a free background job. Encode still costs what a palette GIF costs.

## Encode knobs that belong on the texture

`encode_optimize` defaults to true so ordinary `save_to_path` / `save_to_buffer` calls can use transparency and frame differencing. Recorder captures force it false so each captured frame is a full opaque picture—capture fidelity over file size. `dither` defaults to true for encode and bake edges. `bake_compress` is off by default; turning it on trades quality and load time for smaller stored baked frames when `bake_storage` is Store.

`display_mode` chooses whether the GPU sees raw source patches (`DISPLAY_SOURCE`) or composited full-canvas frames (`DISPLAY_BAKED`). Disposal methods only make sense once you understand that GIF frames are often dirty rectangles on a canvas, not full replacement images. That is why the module bakes at all, and why the product is still a `Texture2D` with a playhead rather than a video decoder.

## What we validated

We validated import, playback, and capture in-house. That pass does not name a title that ships GIF capture as a feature. The module is there because the art pipeline needed a texture, not a video player. The public [gif_module_tests](https://github.com/blazium-games/gif_module_tests) suite still names the older `GIFAnimation` and `GIFSprite2D` API, so do not treat it as current coverage for this tree. Align scripts against the classes registered in your build’s `modules/gif` doc_classes and ClassDB; the texture-centric API above is what this engine tree documents.

## Links

- Module: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/gif
- Tests: https://github.com/blazium-games/gif_module_tests
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
