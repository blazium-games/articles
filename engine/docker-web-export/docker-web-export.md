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

Repo: [blazium-games/docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template). A container plus the web exporter output. Use it for a public web build, a Discord activity, or a YouTube Playable.

The engine preset you export is named `Web` (`EditorExportPlatformWeb.get_name()` returns `"Web"`). Templates and the CDN layout: [Export templates and the CDN](../export-templates-and-cdn/export-templates-and-cdn.md).

![CDN tree](assets/cdn-tree.png)

## Local web

1. Install export templates for the same Blazium version as the editor.
2. Export the `Web` preset from the editor.
3. Copy that folder into the template's `static/` directory. The `.keep` file is not copied into the image.
4. From the template repo, start Compose. The service publishes `8080:8080`.
5. Input:

```text
docker compose up --build
```

6. Open `http://localhost:8080`.

`docker-compose.yaml` builds `Dockerfile` and does nothing else. Nginx serves `/usr/share/nginx/html`.

## Registry push

`make deploy-docker` runs `scripts/deploy.sh`. It reads `.env`:

```text
PROJECT_NAME=hangman
DOCKER_REGISTRY=registry.digitalocean.com
REGISTRY_PATH=blazium
TAG=latest
```

`example.env` is the committed sample. Do not commit a filled `.env`. The Makefile includes `.env` when it is present.

The GitHub workflow that deploys an already-exported artifact is `deploy-docker.yml` in [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game). It expects an artifact named like `Web`. See [GitHub Actions for Blazium](../github-actions-for-blazium/github-actions-for-blazium.md).

## Discord activity

Discord loads the page through `*.discordsays.com` and requires a `/.proxy/` prefix on asset URLs. `nginx/nginx.conf` has that location. The same file sends:

```text
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

On the Discord side you create an application and set URL mappings. The engine side of the embed is the web export flag `blazium/discord_embed/enabled`, which appends the generated `.discord.embed.js`. The node is `DiscordEmbeddedAppClient` in `modules/socialexports`. Walkthrough: [Discord on Blazium](../discord-on-blazium/discord-on-blazium.md).

## YouTube Playables

Check `blazium/youtube_playable/enabled` on the `Web` preset. YouTube Playables wants the initial bundle under 15 MiB, so WASM is precompressed. Nginx `gzip_static` serves `file.wasm.gz` as `file.wasm` when the browser accepts gzip, and falls back to the raw `.wasm` otherwise. The `/ytgame` location drops the COOP/COEP headers that the rest of the site sends.

The handshake class is `YoutubePlayablesClient`, same module as the Discord embed client. This repo only hosts the files.

## What this template does not do

It does not install Blazium, and it does not run the export. It serves a folder you already exported. Login and lobby clients are not part of this image. If a game needs a backend, that is a separate host. The container is the static web build plus the Nginx rules above.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
