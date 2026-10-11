---
title: "ENV, INI, and CSV in Blazium"
description: "DotENV, DotINI, and DotCSV are three modules. Godot's ConfigFile is still there."
cover: "assets/cover.png"
slug: "data-formats"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# ENV, INI, and CSV in Blazium

### Three files, three jobs, and ConfigFile stays

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

A display name, an API URL, and a table of levels do not belong in the same file. Godot's `ConfigFile` already stores INI-shaped variants, and we kept it. `modules/dotenv`, `modules/dotini`, and `modules/dotcsv` are what we added when `.env` files, typed INI, and designer-edited tables kept getting jammed into that one class.

All three build on `blazium-dev` with no SCons opt-in (`can_build` returns true). None of them registers the keys the engine itself reads. A script reads the file. Project Settings are where the engine looks. That split is deliberate: shipping a `.env` next to your game must not silently retarget crash upload or analytics, and a designer CSV must not become an accidental override for `application/config/name`.

![.env, .ini, and .csv](assets/data-formats.png)

## .env and ENV

`ENV` is an engine singleton. It loads `.env` files and can read them back as strings, bools, ints, floats, colors, and vectors. It is not a security boundary. Anyone with the file can read it.

The crash reporter does not read this file. A game's upload URL is `application/crash_reporter/endpoint`. Use `.env` for values your own scripts read.

`auto_config(dir, mode)` loads, in order, `.env`, `.env.local`, `.env.{mode}`, and `.env.{mode}.local` under `dir` (default `res://`). Mode defaults to `development` in the editor and `production` in an export when you leave the argument empty. `config(file)` / `load_env_file` load one file. OS environment wins when `get_prioritize_os_env` is on.

```gdscript
ENV.auto_config("res://")
var url := str(ENV.get_env("API_URL", ""))
var enabled := bool(ENV.get_env_bool("FEATURE_FLAG", false))
var color := ENV.get_env_color("ACCENT", Color.WHITE)
ENV.generate_example("res://.env.example")
ENV.push_to_os_env()
```

`get_env` returns the default when the key is missing. It does not raise. Typed helpers include `get_env_bool`, `get_env_int`, `get_env_float`, `get_env_array`, `get_env_dict`, `get_env_color`, `get_env_vector2`, `get_env_vector3`, and `get_env_vector4`. `require_envs` / `get_missing_envs` check a key list. `expand_string` replaces `${VAR}` markers. `bind_env` maps keys onto node properties. Signals: `file_loaded`, `cleared`, `refreshed`.

Ship `.env.example` from `generate_example` and gitignore the real file. The example analytics server tells you to copy `.env.example` and not commit `.env`. That is the reference server's config, not a claim about how Hangman stores settings.

## .ini and DotIniFile

`DotIniFile` is a `RefCounted` INI with sections, includes, macros, and type constraints. The class reference calls it a more capable alternative to `ConfigFile`, not a replacement you must migrate to.

```gdscript
var ini := DotIniFile.new()
ini.load("res://game.ini")
var game_name := str(ini.get_value("game", "name", ""))
var flag := ini.get_value_bool("game", "flag", false)
ini.add_type_constraint("game", "flag", TYPE_BOOL)
ini.add_macro("BUILD", "release")
var as_cf := ini.to_config_file()
var round_trip := DotIniFile.new()
round_trip.from_config_file(as_cf)
```

`load` replaces the current document unless you pass append. `get_value` interpolates by default; `get_value_raw` skips that. Typed getters mirror ENV (`get_value_int`, `get_value_float`, `get_value_bool`, `get_value_string`, `get_value_array`). `from_config_file` and `from_dictionary` exist when you already have a `ConfigFile` or a `Dictionary`. `get_section_as_dict` / `to_dictionary` are the reverse. Encrypted load/save helpers (`load_encrypted`, `save_encrypted_pass`) are on the class when you need them. Includes and macros are optional. A short settings file does not need them.

Godot's [ConfigFile](https://docs.godotengine.org/en/stable/classes/class_configfile.html) remains the right choice when you want the stock API and nothing else.

## .csv and CSVTable

Release 0.4.90 already imported CSV for translations. `modules/dotcsv` is any other table. `CSV` is a resource (`load_file`, `load_string`, `save_to_string`). `CSVTable` is the query side. `ResourceImporterCSV` is the import dock. `CSVReader` and `CSVWriter` stream. `CSVAsyncTask` is the background path. Dialect sniffing is `CSVDialect.sniff`. Headers, delimiters, and true/false token lists are importer options, not Project Settings.

