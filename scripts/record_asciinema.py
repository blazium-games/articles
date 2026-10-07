#!/usr/bin/env python3
"""Record CLI sessions as asciinema v2 casts and static SVG previews.

Uses the official cast format (https://github.com/asciinema/asciinema).
Hub News cannot play .cast files, so each recording also gets an SVG frame
of the terminal output. Replay locally with: asciinema play file.cast
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAST_DIR = ROOT / "casts"
CLI = Path(r"D:\projects\blazium_ecosystem\blazium-cli\blazium-cli.exe")
TC = Path(r"D:\projects\blazium_ecosystem\blazium-toolchain")
COLS, ROWS = 100, 28
BG = "#121018"
FG = "#f4eefc"
PROMPT = "#e070ff"


def run_cmd(argv: list[str], cwd: Path | None = None) -> tuple[str, int]:
    p = subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (p.stdout or "") + (p.stderr or "")
    if not out.endswith("\n"):
        out += "\n"
    return out, p.returncode


def write_cast(path: Path, command: str, output: str) -> None:
    header = {
        "version": 2,
        "width": COLS,
        "height": ROWS,
        "timestamp": int(time.time()),
        "title": command,
        "env": {"SHELL": "powershell", "TERM": "xterm-256color"},
    }
    events = []
    t = 0.15
    prompt = f"$ {command}\r\n"
    events.append([round(t, 3), "o", prompt])
    t += 0.25
    chunk = ""
    for ch in output.replace("\n", "\r\n"):
        chunk += ch
        if ch == "\n" or len(chunk) >= 80:
            events.append([round(t, 3), "o", chunk])
            t += 0.012
            chunk = ""
    if chunk:
        events.append([round(t, 3), "o", chunk])
        t += 0.05
    events.append([round(t + 0.2, 3), "o", "$ "])
    lines = [json.dumps(header, separators=(",", ":"))]
    for ev in events:
        lines.append(json.dumps(ev, separators=(",", ":")))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_svg(path: Path, command: str, output: str) -> None:
    lines = [f"$ {command}"] + output.replace("\r", "").splitlines()
    lines = lines[:ROWS]
    while lines and lines[-1] == "":
        lines.pop()
    # One blank row under the output. Do not force a 12-row canvas:
    # short commands were rendering as 336px of empty terminal.
    lines.append("")
    width = 16 * COLS + 48
    height = 22 * len(lines) + 72
    parts = [
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
  <title>{command}</title>
  <rect width="{width}" height="{height}" rx="10" fill="{BG}"/>
  <text x="24" y="28" fill="{PROMPT}" font-family="Consolas, Cascadia Mono, monospace" font-size="13">asciinema</text>
'''
    ]
    y = 64
    for i, line in enumerate(lines):
        fill = PROMPT if i == 0 or line.startswith("$") else FG
        esc = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        parts.append(
            f'  <text x="24" y="{y}" fill="{fill}" font-family="Consolas, Cascadia Mono, monospace" font-size="16">{esc}</text>\n'
        )
        y += 22
    parts.append("</svg>\n")
    path.write_text("".join(parts), encoding="utf-8")


RECORDINGS = [
    ("cli-help", [str(CLI), "--help"], None),
    ("cli-version", [str(CLI), "version"], None),
    ("cli-editors", [str(CLI), "editors"], None),
    ("cli-install-path", [str(CLI), "install-path"], None),
    ("cli-templates-help", [str(CLI), "templates", "--help"], None),
    ("cli-remote-help", [str(CLI), "remote", "--help"], None),
    ("cli-handle-uri-help", [str(CLI), "handle-uri", "--help"], None),
    ("cli-update-help", [str(CLI), "update", "--help"], None),
]


ARTICLE_CASTS = {
    "what-is-the-blazium-ecosystem": ["cli-editors"],
    "blazium-cli": [
        "cli-help",
        "cli-version",
        "cli-editors",
        "cli-install-path",
        "cli-templates-help",
        "cli-remote-help",
        "cli-handle-uri-help",
        "cli-update-help",
    ],
    "export-templates-and-cdn": ["cli-templates-help"],
    "remote-control-and-mcp": ["cli-remote-help"],
    "github-actions-for-blazium": ["cli-help"],
    "blazium-toolchain": [],
    "download-and-dev-tools": ["cli-version"],
}


def main() -> None:
    CAST_DIR.mkdir(parents=True, exist_ok=True)
    for stem, argv, cwd in RECORDINGS:
        cmd = " ".join(Path(a).name if a.endswith(".exe") else a for a in argv)
        if argv[0].endswith("blazium-cli.exe"):
            cmd = "blazium-cli " + " ".join(argv[1:])
        out, code = run_cmd(argv, cwd)
        body = out if code == 0 else out + f"\n(exit {code})\n"
        write_cast(CAST_DIR / f"{stem}.cast", cmd, body)
        write_svg(CAST_DIR / f"{stem}.svg", cmd, body)
        print(f"recorded {stem} exit={code}")

    engine = ROOT / "engine"
    for slug, stems in ARTICLE_CASTS.items():
        assets = engine / slug / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        for stem in stems:
            for ext in (".cast", ".svg"):
                src = CAST_DIR / f"{stem}{ext}"
                if src.exists():
                    shutil.copy2(src, assets / f"{stem}{ext}")
        print(f"copied casts -> {slug}")


if __name__ == "__main__":
    main()
