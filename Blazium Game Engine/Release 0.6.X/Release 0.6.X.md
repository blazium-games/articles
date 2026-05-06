---
title: "Blazium Engine Release 0.6.X"  
description: ""  
cover: "assets/cover.jpg"
changes: https://github.com/blazium-games/blazium/milestone/1?closed=1
---

# Blazium Engine Release 0.6.X

## New Features

### DotCSV Module
![](../DotCSV%20Module/assets/dotcsv.jpg)

Learn more about the DotCSV module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/dotcsv-module).

### DotENV Module
![](../DotENV%20Module/assets/dotenv.jpg)

Learn more about the DotENV module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/dotenv-module).

### DotINI Module
![](../DotINI%20Module/assets/dotini.jpg)

Learn more about the DotINI module in the [dedicated article](https://www.indiedb.com/engines/blazium-engine/features/dotini-module).

### Optimized unicode _find_upper and _find_lower.
![](assets/string.png)

Replaced slow binary search with perfect compile time hash table, when converting unicode to uppercase and lowercase.
This increases the speed of `to_lower`/`to_upper` by 4 to 6 times, wich increases the speed of a few other functions,
including GDScript compilation, localization, and stuff in the editor.

**Contributed by [MisterPuma80](https://github.com/blazium-games/blazium/pull/652)**

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
