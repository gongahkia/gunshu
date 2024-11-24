extends Node2D

var smoothed_mouse_pos: Vector2

func _process(_delta: float) -> void:
	smoothed_mouse_pos = lerp(smoothed_mouse_pos, get_global_mouse_position(), 0.3)
	look_at(smoothed_mouse_pos)
