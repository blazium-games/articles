#!/usr/bin/env python3
"""Generate article showcase images with rich mock UI content."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow required: pip install pillow")

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT.parent / "Blazium Game Engine"

W, H = 1280, 720
BG = (26, 29, 35)
PANEL = (37, 40, 48)
PANEL_ALT = (46, 50, 60)
PANEL_INNER = (32, 35, 42)
TEXT = (232, 234, 237)
MUTED = (154, 160, 166)
DIM = (110, 116, 126)
CODE_BG = (21, 24, 32)
BORDER = (60, 64, 72)
OK = (61, 220, 132)
WARN = (255, 193, 7)
DEFAULT_ACCENT = (61, 220, 132)


def fnt(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if mono:
        paths = ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]
    elif bold:
        paths = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    else:
        paths = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines or [""]


def draw_header(draw: ImageDraw.ImageDraw, title: str, accent: tuple[int, int, int]) -> None:
    draw.rectangle((0, 0, W, 72), fill=PANEL)
    draw.rectangle((0, 68, W, 72), fill=accent)
    draw.text((48, 20), title, fill=TEXT, font=fnt(26, True))


def draw_code_block(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], code: str, accent: tuple[int, int, int]) -> None:
    draw.rectangle(box, fill=CODE_BG, outline=BORDER)
    draw.text((box[0] + 12, box[1] + 8), "GDScript", fill=DIM, font=fnt(11))
    y = box[1] + 28
    for line in code.splitlines():
        draw.text((box[0] + 14, y), line, fill=tuple(min(255, c + 50) for c in accent), font=fnt(13, mono=True))
        y += 18
        if y > box[3] - 8:
            break


def draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, accent: tuple[int, int, int]) -> int:
    tw = int(draw.textlength(label, font=fnt(12))) + 20
    draw.rounded_rectangle((x, y, x + tw, y + 24), radius=4, fill=PANEL_INNER, outline=accent)
    draw.text((x + 10, y + 4), label, fill=accent, font=fnt(12))
    return tw + 8


def draw_status_pill(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, ok: bool = True) -> None:
    color = OK if ok else WARN
    tw = int(draw.textlength(label, font=fnt(11))) + 16
    draw.rounded_rectangle((x, y, x + tw, y + 20), radius=10, fill=(*color[:3],))
    draw.text((x + 8, y + 3), label, fill=(20, 20, 20) if ok else BG, font=fnt(11, True))


def draw_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    details: list[str],
    accent: tuple[int, int, int],
    status: str = "",
) -> None:
    draw.rectangle(box, fill=PANEL_ALT, outline=BORDER)
    draw.rectangle((box[0], box[1], box[0] + 4, box[3]), fill=accent)
    draw.text((box[0] + 16, box[1] + 12), title, fill=TEXT, font=fnt(15, True))
    if status:
        tw = int(draw.textlength(status, font=fnt(10)))
        draw.rounded_rectangle((box[2] - tw - 24, box[1] + 10, box[2] - 12, box[1] + 28), radius=8, fill=PANEL_INNER, outline=accent)
        draw.text((box[2] - tw - 18, box[1] + 12), status, fill=accent, font=fnt(10))
    y = box[1] + 38
    for detail in details:
        draw.text((box[0] + 20, y), f"• {detail}", fill=MUTED, font=fnt(12))
        y += 20
        if y > box[3] - 12:
            break


def draw_row(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, label: str, value: str, accent: tuple[int, int, int], ok: bool = True) -> int:
    draw.rectangle((x, y, x + w, y + 36), fill=PANEL_INNER, outline=BORDER)
    draw.ellipse((x + 10, y + 10, x + 26, y + 26), fill=accent if ok else DIM)
    draw.text((x + 36, y + 8), label, fill=TEXT, font=fnt(13, True))
    draw.text((x + 36, y + 22), value, fill=MUTED, font=fnt(11))
    if ok:
        draw.text((x + w - 70, y + 10), "active", fill=OK, font=fnt(11, True))
    return y + 42


def draw_cover(title: str, subtitle: str, badges: list[str], accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    panel = (80, 120, W - 80, H - 120)
    draw.rectangle(panel, fill=PANEL, outline=BORDER, width=2)
    draw.rectangle((panel[0], panel[1], panel[0] + 6, panel[3]), fill=accent)
    draw.text((panel[0] + 48, panel[1] + 64), title, fill=TEXT, font=fnt(46, True))
    y = panel[1] + 150
    for line in wrap(draw, subtitle, fnt(20), panel[2] - panel[0] - 96):
        draw.text((panel[0] + 48, y), line, fill=MUTED, font=fnt(20))
        y += 28
    bx = panel[0] + 48
    by = panel[1] + panel[3] - panel[1] - 100
    for badge in badges:
        bx += draw_badge(draw, bx, by, badge, accent)
    draw.text((panel[0] + 48, panel[3] - 40), "Blazium Game Engine", fill=DIM, font=fnt(13))
    return img


def draw_hero_mock(
    title: str,
    sections: list[dict],
    code: str,
    accent: tuple[int, int, int],
    mock_title: str = "Editor Preview",
) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw, title, accent)

    left = (48, 96, 620, H - 48)
    draw.rectangle(left, fill=PANEL, outline=BORDER)
    draw.text((left[0] + 16, left[1] + 12), mock_title, fill=MUTED, font=fnt(12))
    draw.line((left[0], left[1] + 32, left[2], left[1] + 32), fill=BORDER)

    y = left[1] + 44
    for section in sections:
        draw.text((left[0] + 16, y), section["heading"], fill=accent, font=fnt(14, True))
        y += 24
        for row in section.get("rows", []):
            y = draw_row(draw, left[0] + 12, y, left[2] - left[0] - 24, row["label"], row["value"], accent, row.get("ok", True))
        y += 8

    draw_code_block(draw, (640, 96, W - 48, H - 48), code, accent)
    return img


def draw_hero_steam(accent: tuple[int, int, int]) -> Image.Image:
    sections = [
        {
            "heading": "Achievements",
            "rows": [
                {"label": "FIRST_WIN", "value": "Defeat the first boss", "ok": True},
                {"label": "COLLECTOR", "value": "Find 10 hidden items", "ok": True},
                {"label": "SPEEDRUN", "value": "Finish under 30 minutes", "ok": False},
            ],
        },
        {
            "heading": "Stats",
            "rows": [
                {"label": "KILLS", "value": "142 (+1 pending)", "ok": True},
                {"label": "PLAYTIME", "value": "18.5 hours", "ok": True},
            ],
        },
    ]
    code = (
        'Steam.initialize(1742110)\n'
        'Steam.set_achievement("FIRST_WIN")\n'
        'Steam.store_stats()\n'
        'var info = Steam.get_achievement_info("FIRST_WIN")\n'
        'var items = Steam.get_all_items()'
    )
    return draw_hero_mock("Achievements, Stats & Inventory", sections, code, accent, "Steam API Panel")


def draw_hero_multiuser(accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Live Collaboration Dock", accent)
    left = (48, 96, 620, H - 48)
    draw.rectangle(left, fill=PANEL, outline=BORDER)
    draw.text((left[0] + 16, left[1] + 12), "Session: blazium-dev-room  •  Port 8765", fill=MUTED, font=fnt(12))
    draw.line((left[0], left[1] + 32, left[2], left[1] + 32), fill=BORDER)
    peers = [
        ("You (Host)", "Editing Main.tscn", "Host", True),
        ("Alice", "Editing player.gd", "Editor", True),
        ("Bob", "Viewing level_01.tscn", "Viewer", True),
    ]
    y = left[1] + 44
    for name, activity, role, online in peers:
        y = draw_row(draw, left[0] + 12, y, left[2] - left[0] - 24, name, activity, accent, online)
        tw = int(draw.textlength(role, font=fnt(10)))
        draw.rounded_rectangle((left[2] - tw - 28, y - 34, left[2] - 16, y - 16), radius=6, fill=PANEL_INNER, outline=accent)
        draw.text((left[2] - tw - 22, y - 32), role, fill=accent, font=fnt(10))
    draw.text((left[0] + 16, y + 8), "Sync: scripts ✓  filesystem ✓  locks: 2 active", fill=OK, font=fnt(12))
    code = (
        "multiuser_editor.host_session(8765, \"secret\")\n"
        "multiuser_editor.join_session(\"192.168.1.10\", 8765)\n"
        "# CRDT merges script edits automatically"
    )
    draw_code_block(draw, (640, 96, W - 48, H - 48), code, accent)
    return img


def draw_hero_town(accent: tuple[int, int, int]) -> Image.Image:
    sections = [
        {
            "heading": "Connection",
            "rows": [
                {"label": "Server", "value": "127.0.0.1:7000  v1.4.2", "ok": True},
                {"label": "Auth", "value": "JWT validated", "ok": True},
            ],
        },
        {
            "heading": "Region",
            "rows": [
                {"label": "Current", "value": "town_square (24 players)", "ok": True},
                {"label": "Battle", "value": "battle_7f3a — your turn", "ok": True},
            ],
        },
    ]
    code = (
        'var sdk = Engine.get_singleton("TownSDK")\n'
        'sdk.connect_to_server("127.0.0.1", 7000)\n'
        'sdk.authenticate(jwt)\n'
        'sdk.enter_region("town_square")'
    )
    return draw_hero_mock("TownSdkClient", sections, code, accent, "Town SDK Status")


def draw_hero_justamcp(accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Tool Catalog", accent)
    left = (48, 96, 620, H - 48)
    draw.rectangle(left, fill=PANEL, outline=BORDER)
    tools = [
        ("scene_list_nodes", "SceneTools", "12 nodes in Main.tscn"),
        ("script_read_file", "ScriptTools", "res://player.gd"),
        ("resource_list", "ResourceTools", "847 resources indexed"),
        ("docs_search", "DocumentationTools", "ClassDB, Node, Steam"),
        ("editor_take_screenshot", "EditorTools", "Viewport capture"),
    ]
    y = left[1] + 16
    draw.text((left[0] + 16, y), "Registered MCP Tools (48 total)", fill=MUTED, font=fnt(12))
    y += 28
    for tool, group, desc in tools:
        draw.rectangle((left[0] + 12, y, left[2] - 12, y + 52), fill=PANEL_INNER, outline=BORDER)
        draw.text((left[0] + 24, y + 8), tool, fill=accent, font=fnt(13, mono=True))
        draw.text((left[0] + 24, y + 28), f"{group} — {desc}", fill=MUTED, font=fnt(11))
        draw.text((left[2] - 60, y + 18), "ready", fill=OK, font=fnt(10, True))
        y += 58
    code = (
        "var schemas = JustAMCPToolExecutor.get_tool_schemas()\n"
        "var result = executor.execute_tool(\n"
        '    "scene_list_nodes", {"scene": "Main"}\n'
        ")"
    )
    draw_code_block(draw, (640, 96, W - 48, H - 48), code, accent)
    return img


def draw_hero_tiled(accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "GodotTsonTileson", accent)
    left = (48, 96, 620, H - 48)
    draw.rectangle(left, fill=PANEL, outline=BORDER)
    draw.text((left[0] + 16, left[1] + 12), "world1.tmx — 3 layers, 2 tilesets", fill=MUTED, font=fnt(12))
    # mini tile grid
    colors = [(80, 120, 80), (100, 80, 60), (60, 90, 130), (90, 90, 90)]
    gx, gy = left[0] + 16, left[1] + 40
    for row in range(8):
        for col in range(14):
            c = colors[(row + col) % len(colors)]
            draw.rectangle((gx + col * 38, gy + row * 38, gx + col * 38 + 36, gy + row * 38 + 36), fill=c, outline=(30, 30, 30))
    draw.text((left[0] + 16, left[3] - 80), "Layers: ground, collision, objects", fill=TEXT, font=fnt(12))
    draw.text((left[0] + 16, left[3] - 58), "Objects: 12 spawn points, 4 triggers", fill=MUTED, font=fnt(11))
    code = (
        "var map = GodotTsonTileson.new()\n"
        'map.parse_file("res://levels/world1.tmx")\n'
        "var tile = map.get_tile(3, 5, 0)\n"
        "var gid = tile.get_gid()"
    )
    draw_code_block(draw, (640, 96, W - 48, H - 48), code, accent)
    return img


def draw_hero_gdk(accent: tuple[int, int, int]) -> Image.Image:
    sections = [
        {
            "heading": "GDK Runtime",
            "rows": [
                {"label": "Thunks.dll", "value": "Loaded from GDK install", "ok": True},
                {"label": "XSAPI", "value": "Achievements, stats, presence", "ok": True},
            ],
        },
        {
            "heading": "Export",
            "rows": [
                {"label": "Platform", "value": "Xbox (PC GDK)", "ok": True},
                {"label": "Config", "value": "MicrosoftGame.config valid", "ok": True},
            ],
        },
    ]
    code = (
        "# Xbox export preset\n"
        "MicrosoftGame.config\n"
        "  TitleId, MSAAppId, StoreId\n"
        "# xbox_module_tests tier 0 passes"
    )
    return draw_hero_mock("Xbox Platform Integration", sections, code, accent, "GDK Export Panel")


def draw_usecase_cards(title: str, cards: list[dict], code: str, accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw, title, accent)
    panel = (48, 96, W - 48, H - 48)
    draw.rectangle(panel, fill=PANEL, outline=BORDER)

    code_h = 130 if code else 0
    grid_h = panel[3] - panel[1] - 48 - code_h
    cols = 2
    rows = max(1, (len(cards) + 1) // 2)
    cw = (panel[2] - panel[0] - 48) // cols
    ch = (grid_h - 16) // rows

    for i, card in enumerate(cards):
        col, row = i % cols, i // cols
        x0 = panel[0] + 24 + col * cw
        y0 = panel[1] + 24 + row * ch
        draw_card(draw, (x0, y0, x0 + cw - 16, y0 + ch - 12), card["title"], card.get("details", []), accent, card.get("status", ""))

    if code:
        draw_code_block(draw, (panel[0] + 24, panel[3] - code_h - 12, panel[2] - 24, panel[3] - 24), code, accent)
    return img


def draw_steam_flow(accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Server Authentication Flow", accent)
    steps = [
        ("1. Request Ticket", "Steam.request_web_api_ticket()", "hex ticket ready"),
        ("2. Authenticate", "authenticate_with_server(url, ticket)", "JWT returned"),
        ("3. Backend API", "Bearer token on REST calls", "achievements + stats sync"),
        ("4. Inventory", "Remote grant / modify items", "client inventory updated"),
    ]
    y = 110
    for i, (title, api, result) in enumerate(steps):
        box = (80, y, W - 80, y + 110)
        draw.rectangle(box, fill=PANEL_ALT, outline=BORDER)
        draw.rectangle((box[0], box[1], box[0] + 4, box[3]), fill=accent)
        draw.text((box[0] + 20, box[1] + 14), title, fill=TEXT, font=fnt(16, True))
        draw.text((box[0] + 20, box[1] + 40), api, fill=accent, font=fnt(12, mono=True))
        draw.text((box[0] + 20, box[1] + 68), result, fill=MUTED, font=fnt(12))
        if i < len(steps) - 1:
            draw.polygon([(W // 2 - 8, box[3] + 4), (W // 2 + 8, box[3] + 4), (W // 2, box[3] + 18)], fill=accent)
        y += 130
    return img


MODULES = [
    {
        "article_folder": "Steam Module",
        "accent": (102, 192, 244),
        "scenes": {
            "cover": {
                "layout": "cover",
                "title": "Steam Module",
                "subtitle": "Native Steamworks integration built into Blazium Engine — achievements, stats, inventory, and server auth.",
                "badges": ["Achievements", "Stats", "Inventory", "Web API Tickets"],
                "output": "cover.jpg",
            },
            "hero": {"layout": "steam_hero", "output": "steam_hero.jpg"},
            "usecase": {"layout": "steam_flow", "output": "steam_usecase.jpg"},
        },
    },
    {
        "article_folder": "Multiuser Editor Module",
        "accent": DEFAULT_ACCENT,
        "scenes": {
            "cover": {
                "layout": "cover",
                "title": "Multiuser Editor",
                "subtitle": "Collaborative editing inside the Blazium editor with CRDT sync, filesystem transfer, and role-based permissions.",
                "badges": ["CRDT Sync", "File Transfer", "Ghost Cursors", "Permissions"],
                "output": "cover.jpg",
            },
            "hero": {"layout": "multiuser_hero", "output": "multiuser_editor_hero.jpg"},
            "usecase": {
                "layout": "usecase",
                "title": "Built for Team Workflows",
                "cards": [
                    {"title": "CRDT Script Sync", "details": ["Concurrent edits merge cleanly", "Deterministic operation order", "Export/import state round-trip"], "status": "135 tests"},
                    {"title": "Filesystem Sync", "details": ["Create, update, delete diffs", "Chunked transfer + SHA1 verify", "Rename detection via hash"], "status": "chunked"},
                    {"title": "Permissions", "details": ["Host / Editor / Viewer tiers", "Override parser for relax/tighten", "Git request/response gates"], "status": "3-tier"},
                    {"title": "Security", "details": ["Path canonicalization", "Safe property/node names", "JWT session authentication"], "status": "validated"},
                ],
                "code": "# 135+ engine tests in test_multiuser_editor.h",
                "output": "multiuser_editor_usecase.jpg",
            },
        },
    },
    {
        "article_folder": "Town SDK Module",
        "accent": (244, 162, 97),
        "scenes": {
            "cover": {
                "layout": "cover",
                "title": "Town SDK Module",
                "subtitle": "Connect Blazium games to Town online servers — regions, movement, battles, and admin tools.",
                "badges": ["Regions", "Battles", "JWT Auth", "Admin API"],
                "output": "cover.jpg",
            },
            "hero": {"layout": "town_hero", "output": "town_sdk_hero.jpg"},
            "usecase": {
                "layout": "usecase",
                "title": "Online Multiplayer Backend",
                "cards": [
                    {"title": "Regions", "details": ["enter_region / leave_region", "send_move with held keys", "Persistent shared zones"], "status": "live"},
                    {"title": "Battles", "details": ["ACTION_ATTACK, BLOCK, DEFEND", "Target by player ID", "leave_battle cleanup"], "status": "turn-based"},
                    {"title": "Admin", "details": ["admin_reload(scope)", "admin_kick(user, reason)", "admin_broadcast(message)"], "status": "server"},
                    {"title": "Reliability", "details": ["Auto-reconnect toggle", "Debug log buffer", "Last error message API"], "status": "dev tools"},
                ],
                "code": 'client.battle_action(id, TownSdkClient.ACTION_ATTACK, target)\nclient.admin_broadcast("Maintenance in 5 min")',
                "output": "town_sdk_usecase.jpg",
            },
        },
    },
    {
        "article_folder": "JustAMCP Module",
        "accent": (187, 134, 252),
        "scenes": {
            "cover": {
                "layout": "cover",
                "title": "JustAMCP Module",
                "subtitle": "Model Context Protocol built into the Blazium editor for AI-driven scene, script, and resource automation.",
                "badges": ["MCP Server", "48+ Tools", "Async Tasks", "HTTP/SSE"],
                "output": "cover.jpg",
            },
            "hero": {"layout": "justamcp_hero", "output": "justamcp_hero.jpg"},
            "usecase": {
                "layout": "usecase",
                "title": "Agent-Driven Editor Automation",
                "cards": [
                    {"title": "JustAMCPServer", "details": ["Streamable HTTP transport", "JSON-RPC tool dispatch", "SSE notifications/messages"], "status": "listening"},
                    {"title": "MCP Protocol", "details": ["Capabilities negotiation", "Pagination for large lists", "Logging setLevel support"], "status": "2025-11-25"},
                    {"title": "Task Manager", "details": ["Async task UUID tracking", "tasks/result blocking", "Cancellation + failure states"], "status": "async"},
                    {"title": "Tool Validation", "details": ["Full catalog contract tests", "Concurrency + HTTP protocol", "Settings override coverage"], "status": "autowork"},
                ],
                "code": "JustAMCPRuntime.port = 7777\nJustAMCPRuntime.enabled = true",
                "output": "justamcp_usecase.jpg",
            },
        },
    },
    {
        "article_folder": "Tiled Importer Module",
        "accent": (224, 122, 95),
        "scenes": {
            "cover": {
                "layout": "cover",
                "title": "Tiled Importer Module",
                "subtitle": "Import Tiled .tmx and .json maps into Blazium — tilesets, object layers, animations, and infinite maps.",
                "badges": [".tmx Import", "Tilesets", "Object Layers", "Animations"],
                "output": "cover.jpg",
            },
            "hero": {"layout": "tiled_hero", "output": "tiled_importer_hero.jpg"},
            "usecase": {
                "layout": "usecase",
                "title": "Designer-Friendly Level Pipeline",
                "cards": [
                    {"title": "Tiled Editor", "details": ["Design maps visually", "Export .tmx or .json", "Custom properties per tile"], "status": "external"},
                    {"title": "Blazium Import", "details": [".tmx → Godot scene", "Automatic tileset linking", "Object layer → nodes"], "status": "editor"},
                    {"title": "Map Features", "details": ["Infinite map support", "Margin and spacing tiles", "Flip flags + GID decode"], "status": "full"},
                    {"title": "Test Coverage", "details": ["simple_map.tmx fixtures", "infinite.tmx edge cases", "margin-space-map validation"], "status": "autowork"},
                ],
                "code": '# res://levels/simple_map.tmx\n# → res://levels/simple_map.tscn',
                "output": "tiled_importer_usecase.jpg",
            },
        },
    },
    {
        "article_folder": "GDK Module",
        "accent": (16, 124, 16),
        "scenes": {
            "cover": {
                "layout": "cover",
                "title": "GDK Module",
                "subtitle": "Microsoft Game Development Kit on PC — XSAPI services, Xbox export, and validated packaging for Blazium.",
                "badges": ["GDK Runtime", "XSAPI", "Xbox Export", "xbox_module_tests"],
                "output": "cover.jpg",
            },
            "hero": {"layout": "gdk_hero", "output": "gdk.jpg"},
            "usecase": {
                "layout": "usecase",
                "title": "Ship Xbox Titles from Blazium",
                "cards": [
                    {"title": "MicrosoftGame.config", "details": ["TitleId, MSAAppId, StoreId", "XML rewrite validation", "Packaging smoke tests"], "status": "tier 0"},
                    {"title": "GDK Toolchain", "details": ["Thunks.dll staging", "Editor plugin integration", "Export platform preset"], "status": "Windows"},
                    {"title": "XSAPI Services", "details": ["Achievements + leaderboards", "Presence + multiplayer activity", "Title storage + store APIs"], "status": "live-ready"},
                    {"title": "Test Tiers", "details": ["Tier 0/1: no credentials", "LIVE_TESTS=1: signed-in flows", "LIVE_WRITE_TESTS=1: stateful"], "status": "gated"},
                ],
                "code": "# xbox_module_tests\n# packaging/test_gdk_toolchain.gd\n# test_achievements.gd (LIVE_TESTS=1)",
                "output": "gdk_usecase.jpg",
            },
        },
    },
]


def render_scene(cfg: dict, accent: tuple[int, int, int]) -> Image.Image:
    layout = cfg["layout"]
    if layout == "cover":
        return draw_cover(cfg["title"], cfg.get("subtitle", ""), cfg.get("badges", []), accent)
    if layout == "steam_hero":
        return draw_hero_steam(accent)
    if layout == "steam_flow":
        return draw_steam_flow(accent)
    if layout == "multiuser_hero":
        return draw_hero_multiuser(accent)
    if layout == "town_hero":
        return draw_hero_town(accent)
    if layout == "justamcp_hero":
        return draw_hero_justamcp(accent)
    if layout == "tiled_hero":
        return draw_hero_tiled(accent)
    if layout == "gdk_hero":
        return draw_hero_gdk(accent)
    if layout == "usecase":
        return draw_usecase_cards(cfg["title"], cfg.get("cards", []), cfg.get("code", ""), accent)
    raise ValueError(f"unknown layout: {layout}")


def save_module(module: dict) -> None:
    accent = tuple(module.get("accent", DEFAULT_ACCENT))
    out_dir = ARTICLES / module["article_folder"] / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    for _key, cfg in module["scenes"].items():
        img = render_scene(cfg, accent)
        path = out_dir / cfg["output"]
        img.save(path, "JPEG", quality=93)
        print(f"wrote {path}")


def main() -> None:
    for module in MODULES:
        save_module(module)


if __name__ == "__main__":
    main()
