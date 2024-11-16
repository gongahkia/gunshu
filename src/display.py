# ----- REQUIRED IMPORT -----

import pygame
from enum import Enum
import math

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

# PLAYER CONTROL ENUM

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    NORTHEAST = "northeast"
    SOUTHEAST = "southeast"
    SOUTHWEST = "southwest"
    NORTHWEST = "northwest"
    STATIC = "static"

# ----- HELPER FUNCTIONS -----

def init_display():
    """
    initialize pygame and return the screen object and clock
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("gunshu")
    clock = pygame.time.Clock()
    return screen, clock


def calculate_direction(player_pos, mouse_pos):
    """
    calculate the direction based on the angle between the player and the mouse, supporting 8 cardinal directions
    """
    player_x, player_y = player_pos
    mouse_x, mouse_y = mouse_pos
    angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
    angle_degrees = math.degrees(angle)
    if angle_degrees < 0:
        angle_degrees += 360
    if 337.5 <= angle_degrees or angle_degrees < 22.5:
        return Direction.EAST  
    elif 22.5 <= angle_degrees < 67.5:
        return Direction.SOUTHEAST  
    elif 67.5 <= angle_degrees < 112.5:
        return Direction.SOUTH  
    elif 112.5 <= angle_degrees < 157.5:
        return Direction.SOUTHWEST  
    elif 157.5 <= angle_degrees < 202.5:
        return Direction.WEST  
    elif 202.5 <= angle_degrees < 247.5:
        return Direction.NORTHWEST  
    elif 247.5 <= angle_degrees < 292.5:
        return Direction.NORTH  
    elif 292.5 <= angle_degrees < 337.5:
        return Direction.NORTHEAST  


def handle_input_with_mouse_8_directions(player_pos):
    """
    handle player input and mouse position to update movement and 8 cardinal directions
    """
    dx, dy = 0, 0
    direction = Direction.STATIC
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED
    if keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED
    mouse_pos = pygame.mouse.get_pos()
    direction = calculate_direction(player_pos, mouse_pos)
    return dx, dy, direction


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


def render_with_8_directions(screen, positions, sprites, animation_states, direction):
    """
    render the game state with player facing 8 possible directions
    """
    screen.fill(WHITE)
    for player_id, pos in positions.items():
        animation_states[player_id] = (animation_states.get(player_id, 0) + 1) % len(
            sprites
        )
        frame = sprites[animation_states[player_id]]
        if direction == Direction.NORTH:
            frame = pygame.transform.rotate(frame, 180)
        elif direction == Direction.NORTHEAST:
            frame = pygame.transform.rotate(frame, 135)
        elif direction == Direction.EAST:
            frame = pygame.transform.rotate(frame, 90)
        elif direction == Direction.SOUTHEAST:
            frame = pygame.transform.rotate(frame, 45)
        elif direction == Direction.SOUTH:
            frame = pygame.transform.rotate(frame, 0)
        elif direction == Direction.SOUTHWEST:
            frame = pygame.transform.rotate(frame, -45)
        elif direction == Direction.WEST:
            frame = pygame.transform.rotate(frame, -90)
        elif direction == Direction.NORTHWEST:
            frame = pygame.transform.rotate(frame, -135)
        screen.blit(
            frame, (pos["x"] - PLAYER_SPRITE_SIZE // 2, pos["y"] - PLAYER_SPRITE_SIZE // 2)
        )
    pygame.display.flip()


def quit_display():
    """
    quit pygame
    """
    pygame.quit()
    print("exiting pygame now...")