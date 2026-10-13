# Asciinema recordings

Official [asciinema](https://github.com/asciinema/asciinema) v2 casts of Blazium CLI.

```text
asciinema play cli-help.cast
```

Install the player: https://github.com/asciinema/asciinema

Regenerate from a live CLI:

```text
asciinema rec --title "blazium-cli editors" cli-editors.cast
blazium-cli editors
exit
```

Hub News cannot embed the player. Articles show the matching `.svg` preview and keep the `.cast` next to it for replay. Record new sessions with `asciinema rec`, not screenshots of a terminal.

`articles/scripts/record_asciinema.py` rebuilds help/version/editors casts from `blazium-cli.exe` on this machine.
