# ----- REQUIRED IMPORT -----

import math
import pygame
from camera import (
    Camera,
)

# ----- PREDEFINED VALUES -----

# PYGAME VALUES

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# PLAYER VALUES

PLAYER_SPRITE_SIZE = 40
PLAYER_SPEED = 15
PLAYER_BLINK_DISTANCE = 200
PLAYER_BLINK_COOLDOWN_TIME = 3  # in seconds

# ----- HELPER FUNCTIONS -----

# GENERAL


def init_display():
    """
    initialize pygame and return the screen object and clock
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("gunshu")
    clock = pygame.time.Clock()
    return screen, clock


def load_sprite_frames(target_filepath, sprite_size):
    """
    load individual frame images stored as pngs from the given file path
    """
    import os

    frames = []
    for file_name in sorted(os.listdir(target_filepath)):
        if file_name.endswith(".png"):
            full_filepath = os.path.join(target_filepath, file_name)
            print(full_filepath)
            frame = pygame.image.load(full_filepath).convert_alpha()
            frame = pygame.transform.scale(frame, (sprite_size, sprite_size))
            print(f"scaled frame size: {frame.get_size()}")
            frames.append(frame)
    return frames


def load_sprite_sheet(target_filepath, frame_width, frame_height, output_sprite_size):
    """
    load individual sprite frames from a sprite sheet
    """
    try:
        sprite_sheet = pygame.image.load(target_filepath).convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frames = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sprite_sheet.subsurface(
                pygame.Rect(x, y, frame_width, frame_height)
            )
            frame = pygame.transform.scale(
                frame, (output_sprite_size, output_sprite_size)
            )
            frames.append(frame)
    return frames


def load_directional_sprite(
    sprite_sheet, frame_width, frame_height, direction, output_sprite_size
):
    """
    get the frame corresponding to the direction from the sprite sheet using direction enum
    """
    direction_str = direction.value
    DIRECTIONS = [
        "north",
        "northeast",
        "east",
        "southeast",
        "south",
        "southwest",
        "west",
        "northwest",
    ]
    direction_index = DIRECTIONS.index(direction_str)
    frames_per_row = sprite_sheet.get_width() // frame_width
    x = (direction_index % frames_per_row) * frame_width
    y = (direction_index // frames_per_row) * frame_height
    frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
    frame = pygame.transform.scale(frame, (output_sprite_size, output_sprite_size))
    return frame


def render_with_8_directions(
    screen,
    positions,
    sprites,
    frame_width,
    frame_height,
    output_sprite_size,
    direction,
    camera,
):
    """
    render the game state with player facing 8 possible directions
    """
    screen.fill((255, 255, 255))
    for player_id, pos in positions.items():
        x, y = camera.apply_position((pos["x"], pos["y"]))
        frame = load_directional_sprite(
            sprites, frame_width, frame_height, direction, output_sprite_size
        )
        screen.blit(
            frame,
            (x - output_sprite_size // 2, y - output_sprite_size // 2),
        )
    pygame.display.flip()


def quit_display():
    """
    quit pygame
    """
    pygame.quit()
    print("exiting pygame now...")


def check_assets(player_sprite_sheet, font_asset):
    """
    FUA continue adding asset checks here and update the docstring as required

    checks the following assets - player_sprite_sheet, font
    """
    if not player_sprite_sheet:
        print(
            "Error: No sprites loaded from the sprite sheet. Please check the sprite filepath."
        )
        return False
    if not font_asset:
        print(
            "Error: No font loaded from the specified filepath. Please check the font filepath."
        )
        return False
    return True


def write_debug_information(fps_count, player_pos, direction, screen, font_asset):
    """
    FUA continue adding debug information to be written here and update the docstring as required

    writes relevant debug information to the screen
    """
    try:
        debug_text = f"FPS: {fps_count} | Position: {math.floor(player_pos['x'])},{math.floor(player_pos['y'])} | Direction: {direction.name}"
        debug_surface = font_asset.render(debug_text, True, (0, 0, 0))
        screen.blit(
            debug_surface,
            (
                SCREEN_WIDTH - debug_surface.get_width() - 10,
                SCREEN_HEIGHT - debug_surface.get_height() - 10,
            ),
        )
        return True
    except:
        return False
