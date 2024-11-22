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
    write_debug_information,
)
from player_input import (
    handle_input_with_mouse_8_directions,
)
from inventory import (
    render_player_inventory_base,
    render_responsive_dragging,
    handle_inventory_click,
    move_item_to_armour,
    move_item_to_inventory,
    render_dragged_item,
)
from blink import (
    update_player_position,
    render_current_blink_status,
)
from powerup_bar import (
    render_powerup_bar,
)
from camera import (
    Camera,
)

# ----- PREDEFINED CONSTANTS -----

# PYGAME VALUES

SCREEN_FPS = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SPRITE VALUES

SPRITE_SHEET_FILEPATH = "./sprite/player/purple_static.png"
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24

BLINK_INACTIVE_SPRITE_FILEPATH_ARRAY = [
    "./sprite/player/blink_inactive_1.png",
    "./sprite/player/blink_inactive_2.png",
    "./sprite/player/blink_inactive_3.png",
]
BLINK_ACTIVE_SPRITE_FILEPATH = "./sprite/player/blink_active.png"
BLINK_SPRITE_WIDTH = 40
BLINK_SPRITE_HEIGHT = 40
BLINK_TARGET_RADIUS = 10

# POWERUP BAR VALUES

POWERUP_JSON_FILEPATH = "./powerup.json"
PLAYER_POWERUP_ARRAY = [
    "cosmos_ofuda",
    "death_ofuda",
    "cosmos_ofuda",
    "katana_weapon",
]  # FUA this is to be edited dynamically in the future

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

    active_camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    active_camera.set_target(player_pos)

    font_asset = pygame.font.Font(FONT_FILEPATH, FONT_SIZE)
    player_sprite_sheet = pygame.image.load(SPRITE_SHEET_FILEPATH).convert_alpha()

    if not check_assets(player_sprite_sheet, font_asset):
        print("Error: Exiting due to missing assets.")
        return None

    pygame.mouse.set_visible(False)  # make the mouse invisible

    running = True
    last_blink_time = 0

    inventory_open = False
    dragging_item = False

    # dragged_item = None
    # drag_start_pos = None

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

        if inventory_open:  # inventory open

            inventory_positions, armour_positions = render_player_inventory_base(
                screen, font_asset
            )
            render_responsive_dragging(
                dragging_item, screen, inventory_positions, armour_positions
            )

        else:  # inventory not open

            player_pos = update_player_position(
                player_blink,
                player_pos,
                new_player_pos,
                dx,
                dy,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
            )

            active_camera.update(player_pos)
            screen.fill((255, 255, 255))

            render_with_8_directions(
                screen,
                positions,
                player_sprite_sheet,
                SPRITE_WIDTH,
                SPRITE_HEIGHT,
                40,
                direction,
                active_camera,
            )

            if not render_current_blink_status(
                screen,
                player_pos,
                BLINK_TARGET_RADIUS,
                blink_target_pos,
                remaining_time,
                PLAYER_BLINK_DISTANCE,
                PLAYER_BLINK_COOLDOWN_TIME,
                BLINK_SPRITE_WIDTH,
                BLINK_SPRITE_HEIGHT,
                BLINK_ACTIVE_SPRITE_FILEPATH,
                BLINK_INACTIVE_SPRITE_FILEPATH_ARRAY,
            ):
                print("Error: Unable to render player's blink indicator")

            if not render_powerup_bar(
                screen, font_asset, PLAYER_POWERUP_ARRAY, POWERUP_JSON_FILEPATH
            ):
                print("Error: Unable to render powerup bar")

            fps = int(clock.get_fps())
            if not write_debug_information(
                fps, player_pos, direction, screen, font_asset
            ):
                print("Error: Exiting due to missing debug information.")

        pygame.display.flip()
        clock.tick(SCREEN_FPS)

    quit_display()


# ----- MAIN EXECUTION CODE -----

if __name__ == "__main__":
    main()
