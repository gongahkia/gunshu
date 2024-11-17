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
PLAYER_BLINK_DISTANCE = 200
PLAYER_BLINK_COOLDOWN_TIME = 3  # in seconds

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

# INVENTORY VALUES

INVENTORY_GRID_SIZE = 5  
INVENTORY_BOX_SIZE = 50
INVENTORY_MARGIN = 10
ARMOR_SLOT_SIZE = 60
ARMOR_SLOT_PADDING = 20

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
    screen, positions, sprites, frame_width, frame_height, output_sprite_size, direction
):
    """
    render the game state with player facing 8 possible directions
    """
    screen.fill(WHITE)
    for player_id, pos in positions.items():
        frame = load_directional_sprite(
            sprites, frame_width, frame_height, direction, output_sprite_size
        )
        screen.blit(
            frame,
            (pos["x"] - output_sprite_size // 2, pos["y"] - output_sprite_size // 2),
        )
    pygame.display.flip()


def quit_display():
    """
    quit pygame
    """
    pygame.quit()
    print("exiting pygame now...")


# EFFECTS


def load_effect_frames(sprite_filepath, frame_count):
    """
    to load in particle effects
    """
    sprite_sheet = pygame.image.load(sprite_filepath).convert_alpha()
    frame_width = 80
    frame_height = 80
    frames = []
    for i in range(frame_count):
        row = i // 4
        col = i % 4
        frame = sprite_sheet.subsurface(
            pygame.Rect(
                col * frame_width, row * frame_height, frame_width, frame_height
            )
        )
        frames.append(frame)
    return frames


# USER CONTROLS


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
        pygame.time.wait(150) # prevent user from rapidly toggling in and out

    return (
        dx,
        dy,
        direction,
        player_blink,
        player_pos,
        remaining_time,
        last_blink_time,
        mouse_pos,
        inventory_open
    )

# USER INTERFACE

def render_player_inventory(screen, font):
    """
    render the inventory overlay
    """
    for row in range(INVENTORY_GRID_SIZE):
        for col in range(INVENTORY_GRID_SIZE):
            x = INVENTORY_MARGIN + col * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            y = INVENTORY_MARGIN + row * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            pygame.draw.rect(screen, (200, 200, 200), (x, y, INVENTORY_BOX_SIZE, INVENTORY_BOX_SIZE))
            pygame.draw.rect(screen, (50, 50, 50), (x, y, INVENTORY_BOX_SIZE, INVENTORY_BOX_SIZE), 2)
    armor_slot_names = ["Head", "Body", "Legs"]
    start_x = SCREEN_WIDTH - ARMOR_SLOT_SIZE - ARMOR_SLOT_PADDING
    start_y = (SCREEN_HEIGHT - 3 * ARMOR_SLOT_SIZE - 2 * ARMOR_SLOT_PADDING) // 2
    for i, slot in enumerate(armor_slot_names):
        x = start_x
        y = start_y + i * (ARMOR_SLOT_SIZE + ARMOR_SLOT_PADDING)
        pygame.draw.rect(screen, (180, 180, 180), (x, y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE))
        pygame.draw.rect(screen, (50, 50, 50), (x, y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE), 2)
        label_surface = font.render(slot, True, (0, 0, 0))
        screen.blit(label_surface, (x + (ARMOR_SLOT_SIZE - label_surface.get_width()) // 2, y + ARMOR_SLOT_SIZE + 5))

# ARCHIVED

# def render_with_8_directions(screen, positions, sprites, animation_states, direction):
#     """
#     render the game state with player facing 8 possible directions, but note this function also rotates the literal sprite around its central axis which I want to avoid
#     """
#     screen.fill(WHITE)
#     for player_id, pos in positions.items():
#         animation_states[player_id] = (animation_states.get(player_id, 0) + 1) % len(
#             sprites
#         )
#         frame = sprites[animation_states[player_id]]
#         if direction == Direction.NORTH:
#             frame = pygame.transform.rotate(frame, 180)
#         elif direction == Direction.NORTHEAST:
#             frame = pygame.transform.rotate(frame, 135)
#         elif direction == Direction.EAST:
#             frame = pygame.transform.rotate(frame, 90)
#         elif direction == Direction.SOUTHEAST:
#             frame = pygame.transform.rotate(frame, 45)
#         elif direction == Direction.SOUTH:
#             frame = pygame.transform.rotate(frame, 0)
#         elif direction == Direction.SOUTHWEST:
#             frame = pygame.transform.rotate(frame, -45)
#         elif direction == Direction.WEST:
#             frame = pygame.transform.rotate(frame, -90)
#         elif direction == Direction.NORTHWEST:
#             frame = pygame.transform.rotate(frame, -135)
#         screen.blit(
#             frame,
#             (pos["x"] - PLAYER_SPRITE_SIZE // 2, pos["y"] - PLAYER_SPRITE_SIZE // 2),
#         )
#     pygame.display.flip()
