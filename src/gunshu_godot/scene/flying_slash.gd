extends Area2D

var slash_travelled_distance = 0
const SLASH_SPEED = 100
const SLASH_RANGE = 1200

func _physics_process(delta: float) -> void:
	var direction = Vector2.RIGHT.rotated(rotation)
	global_position +=  direction * SLASH_SPEED * delta # makes the slash speed client dependent
	slash_travelled_distance += SLASH_SPEED * delta
	if slash_travelled_distance > SLASH_RANGE:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	print("slash collided with another entity...")
	queue_free()
	if body.has_method("take_damage"):
		body.take_damage()
	
