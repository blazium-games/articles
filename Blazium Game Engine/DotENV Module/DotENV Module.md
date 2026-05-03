---
title: "DotENV Module"
description: "Introducing the DotENV Module"
cover: "assets/cover.jpg"
---

# Introducing the DotENV Module  

![](assets/dotenv.jpg)  

**DotENV** is a lightweight and flexible environment‑variable parsing module built directly into **Blazium Engine**,
designed to make working with configuration data effortless inside your projects. Whether you’re handling project
settings, API keys, or per‑project overrides, DotENV provides a clean and efficient API without requiring any external libraries.

## Key Features  
- **Simple Parsing** — Load environment variables into structured objects (key/value pairs) with minimal boilerplate.  
- **Custom Delimiters** — Supports JSON‑like formatting (`{name = value;}` or `name=value` per line) to
adapt to any naming convention you need.  
- **Read & Write Support** — Not just a parser, DotENV allows you to generate and write environment‑variable
strings back to a file when required (e.g., for deployment scripts).  
- **Type‑Friendly Handling** — Values are returned as the correct type (strings, numbers, booleans)
based on their appearance in the source. No extra conversion code needed.  
- **Lightweight Design** — Minimal runtime overhead ensures fast execution even when processing many variables or
large configuration blocks.  
- **Engine‑Native Integration** — Fully compatible with GDScript and C#, no external dependencies required.  
- **Robust Error Handling** — Gracefully deals with missing, malformed, or duplicate entries; logs warnings instead of crashing.

## Why Use DotENV in Your Blazium Projects?  

![](assets/dotenv_code.jpg)  

DotENV solves the common need to keep project settings out of code while still being easily editable:

- **Data‑Driven Design** — Store API keys, UI themes, or physics tweaks in simple text files that designers can
adjust without touching scripts.  
- **Tooling & Pipelines** — Integrate with CI/CD or dev tools (e.g., `dotenv` parsers) and feed the resulting
values directly into Blazium’s configuration system.  
- **Rapid Iteration** — Update a value in a file and redeploy instantly—no code rebuilds required.  
- **Save/Export Systems** — Generate environment‑variable dumps for debugging or to share settings between
environments(dev / test / prod).  
- **Interoperability** — Environment files are universally supported, making them ideal for external tools and
collaborative workflows.

From indie prototypes to large‑scale production engines, DotENV helps keep your configuration workflows
clean, readable, and efficient.  

## Documentation & Next Steps  

The module is already bundled with the [latest nightly of Blazium](https://blazium.app/download) and comes with a
comprehensive test suite (see the dedicated [dotenv_module_tests repository](https://github.com/blazium-games/dotenv_module_tests)
for validation examples).  

DotENV brings straightforward, engine‑native environment‑variable handling to Blazium — helping you build
configurable systems faster and with less friction.  

---  

**[Jump into our Discord](https://blazium.app/chat)** for real‑time chats, dev support and feedback!

Or follow us everywhere else:  

- **[IndieDB](https://www.indiedb.com/engines/blazium-engine/articles)**  
- **[X / Twitter](https://x.com/BlaziumGames)**  
- **[YouTube](https://www.youtube.com/@blazium)**  
- **[itch.io](https://blaziumengine.itch.io)**
