---
title: "GDK Module"
description: "Introducing the GDK Module"
cover: "assets/cover.jpg"
---

# Introducing the GDK Module

![](assets/gdk.jpg)
*Microsoft's Game Development Kit straight into the editor, with export tooling, live services, and a test suite to keep it honest.*
GDK Module is a working integration with Microsoft's GDK running on PC, complete with export tooling, an editor plugin, and a full automated test pass behind it.
For everyone building games on Blazium who has eyed that Xbox ecosystem and wondered when the engine would meet them halfway: it's here.

## Key Features

- **GDK runtime integration** — the engine links against the GDK on PC using `Thunks.dll`, following Microsoft's custom-engine guidance for PC titles.
- **XSAPI services** — the Xbox Services API layer is wired in, which is the gateway to the kind of platform features Xbox developers expect to reach for.
- **Export platform** — a dedicated Xbox export target, so packaging a build isn't a manual side-quest.
- **Editor plugin** — tooling that lives right inside the Blazium editor instead of bolted on from the outside.

The thing we're most happy about is how little ceremony it takes to get going. The module **auto-discovers** your GDK install from the standard `C:\Program Files (x86)\Microsoft GDK` location, and it stages the runtime DLLs into your `bin/` directory for you. No hunting through environment variables, no copy-pasting DLLs by hand. Install the GDK, build the module, and the plumbing sorts itself out.

## Documentation & Next Steps
The module is already available in the[latest nightly of Blazium](https://blazium.app/download)
and it comes with comprehensive tests see the dedicated [blazium-games/xbox_module_tests](https://github.com/blazium-games/xbox_module_tests) for validation examples.
GDK module brings Microsoft's GDK straight into Blazium on PC

---
[Jump into our Discord](https://blazium.app/chat) for real-time chats, dev support and feedback!
Or follow us everywhere else:

- **[IndieDB](https://www.indiedb.com/engines/blazium-engine/articles)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[Youtube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
