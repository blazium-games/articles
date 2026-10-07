---
title: "Crash Reporter & Analytics"
description: "Native crash capture and an opt-in analytics layer for the editor and for shipped games."
cover: "assets/cover.png"
slug: "crash-reporter-and-analytics"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---

# Crash Reporting & Analytics in Blazium

Blazium ships two modules that answer different questions. The **Crash Reporter** tells you why a process died. The **Analytics** system tells you what people ran, and only after they agree. Both can share an app id and a build id. They can post to the same host or to two hosts. Neither one is on unless the build and the settings say so.

We added them because Hub, the editor, and our own tools needed the same story a game needs: a dump on disk, a person in the loop before upload, and usage numbers that stay off until consent is given. The engine stays MIT. These modules are part of that tree (`modules/crash_reporter`, `modules/analytics`).

They are available in the editor and in export templates when the matching SCons flags are set: `editor_crash_reporter=yes` / `crash_reporter=yes`, and `editor_analytics=yes` / `analytics=yes`. Crash reporting compiles on Windows and Linux/BSD only.

## Crash Reporter

The `CrashReporter` singleton writes a Breakpad minidump and a JSON sidecar, then either keeps them, uploads them, hands them to a reporter program, or does both.

### How it works

On a crash, the engine writes `{id}.dmp` and `{id}.json` into the crash directory. The next launch can see pending reports (`has_pending_reports`, `get_pending_reports`).

`upload_mode` is an enum:

| Value | Name | What happens |
|---|---|---|
| 0 | Disabled | Files stay on disk |
| 1 | In-engine | The game POSTs the dump |
| 2 | Sidecar | A separate UI asks, then uploads |
| 3 | Both | In-engine and sidecar |

Editor builds do not HTTP-upload. If you pass `--crash-reporter <path>`, the mode is sidecar. Otherwise the editor writes dumps and stops. Export templates are the builds that can POST.

Games connect `upload_started`, `upload_progress`, `upload_succeeded`, and `upload_failed` if they want a progress UI. `application/crash_reporter/require_user_consent` defaults to true.

Official Hub builds bake `editor_app_id=blazium-hub` and `https://crash.blazium.app/v1/reports`. A local engine build defaults to `custom_blazium_engine` and an empty endpoint. Empty endpoint still writes dumps. It does not upload.

The field-by-field settings and the sidecar argv are in [Crash reports in Blazium](../crash-reporter/crash-reporter.md).

## Analytics system

The `Analytics` singleton is a consent-gated queue. Events are JSON objects on disk (`{"events":[...]}` on flush) and are posted with the same `X-App-Id` and `X-Build-Id` headers crash reports use.

By default nothing is uploaded. Consent has to be given. Anonymous mode is the default, so `device_uid` is omitted unless the user turns identification on. `identify()` and `set_user_properties()` no-op while anonymous mode is on.

Editor builds compiled with `editor_analytics=yes` record `editor_launched`, `editor_session_ended`, and export start/finish after consent is given. If the baked `editor_analytics_endpoint` is empty, the editor does not collect any data. There is no CLI flag that fills that URL in later.

Export templates compiled with `analytics=yes` expose `Analytics.track` for the game. `application/analytics/enabled` defaults to false. If `require_user_consent` is true, consent still has to be `accepted` before a row is queued.

```gdscript
Analytics.set_consent(true)
Analytics.track("level_complete", {"level": 3})
Analytics.flush()
```

`flush()` is explicit. Quitting the process queues `session_end` and does not POST on its own.

Consent order, for both editor and game: `--analytics=accepted|declined`, then `BLAZIUM_ANALYTICS_CONSENT`, then `Analytics.set_consent`, then `blazium/analytics/consent`.

The settings table is in [Opt-in analytics](../analytics-opt-in/analytics-opt-in.md).

## Shared identity and privacy

`AppIdentity` resolves one app id and one build id for both modules. A non-empty SCons bake wins. Then project keys (`application/crash_reporter/*`, then `application/analytics/*`). Then `custom_blazium_engine` and the git hash.

`CrashReporter.get_resolved_config()` and `Analytics.get_resolved_config()` return that resolved set. Useful when a settings screen should show what will actually be sent.

Analytics is strictly opt-in. Crash upload can require consent too, and on templates it does by default. Sidecar reporters can show the privacy-policy and contact URLs the engine passed on the command line. Traffic is an HTTP POST to the endpoint you configured. Nothing goes to a third-party collector unless that endpoint is one.

## Tests

Both modules are in current `blazium-dev`. Example projects:

- [crash_reporter_module_tests](https://github.com/blazium-games/crash_reporter_module_tests)
- [analytics_module_tests](https://github.com/blazium-games/analytics_module_tests)
- [example_crash_reporter_server](https://github.com/blazium-games/example_crash_reporter_server)
- [example_analytics_server](https://github.com/blazium-games/example_analytics_server)

The sidecar UI screenshots are not in this draft. The contract above is the engine side: argv, modes, and the consent gate.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
