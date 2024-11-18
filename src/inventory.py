# ----- IMPORTS -----

import pygame

# ----- PREDEFINED VALUES -----

# PYGAME VALUES

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# INVENTORY VALUES

INVENTORY_GRID_SIZE = 5
INVENTORY_BOX_SIZE = 50
INVENTORY_MARGIN = 10
ARMOR_SLOT_SIZE = 60
ARMOR_SLOT_PADDING = 20

INVENTORY_ITEMS_ARRAY = [None] * (INVENTORY_GRID_SIZE**2)
ARMOR_SLOTS_ARRAY = [None] * 3

# ----- INVENTORY LOGIC -----


def render_player_inventory(screen, font):
    """
    render the inventory overlay and return positions of inventory boxes and armor slots
    """
    inventory_positions = []
    armor_positions = []
    for row in range(INVENTORY_GRID_SIZE):
        for col in range(INVENTORY_GRID_SIZE):
            x = INVENTORY_MARGIN + col * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            y = INVENTORY_MARGIN + row * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            rect = pygame.Rect(x, y, INVENTORY_BOX_SIZE, INVENTORY_BOX_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)
            inventory_positions.append(rect)
    armor_slot_names = ["Head", "Body", "Legs"]
    start_x = SCREEN_WIDTH - ARMOR_SLOT_SIZE - ARMOR_SLOT_PADDING
    start_y = (SCREEN_HEIGHT - 3 * ARMOR_SLOT_SIZE - 2 * ARMOR_SLOT_PADDING) // 2
    for i, slot in enumerate(armor_slot_names):
        x = start_x
        y = start_y + i * (ARMOR_SLOT_SIZE + ARMOR_SLOT_PADDING)
        rect = pygame.Rect(x, y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE)
        pygame.draw.rect(screen, (180, 180, 180), rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 2)
        label_surface = font.render(slot, True, (0, 0, 0))
        screen.blit(
            label_surface,
            (
                x + (ARMOR_SLOT_SIZE - label_surface.get_width()) // 2,
                y + ARMOR_SLOT_SIZE + 5,
            ),
        )
        armor_positions.append(rect)
    return inventory_positions, armor_positions


def handle_inventory_click(screen, mouse_pos, inventory_positions, armor_positions):
    """
    detect clicks on inventory boxes or armor slots and provide visual feedback, then return the selected inventory box index or armor slot index
    """
    selected_inventory_box = None
    selected_armor_slot = None
    for i, rect in enumerate(inventory_positions):
        if rect.collidepoint(mouse_pos):
            selected_inventory_box = i
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)
    for i, rect in enumerate(armor_positions):
        if rect.collidepoint(mouse_pos):
            selected_armor_slot = i
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)
    return selected_inventory_box, selected_armor_slot


def move_item_to_armor(inventory_index, armor_index):
    """
    move an item from the inventory to an armor slot
    """
    global INVENTORY_ITEMS_ARRAY, ARMOR_SLOTS_ARRAY
    if INVENTORY_ITEMS_ARRAY[inventory_index]:
        ARMOR_SLOTS_ARRAY[armor_index] = INVENTORY_ITEMS_ARRAY[inventory_index]
        INVENTORY_ITEMS_ARRAY[inventory_index] = None


def move_item_to_inventory(armor_index, inventory_index):
    """
    move an item from an armor slot back to the inventory
    """
    global INVENTORY_ITEMS_ARRAY, ARMOR_SLOTS_ARRAY
    if ARMOR_SLOTS_ARRAY[armor_index]:
        INVENTORY_ITEMS_ARRAY[inventory_index] = ARMOR_SLOTS_ARRAY[armor_index]
        ARMOR_SLOTS_ARRAY[armor_index] = None


def render_dragged_item(screen, item_index, mouse_pos, positions):
    """
    render the dragged item at the mouse position
    """
    if item_index is None:
        return
    rect = positions[item_index]
    pygame.draw.rect(
        screen,
        BLUE,
        (
            mouse_pos[0] - rect.width // 2,
            mouse_pos[1] - rect.height // 2,
            rect.width,
            rect.height,
        ),
    )
