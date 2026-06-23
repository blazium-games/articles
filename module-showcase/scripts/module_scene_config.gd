class_name ModuleSceneConfig
extends RefCounted

const ThemeRes = preload("res://scripts/article_theme.gd")


static func all_modules() -> Array:
	return [steam(), multiuser_editor(), town_sdk(), justamcp(), tiled_importer(), gdk()]


static func steam() -> Dictionary:
	var accent := Color("66c0f4")
	return {
		"id": "steam",
		"article_dir": "../Blazium Game Engine/Steam Module/assets",
		"accent": accent,
		"scenes": {
			"cover": {
				"layout": "cover",
				"title": "Steam Module",
				"subtitle": "Native Steamworks integration built into Blazium Engine — achievements, stats, inventory, and server auth.",
				"badges": ["Achievements", "Stats", "Inventory", "Web API Tickets"],
				"accent": accent,
				"output": "cover.jpg",
			},
			"hero": {
				"layout": "hero",
				"title": "Achievements, Stats & Inventory",
				"mock_title": "Steam API Panel",
				"mock_sections": [
					{"heading": "Achievements", "rows": [
						{"label": "FIRST_WIN", "value": "Defeat the first boss", "ok": true},
						{"label": "COLLECTOR", "value": "Find 10 hidden items", "ok": true},
					]},
					{"heading": "Stats", "rows": [
						{"label": "KILLS", "value": "142 (+1 pending)", "ok": true},
						{"label": "PLAYTIME", "value": "18.5 hours", "ok": true},
					]},
				],
				"code": "Steam.initialize(1742110)\nSteam.set_achievement(\"FIRST_WIN\")\nSteam.store_stats()\nvar items = Steam.get_all_items()",
				"accent": accent,
				"output": "steam_hero.jpg",
			},
			"usecase": {
				"layout": "flow",
				"title": "Server Authentication Flow",
				"cards": [
					{"title": "1. Request Ticket", "api": "Steam.request_web_api_ticket()", "result": "hex ticket ready"},
					{"title": "2. Authenticate", "api": "authenticate_with_server(url, ticket)", "result": "JWT returned"},
					{"title": "3. Backend API", "api": "Bearer token on REST calls", "result": "achievements + stats sync"},
					{"title": "4. Inventory", "api": "Remote grant / modify items", "result": "client inventory updated"},
				],
				"accent": accent,
				"output": "steam_usecase.jpg",
			},
		},
	}


static func multiuser_editor() -> Dictionary:
	var accent := ThemeRes.ACCENT
	return {
		"id": "multiuser_editor",
		"article_dir": "../Blazium Game Engine/Multiuser Editor Module/assets",
		"accent": accent,
		"scenes": {
			"cover": {
				"layout": "cover",
				"title": "Multiuser Editor",
				"subtitle": "Collaborative editing inside the Blazium editor with CRDT sync, filesystem transfer, and role-based permissions.",
				"badges": ["CRDT Sync", "File Transfer", "Ghost Cursors", "Permissions"],
				"accent": accent,
				"output": "cover.jpg",
			},
			"hero": {
				"layout": "hero",
				"title": "Live Collaboration Dock",
				"mock_title": "Session: blazium-dev-room  •  Port 8765",
				"mock_sections": [
					{"heading": "Connected Peers", "rows": [
						{"label": "You (Host)", "value": "Editing Main.tscn", "ok": true},
						{"label": "Alice", "value": "Editing player.gd", "ok": true},
						{"label": "Bob", "value": "Viewing level_01.tscn", "ok": true},
					]},
				],
				"code": "multiuser_editor.host_session(8765, \"secret\")\nmultiuser_editor.join_session(host, 8765)",
				"accent": accent,
				"output": "multiuser_editor_hero.jpg",
			},
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
				"accent": accent,
				"output": "multiuser_editor_usecase.jpg",
			},
		},
	}


