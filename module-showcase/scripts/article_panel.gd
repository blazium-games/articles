class_name ArticlePanel
extends Control

const ThemeRes = preload("res://scripts/article_theme.gd")

@export var module_title: String = "Module"
@export var module_subtitle: String = ""
@export var accent_color: Color = ThemeRes.ACCENT
@export_multiline var code_snippet: String = ""
@export var feature_lines: PackedStringArray = PackedStringArray()
@export var cover_badges: PackedStringArray = PackedStringArray()
@export var feature_cards: Array = []
@export var mock_sections: Array = []
@export var layout_mode_name: String = "cover"
@export var mock_title: String = "Editor Preview"


func _ready() -> void:
	custom_minimum_size = ThemeRes.SIZE
	size = ThemeRes.SIZE
	queue_redraw()


func _draw() -> void:
	var rect := Rect2(Vector2.ZERO, size)
	draw_rect(rect, ThemeRes.BG)
	match layout_mode_name:
		"cover":
			_draw_cover(rect)
		"hero":
			_draw_hero(rect)
		"usecase":
			_draw_usecase(rect)
		"flow":
			_draw_flow(rect)
		_:
			_draw_cover(rect)


func _draw_cover(rect: Rect2) -> void:
	var panel := Rect2(80, 120, rect.size.x - 160, rect.size.y - 240)
	draw_rect(panel, ThemeRes.PANEL)
	draw_rect(panel, ThemeRes.BORDER, false, 2.0)
	draw_rect(Rect2(panel.position.x, panel.position.y, 6, panel.size.y), accent_color)
	_draw_text_block(module_title, panel.position + Vector2(48, 64), ThemeRes.FONT_TITLE, ThemeRes.TEXT)
	if not module_subtitle.is_empty():
		_draw_text_block(module_subtitle, panel.position + Vector2(48, 150), ThemeRes.FONT_SUBTITLE, ThemeRes.MUTED, panel.size.x - 96)
	var bx := panel.position.x + 48.0
	var by := panel.position.y + panel.size.y - 100.0
	for badge in cover_badges:
		var tw := ThemeDB.fallback_font.get_string_size(badge, HORIZONTAL_ALIGNMENT_LEFT, -1, ThemeRes.FONT_SMALL).x + 20.0
		draw_rect(Rect2(bx, by, tw, 24), ThemeRes.PANEL_ALT)
		draw_rect(Rect2(bx, by, tw, 24), accent_color, false, 1.0)
		draw_string(ThemeDB.fallback_font, Vector2(bx + 10, by + 4), badge, HORIZONTAL_ALIGNMENT_LEFT, -1, ThemeRes.FONT_SMALL, accent_color)
		bx += tw + 8.0
	_draw_text_block("Blazium Game Engine", panel.position + Vector2(48, panel.size.y - 40), ThemeRes.FONT_SMALL, ThemeRes.MUTED)


func _draw_hero(rect: Rect2) -> void:
	_draw_header(rect, module_title)
	var left := Rect2(48, 96, 572, rect.size.y - 144)
	draw_rect(left, ThemeRes.PANEL)
	draw_rect(left, ThemeRes.BORDER, false, 1.0)
	_draw_text_block(mock_title, left.position + Vector2(16, 12), ThemeRes.FONT_SMALL, ThemeRes.MUTED)
	draw_line(Vector2(left.position.x, left.position.y + 32), Vector2(left.position.x + left.size.x, left.position.y + 32), ThemeRes.BORDER)
	var y := left.position.y + 44.0
	if not mock_sections.is_empty():
		for section in mock_sections:
			if section is Dictionary:
				_draw_text_block(str(section.get("heading", "")), Vector2(left.position.x + 16, y), 14, accent_color)
				y += 24.0
				for row in section.get("rows", []):
					if row is Dictionary:
						y = _draw_status_row(left, y, str(row.get("label", "")), str(row.get("value", "")), bool(row.get("ok", true)))
				y += 8.0
	else:
		for line in feature_lines:
			if line.begins_with("##"):
				_draw_text_block(line.trim_prefix("##").strip_edges(), Vector2(left.position.x + 16, y), ThemeRes.FONT_HEADING, accent_color)
				y += 32.0
			else:
				_draw_text_block("• " + line, Vector2(left.position.x + 16, y), ThemeRes.FONT_BODY, ThemeRes.TEXT, left.size.x - 32)
				y += 26.0
	var right := Rect2(640, 96, rect.size.x - 688, rect.size.y - 144)
	draw_rect(right, ThemeRes.CODE_BG)
	draw_rect(right, ThemeRes.BORDER, false, 1.0)
	_draw_code_block(code_snippet, right.position + Vector2(12, 28), right.size - Vector2(24, 36))


func _draw_usecase(rect: Rect2) -> void:
	_draw_header(rect, module_subtitle if not module_subtitle.is_empty() else module_title)
	var panel := Rect2(48, 96, rect.size.x - 96, rect.size.y - 144)
	draw_rect(panel, ThemeRes.PANEL)
	draw_rect(panel, ThemeRes.BORDER, false, 1.0)
	var code_h := 130.0 if not code_snippet.is_empty() else 0.0
	var grid_h := panel.size.y - 48.0 - code_h
	var cols := 2
	var card_count := maxi(feature_cards.size(), 1)
	var rows := ceili(float(card_count) / float(cols))
	var cw := (panel.size.x - 48.0) / cols
	var ch := (grid_h - 16.0) / rows
	for i in range(feature_cards.size()):
		var card: Dictionary = feature_cards[i]
		var col := i % cols
		var row := i / cols
		var cell := Rect2(
			panel.position.x + 24 + col * cw,
			panel.position.y + 24 + row * ch,
			cw - 16,
			ch - 12
		)
		_draw_card(cell, str(card.get("title", "")), card.get("details", []), str(card.get("status", "")))
	if not code_snippet.is_empty():
		var code_rect := Rect2(panel.position.x + 24, panel.position.y + panel.size.y - code_h - 12, panel.size.x - 48, code_h)
		draw_rect(code_rect, ThemeRes.CODE_BG)
		_draw_code_block(code_snippet, code_rect.position + Vector2(12, 10), code_rect.size - Vector2(24, 20))


