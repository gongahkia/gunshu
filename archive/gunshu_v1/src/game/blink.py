import pygame

# FUA add the blink controls and rendering code


def update_player_position(
    player_blink_status,
    old_player_pos,
    new_player_pos,
    dx,
    dy,
    screen_width,
    screen_height,
):
    """
    update the current player position based on whether the player is blinking or not, then normalises the player position to account for edge bounding
    """
    if player_blink_status:  # player blinks

        old_player_pos["x"], old_player_pos["y"] = new_player_pos

    else:  # player not blinking

        old_player_pos["x"] += dx
        old_player_pos["y"] += dy

    old_player_pos["x"] = max(0, min(old_player_pos["x"], screen_width))
    old_player_pos["y"] = max(0, min(old_player_pos["y"], screen_height))

    return old_player_pos


def render_current_blink_status(
    screen,
    player_pos,
    blink_target_radius,
    blink_target_pos,
    remaining_time,
    player_blink_distance,
    player_blink_cooldown_time,
    blink_sprite_width,
    blink_sprite_height,
    active_blink_sprite_filepath,
    inactive_blink_sprite_filepath_array,
):
    """
    renders the blink indicator for where the player is able to blink to, as well as if blink has yet to finish cooling down
    """
    try:
        inactive_blink_sprite_1_filepath = inactive_blink_sprite_filepath_array[0]
        inactive_blink_sprite_2_filepath = inactive_blink_sprite_filepath_array[1]
        inactive_blink_sprite_3_filepath = inactive_blink_sprite_filepath_array[2]
        max_distance_vector = pygame.math.Vector2(
            blink_target_pos[0] - player_pos["x"],
            blink_target_pos[1] - player_pos["y"],
        )
        if max_distance_vector.length() > 0:
            max_distance_vector = (
                max_distance_vector.normalize() * player_blink_distance
            )
        blink_indicator_pos = (
            player_pos["x"] + max_distance_vector.x,
            player_pos["y"] + max_distance_vector.y,
        )
        if remaining_time >= player_blink_cooldown_time:
            active_blink_sprite = pygame.image.load(
                active_blink_sprite_filepath
            ).convert_alpha()
            active_blink_sprite = pygame.transform.scale(
                active_blink_sprite, (blink_sprite_width, blink_sprite_height)
            )
            screen.blit(
                active_blink_sprite,
                (
                    blink_indicator_pos[0] - blink_target_radius,
                    blink_indicator_pos[1] - blink_target_radius,
                ),
            )
        else:
            if remaining_time <= 1:
                inactive_blink_sprite = pygame.image.load(
                    inactive_blink_sprite_1_filepath
                ).convert_alpha()
            elif remaining_time <= 2:
                inactive_blink_sprite = pygame.image.load(
                    inactive_blink_sprite_2_filepath
                ).convert_alpha()
            elif remaining_time <= player_blink_cooldown_time:
                inactive_blink_sprite = pygame.image.load(
                    inactive_blink_sprite_3_filepath
                ).convert_alpha()
            else:
                print("Error: Unknown edgecase has been hit")
                return False
            inactive_blink_sprite = pygame.transform.scale(
                inactive_blink_sprite, (blink_sprite_width, blink_sprite_height)
            )
            screen.blit(
                inactive_blink_sprite,
                (
                    blink_indicator_pos[0] - blink_target_radius,
                    blink_indicator_pos[1] - blink_target_radius,
                ),
            )
            print(f"{remaining_time} till cooldown")
        return True
    except:
        return False
