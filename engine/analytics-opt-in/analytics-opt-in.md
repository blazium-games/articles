---
title: "Opt-in analytics"
description: "Editor demographics and optional game events. Off until you consent. Same app and build ids as crash reports."
cover: "assets/cover.png"
slug: "analytics-opt-in"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Nothing is sent until consent is on. Anonymous mode (the default) omits `device_uid`. Official editor ingest URL is baked at compile time. An empty baked URL means the editor does not collect.

![Crash and analytics share the stack](assets/ecosystem-map.png)

## Consent

Priority, first match wins:

1. CLI `--analytics=`
2. Env `BLAZIUM_ANALYTICS_CONSENT`
3. Editor Settings, or `Analytics.set_consent`

<!-- CAPTURE: assets/analytics-settings.png | Editor | Editor Settings analytics consent toggle -->
<!-- CAPTURE: assets/cover.png | Editor | Same toggle, 16:9 -->

## What is sent

JSON events. Every event carries `app_id`, `build_id`, channel. Headers `X-App-Id` / `X-Build-Id` on flush. Same ids as [crash reports](../crash-reporter/crash-reporter.md): `blazium-editor`, `blazium-hub`, `custom_blazium_engine`.

Editor identity is SCons-baked (`editor_app_id`, `editor_build_id`, `editor_analytics_endpoint`). There is no engine CLI override for those fields.

## Games

Templates compiled with `analytics=yes` expose `Analytics.track` plus session start/end. If the template did not bake an endpoint, Project Settings supply it. An empty template URL means "use Project Settings", not "disable".

```gdscript
Analytics.track("level_clear", {"level": 3})
```

## Leave it off

Do not pass `--analytics=`. Leave Editor Settings off. Ship templates without `analytics=yes` if you do not want a game SDK at all. Consent is not implied by installing Hub.
