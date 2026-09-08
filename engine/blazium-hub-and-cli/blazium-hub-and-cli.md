---
title: "Blazium Hub & Blazium CLI"
description: >-
    Easy Blazium Engine versions and projects managment with Blazium Hub and Blazium CLI.
cover: "assets/cover.png"
slug: "blazium-hub-and-cli"
deployed: false
date: "2026-09-03"
author: "sshiiden"
hosts: []
---
# Blazium Hub & Blazium CLI

We have worked on two complementary tools designed to simplify engine and project management:
**Blazium Hub**, a graphical application for managing engine versions and projects,
and **Blazium CLI**, the command-line foundation that powers the Hub and provides additional
capabilities on its own.
Together they give developers a consistent way to install, organize, and launch Blazium projects while keeping full control over versions and workflows.

# Blazium Hub

Blazium Hub is a desktop application that combines engine version management and project management
in a single interface.
You can scan your projects folder and manage each project with per-project engine versioning,
favourites, and tags.

<!-- image of various projects, some with different versions, tags and from a separate folder -->

Download and track the engine versions your projects require, including custom local builds.

<!-- image of the engine version manager view, with a custom local build in the list -->

The Hub is built on top of the CLI, so everything you do in the interface is backed by the
same reliable command-line tooling.

A news page is also included, pulling the latest articles from Blazium Games through the
official RSS feed so you can stay up to date without leaving the application.

<!-- image of the news -->

You can download Blazium Hub at [blazium.app](https://blazium.app/dev-tools/download?tool=hub).

# Blazium CLI

Blazium CLI is the command-line tool responsible for downloading and managing engine versions and
export templates, as well as registering and managing projects and more.
Blazium Hub serves as its official graphical front-end.

<!-- image of --help output -->

The CLI can be controlled through deep links using the `blazium://` scheme.
For example, `blazium://open?path=` opens a project, and `blazium://install?version=` installs
a specific editor version.

<!-- image of deep link example -->

When used with an editor that includes the Remote Control module, the `remote` command allows you
to trigger selected engine features directly from the terminal.

<!-- image of remote --help output -->

Read [The Remote Control module](../remote-control-module/remote-control-module.md) article for more info.

You can download Blazium CLI at [blazium.app](https://blazium.app/dev-tools/download?tool=cli).

## Next Steps

For more details on how the Hub, CLI, and other tools work together, see
[The Blazium Ecosystem](../what-is-the-blazium-ecosystem/what-is-the-blazium-ecosystem.md).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[X / Twitter](https://x.com/BlaziumGames)**
- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**