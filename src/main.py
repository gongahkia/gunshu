# ----- REQUIRED IMPORTS -----

import pygame
import math
from display import (
    init_display,
    render_with_8_directions,
    quit_display,
    load_sprite_frames,
    load_sprite_sheet,
    check_assets,
)
from player_input import (
    handle_input_with_mouse_8_directions,
)
from inventory import (
    render_player_inventory,
    handle_inventory_click,
    handle_left_mouse_click,
    move_item_to_armour,
    move_item_to_inventory,
    render_dragged_item,
)

# ----- PREDEFINED CONSTANTS -----

# PYGAME VALUES

SCREEN_FPS = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SPRITE VALUES

SPRITE_SHEET_FILEPATH = "./placeholder_sprite/white_static.png"
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24

BLINK_INACTIVE_SPRITE_FILEPATH = "./placeholder_sprite/blink_inactive.png"
BLINK_ACTIVE_SPRITE_FILEPATH = "./placeholder_sprite/blink_active.png"
BLINK_SPRITE_WIDTH = 40
BLINK_SPRITE_HEIGHT = 40

# CURSOR_SPRITE_FILEPATH = "./placeholder_sprite/cursor.png"
# CURSOR_SPRITE_WIDTH = 40
# CURSOR_SPRITE_HEIGHT = 40

# FONT VALUES

FONT_FILEPATH = "./font/zero_liability_please.ttf"
FONT_SIZE = 20

# PLAYER VALUES

PLAYER_BLINK_DISTANCE = 200
PLAYER_BLINK_COOLDOWN_TIME = 3  # in seconds


def main():

    screen, clock = init_display()
    player_pos = {"x": 400, "y": 300}
    positions = {1: player_pos}

    font_asset = pygame.font.Font(FONT_FILEPATH, FONT_SIZE)
    player_sprite_sheet = pygame.image.load(SPRITE_SHEET_FILEPATH).convert_alpha()

    if not check_assets(player_sprite_sheet, font_asset):
        print("exiting due to missing assets...")
        return None

    pygame.mouse.set_visible(False)  # make the mouse invisible

    running = True
    last_blink_time = 0

    inventory_open = False
    dragging_item = False
    dragged_item = None
    drag_start_pos = None

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        (
            dx,
            dy,
            direction,
            player_blink,
            new_player_pos,
            remaining_time,
            last_blink_time,
            blink_target_pos,
            inventory_open_toggle,
        ) = handle_input_with_mouse_8_directions(
            [player_pos["x"], player_pos["y"]], last_blink_time, inventory_open
        )

        inventory_open = inventory_open_toggle

        if inventory_open:

            screen.fill((50, 50, 50, 128))
            inventory_positions, armour_positions = render_player_inventory(
                screen, font_asset
            )
            handle_left_mouse_click(
                dragging_item, screen, inventory_positions, armour_positions
            )

        else:

            if player_blink:
                player_pos["x"], player_pos["y"] = new_player_pos
            else:
                player_pos["x"] += dx
                player_pos["y"] += dy

            player_pos["x"] = max(0, min(player_pos["x"], SCREEN_WIDTH))
            player_pos["y"] = max(0, min(player_pos["y"], SCREEN_HEIGHT))

            render_with_8_directions(
                screen,
                positions,
                player_sprite_sheet,
                SPRITE_WIDTH,
                SPRITE_HEIGHT,
                40,
                direction,
            )

            blink_indicator_radius = 10
            max_distance_vector = pygame.math.Vector2(
                blink_target_pos[0] - player_pos["x"],
                blink_target_pos[1] - player_pos["y"],
            )
            if max_distance_vector.length() > 0:
                max_distance_vector = (
                    max_distance_vector.normalize() * PLAYER_BLINK_DISTANCE
                )
            blink_indicator_pos = (
                player_pos["x"] + max_distance_vector.x,
                player_pos["y"] + max_distance_vector.y,
            )
            if remaining_time >= PLAYER_BLINK_COOLDOWN_TIME:
                active_blink_sprite = pygame.image.load(
                    BLINK_ACTIVE_SPRITE_FILEPATH
                ).convert_alpha()
                active_blink_sprite = pygame.transform.scale(
                    active_blink_sprite, (BLINK_SPRITE_WIDTH, BLINK_SPRITE_HEIGHT)
                )
                screen.blit(
                    active_blink_sprite,
                    (
                        blink_indicator_pos[0] - blink_indicator_radius,
                        blink_indicator_pos[1] - blink_indicator_radius,
                    ),
                )
            else:
                inactive_blink_sprite = pygame.image.load(
                    BLINK_INACTIVE_SPRITE_FILEPATH
                ).convert_alpha()
                inactive_blink_sprite = pygame.transform.scale(
                    inactive_blink_sprite, (BLINK_SPRITE_WIDTH, BLINK_SPRITE_HEIGHT)
                )
                screen.blit(
                    inactive_blink_sprite,
                    (
                        blink_indicator_pos[0] - blink_indicator_radius,
                        blink_indicator_pos[1] - blink_indicator_radius,
                    ),
                )
                print(remaining_time)

            fps = int(clock.get_fps())
            debug_text = f"FPS: {fps} | Position: {math.floor(player_pos['x'])},{math.floor(player_pos['y'])} | Direction: {direction.name}"
            debug_surface = font_asset.render(debug_text, True, (0, 0, 0))

            screen.blit(
                debug_surface,
                (
                    SCREEN_WIDTH - debug_surface.get_width() - 10,
                    SCREEN_HEIGHT - debug_surface.get_height() - 10,
                ),
            )

        pygame.display.flip()
        clock.tick(SCREEN_FPS)

    quit_display()


if __name__ == "__main__":
    main()