func _draw_flow(rect: Rect2) -> void:
	_draw_header(rect, module_subtitle if not module_subtitle.is_empty() else module_title)
	var y := 110.0
	for i in range(feature_cards.size()):
		var step: Dictionary = feature_cards[i]
		var box := Rect2(80, y, rect.size.x - 160, 110)
		draw_rect(box, ThemeRes.PANEL_ALT)
		draw_rect(Rect2(box.position.x, box.position.y, 4, box.size.y), accent_color)
		_draw_text_block(str(step.get("title", "")), box.position + Vector2(20, 14), 16, ThemeRes.TEXT)
		_draw_text_block(str(step.get("api", "")), box.position + Vector2(20, 40), ThemeRes.FONT_CODE, accent_color)
		_draw_text_block(str(step.get("result", "")), box.position + Vector2(20, 68), ThemeRes.FONT_BODY, ThemeRes.MUTED)
		if i < feature_cards.size() - 1:
			var cx := rect.size.x * 0.5
			draw_colored_polygon(PackedVector2Array([Vector2(cx - 8, box.position.y + box.size.y + 4), Vector2(cx + 8, box.position.y + box.size.y + 4), Vector2(cx, box.position.y + box.size.y + 18)]), accent_color)
		y += 130.0


func _draw_card(cell: Rect2, title: String, details: Array, status: String) -> void:
	draw_rect(cell, ThemeRes.PANEL_ALT)
	draw_rect(cell, ThemeRes.BORDER, false, 1.0)
	draw_rect(Rect2(cell.position.x, cell.position.y, 4, cell.size.y), accent_color)
	_draw_text_block(title, cell.position + Vector2(16, 12), 15, ThemeRes.TEXT)
	if not status.is_empty():
		draw_string(ThemeDB.fallback_font, Vector2(cell.position.x + cell.size.x - 80, cell.position.y + 12), status, HORIZONTAL_ALIGNMENT_LEFT, -1, ThemeRes.FONT_SMALL, accent_color)
	var y := cell.position.y + 38.0
	for detail in details:
		_draw_text_block("• " + str(detail), Vector2(cell.position.x + 20, y), ThemeRes.FONT_BODY, ThemeRes.MUTED, cell.size.x - 28)
		y += 20.0
		if y > cell.position.y + cell.size.y - 12:
			break


func _draw_status_row(panel: Rect2, y: float, label: String, value: String, ok: bool) -> float:
	var row := Rect2(panel.position.x + 12, y, panel.size.x - 24, 36)
	draw_rect(row, Color(0.125, 0.137, 0.165))
	draw_rect(row, ThemeRes.BORDER, false, 1.0)
	draw_circle(Vector2(row.position.x + 18, row.position.y + 18), 8, accent_color if ok else ThemeRes.MUTED)
	_draw_text_block(label, Vector2(row.position.x + 36, row.position.y + 6), 13, ThemeRes.TEXT)
	_draw_text_block(value, Vector2(row.position.x + 36, row.position.y + 22), 11, ThemeRes.MUTED)
	if ok:
		draw_string(ThemeDB.fallback_font, Vector2(row.position.x + row.size.x - 70, row.position.y + 10), "active", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, ThemeRes.ACCENT)
	return y + 42.0


func _draw_header(rect: Rect2, title: String) -> void:
	draw_rect(Rect2(0, 0, rect.size.x, 72), ThemeRes.PANEL)
	draw_rect(Rect2(0, 68, rect.size.x, 4), accent_color)
	_draw_text_block(title, Vector2(48, 20), ThemeRes.FONT_HEADING, ThemeRes.TEXT)


func _draw_text_block(text: String, pos: Vector2, font_size: int, color: Color, max_width: float = 0.0) -> void:
	var font := ThemeDB.fallback_font
	if max_width <= 0.0:
		draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)
		return
	var words := text.split(" ")
	var line := ""
	var y := pos.y
	for word in words:
		var test := line + (" " if not line.is_empty() else "") + word
		if font.get_string_size(test, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x > max_width and not line.is_empty():
			draw_string(font, Vector2(pos.x, y), line, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)
			line = word
			y += font_size + 6
		else:
			line = test
	if not line.is_empty():
		draw_string(font, Vector2(pos.x, y), line, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)


func _draw_code_block(text: String, pos: Vector2, area: Vector2) -> void:
	draw_string(ThemeDB.fallback_font, pos, "GDScript", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, ThemeRes.MUTED)
	var y := pos.y
	for line in text.split("\n"):
		draw_string(ThemeDB.fallback_font, Vector2(pos.x, y), line, HORIZONTAL_ALIGNMENT_LEFT, area.x, ThemeRes.FONT_CODE, accent_color.lightened(0.15))
		y += ThemeRes.FONT_CODE + 4
		if y > pos.y + area.y - 8:
			break
