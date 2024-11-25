extends CharacterBody2D

const SQUARE_SPEED = 150
const SQUARE_HEALTH = 3

var square_instance_health = SQUARE_HEALTH

@onready var player = get_node("/root/main_game/player")
@onready var square_sprite = get_node("square-alert")
@onready var square_alert_sprite = preload("res://asset/entity/hostile/square-alert.jpg")
@onready var square_hurt_sprite = preload("res://asset/entity/hostile/square-hurt.jpg")

func _physics_process(_delta: float) -> void:
	var direction = global_position.direction_to(player.global_position)
	velocity = direction * SQUARE_SPEED
	move_and_slide()

func take_damage() -> void:
	print("square took damage...")
	square_instance_health -= 1
	square_sprite.texture = square_hurt_sprite
	if square_instance_health == 0:
		print("square died...")
		queue_free()
