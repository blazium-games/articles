---
title: "Crash Reporter & Analytics"
description: >-
    Reliable native crash capture, and a flexible, privacy-respecting analytics layer
    that works for both the editor and shipped games.
cover: "assets/cover.png"
slug: "crash-reporter-and-analytics"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---
# Crash Reporting & Analytics in Blazium

Blazium Engine now includes two complementary modules that give developers clear insight into
stability and usage: a **Crash Reporter** and an **Analytics** system.
Both share the same identity (App ID and Build ID), respect user choice and privacy,
and can send data to the same or separate endpoints.

These modules are available in the editor and in export templates, if compiled with the corresponding flags.
The Blazium Games team also uses them across our own tools, including the engine editor, Hub, and other
utilities, so we can improve the software while always giving users full control.

## Crash Reporter

The **CrashReporter** singleton detects native crashes, writes Breakpad minidumps, stores rich metadata,
and optionally uploads reports or launches a sidecar reporter UI.

### How it works

When the engine is built with crash reporting enabled, a crash automatically creates a dump file along
with useful metadata and stores them in a dedicated folder.
The next time the application launches, it can detect these pending reports and handle them according
to the chosen upload mode: keep them local only, upload them directly from the game or editor,
hand them off to a separate reporter application, or do both.

<!-- image showing the crash reporter application -->

The system identifies each report using a consistent app ID and build ID
(the same approach is used by the Analytics module).
These values are either baked in at compile time or taken from project settings, and they are sent along
with other details such as the app name, version, and privacy-related links.
Project settings under the crash reporter section control the upload endpoint, whether user consent is
required, and the path to any external reporter tool.

Games can connect to built-in signals to show progress or react to upload results.
If you prefer your own reporter tool instead of the official one, you can point the editor to it
with a simple command-line option.

## Analytics

The **Analytics** singleton provides a lightweight, consent-gated event pipeline for both the editor
and shipped games.

### Design

Events are stored as simple JSON lines on disk and later sent to the configured endpoint,
using the same identity headers as Crash Reporter.
By default nothing is uploaded until the user gives consent.
The device’s unique ID is left out unless the user chooses to identify themselves,
in which case the unique ID and any extra details supplied by the developer
(through `identify()` or other user properties) can be included.

<!-- image showing the analytics dialog -->

Editor builds that are compiled with analytics support record demographic and usage events
after consentis granted.
Export templates compiled with analytics enabled expose the game-facing API so shipped projects
can send their own events in the same way.

## Shared Identity, Configuration & Privacy

Both Analytics and Crash Reporter share the same core identity values.
App ID, Build ID, and endpoint can be baked in at compile time for the editor, or taken from a
template bake or Project Settings for exported games.
Version and channel information always come from the project or runtime.
Either singleton can return the fully resolved configuration through `get_resolved_config()`,
which is useful for debugging or displaying settings in the UI.
Leaving the analytics endpoint empty simply disables collection,
while crash reporting can still write dump files even when uploads are turned off.

<!-- image showing the crash reporter project settings -->

Analytics is strictly opt-in: no events are sent until the user gives explicit consent.
Crash reporting can also be configured to require consent before any upload.
By default, analytics runs in anonymous mode.
Sidecar reporters can display the privacy-policy and contact URLs supplied by the engine.
All network traffic consists of explicit HTTP POSTs to the endpoints you configure;
othing is sent to third-party services unless you set it up that way.

<!-- image showing the analytics project settings -->

Both Analytics and Crash Reporter share the same core identity values (App ID, Build ID, and endpoint). These can be baked in at compile time for the editor, or taken from a template bake or Project Settings for exported games. Version and channel information always come from the project or runtime. Either singleton can return the fully resolved configuration via get_resolved_config() for debugging or UI display.
Analytics is strictly opt-in and runs anonymously by default—no events are sent without explicit consent. Crash reporting can also require consent before upload. Leaving the analytics endpoint empty disables collection, while crash dumps can still be written even when uploads are turned off. All network traffic consists of explicit HTTP POSTs to the endpoints you configure; nothing is sent to third-party services unless you set it up that way.

## Documentation & Next Steps

Both modules are already available in the [latest release of Blazium](https://blazium.app/download)
and dedicated tests projects are available at
[crash_reporter_module_tests](https://github.com/blazium-games/crash_reporter_module_tests) and
[analytics_module_tests](https://github.com/blazium-games/analytics_module_tests).

Together, the CrashReporter and Analytics modules give Blazium projects a complete,
first-party telemetry foundation:
reliable native crash capture with optional user-facing reporting, plus a flexible, privacy-respecting
analytics layer that works for both the editor and shipped games. All controlled from Project Settings
and a small, consistent GDScript API.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**