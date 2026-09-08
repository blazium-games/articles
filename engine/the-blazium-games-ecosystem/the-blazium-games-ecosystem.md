---
title: "The Blazium Games Ecosystem"
description: >-
  How Blazium Games tools and services work together to give developers
  everything they need to create, build, ship, and maintain games and applications.
cover: "assets/cover.png"
slug: "the-blazium-games-ecosystem"
deployed: false
date: "2026-09-08"
author: "sshiiden"
hosts: []
---
# The Blazium Games Ecosystem

Since Project Hangman, Blazium Games has built a connected set of tools and services.
The goal is simple: give developers everything required to create, build, ship, and
maintain games without fragmented third-party stacks or restrictive platforms.

What started as a community-driven Godot fork is now a full ecosystem: the engine,
automated build and distribution pipelines, a CDN, internal build tracking, crash
reporting, editor management tools, specialized export toolchains, reusable GitHub
Actions, multiplayer services, and a storefront at blazium.games.

These pieces form a practical loop. Develop in the engine, pull exact builds via
CLI or Hub, automate with Actions and CI/CD, target modern and specialized
platforms, add multiplayer through the services, and close the quality loop with
crash reporting.

## Blazium Game Engine

Blazium Engine is a free, open-source, multi-platform 2D and 3D game engine forked from
Godot in late 2024. It keeps full compatibility with Godot projects and GDExtensions
while adding quality-of-life improvements, extra modules, platform integrations, and
services built for shipping games.

It receives frequent updates and ships 38 custom modules (SQLite, RCON, IRC,
crash reporting, platform integrations, MCP/AI tooling, and more). Everything else in
the ecosystem exists to serve this engine.

Learn more at [blazium.app](https://blazium.app).

## The Engine CI/CD

Blazium runs a full CI/CD pipeline that produces nightlies and official releases.
Builds are published to GitHub Releases, the public CDN, and itch.io. The pipeline
handles editor binaries, export templates, multi-platform packaging, signing, and
version tracking.

Open-source reusable actions and scripts power much of the automation so both the
core team and external developers can reproduce the same flow. Once a build finishes,
the pipeline notifies Cerebro and publishes artifacts to the CDN.

Browse the CI/CD at [blazium-games/cicd](https://github.com/blazium-games/cicd).

## Our CDN

cdn.blazium.app serves static files for the ecosystem: JSON metadata, editor binaries,
export templates, tools, and other artifacts. It is the primary distribution point used
by the CLI, GitHub Actions, the website, and internal tooling. Versioned nightlies and
releases, checksums, and efficient delivery let developers fetch exact builds quickly.

## Cerebro

Cerebro is the internal system that securely tracks editor build data and binaries:
state, metadata, checksums, deployment type (nightly vs release), platforms, and
production status. CI/CD notifies it at key stages, providing a controlled source of
truth separate from the public CDN.

## Crash Reporter

The Crash Reporter works with the engine module to provide stability insights. Built
around Breakpad-style dump collection, it supports in-engine reporting, sidecar upload,
or both. Features include configurable upload behavior, metadata enrichment,
consent-aware sidecars, and example ingest servers (with optional Discord webhooks).

It closes the feedback loop so crashes in the engine, tools, or shipped games can be
diagnosed and fixed quickly.

Learn more in the
[dedicated article](../crash-reporter-and-analytics/crash-reporter-and-analytics.md).

## Blazium Hub & Blazium CLI

Blazium Hub manages editor versions and templates in a consistent local layout. The
CLI is its command-line counterpart and the foundation for both local workflows and
GitHub Actions. It downloads the engine, templates, and tools from the CDN, supports
pinning exact versions or nightlies, and makes installation scriptable.

Learn more in the [dedicated article](../blazium-hub-and-cli/blazium-hub-and-cli.md).

## Blazium Toolchain

The Toolchain adds specialized and retro export pipelines beyond standard desktop,
mobile, and web targets. Current support includes:

- PlayStation 1 (PS1)
- PlayStation 2 (PS2)
- Nintendo 64 (N64)
- Interactive DVD authoring
- Windows Screensaver exports

PS3 and PS4 support are planned. These targets use the same editor, project format,
and CI/CD flow as regular exports.

Learn more in the [dedicated article](../blazium-toolchain/blazium-toolchain.md).

## GitHub Actions

Reusable Actions lower the barrier to automated builds and deployments:

- [**setup-blazium-engine**](https://github.com/blazium-games/setup-blazium-engine):
Installs a chosen engine version (and optionally templates) via CLI and CDN.
- [**setup-blazium-cli**](https://github.com/blazium-games/setup-blazium-cli):
Installs the CLI itself.
- [**export-blazium-game**](https://github.com/blazium-games/export-blazium-game):
Builds, signs, and prepares games for multiple platforms.
- [**deploy-blazium-game**](https://github.com/blazium-games/deploy-blazium-game):
Pushes builds to a store.

These power the team’s own pipelines and let any project achieve consistent
multi-platform exports with minimal custom scripting.

## Blazium Services

Blazium Services is a lightweight suite of backend services for multiplayer and online
features, born from the needs of Project Hangman and designed to scale toward larger
experiences.

Available and planned capabilities include:

- Lobby / matchmaking (with Luau scripting)
- Login / authentication (including social providers)
- Master server (tracking dedicated game servers)
- Leaderboards
- Additional networking, VoIP, and game-server services

Services appear as engine nodes with a free hosted endpoint so developers can start
immediately. They emphasize low resource usage and cross-platform reach (desktop,
mobile, web, consoles).

Documentation is at [docs.blazium.app](https://docs.blazium.app).

# Conclusion

Develop in the engine, add multiplayer through the services, automate builds and
distribution with the CLI, Hub, CI/CD and Actions, target modern and specialized
platforms via the toolchain, and improve stability with the crash reporter.

The same infrastructure that ships the team’s games is available to every developer.
Start today at [blazium.app](https://blazium.app) or join the [Discord](https://blazium.app/chat).

---

- **[Discord](https://blazium.app/chat)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**