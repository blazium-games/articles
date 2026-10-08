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

## Why we built it

The engine commits that add the modules are "Add opt-in CrashReporter with Breakpad minidumps" and "Add opt-in Analytics module with identity, consent, and HTTP queue." A later commit identifies both by one app id and one build id, and another bakes the editor app id, build id, and analytics URL so they cannot be changed at runtime. The sidecar README says the UI is for first-party utilities: the engine, Hub, and other internal tools. It does not contain Breakpad. The engine writes the files. The sidecar presents them and uploads after confirm.

## What Blazium Games uses it for

Hub CI (`blazium-hub/ci/hub_scons.env`) bakes `editor_app_id=blazium-hub`, reports at `https://crash.blazium.app/v1/reports`, and events at `https://crash.blazium.app/v1/events`. That is the official Hub binary's configuration. The example ingest servers are marked "Not a hosted product." They are references. They are not the Hub endpoint.

<!-- QUESTION FOR BIOBLAZE: Does anyone read `crash.blazium.app` reports or events for Hub, the editor, or a shipped game? The bake and the sidecar README show the plumbing. They do not say the data is used for support, and they do not name Demon Lord: Clicker. -->

## What other projects get

An export template built with the matching SCons flag can write the same dump pair, and can queue events after consent. `require_user_consent` on crash upload defaults to true. Analytics ships nothing until consent is given. Games set their own endpoint. They do not inherit Hub's URL unless they bake or configure it.

Those are two modules, `modules/crash_reporter` and `modules/analytics`, on `blazium-dev`. They can share an app id and a build id. They do not share a switch.

The field lists are in [Crash reports in Blazium](../crash-reporter/crash-reporter.md) and [Opt-in analytics](../analytics-opt-in/analytics-opt-in.md). This page is why they are split, and what a build actually does today.

## Why a dump is not a metric

A crash file is evidence. An analytics event is a counter. Mixing them means a crash upload that also starts a session log, or a metrics SDK that tries to explain a segfault. The crash module writes `{id}.dmp` and `{id}.json`, then either leaves them, hands them to a sidecar, or (in an export template) POSTs them. The analytics module queues JSON events and POSTs `{"events":[...]}` only after consent is given and `flush()` runs. Shutdown queues `session_end`. It does not POST by itself.

`AppIdentity` resolves one app id and one build id for both. A non-empty SCons bake wins, then project keys, then `custom_blazium_engine` and the git hash. `CrashReporter.get_resolved_config()` and `Analytics.get_resolved_config()` return that set. A settings screen can show it. The headers on an analytics POST are `X-App-Id` and `X-Build-Id`.

## What official builds do

Hub CI (`blazium-hub/ci/hub_scons.env`) bakes `editor_app_id=blazium-hub`, crash reports at `https://crash.blazium.app/v1/reports`, and analytics at `https://crash.blazium.app/v1/events`. Consent still has to be given before analytics rows leave the machine. Crash upload on a template waits on `require_user_consent`, which defaults to true. The sidecar UI is Send, Discard, or Refresh. The privacy URL is an argument so the dialog can show where the bytes would go.

A local engine build does not inherit that bake. `editor_app_id` defaults to `custom_blazium_engine`. An empty `editor_analytics_endpoint` means the editor does not collect any data. An empty crash endpoint still writes dumps. It does not upload. There is no CLI flag that fills those baked URLs in later.

Editor builds never HTTP-upload a dump. `is_http_upload_available()` is false in the editor. `--crash-reporter <path>` selects the sidecar. Otherwise the editor writes files and stops.

## What is not in the tree

Crash reporting compiles on Windows and Linux/BSD only (`config.py`). macOS, web, Android, and iOS do not build the module. Breakpad is the in-process client. The module does not ship `crash_generation_server`. The sidecar repo, [blazium_crash_reporter](https://github.com/blazium-games/blazium_crash_reporter), has no Breakpad. It shows the two files and uploads after confirm.

There is no analytics consent dialog in the editor. The control is Editor Settings `blazium/analytics/consent` (`unset`, `accepted`, `declined`), or `--analytics=accepted|declined`, or `BLAZIUM_ANALYTICS_CONSENT`, or `Analytics.set_consent`. Anonymous mode is the default, so `device_uid` is omitted. `identify()` and `set_user_properties()` do nothing while that mode is on.

Sidecar screenshots are not in this draft.

## Where to read the contract

Example servers and module tests:

- [example_crash_reporter_server](https://github.com/blazium-games/example_crash_reporter_server)
- [example_analytics_server](https://github.com/blazium-games/example_analytics_server)
- [crash_reporter_module_tests](https://github.com/blazium-games/crash_reporter_module_tests)
- [analytics_module_tests](https://github.com/blazium-games/analytics_module_tests)

Engine docs: [docs.blazium.app](https://docs.blazium.app). The engine repo is [blazium](https://github.com/blazium-games/blazium) on `blazium-dev`.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
