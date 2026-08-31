---
title: "Docker web export"
description: "The docker-webbuild-template hosts a Blazium web export, including Discord activity .proxy rewrites."
cover: "assets/cover.png"
slug: "docker-web-export"
deployed: false
date: "2026-08-31"
author: "Blazium"
hosts: []
---

Repo: [blazium-games/docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template). A container plus your web export. Use it for a public web build, a Discord activity, or a YouTube Playable.

Templates and web flags: [Export templates and the CDN](../export-templates-and-cdn/export-templates-and-cdn.md).

![CDN tree](assets/cdn-tree.png)

## Plain web

1. Export Web from the editor (templates installed for this Blazium version).
2. Copy the export into the template's web root.
3. `docker compose up`.
4. Open localhost.

```text
docker compose up --build
```

<!-- ASCIINEMA: assets/docker-compose-up.cast | docker compose up --build -->
<!-- CAPTURE: record asciinema rec from the template directory once the repo is cloned -->
<!-- CAPTURE: assets/compose-browser.png | Browser | localhost showing the web game, compose logs beside it -->
<!-- CAPTURE: assets/cover.png | Browser + terminal | Replace diagram cover -->

## Discord activity

Discord only accepts the game through `*.discordsays.com` and mapped `.proxy` paths. The Docker template rewrites those paths. On the Discord admin side: create an application, set URL mappings. Blazium service nodes (`LoginClient`, `LobbyClient`) detect that environment and rewrite their default URLs. Full node and authorize walk: [Discord on Blazium](../discord-on-blazium/discord-on-blazium.md).

<!-- CAPTURE: assets/discord-proxy.png | Discord Admin | URL mappings. Existing articles/engine/blazium-deploy-games-on-discord/assets/config.png is a candidate. -->

## YouTube Playables

Check `blazium/youtube_playable` on the web export. Budget: 15 MB, gzip WASM. Handshake lives in `YoutubePlayablesClient`. This article only hosts the file. The node is a sibling export story.

## Compose

Clone the template, drop the export in, run compose. Do not commit `.env` secrets. Keep Discord mappings in the admin console, not in the image.
