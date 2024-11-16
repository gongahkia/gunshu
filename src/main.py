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

SCREEN_FPS = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SPRITE VALUES

SPRITE_SHEET_FILEPATH = "./placeholder_sprite/static.png"
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24

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
            screen, positions, sprite_sheet, SPRITE_WIDTH, SPRITE_HEIGHT, 40, direction
        )

        fps = int(clock.get_fps())
        debug_text = f"FPS: {fps}\nPlayer position: {player_pos['x']},{player_pos['y']}\nPlayer direction: {direction.name}"
        debug_surface = font.render(debug_text, True, (0, 0, 0))

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
