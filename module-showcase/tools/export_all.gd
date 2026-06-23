extends SceneTree

const ModuleSceneConfig = preload("res://scripts/module_scene_config.gd")
const ExportBootstrap = preload("res://tools/export_bootstrap.gd")

const EXPORTER_SCENE := preload("res://scenes/exporter.tscn")


func _initialize() -> void:
	if ExportBootstrap.uses_dummy_renderer():
		push_error("RendererDummy cannot export SubViewport textures — run without --headless")
		quit(1)
		return

	var root := Window.new()
	root.title = "Module Showcase Export"
	root.size = Vector2i(1280, 720)
	root.mode = Window.MODE_MINIMIZED
	root.visible = false
	root.add_child(EXPORTER_SCENE.instantiate())
	root.set_content_scale_size(Vector2i(1280, 720))
	root.set_content_scale_mode(Window.CONTENT_SCALE_MODE_DISABLED)
	root.set_content_scale_aspect(Window.CONTENT_SCALE_ASPECT_IGNORE)

	var exporter: Node = root.get_child(0)
	if not exporter.has_method("capture_config"):
		push_error("Exporter missing capture_config")
		quit(1)
		return

	root.call_deferred("show")
	root.call_deferred("move_to_foreground")

	call_deferred("_run_export", root, exporter)


func _run_export(root: Window, exporter: Node) -> void:
	await ExportBootstrap.wait_for_render(self, 3)

	var project_root := ProjectSettings.globalize_path("res://")
	var exports_root := project_root.path_join("exports")
	DirAccess.make_dir_recursive_absolute(exports_root)

	var failures := 0
	for module in ModuleSceneConfig.all_modules():
		var module_id: String = module["id"]
		var module_exports := exports_root.path_join(module_id)
		DirAccess.make_dir_recursive_absolute(module_exports)

		var article_assets := project_root.path_join(module["article_dir"])
		DirAccess.make_dir_recursive_absolute(article_assets)

		for scene_key in module["scenes"]:
			var scene_cfg: Dictionary = module["scenes"][scene_key]
			scene_cfg["accent"] = module["accent"]
			var output_name: String = scene_cfg["output"]
			print("[export] %s / %s -> %s" % [module_id, scene_key, output_name])

			var image: Image = await exporter.capture_config(scene_cfg)
			if image == null or image.is_empty():
				push_error("Failed to capture %s/%s" % [module_id, scene_key])
				failures += 1
				continue

			var png_path := module_exports.path_join(output_name.replace(".jpg", ".png"))
			var jpg_path := article_assets.path_join(output_name)
			var err := image.save_png(png_path)
			if err != OK:
				push_error("save_png failed: %s" % png_path)
				failures += 1
				continue
			err = image.save_jpg(jpg_path, 0.92)
			if err != OK:
				push_error("save_jpg failed: %s" % jpg_path)
				failures += 1
				continue
			print("[export] wrote %s" % jpg_path)

	root.queue_free()
	print("[export] done failures=%d" % failures)
	quit(1 if failures > 0 else 0)
