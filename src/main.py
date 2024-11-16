# ----- REQUIRED IMPORTS -----

import pygame
from display import (
    init_display,
    handle_input_with_mouse_8_directions,
    load_sprite_frames,
    load_sprite_sheet,
    render_with_8_directions,
    quit_display,
)

# ----- PREDEFINED CONSTANTS -----

# PYGAME VALUES

SCREEN_FPS = 72
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SPRITE VALUES

SPRITE_SHEET_FILEPATH = "./placeholder_sprite/static.png"
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24


def main():
    screen, clock = init_display()
    player_pos = {"x": 400, "y": 300}
    positions = {1: player_pos}
    animation_states = {}

    sprite_sheet = pygame.image.load(SPRITE_SHEET_FILEPATH).convert_alpha()

    if not sprite_sheet:
        print(
            "Error: No sprites loaded from the sprite sheet. Please check the sprite sheet path."
        )
        return

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx, dy, direction = handle_input_with_mouse_8_directions(
            (player_pos["x"], player_pos["y"])
        )

        player_pos["x"] += dx
        player_pos["y"] += dy

        player_pos["x"] = max(0, min(player_pos["x"], SCREEN_WIDTH))
        player_pos["y"] = max(0, min(player_pos["y"], SCREEN_HEIGHT))

        # render_with_8_directions(
        #     screen, positions, sprites, animation_states, direction
        # )

        render_with_8_directions(
            screen, positions, sprite_sheet, SPRITE_WIDTH, SPRITE_HEIGHT, 40, direction
        )

        clock.tick(SCREEN_FPS)

    quit_display()


if __name__ == "__main__":
    main()
