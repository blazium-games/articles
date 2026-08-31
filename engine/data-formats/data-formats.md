---
title: "ENV, INI, and CSV in Blazium"
description: "The same config record in .env, .ini, and .csv, and when to use each."
cover: "assets/cover.png"
slug: "data-formats"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

One record: a display name, an API URL, a feature flag. Three files. Pick the format that matches the job.

![.env, .ini, .csv](assets/data-formats.png)

## `.env` / `ENV`

Secrets and per-machine values, next to the executable. Not a security boundary. Anyone with the file can read it. Keep crash-reporter tokens in Project Settings if that is where the engine looks.

```env
GAME_NAME=Hangman
API_URL=https://api.example
FEATURE_FLAG=1
OBS_HOST=127.0.0.1
OBS_PORT=4455
```

```gdscript
var url := ENV.get_value("API_URL")
```

<!-- CAPTURE: assets/env-inspector.png | Editor | ENV singleton in use at runtime -->

## `.ini` / `DotIniFile`

Typed sections. Includes and macros if you use them. Godot `ConfigFile` still exists. DotINI is the extra type-checking path, not a replacement you must migrate to.

```ini
[game]
name=Hangman
flag=true

[net]
api_url=https://api.example
```

## `.csv` / `CSVTable`

Designer tables. Import dock plus runtime parse/write. 0.4.90 already had CSV import presets for translations. This is "any table", not only localization.

```csv
id,name,flag
1,Hangman,1
```

<!-- CAPTURE: assets/csv-import.png | Editor | Import dock for a CSV -->
<!-- CAPTURE: assets/cover.png | Editor | Three files open, same keys highlighted -->

## Decision

| Kind | Put it in |
|---|---|
| Secret, machine-local | `.env` |
| Structured settings | `.ini` or Project Settings |
| Bulk rows a designer edits | `.csv` |

Do not commit production secrets. `.env` belongs in `.gitignore`. Ship `.env.example`.