static func town_sdk() -> Dictionary:
	var accent := Color("f4a261")
	return {
		"id": "town_sdk",
		"article_dir": "../Blazium Game Engine/Town SDK Module/assets",
		"accent": accent,
		"scenes": {
			"cover": {
				"layout": "cover",
				"title": "Town SDK Module",
				"subtitle": "Connect Blazium games to Town online servers — regions, movement, battles, and admin tools.",
				"badges": ["Regions", "Battles", "JWT Auth", "Admin API"],
				"accent": accent,
				"output": "cover.jpg",
			},
			"hero": {
				"layout": "hero",
				"title": "TownSdkClient",
				"mock_title": "Town SDK Status",
				"mock_sections": [
					{"heading": "Connection", "rows": [
						{"label": "Server", "value": "127.0.0.1:7000  v1.4.2", "ok": true},
						{"label": "Auth", "value": "JWT validated", "ok": true},
					]},
					{"heading": "Region", "rows": [
						{"label": "Current", "value": "town_square (24 players)", "ok": true},
						{"label": "Battle", "value": "battle_7f3a — your turn", "ok": true},
					]},
				],
				"code": "var sdk = Engine.get_singleton(\"TownSDK\")\nsdk.connect_to_server(\"127.0.0.1\", 7000)\nsdk.enter_region(\"town_square\")",
				"accent": accent,
				"output": "town_sdk_hero.jpg",
			},
			"usecase": {
				"layout": "usecase",
				"title": "Online Multiplayer Backend",
				"cards": [
					{"title": "Regions", "details": ["enter_region / leave_region", "send_move with held keys", "Persistent shared zones"], "status": "live"},
					{"title": "Battles", "details": ["ACTION_ATTACK, BLOCK, DEFEND", "Target by player ID", "leave_battle cleanup"], "status": "turn-based"},
					{"title": "Admin", "details": ["admin_reload(scope)", "admin_kick(user, reason)", "admin_broadcast(message)"], "status": "server"},
					{"title": "Reliability", "details": ["Auto-reconnect toggle", "Debug log buffer", "Last error message API"], "status": "dev tools"},
				],
				"code": "client.battle_action(id, TownSdkClient.ACTION_ATTACK, target)",
				"accent": accent,
				"output": "town_sdk_usecase.jpg",
			},
		},
	}


static func justamcp() -> Dictionary:
	var accent := Color("bb86fc")
	return {
		"id": "justamcp",
		"article_dir": "../Blazium Game Engine/JustAMCP Module/assets",
		"accent": accent,
		"scenes": {
			"cover": {
				"layout": "cover",
				"title": "JustAMCP Module",
				"subtitle": "Model Context Protocol built into the Blazium editor for AI-driven scene, script, and resource automation.",
				"badges": ["MCP Server", "48+ Tools", "Async Tasks", "HTTP/SSE"],
				"accent": accent,
				"output": "cover.jpg",
			},
			"hero": {
				"layout": "hero",
				"title": "Tool Catalog",
				"mock_title": "Registered MCP Tools (48 total)",
				"features": [
					"scene_list_nodes — SceneTools",
					"script_read_file — ScriptTools",
					"resource_list — ResourceTools",
					"docs_search — DocumentationTools",
				],
				"code": "var schemas = JustAMCPToolExecutor.get_tool_schemas()\nexecutor.execute_tool(\"scene_list_nodes\", {})",
				"accent": accent,
				"output": "justamcp_hero.jpg",
			},
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
				"accent": accent,
				"output": "justamcp_usecase.jpg",
			},
		},
	}


