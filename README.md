# Blazium Articles

This repository serves as a centralized space for all articles written by the team to publish on
the various platform we are active on (X, IndieDB, itch.io, Patreon).

## Structure

The directories should follow the following structure:

```
- Main Topic
| - Article Topic
  | - Article.md
  | - assets (optional folder)
    | - image1.jpg
    | - image2.png
    | - image3.gif
    | - video1.mp4
```

## Scripts

Under the `/scripts` directory you can fine `md_to_html.js`, use it to convert a
markdown file to HTML to make the process of publishing for IndieDB and itch.io easier,
**images/videos will still need to be added manually**.

```bash
node scripts/md_to_html.js "Blazium Game Engine/Release 0.6.X/Release 0.6.X.md"
```