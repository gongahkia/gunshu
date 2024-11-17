# ----- REQUIRED IMPORTS -----

import pygame
import math
from display import (
    init_display,
    handle_input_with_mouse_8_directions,
    load_sprite_frames,
    load_sprite_sheet,
    render_with_8_directions,
    quit_display,
)
from inventory import render_player_inventory

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


def main():

    screen, clock = init_display()
    player_pos = {"x": 400, "y": 300}
    positions = {1: player_pos}
    animation_states = {}

    font = pygame.font.Font(FONT_FILEPATH, FONT_SIZE)
    sprite_sheet = pygame.image.load(SPRITE_SHEET_FILEPATH).convert_alpha()

    if not sprite_sheet:
        print(
            "Error: No sprites loaded from the sprite sheet. Please check the sprite filepath."
        )
        return None

    if not font:
        print(
            "Error: No font loaded from the specified filepath. Please check the font filepath."
        )
        return None

    # cursor_sprite = pygame.image.load(CURSOR_SPRITE_FILEPATH).convert_alpha()
    # cursor_sprite = pygame.transform.scale(
    #     cursor_sprite, (CURSOR_SPRITE_WIDTH, CURSOR_SPRITE_HEIGHT)
    # )
    # cursor_rect = cursor_sprite.get_rect()
    pygame.mouse.set_visible(False)

    running = True
    last_blink_time = 0
    inventory_open = False

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
            render_player_inventory(screen, font)

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
                sprite_sheet,
                SPRITE_WIDTH,
                SPRITE_HEIGHT,
                40,
                direction,
            )

            PLAYER_BLINK_DISTANCE = 200
            PLAYER_BLINK_COOLDOWN_TIME = 3  # in seconds

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
                # green_blink_indicator_color = (0, 255, 0)
                # pygame.draw.circle(
                #     screen,
                #     green_blink_indicator_color,
                #     blink_indicator_pos,
                #     blink_indicator_radius,
                # )
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
                # red_blink_indicator_color = (255, 0, 0)
                # pygame.draw.circle(
                #     screen,
                #     red_blink_indicator_color,
                #     blink_indicator_pos,
                #     blink_indicator_radius,
                # )
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
            debug_surface = font.render(debug_text, True, (0, 0, 0))

            screen.blit(
                debug_surface,
                (
                    SCREEN_WIDTH - debug_surface.get_width() - 10,
                    SCREEN_HEIGHT - debug_surface.get_height() - 10,
                ),
            )

            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # cursor_rect.topleft = (
            #     mouse_x - cursor_rect.width // 2,
            #     mouse_y - cursor_rect.height // 2,
            # )
            # screen.blit(cursor_sprite, cursor_rect)

        pygame.display.flip()
        clock.tick(SCREEN_FPS)

    quit_display()


if __name__ == "__main__":
    main()
