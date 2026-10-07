---
title: "Opt-in analytics"
description: "Editor demographics and optional game events. Off until consent is given. Same app and build ids as crash reports."
cover: "assets/cover.png"
slug: "analytics-opt-in"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Nothing is sent until consent is given. Anonymous mode (the default) omits `device_uid`. The official editor ingest URL is baked at compile time. An empty baked URL means the editor does not collect any data.

![Crash and analytics share the stack](assets/ecosystem-map.png)

The module is `modules/analytics`. The engine singleton is `Analytics`. Export templates include it only when SCons is passed `analytics=yes`. Editor builds include the sending path only when `editor_analytics=yes`. Without those flags, `Analytics` is still present, but `_can_queue()` stays false and nothing is stored.

## Consent

Priority, first match wins. This is the order in `Analytics` (`modules/analytics/analytics.cpp`):

1. CLI `--analytics=accepted` or `--analytics=declined`
2. Env `BLAZIUM_ANALYTICS_CONSENT`
3. A call to `Analytics.set_consent`
4. Editor Settings key `blazium/analytics/consent` (`unset`, `accepted`, or `declined`, default `unset`)

Anonymous mode follows the same idea: `--analytics-mode=anonymous|identified`, then `BLAZIUM_ANALYTICS_ANONYMOUS`, then `blazium/analytics/anonymous` (default `true`). `identify()` and `set_user_properties()` do nothing while anonymous mode is on.

There is no separate consent dialog in the editor tree. The toggle is the Editor Settings key above.

## What is sent

An event JSON object for every event. The flush body is `{"events":[...]}`, posted to the endpoint with `/v1/events` appended if you did not include it. Headers on that POST are `X-App-Id` and `X-Build-Id`.

Every queued row carries `app_id`, `build_id`, `engine_version`, `session_id`, `anonymous`, `event`, `timestamp`, and `properties`. Same identity resolution as [crash reports](../crash-reporter/crash-reporter.md): a non-empty bake wins, then project settings, then the fallback `custom_blazium_engine`.

Official Hub CI passes `editor_app_id=blazium-hub` and `editor_analytics_endpoint=https://crash.blazium.app/v1/events` (`blazium-hub/ci/hub_scons.env`). A local editor build keeps the SCons default `editor_app_id=custom_blazium_engine` and an empty `editor_analytics_endpoint`, which means the editor does not collect any data. There is no engine CLI flag that overrides the baked editor app id, build id, or endpoint.

Built-in editor events are `editor_launched`, `editor_session_ended`, `editor_export_started`, and `editor_export_finished`. Games get `session_start` and `session_end` when the template was built with analytics.

`Analytics.flush()` is manual. Shutdown queues `session_end` and does not POST by itself. An empty endpoint makes flush fail and leaves the queue on disk (`BLAZIUM_ANALYTICS_QUEUE_DIR` overrides the queue directory).

## Games

Templates compiled with `analytics=yes` expose `Analytics.track` plus session start and end. Project Settings (defaults from `analytics_project_settings.cpp`):

| Key | Default |
|---|---|
| `application/analytics/enabled` | `false` |
| `application/analytics/require_user_consent` | `false` |
| `application/analytics/anonymous` | `true` |
| `application/analytics/endpoint` | template bake, or empty |
| `application/analytics/app_id` | template bake, or empty |
| `application/analytics/build_id` | template bake, or empty |
| `application/analytics/build_channel` | `release` |
| `application/analytics/timeout_sec` | `15` |
| `application/analytics/verify_tls` | `true` |

A game queues only when `application/analytics/enabled` is true and, if `require_user_consent` is true, consent is `accepted`. An empty template endpoint does not disable the module. It means "use Project Settings". Flush still fails until that setting has a URL.

```gdscript
Analytics.set_consent(true)
Analytics.track("level_complete", {"level": 3})
Analytics.flush()
```

`flush_succeeded(count)` and `flush_failed(message)` are the signals.

## Leave it off

Do not pass `--analytics=accepted`. Leave `blazium/analytics/consent` at `unset` or `declined`. Ship templates without `analytics=yes` if you do not want the game SDK at all. Installing Hub does not imply consent. Hub's own editor is a separate binary baked with `blazium-hub` and its own endpoint.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
