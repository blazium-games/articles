---
title: "Opt-in analytics"
description: "Consent-gated editor demographics and configurable game-event analytics, with an on-disk queue and explicit flush."
cover: "assets/cover.png"
slug: "analytics-opt-in"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Opt-in analytics

### An editor opt-in and a game consent gate you configure explicitly

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

Crash reports tell us the engine died. They do not tell us whether anyone finished a level, or whether an export button is used. `modules/analytics` is that counter. We used it while building Hangman and Demon Lord: Clicker. Hangman shipped on Steam, Discord, Google Play, and the Apple App Store. Demon Lord: Clicker was built in part to validate the newer tools, modules, and the 2D side.

Official editor analytics does not queue until consent is accepted. Exported games are configurable: `application/analytics/require_user_consent` defaults to `false`, so a developer who enables analytics must turn that setting on when the game should wait for `set_consent(true)`. An empty baked editor endpoint means the editor does not collect any data. Analytics events are not what engine crash patches are based on. Crash reports are.

![Crash and analytics share a host, not a switch](assets/ecosystem-map.png)

![Consent order](assets/analytics-consent.png)

## What is compiled

The module is on `blazium-dev`. Export templates include the sender when SCons gets `analytics=yes`. Editor builds include the send path when `editor_analytics=yes` (that flag sets `ANALYTICS_ENABLED`). The singleton still registers without those flags; `_can_queue()` returns false and nothing is stored.

Official Hub CI bakes `editor_app_id=blazium-hub` and `editor_analytics_endpoint=https://crash.blazium.app/v1/events`. A local editor build keeps `editor_app_id=custom_blazium_engine` and an empty endpoint. There is no CLI flag that fills the baked app id, build id, or endpoint in later. Editor Settings show those three fields read-only. There is no consent dialog in the editor tree. Consent is the flag, the environment variable, `set_consent`, or Editor Settings.

