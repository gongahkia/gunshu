extends CharacterBody2D

# ----- CONSTANT DEFINITIONS -----

const PLAYER_SPEED = 500 
var mouse_position = null
var direction_textures = {
	"north": preload("res://asset/entity/player/player_north.jpg"),
	"northeast": preload("res://asset/entity/player/player_north_east.jpg"),
	"east": preload("res://asset/entity/player/player_east.jpg"),
	"southeast": preload("res://asset/entity/player/player_south_east.jpg"),
	"south": preload("res://asset/entity/player/player_south.jpg"),
	"southwest": preload("res://asset/entity/player/player_south_west.jpg"),
	"west": preload("res://asset/entity/player/player_west.jpg"),
	"northwest": preload("res://asset/entity/player/player_north_west.jpg"),
}
@onready var sprite = get_node("player_idle")

# ----- HELPER FUNCTIONS -----

func _physics_process(_delta: float) -> void:
	var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down") # i guess there's a fixed order to this
	velocity = direction * PLAYER_SPEED
	move_and_slide()
	mouse_position = get_global_mouse_position()
	update_sprite_direction()
	if Input.is_action_just_pressed("attack_parry"): # bound to left mouse button
		print("ATTACK/PARRY (left mouse button clicked)")
		var katana = get_node("generic_weapon")
		# FUA to add checks here to detect whether its a parry or slash in the future
		katana.slash()
		print("slashing...")
	elif Input.is_action_just_pressed("block"): # bound to right mouse button
		print("BLOCK (right mouse button clicked)")

func update_sprite_direction() -> void:
	var dir_to_mouse = (mouse_position - global_position).normalized()
	var angle = dir_to_mouse.angle()
	angle = wrapf(angle, 0, TAU)
	var direction = ""
	if angle < PI / 8 or angle > 15 * PI / 8:
		direction = "east"
	elif angle < 3 * PI / 8:
		direction = "southeast"
	elif angle < 5 * PI / 8:
		direction = "south"
	elif angle < 7 * PI / 8:
		direction = "southwest"
	elif angle < 9 * PI / 8:
		direction = "west"
	elif angle < 11 * PI / 8:
		direction = "northwest"
	elif angle < 13 * PI / 8:
		direction = "north"
	else:
		direction = "northeast"
	# print("Angle: ", angle, " Direction: ", direction)
	sprite.texture = direction_textures[direction]	
