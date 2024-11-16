# ----- REQUIRED IMPORTS -----

import pygame
from helper_functions import (
    init_display,
    handle_input_with_mouse_8_directions,
    load_sprite_frames,
    render_with_8_directions,
    quit_display,
)

# ----- PREDEFINED CONSTANTS -----

SPRITE_FILEPATH = "path/to/sprites"


def main():

    screen, clock = init_display()
    player_pos = {"x": 400, "y": 300}
    positions = {1: player_pos}
    animation_states = {}
    sprites = load_sprite_frames(SPRITE_FILEPATH, 40)

    if not sprites:
        print("Error: No sprites loaded. Please check the sprite path.")
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

        player_pos["x"] = max(0, min(player_pos["x"], 800))
        player_pos["y"] = max(0, min(player_pos["y"], 600))

        render_with_8_directions(
            screen, positions, sprites, animation_states, direction
        )

        clock.tick(30)

    quit_display()


if __name__ == "__main__":
    main()
