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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SHEET_FILEPATH = "path/to/sprites"
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64


def main():
    screen, clock = init_display()
    player_pos = {"x": 400, "y": 300}
    positions = {1: player_pos}
    animation_states = {}

    sprites = load_sprite_sheet(SPRITE_SHEET_FILEPATH, SPRITE_WIDTH, SPRITE_HEIGHT, 40)

    if not sprites:
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

        render_with_8_directions(
            screen, positions, sprites, animation_states, direction
        )

        clock.tick(30)

    quit_display()


if __name__ == "__main__":
    main()
