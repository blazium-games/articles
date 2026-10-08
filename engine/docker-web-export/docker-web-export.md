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

## Why we built it

The template README says it hosts a Blazium web export as a Discord Embedded Application, including Nginx rules for Discord's `/.proxy/` asset prefix. A note dated 2025-02-22 in that README adds YouTube Playables: the initial bundle must be under 15 MiB, so WASM is precompressed and `gzip_static` serves it, and `/ytgame` drops the COOP and COEP headers. The committed `example.env` sets `PROJECT_NAME=hangman`. That value is our example Hangman game, the one that shipped as a Discord app. It is not a commercial title, and the name in `.env` is not a claim that this image is the production host.

## What Blazium Games uses it for

Blazium Games used this template in-house to validate Discord `/.proxy/` hosting and YouTube Playables bundle serving. `PROJECT_NAME=hangman` in `example.env` is the example Hangman game, which shipped as a Discord app. Registry push is `make deploy-docker`, which reads `.env` for `DOCKER_REGISTRY`, `REGISTRY_PATH`, and `TAG`. The sample registry is `registry.digitalocean.com` and `REGISTRY_PATH=blazium`. The 2025 community update lists a DigitalOcean sponsorship. It does not say this image is the host Hangman runs in production.

## What other projects get

Copy a `Web` export into `static/`, then `docker compose up --build`. The image does not install the engine and does not run the export. Discord URL mappings and a YouTube Playables listing are configured on those platforms, not in this repo.

Repo: [blazium-games/docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template). A container plus the web exporter output. Use it for a public web build, a Discord activity, or a YouTube Playable.

## Status

The template serves a folder you already exported. It does not install Blazium and it does not run the export. `docker-compose.yaml` builds `Dockerfile` and publishes `8080:8080`. Nginx serves `/usr/share/nginx/html`. `static/` is that web root. The `.keep` file is not copied into the image.

`make deploy-docker` is the registry path (`scripts/deploy.sh`, reading `.env`). Local preview is `docker compose up --build`. The GitHub workflow that deploys an already-exported artifact is `deploy-docker.yml` in [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game). Steam and itch reusable workflows in that repo are deprecated. This Docker workflow is not.

YouTube Playables wants the initial bundle under 15 MiB. That limit is YouTube's, and the template's answer is precompressed WASM plus `gzip_static`. Discord activities need the `/.proxy/` location and the COOP/COEP headers already in `nginx/nginx.conf`. `/ytgame` drops those two headers. Nothing in the template creates the Discord application or the YouTube Playable listing.

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

Login and lobby clients are not part of this image. `blazium-dev` does not register those classes, and this repo does not add them. If a game needs a backend, that is a separate host. The container is the static web build plus the Nginx rules above.

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
