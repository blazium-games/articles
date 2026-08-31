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

Import a gif onto a sprite. Record the editor or a game viewport back out to a gif. This module is how Hub News gifs can be captured from inside Blazium.

## Import

Drop a `.gif` into the project. `GIFTexture` plays it. Frame importer exists for sprite sheets (`ResourceImporterGIFFrames`).

<!-- CAPTURE: assets/gif-playback.gif | Editor | GIFTexture on a Sprite2D, animating -->
<!-- CAPTURE: assets/cover.png | Editor | Sprite playing a gif, output file in the filesystem dock -->

## Record

```gdscript
var err := GIFRecorder.record_viewport($Viewport, "user://clip.gif", 4.0, 12)
if err != OK:
    push_error(err)
```

`GIFRecorder` also has `start_viewport`, `start_window`, `start_screen`, `add_frame`, `stop`, `save`. Works in the editor and in exported templates.

<!-- CAPTURE: assets/gif-record.gif | Editor | Recorder running, file appears in the filesystem -->

## Movie writer

GIF is a movie-writer target (`MovieWriter`). Use it when you want a clip of a running scene without the recorder API.

Record other Hub articles' UI loops at 10–15 fps, under eight seconds, then keep the mp4 master beside the gif.
