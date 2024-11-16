# ----- REQUIRED IMPORTS -----

import pygame
from enum import Enum

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SIZE = 40

PLAYER_SPEED = 15  # modify this to make player go faster or slower

# ----- PREDEFINED ENUMS ------


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    STATIC = "static"


def init_display():
    """
    initialize pygame and return the screen object and clock
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("gunshu")
    clock = pygame.time.Clock()
    return screen, clock


def handle_input():
    """
    handle player input and return movement deltas dx and dy and sets the direction enum
    """
    dx, dy = 0, 0
    direction = Direction.STATIC
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
        direction = Direction.LEFT
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED
        direction = Direction.RIGHT
    if keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
        direction = Direction.UP
    if keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED
        direction = Direction.DOWN
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
            # print(file_name)
            print(full_filepath)
            frame = pygame.image.load(full_filepath).convert_alpha()
            frame = pygame.transform.scale(frame, (sprite_size, sprite_size))
            print(f"scaled frame size: {frame.get_size()}")
            frames.append(frame)
    return frames


def render(screen, positions, client_id, sprites, animation_states, direction):
    """
    render the game state based on player positions
    """
    screen.fill(WHITE)
    for player_id, pos in positions.items():
        # color = BLUE if str(player_id) == str(client_id) else RED
        # pygame.draw.circle(screen, color, (pos["x"], pos["y"]), 20)
        print(f"player {player_id} position: ({pos['x']}, {pos['y']})")
        print(f"player {player_id} direction enum: {direction}")
        animation_states[player_id] = (animation_states.get(player_id, 0) + 1) % len(
            sprites
        )
        frame = sprites[animation_states[player_id]]
        print(f"player {player_id} animation state: {animation_states[player_id]}")
        print(f"sprite size: {frame.get_size()}")
        screen.blit(
            frame, (pos["x"] - SPRITE_SIZE // 2, pos["y"] - SPRITE_SIZE // 2)
        )  # draw the frame at the player's position
    pygame.display.flip()  # update display


def quit_display():
    """
    quit pygame
    """
    pygame.quit()
    print("exiting pygame now...")
