---
title: "Crash reports in Blazium"
description: "The engine writes a dump. A sidecar asks you. Nothing leaves the machine until you confirm."
cover: "assets/cover.png"
slug: "crash-reporter"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Confirm-before-upload is the product. The engine writes files. A sidecar UI asks. Send is a decision, not a default.

![Where the sidecar sits in the stack](assets/ecosystem-map.png)

## What the engine writes

`{crash-dir}/{id}.dmp` plus `{id}.json`. Breakpad lives in `modules/crash_reporter` inside the engine. The sidecar repo does not contain Breakpad. It only presents and uploads those two files.

## The sidecar

Launch contract (the engine already resolved identity):

```text
crash_reporter --crash-dir <dir> --report-id <id> --endpoint <url> --app-id <id> --build-id <id> --contact-url <url> --privacy-url <url>
```

Buttons: Send, Discard, Refresh. Fields: what happened, include attachments, send anonymous. Privacy URL is on the dialog.

<!-- CAPTURE: assets/sidecar-blocked.png | Crash sidecar | Consent off, Send disabled or warning -->
<!-- CAPTURE: assets/sidecar-ready.png | Crash sidecar | What happened filled, anonymous on, Send enabled -->
<!-- CAPTURE: assets/sidecar-discard.gif | Crash sidecar | Kill editor, sidecar, Discard -->
<!-- CAPTURE: assets/sidecar-send.gif | Crash sidecar | Kill editor, sidecar, Send, confirmation -->
<!-- CAPTURE: assets/cover.png | Crash sidecar | Replace diagram cover with filled sidecar, 16:9 -->
<!-- CAPTURE: assets/privacy-crop.png | Website | Real privacy policy URL crop -->

## Editor

Official CI editors bake `editor_app_id=blazium-editor`. There is no engine `--app-id` flag. Point at a local sidecar with `--crash-reporter <path>` (relative paths resolve next to the editor executable).

## Exported games

Place `crash_reporter.exe` (Windows) or `crash_reporter` (Linux) next to the game. Project Settings:

| Key | Typical |
|---|---|
| `application/crash_reporter/enabled` | true |
| `application/crash_reporter/upload_mode` | Sidecar or Both |
| `application/crash_reporter/reporter_filename` | `crash_reporter` / `crash_reporter.exe` |
| `application/crash_reporter/reporter_path` | fallback, relative or absolute |
| `application/crash_reporter/endpoint` | ingest URL |
| `application/crash_reporter/reporter_sha256` | optional, lowercase hex |

<!-- CAPTURE: assets/project-settings-crash.png | Editor | application/crash_reporter inspector -->

## App ids

| id | Who |
|---|---|
| `blazium-editor` | Official CI editors |
| `blazium-hub` | Hub |
| `custom_blazium_engine` | Unofficial local editors |

Same ids as [opt-in analytics](../analytics-opt-in/analytics-opt-in.md).

## Where it goes

`https://crash.blazium.app/v1/reports`. Multipart dump + metadata JSON. Staff Discord commands are not this article.

Hub ships the sidecar next to itself. A Hub update can refresh that binary.
