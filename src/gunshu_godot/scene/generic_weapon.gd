extends Node2D

var smoothed_mouse_pos: Vector2

func _process(_delta: float) -> void:
	smoothed_mouse_pos = lerp(smoothed_mouse_pos, get_global_mouse_position(), 0.3)
	look_at(smoothed_mouse_pos)

func slash() -> void:
	const FLYING_SLASH = preload("res://scene/flying_slash.tscn")
	var new_flying_slash = FLYING_SLASH.instantiate()
	new_flying_slash.global_position = get_node("weapon_pivot/KatanaWeapon/firing_point").global_position
	new_flying_slash.global_rotation = get_node("weapon_pivot/KatanaWeapon/firing_point").global_rotation
	get_node("weapon_pivot/KatanaWeapon/firing_point").add_child(new_flying_slash)