The reference ingest is [example_analytics_server](https://github.com/blazium-games/example_analytics_server). Its README says it is not a hosted product. Hub's events URL is the bake above, not that example server. Module-side checks live in [analytics_module_tests](https://github.com/blazium-games/analytics_module_tests): headless `run_tests.gd` asserts the singleton, JSONL queue rows, game-context properties, and that anonymous events omit `device_uid`.

## Consent

First match wins, in `modules/analytics/analytics.cpp`:

1. `--analytics=accepted` or `--analytics=declined`
2. `BLAZIUM_ANALYTICS_CONSENT`
3. `Analytics.set_consent` (process override; editor builds also persist to Editor Settings)
4. Editor Settings `blazium/analytics/consent` (`unset`, `accepted`, or `declined`, default `unset`)

Anonymous mode follows the same shape: `--analytics-mode=anonymous|identified`, then `BLAZIUM_ANALYTICS_ANONYMOUS`, then `set_anonymous`, then `blazium/analytics/anonymous` / `application/analytics/anonymous`. The default is anonymous. `identify()` and `set_user_properties()` do nothing while anonymous mode is on. Identified mode sends `OS.get_unique_id` as `device_uid`. Already-queued events keep the anonymity flag they were created with.

`application/analytics/require_user_consent` defaults to **false**. That is the opposite of the crash reporter, whose `require_user_consent` defaults to true. A game that sets `enabled` and leaves `require_user_consent` false will queue without a separate consent call. Turn the flag on if the game must wait for `set_consent(true)`.

Editor context is stricter than games: even with `editor_analytics=yes`, an empty baked endpoint disables collection entirely (no queue growth), and consent must be `accepted` before anything is queued.

## What is sent

One JSON object per event. The flush body is `{"events":[...]}`, posted to the endpoint, with `/v1/events` appended if you did not include it. Headers are `X-App-Id` and `X-Build-Id`. Timeout defaults to 15 seconds. TLS verification defaults to on.

Every queued row carries `app_id`, `build_id`, `engine_version`, `session_id`, `anonymous`, `event`, `timestamp`, and `properties`. Identity resolution matches crash reports: a non-empty bake wins, then project settings, then `custom_blazium_engine`. Call `Analytics.get_resolved_config()` when you need the values the process actually used.

Built-in editor events are `editor_launched` and `editor_session_ended`. The export plugin also tracks `editor_export_started` and `editor_export_finished`. Games get `session_start` and `session_end` when the template was built with analytics, plus whatever you pass to `track`.

The example server accepts one object, an array, or `{ "events": [...] }` on `POST /v1/events`, optional `X-API-Key`, max body 8 MiB, and stores `analytics_store/{app_id}/{build_id}.jsonl`.

```text
curl -sS http://127.0.0.1:8091/health
curl -sS -H "Content-Type: application/json" \
  -d '{"app_id":"my-game","event":"session_start","anonymous":true}' \
  http://127.0.0.1:8091/v1/events
curl -sS "http://127.0.0.1:8091/v1/events?app_id=my-game"
```

## Games

An empty template endpoint does not remove the module. It means use Project Settings. `flush()` fails until that setting has a URL, and the queue stays on disk. `BLAZIUM_ANALYTICS_QUEUE_DIR` overrides the queue directory.

```gdscript
Analytics.set_consent(true)
Analytics.set_anonymous(true)
Analytics.track("level_complete", {"level": 3, "seconds": 42})
Analytics.flush_succeeded.connect(func(count): print("sent ", count))
Analytics.flush_failed.connect(func(msg): push_warning(msg))
Analytics.flush()
print(Analytics.get_queue_size())
print(Analytics.get_resolved_config())
```

`flush_succeeded(count)` and `flush_failed(message)` are the signals. `flush()` is manual. Quitting queues `session_end` and does not POST by itself. `is_available()` is true when the module is compiled in; `is_enabled()` is true only when queueing is actually allowed (feature flag plus consent, and a non-empty editor endpoint in the editor).

[analytics_module_tests](https://github.com/blazium-games/analytics_module_tests) defaults to `enabled=true`, `app_id=analytics-module-test`, `build_id=dev-local`, empty endpoint (queue only). Set `application/analytics/endpoint` or `ANALYTICS_ENDPOINT` for a live POST against the example server. That project is a game consumer: it does not exercise editor-demographic events.

## SDK surface

| Method | Role |
|---|---|
| `track(event, properties={})` | Queue one event |
| `flush()` | POST the queue |
| `set_consent(accepted)` / `get_consent()` | `unset` / `accepted` / `declined` |
| `set_anonymous` / `is_anonymous` / `get_device_uid` | Identity mode |
| `identify` / `set_user_properties` | No-op while anonymous |
| `get_app_id` / `get_build_id` / `get_app_version` / `get_build_channel` | Identity |
| `get_queue_size` / `get_resolved_config` | Introspection |
| `is_available` / `is_enabled` | Compile vs queue gate |

Constants: `CONSENT_UNSET`, `CONSENT_ACCEPTED`, `CONSENT_DECLINED`.

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

| Editor Setting | Default | Notes |
|---|---|---|
| `blazium/analytics/consent` | `unset` | `unset` / `accepted` / `declined` |
| `blazium/analytics/anonymous` | `true` | |
| `blazium/analytics/endpoint` | bake | read-only |
| `blazium/analytics/app_id` | bake or `custom_blazium_engine` | read-only |
| `blazium/analytics/build_id` | bake or git hash | read-only |

## Edge cases

- Passing `--analytics=accepted` on a local editor with an empty bake still cannot collect: empty editor endpoint wins for queueing.
- `require_user_consent=false` on a game means `enabled=true` is enough to queue. That is intentional and easy to misread if you assume crash-reporter defaults.
- Identified mode plus `identify("player-1")` still attaches `device_uid` from `OS.get_unique_id`; anonymous mode drops both.
- `analytics=yes` on an editor SCons line is ignored; use `editor_analytics=yes`. The reverse warning fires on templates.
- Installing Hub does not imply consent. Hub's binary is a separate build from the editors you install off the CDN.
- Ship templates without `analytics=yes` if the game should not include the sender at all.
- The example server rejects an empty `app_id`. Max body is 8 MiB. Optional `X-API-Key` is server-side, not an engine Project Setting.

## Keeping the editor silent

Do not pass `--analytics=accepted` if you want the editor silent. Leave `blazium/analytics/consent` at `unset` or `declined`. A custom engine bake with an empty `editor_analytics_endpoint` never queues, even if someone flips consent later in Editor Settings. Official Hub editors bake a real URL; consent is the gate there.

Crash reports use the same app id and build id, on `/v1/reports`. That shared identity does not share consent, queues, or upload UI. If you are wiring both modules in one game, configure each endpoint and each consent flag explicitly — copying only `app_id` is not enough.

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
