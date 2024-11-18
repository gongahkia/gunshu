# ----- REQUIRED IMPORT -----

import pygame
import math
from enum import Enum

# ----- PREDEFINED VALUES -----

# PLAYER VALUES

PLAYER_SPRITE_SIZE = 40
PLAYER_SPEED = 15
PLAYER_BLINK_DISTANCE = 200
PLAYER_BLINK_COOLDOWN_TIME = 3  # in seconds

# USER CONTROLS

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


def handle_input_with_mouse_8_directions(player_pos, last_blink_time, inventory_open):
    """
    handle player input and mouse position to update movement and 8 cardinal directions
    """

    dx, dy = 0, 0
    direction = Direction.STATIC
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    direction = calculate_direction(player_pos, mouse_pos)
    player_blink = False
    current_time = pygame.time.get_ticks() / 1000
    remaining_time = current_time - last_blink_time

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += PLAYER_SPEED

    if keys[pygame.K_LSHIFT] or keys[pygame.K_SPACE]:
        if remaining_time >= PLAYER_BLINK_COOLDOWN_TIME:
            print("player blinking...")
            player_blink = True
            blink_vector = pygame.math.Vector2(
                mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]
            )
            if blink_vector.length() > 0:
                blink_vector = blink_vector.normalize() * PLAYER_BLINK_DISTANCE
                player_pos = [
                    player_pos[0] + blink_vector.x,
                    player_pos[1] + blink_vector.y,
                ]
                dx, dy = 0, 0
                last_blink_time = current_time
        else:
            print("player cannot blink as blink is still cooling down...")
            pass

    if keys[pygame.K_e] or keys[pygame.K_i]:
        print("toggling inventory...")
        inventory_open = not inventory_open
        pygame.time.wait(150)  # prevent user from rapidly toggling in and out

    return (
        dx,
        dy,
        direction,
        player_blink,
        player_pos,
        remaining_time,
        last_blink_time,
        mouse_pos,
        inventory_open,
    )
