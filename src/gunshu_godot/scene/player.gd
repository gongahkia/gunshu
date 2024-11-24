extends CharacterBody2D

# ----- CONSTANT DEFINITIONS -----

const PLAYER_SPEED = 500 
var mouse_position = null
var direction_textures = {
	"north": preload("res://asset/png/player/player_north.png"),
	"northeast": preload("res://asset/png/player/player_north_east.png"),
	"east": preload("res://asset/png/player/player_east.png"),
	"southeast": preload("res://asset/png/player/player_south_east.png"),
	"south": preload("res://asset/png/player/player_south.png"),
	"southwest": preload("res://asset/png/player/player_south_west.png"),
	"west": preload("res://asset/png/player/player_west.png"),
	"northwest": preload("res://asset/png/player/player_north_west.png"),
}
@onready var sprite = get_node("player_idle")

# ----- HELPER FUNCTIONS -----

func _physics_process(_delta: float) -> void:
	var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down") # i guess there's a fixed order to this
	velocity = direction * PLAYER_SPEED
	move_and_slide()
	mouse_position = get_global_mouse_position()
	update_sprite_direction()

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