```gdscript
var table := CSVTable.from_file("res://data/levels.csv")
for row in table.where_equals("name", "Hangman").get_rows():
    print(row)

var subset := table \
    .select_columns(PackedStringArray(["name", "difficulty"])) \
    .sort_by("difficulty") \
    .limit(10)
print(subset.row_count())
```

`from_file` and `where_equals` return a `CSVTable`, not an array. Also on the class: `where_in`, `select_columns`, `drop_columns`, `sort_by`, `sort_by_columns`, `group_by`, `inner_join`, `left_join`, `limit`, `distinct`, `filter_rows`, `map_rows`, `build_index`, and `apply_model` / `validate_model` with `CSVRowModel`. DSV variants (`DSVReader`, `DSVWriter`, `DSVImporter`, `DSVExporter`) cover delimiter-separated files beyond comma.

## Which file for which job

| Kind | Put it in |
|---|---|
| Secret or machine-local string a script reads | `.env` via `ENV` |
| Structured settings with sections | `DotIniFile`, or Project Settings when the engine must see the key |
| Bulk rows a designer edits | `.csv` via `CSVTable` or the import dock |
| Crash upload URL, app id, analytics endpoint | `application/crash_reporter/*` / `application/analytics/*`, not `.env` |
| Stock Godot INI without macros | `ConfigFile` |

## Edge cases and limits

- `ENV` is not encryption. Do not put private keys in a shipped `.env` and expect safety.
- `auto_config` only loads files that exist; missing layers are skipped, not errors.
- Later `auto_config` layers override earlier ones when the same key appears (`.env.local` wins over `.env`, mode-specific files win after that).
- `DotIniFile.load(..., append=false)` replaces the in-memory document; pass append when merging includes intentionally.
- `CSVTable` query methods return new tables; chain them, then call `get_rows()`.
- Boolean CSV tokens are importer/dialect configuration. Do not assume `"true"`/`"false"` if the spreadsheet exported `YES`/`NO` unless you set the whitelist.
- None of these modules write engine Project Settings. Setting `application/crash_reporter/endpoint` in `.env` does nothing unless your script copies it across.
- Module tests for dotenv: https://github.com/blazium-games/dotenv_module_tests

`ENV` also exposes `export_json`, `save`, `get_envs_matching`, `get_env_group`, and `set_bool_whitelist` when you need stricter parsing than the defaults. `DotIniFile` can `merge_with` another document and toggle `autosave` / `read_only` for tool UIs. Prefer those APIs over hand-rolled parsers once the file is in-tree.

## Streaming and import path (CSV)

For files too large to hold as one `CSVTable`, use `CSVReader` / `CSVWriter` (and the DSV twins) to stream rows. `CSVAsyncTask` moves heavy parse/export off the frame that opened the dialog. `ResourceImporterCSV` is what the FileSystem dock uses when you set import options for headers, delimiter, and boolean token lists — those options live on the importer, not under `application/*` Project Settings.

`CSVDialect.sniff` is the autodetection helper when a designer exports from a spreadsheet with an unexpected delimiter. Prefer an explicit dialect in shipping code once you know the file shape.

## Practical split

Keep `.env` for machine-local overrides and CI secrets your scripts inject. Keep designer balance sheets in CSV so a spreadsheet round-trip stays honest. Keep sectioned game options in `DotIniFile` or Project Settings depending on whether the engine core must read them. Leave crash and analytics identity on their Project Settings keys so the modules that own those pipelines resolve them the same way every time. When in doubt, one file format per concern beats a clever mega-`ConfigFile`.

```gdscript
# Pattern: script-owned config, engine-owned telemetry keys stay in Project Settings.
ENV.auto_config("res://")
var api := str(ENV.get_env("API_URL", "https://example.invalid"))

var ini := DotIniFile.new()
ini.load("res://game.ini")
var title := str(ini.get_value("game", "name", "Untitled"))

var levels := CSVTable.from_file("res://data/levels.csv")
print(levels.where_equals("unlocked", "true").row_count())
```

These three modules ship in editor and export builds alike. They do not replace translations CSV import, and they do not register engine singletons beyond `ENV`. If a key must affect the editor or export pipeline itself, put it in Project Settings — not in a designer spreadsheet.

## Links

- dotenv: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/dotenv
- dotini: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/dotini
- dotcsv: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/dotcsv
- Tests: https://github.com/blazium-games/dotenv_module_tests
- Godot ConfigFile: https://docs.godotengine.org/en/stable/classes/class_configfile.html
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