static func tiled_importer() -> Dictionary:
	var accent := Color("e07a5f")
	return {
		"id": "tiled_importer",
		"article_dir": "../Blazium Game Engine/Tiled Importer Module/assets",
		"accent": accent,
		"scenes": {
			"cover": {
				"layout": "cover",
				"title": "Tiled Importer Module",
				"subtitle": "Import Tiled .tmx and .json maps into Blazium — tilesets, object layers, animations, and infinite maps.",
				"badges": [".tmx Import", "Tilesets", "Object Layers", "Animations"],
				"accent": accent,
				"output": "cover.jpg",
			},
			"hero": {
				"layout": "hero",
				"title": "GodotTsonTileson",
				"mock_title": "world1.tmx — 3 layers, 2 tilesets",
				"features": [
					"##Tile Grid",
					"8×14 preview with flip flags",
					"##Layers",
					"ground, collision, objects",
					"##Objects",
					"12 spawn points, 4 triggers",
				],
				"code": "var map = GodotTsonTileson.new()\nmap.parse_file(\"res://levels/world1.tmx\")",
				"accent": accent,
				"output": "tiled_importer_hero.jpg",
			},
			"usecase": {
				"layout": "usecase",
				"title": "Designer-Friendly Level Pipeline",
				"cards": [
					{"title": "Tiled Editor", "details": ["Design maps visually", "Export .tmx or .json", "Custom properties per tile"], "status": "external"},
					{"title": "Blazium Import", "details": [".tmx → Godot scene", "Automatic tileset linking", "Object layer → nodes"], "status": "editor"},
					{"title": "Map Features", "details": ["Infinite map support", "Margin and spacing tiles", "Flip flags + GID decode"], "status": "full"},
					{"title": "Test Coverage", "details": ["simple_map.tmx fixtures", "infinite.tmx edge cases", "margin-space-map validation"], "status": "autowork"},
				],
				"code": "# res://levels/simple_map.tmx → .tscn",
				"accent": accent,
				"output": "tiled_importer_usecase.jpg",
			},
		},
	}


static func gdk() -> Dictionary:
	var accent := Color("107c10")
	return {
		"id": "gdk",
		"article_dir": "../Blazium Game Engine/GDK Module/assets",
		"accent": accent,
		"scenes": {
			"cover": {
				"layout": "cover",
				"title": "GDK Module",
				"subtitle": "Microsoft Game Development Kit on PC — XSAPI services, Xbox export, and validated packaging for Blazium.",
				"badges": ["GDK Runtime", "XSAPI", "Xbox Export", "xbox_module_tests"],
				"accent": accent,
				"output": "cover.jpg",
			},
			"hero": {
				"layout": "hero",
				"title": "Xbox Platform Integration",
				"mock_title": "GDK Export Panel",
				"mock_sections": [
					{"heading": "GDK Runtime", "rows": [
						{"label": "Thunks.dll", "value": "Loaded from GDK install", "ok": true},
						{"label": "XSAPI", "value": "Achievements, stats, presence", "ok": true},
					]},
					{"heading": "Export", "rows": [
						{"label": "Platform", "value": "Xbox (PC GDK)", "ok": true},
						{"label": "Config", "value": "MicrosoftGame.config valid", "ok": true},
					]},
				],
				"code": "# Xbox export preset\nMicrosoftGame.config\n# xbox_module_tests tier 0",
				"accent": accent,
				"output": "gdk.jpg",
			},
			"usecase": {
				"layout": "usecase",
				"title": "Ship Xbox Titles from Blazium",
				"cards": [
					{"title": "MicrosoftGame.config", "details": ["TitleId, MSAAppId, StoreId", "XML rewrite validation", "Packaging smoke tests"], "status": "tier 0"},
					{"title": "GDK Toolchain", "details": ["Thunks.dll staging", "Editor plugin integration", "Export platform preset"], "status": "Windows"},
					{"title": "XSAPI Services", "details": ["Achievements + leaderboards", "Presence + multiplayer activity", "Title storage + store APIs"], "status": "live-ready"},
					{"title": "Test Tiers", "details": ["Tier 0/1: no credentials", "LIVE_TESTS=1: signed-in flows", "LIVE_WRITE_TESTS=1: stateful"], "status": "gated"},
				],
				"code": "# xbox_module_tests\n# test_gdk_toolchain.gd",
				"accent": accent,
				"output": "gdk_usecase.jpg",
			},
		},
	}
