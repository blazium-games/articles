class_name ExportBootstrap
extends RefCounted


static func wait_for_render(tree: SceneTree = null, frames: int = 2) -> void:
	if tree == null and Engine.get_main_loop() is SceneTree:
		tree = Engine.get_main_loop()
	if tree == null:
		return
	for _i in range(frames):
		await tree.process_frame
		RenderingServer.force_draw(true, 0.0)
		await tree.process_frame


static func uses_dummy_renderer() -> bool:
	return RenderingServer.get_rendering_device() == null
