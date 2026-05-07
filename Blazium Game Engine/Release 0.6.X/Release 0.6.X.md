---
title: "Blazium Engine Release 0.6.X"  
description:
    "A major update introducing new built-in modules, workflow improvements, tooling integrations, rendering fixes, and performance optimizations across the engine."  
cover: "assets/cover.jpg"
changes: https://github.com/blazium-games/blazium/milestone/1?closed=1
---

# Blazium Engine Release 0.6.X

Blazium Engine 0.6.X is one of the biggest updates to the engine so far, bringing a wide range of new built-in modules,
workflow improvements, tooling integrations, renderer fixes, and performance upgrades.

This release focuses heavily on developer productivity, data handling, automation, and modern tooling support while
continuing to improve engine stability and runtime performance.

[Download the latest release on blazium.app](https://blazium.app/download)

## New Features

### Autowork Module
![](../Autowork%20testing%20framework/assets/autowork.jpg)

**Autowork** is a powerful new built-in testing framework designed specifically for game and application development.
It provides an easy way to automate gameplay testing, validation workflows, regression testing, and project verification directly inside the engine.

Learn more about the Autowork module in the
[dedicated article](https://www.indiedb.com/engines/blazium-engine/features/autowork-testing-framework-module).

### Integrated MCP

Blazium Engine now includes integrated **MCP** support, improving interoperability with external tools, automation workflows, and
AI-assisted development pipelines.
This integration streamlines communication between the editor, external utilities, and development environments.

### DotCSV Module
![](../DotCSV%20Module/assets/dotcsv.jpg)

**DotCSV** is a lightweight and flexible CSV parsing and writing module built directly into **Blazium Engine**,
designed to make working with structured text data effortless inside your projects.

Learn more about the DotCSV module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/dotcsv-module).

### DotENV Module
![](../DotENV%20Module/assets/dotenv.jpg)

**DotENV** is a lightweight and practical environment configuration module built directly into **Blazium Engine**,
designed to simplify how projects manage environment variables and configuration files.

Learn more about the DotENV module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/dotenv-module).

### DotINI Module
![](../DotINI%20Module/assets/dotini.jpg)

**DotINI** is a lightweight and intuitive INI parsing and writing module built directly into **Blazium Engine**,
designed to simplify working with configuration-style data in your projects.

Learn more about the DotINI module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/dotini-module).

### GOAP Module
![](../GOAP%20Module/assets/planning_showcase.gif)

The new **GOAP (Goal-Oriented Action Planning)** module introduces advanced AI planning systems directly into Blazium Engine.
This allows developers to build more dynamic and intelligent NPC behaviors using goal-based decision making instead of rigid state machines.

Learn more about the GOAP module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/goap-module).

### BigNum++ Integration
![](../BlaziumBigNum/assets/bignum_test.jpg)

Blazium Engine now integrates **BigNum++**, enabling support for arbitrary precision mathematics.
This is especially useful for idle games, simulation projects, scientific tooling, financial systems, and
projects that require extremely large or highly precise numeric values.

Learn more about the BigNum integration in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/bignum-integration).

### JWT Module
![](../JWTTool%20Module/assets/jwttool_code_hero.jpg)

A brand new **JWT (JSON Web Token)** module has been added to simplify secure authentication workflows.
Developers can now easily generate, validate, and decode JWT tokens directly from inside the engine for backend services,
multiplayer systems, APIs, and online authentication.

Learn more about the JWT module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/jwttool-module).

### Tiled Importer

Blazium Engine now supports importing maps created with **Tiled**, making it easier to integrate external level design workflows into your projects.

## Updates

### Updated SQLite Module

The built-in SQLite module received major improvements, including updated bindings, improved reliability, and better integration with
modern database workflows. This update improves performance and stability for projects relying heavily on local storage and structured data.

### Optimized unicode _find_upper and _find_lower.
![](assets/string.png)

Replaced slow binary search with perfect compile time hash table, when converting unicode to uppercase and lowercase.
This increases the speed of `to_lower`/`to_upper` by 4 to 6 times, wich increases the speed of a few other functions,
including GDScript compilation, localization, and stuff in the editor.

**Contributed by [MisterPuma80](https://github.com/blazium-games/blazium/pull/652)**

### Fix textures repeat mode for GLES3 renderer.

Fixed texture repeat handling in the GLES3 renderer, improving compatibility and rendering correctness for materials and
textures relying on repeat sampling modes.

**[pull/632](https://github.com/blazium-games/blazium/pull/632)**

### Updated Engine.get_version_info

`Engine.get_version_info()` has been expanded to provide Blazium Engine version info along with Godot's.

**[pull/642](https://github.com/blazium-games/blazium/pull/642)**

## Download

[Download the latest release on blazium.app](https://blazium.app/download)

For the complete list of changes, see the [changelog](https://blazium.app/changelog?v=release_0.6.X).

---

**[Jump into our Discord](https://blazium.app/chat)** for real-time chats, dev support and feedback

Or follow us everywhere else:

- **[IndieDB](https://www.indiedb.com/engines/blazium-engine)**
- **[X / Twitter](https://x.com/BlaziumGames)**
- **[YouTube](https://www.youtube.com/@blazium)**
- **[itch.io](https://blaziumengine.itch.io)**
