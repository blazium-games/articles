---
title: "Opt-in analytics"
description: "Editor demographics and optional game events. Nothing is sent until consent is given."
cover: "assets/cover.png"
slug: "analytics-opt-in"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Opt-in analytics

### A counter that stays on disk until someone opts in

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

Crash reports tell us the engine died. They do not tell us whether anyone finished a level, or whether an export button is used. `modules/analytics` is that counter. We used it while building Hangman and Demon Lord: Clicker. Hangman shipped on Steam, Discord, Google Play, and the Apple App Store. Demon Lord: Clicker was built in part to validate the newer tools, modules, and the 2D side.

Nothing is sent until consent is given. An empty baked editor endpoint means the editor does not collect any data. Analytics events are not what engine crash patches are based on. Crash reports are.

![Crash and analytics share a host, not a switch](assets/ecosystem-map.png)

![Consent order](assets/analytics-consent.png)

## What is compiled

The module is on `blazium-dev`. Export templates include the sender when SCons gets `analytics=yes`. Editor builds include it when `editor_analytics=yes`. Without those flags the `Analytics` singleton is still registered and nothing is stored.

Official Hub CI bakes `editor_app_id=blazium-hub` and `editor_analytics_endpoint=https://crash.blazium.app/v1/events`. A local editor build keeps `editor_app_id=custom_blazium_engine` and an empty endpoint. There is no CLI flag that fills the baked app id, build id, or endpoint in later. There is no consent dialog in the editor tree. Consent is the flag, the environment variable, `set_consent`, or Editor Settings.

The reference ingest is [example_analytics_server](https://github.com/blazium-games/example_analytics_server). Its README says it is not a hosted product. Hub's events URL is the bake above, not that example server.

## Consent

First match wins, in `modules/analytics/analytics.cpp`:

1. `--analytics=accepted` or `--analytics=declined`
2. `BLAZIUM_ANALYTICS_CONSENT`
3. `Analytics.set_consent`
4. Editor Settings `blazium/analytics/consent` (`unset`, `accepted`, or `declined`, default `unset`)

Anonymous mode follows the same shape: `--analytics-mode=anonymous|identified`, then `BLAZIUM_ANALYTICS_ANONYMOUS`, then `blazium/analytics/anonymous`. The default is anonymous. `identify()` and `set_user_properties()` do nothing while anonymous mode is on. Identified mode sends `OS.get_unique_id` as `device_uid`.

`application/analytics/require_user_consent` defaults to **false**. That is the opposite of the crash reporter, whose `require_user_consent` defaults to true. A game that sets `enabled` and leaves `require_user_consent` false will queue without a separate consent call. Turn the flag on if the game must wait for `set_consent(true)`.

## What is sent

One JSON object per event. The flush body is `{"events":[...]}`, posted to the endpoint, with `/v1/events` appended if you did not include it. Headers are `X-App-Id` and `X-Build-Id`.

Every queued row carries `app_id`, `build_id`, `engine_version`, `session_id`, `anonymous`, `event`, `timestamp`, and `properties`. Identity resolution matches crash reports: a non-empty bake wins, then project settings, then `custom_blazium_engine`.

Built-in editor events are `editor_launched` and `editor_session_ended`. Games get `session_start` and `session_end` when the template was built with analytics, plus whatever you pass to `track`.

## Games

An empty template endpoint does not remove the module. It means use Project Settings. `flush()` fails until that setting has a URL, and the queue stays on disk.

```gdscript
Analytics.set_consent(true)
Analytics.track("level_complete", {"level": 3})
Analytics.flush()
```

`flush_succeeded(count)` and `flush_failed(message)` are the signals. `flush()` is manual. Quitting queues `session_end` and does not POST by itself.

| Key | Default |
|---|---|
| `application/analytics/enabled` | `false` |
| `application/analytics/require_user_consent` | `false` |
| `application/analytics/anonymous` | `true` |
| `application/analytics/endpoint` | template bake, or empty |
| `application/analytics/build_channel` | `release` |
| `application/analytics/timeout_sec` | `15` |
| `application/analytics/verify_tls` | `true` |

`BLAZIUM_ANALYTICS_QUEUE_DIR` overrides the queue directory.

Do not pass `--analytics=accepted` if you want the editor silent. Leave `blazium/analytics/consent` at `unset` or `declined`. Ship templates without `analytics=yes` if the game should not include the sender. Installing Hub does not imply consent. Hub's binary is a separate build from the editors you install off the CDN.

Crash reports use the same app id and build id, on `/v1/reports`.

## Links

- Module: https://github.com/blazium-games/blazium/tree/blazium-dev/modules/analytics
- Example server: https://github.com/blazium-games/example_analytics_server
- Module tests: https://github.com/blazium-games/analytics_module_tests
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
