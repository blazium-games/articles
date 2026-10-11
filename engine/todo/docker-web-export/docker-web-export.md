---
title: "Docker web export"
description: "docker-webbuild-template serves a Web export. It does not run the editor, and it is not the web editor image."
cover: "assets/cover.png"
slug: "docker-web-export"
deployed: false
date: "2026-10-11"
author: "Bioblaze Payne"
hosts: []
---

# Docker web export

### A container for the files the Web preset already wrote

*By Bioblaze Payne, Co-Founder of [Blazium Games](https://blazium.games)*

---

A Blazium web export is a folder: `index.html`, a `.wasm`, a `.pck`, and whatever the preset added for Discord or YouTube. [docker-webbuild-template](https://github.com/blazium-games/docker-webbuild-template) is Nginx in front of that folder. It does not install the engine and it does not run the export.

We needed it because a Discord activity is not a zip you hand someone. Discord loads the page through `*.discordsays.com` and requires a `/.proxy/` prefix on asset URLs, plus COOP and COEP. YouTube Playables wants the initial bundle under 15 MiB, which is YouTube's limit, so the template serves precompressed WASM. Hangman's `example.env` sets `PROJECT_NAME=hangman`. Hangman shipped as a Discord app. The sample registry in that file (`registry.digitalocean.com`, `REGISTRY_PATH=blazium`) is not a claim about the host Hangman runs on in production.

This image is not the web editor. CI builds a separate web-editor artifact. Do not conflate them.

![Export, then static/, then Nginx](assets/docker-host.png)

## Local

1. Install export templates for the same Blazium version as the editor. The CLI pulls them from `cdn.blazium.app`. The editor's mirror list still points at GitHub.
2. Export the preset named `Web`. `EditorExportPlatformWeb.get_name()` returns that string.
3. Copy the export into the template's `static/` directory. The `.keep` file is not copied into the image.
4. From the template repo:

```text
docker compose up --build
```

5. Open `http://localhost:8080`.

`docker-compose.yaml` builds the Dockerfile and publishes `8080:8080`. The image is `FROM nginx:latest`, replaces `/etc/nginx/nginx.conf`, copies `static/` to `/usr/share/nginx/html`, and exposes 8080. Nginx serves `/usr/share/nginx/html`. The README's primary registry path is `make deploy-docker`, which runs `scripts/deploy.sh` and reads `.env` for `DOCKER_REGISTRY`, `REGISTRY_PATH`, and `TAG`. Do not commit a filled `.env`. The Makefile includes `.env` when it is present.

```plaintext
PROJECT_NAME=hangman
DOCKER_REGISTRY=registry.digitalocean.com
REGISTRY_PATH=blazium
TAG=latest
```

The clone URL in that README still says `blazium-engine/docker-webbuild-template`. The repository is `blazium-games/docker-webbuild-template`.

## Nginx map

| Location | Behavior |
|---|---|
| `/` | Static files; COOP `same-origin` + COEP `require-corp` |
| `/.proxy/` | Alias of the same root for Discord asset URLs; same COOP/COEP |
| `/ytgame` | Same files without COOP/COEP (YouTube Playables) |
| `~* \.(wasm)$` | `gzip_static on`; serves `.wasm.gz` when the client accepts gzip |
| `/health` | `OK` text, or `{"status":"ok"}` when `Accept` asks for JSON |

```text
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Those two headers are on `/` and `/.proxy/`. They are intentionally absent on `/ytgame`.

## Discord

On the Discord side you create the application and set URL mappings so assets resolve through `/.proxy/`. On the engine side, `blazium/discord_embed/enabled` appends `{name}.discord.embed.js`. `blazium/discord_embed/autodetect` controls the embed bootstrap. The node is `DiscordEmbeddedAppClient` in `modules/socialexports`. `is_discord_environment()` checks that the page is inside Discord.

The GitHub workflow that deploys an already-exported artifact is `deploy-docker.yml` in [deploy-blazium-game](https://github.com/blazium-games/deploy-blazium-game) at tag `v0.0.2`. It expects an artifact whose preset name is `Web`. Steps: checkout the webbuild template, download the artifact into `static/`, buildx push as `{registry}/{path}:latest` and `:{sha}`. Steam and itch workflows in that repo are deprecated. This Docker workflow is not.

```yml
deploy-docker:
  uses: blazium-games/deploy-blazium-game/.github/workflows/deploy-docker.yml@v0.0.2
  with:
    artifact-name: Web
    docker-registry: registry.digitalocean.com
    registry-path: org-name/image-name
  secrets:
    docker-username: ${{ secrets.DOCKER_USERNAME }}
    docker-token: ${{ secrets.DOCKER_TOKEN }}
```

## YouTube Playables

Check `blazium/youtube_playable/enabled` on the `Web` preset. For size, also enable `blazium/export_gzip_compressed_wasm/enabled`. Optionally keep the raw file with `blazium/export_gzip_compressed_wasm/keep_uncompressed_wasm` so Nginx can fall back when gzip is not accepted.

Nginx `gzip_static` serves `file.wasm.gz` as `file.wasm` when the browser accepts gzip, and falls back to the raw file otherwise. The `/ytgame` location drops the COOP and COEP headers the rest of the site sends. The handshake class is `YoutubePlayablesClient`, same module as the Discord embed client. This repo only hosts the files.

YouTube's published initial-bundle limit is 15 MiB. That limit is YouTube's, not something Nginx enforces. The compression path is how exports stay under it.

## Export checklist before you build the image

1. Preset name is exactly `Web`.
2. Templates for this Blazium version are installed (`blazium-cli install <ver> --templates` or `templates download <ver> --tpz`).
3. Discord and/or YouTube preset flags match the host you will use.
4. `static/` contains `index.html` and the wasm/pck pair the export wrote — not the project source tree.
5. `.env` exists locally for `make deploy-docker`, and is gitignored when filled.

## What it does not do

Login and lobby clients are not in this image, and they are not in the `blazium-dev` module tree. They live in [blazium-sdk-module](https://github.com/blazium-games/blazium-sdk-module). If a game needs a backend, that is a separate host.

The image does not run Autowork, does not call `blazium-cli`, and does not fetch templates. Those jobs happen before `static/` is filled. The CDN layout for editor and template zips is a different problem. Those files are what you export *with*. This container is what you export *into*.

![Where editor zips live on the CDN](assets/cdn-tree.png)

## Makefile and scripts

The template's `Makefile` is the local operator path. `make deploy-docker` runs `scripts/deploy.sh`, which expects Docker login against `DOCKER_REGISTRY` and tags `{DOCKER_REGISTRY}/{REGISTRY_PATH}:{TAG}`. `scripts/credits.sh` is metadata export for authors — it is not required to serve the game. Keep secrets in `.env` on the machine that pushes; the image itself contains only the static export.

For a smoke test without a registry:

```text
docker compose up --build
curl -sS http://localhost:8080/health
curl -sS -H 'Accept: application/json' http://localhost:8080/health
```

`/health` returns plain `OK` by default and JSON when `Accept` asks for it. That endpoint is for probes; it does not prove Discord URL mappings or YouTube package size.

## From export action to this image

A typical pipeline is: `setup-blazium-engine` with `download_template: true` → `export-blazium-game` with `platform-name: Web` → upload the `build/` artifact → `deploy-docker.yml` with `artifact-name: Web`. The deploy workflow does not re-export. If the artifact is missing `index.html` or the wasm file, Nginx will still start and `/health` will still pass. Check the artifact listing step in the workflow log before you chase Discord config.

## Limits

- Base image is `nginx:latest`; pin a digest in your fork if you need bit-for-bit rebuilds.
- `deploy-docker.yml` still checks out `blazium-engine/docker-webbuild-template` in its workflow file even though the canonical repo is under `blazium-games`. Fork or patch the workflow if that clone path breaks for you.
- COOP/COEP on `/` will break some third-party embeds that are not Discord; use `/ytgame` only for the YouTube path that needs headers off.
- This container does not terminate TLS. Put a reverse proxy or platform load balancer in front for `https` Discord/YouTube URLs.
- Worker count is `worker_processes 1` and `worker_connections 1024` in the shipped `nginx.conf`. That is enough for an activity or Playables page; it is not a general CDN substitute for large concurrent downloads of unrelated assets.
- Mime types come from Nginx's default `mime.types` include; custom game asset extensions still serve as `application/octet-stream` unless you extend the config in a fork.

## Links

- Template: https://github.com/blazium-games/docker-webbuild-template
- Deploy workflow: https://github.com/blazium-games/deploy-blazium-game
- Engine: https://github.com/blazium-games/blazium
- Blazium Games: https://blazium.games

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[GitHub](https://github.com/blazium-games)**
- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
