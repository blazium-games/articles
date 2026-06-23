extends Control

const ArticlePanelScript = preload("res://scripts/article_panel.gd")

@onready var export_viewport: SubViewport = %ExportViewport


func apply_scene_config(config: Dictionary) -> ArticlePanel:
	for child in export_viewport.get_children():
		child.queue_free()

	var panel := ArticlePanelScript.new()
	panel.layout_mode_name = config.get("layout", "cover")
	panel.module_title = config.get("title", "Module")
	panel.module_subtitle = config.get("subtitle", "")
	panel.mock_title = config.get("mock_title", "Editor Preview")
	panel.accent_color = config.get("accent", Color("3ddc84"))
	panel.code_snippet = config.get("code", "")
	panel.feature_lines = PackedStringArray(config.get("features", []))
	panel.cover_badges = PackedStringArray(config.get("badges", []))
	panel.feature_cards = config.get("cards", [])
	panel.mock_sections = config.get("mock_sections", [])
	panel.custom_minimum_size = Vector2(1280, 720)
	panel.size = Vector2(1280, 720)
	export_viewport.add_child(panel)
	return panel


func capture_config(config: Dictionary) -> Image:
	apply_scene_config(config)
	for _i in range(4):
		await get_tree().process_frame
	RenderingServer.force_draw(true, 0.0)
	await get_tree().process_frame
	export_viewport.size = Vector2i(1280, 720)
	return export_viewport.get_texture().get_image()
