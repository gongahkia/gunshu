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
ARMOUR_SLOT_SIZE = 60
ARMOUR_SLOT_PADDING = 20

INVENTORY_ITEMS_ARRAY = [None] * (INVENTORY_GRID_SIZE**2)
ARMOUR_SLOTS_ARRAY = [None] * 3

# ----- INVENTORY LOGIC -----


def render_player_inventory_base(screen, font):
    """
    render the inventory overlay and return positions of inventory boxes and armour slots
    """
    screen.fill((50, 50, 50, 128))
    inventory_positions = []
    armour_positions = []
    for row in range(INVENTORY_GRID_SIZE):
        for col in range(INVENTORY_GRID_SIZE):
            x = INVENTORY_MARGIN + col * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            y = INVENTORY_MARGIN + row * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            rect = pygame.Rect(x, y, INVENTORY_BOX_SIZE, INVENTORY_BOX_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)
            inventory_positions.append(rect)
    armour_slot_names = ["Head", "Body", "Legs"]
    start_x = SCREEN_WIDTH - ARMOUR_SLOT_SIZE - ARMOUR_SLOT_PADDING
    start_y = (SCREEN_HEIGHT - 3 * ARMOUR_SLOT_SIZE - 2 * ARMOUR_SLOT_PADDING) // 2
    for i, slot in enumerate(armour_slot_names):
        x = start_x
        y = start_y + i * (ARMOUR_SLOT_SIZE + ARMOUR_SLOT_PADDING)
        rect = pygame.Rect(x, y, ARMOUR_SLOT_SIZE, ARMOUR_SLOT_SIZE)
        pygame.draw.rect(screen, (180, 180, 180), rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 2)
        label_surface = font.render(slot, True, (0, 0, 0))
        screen.blit(
            label_surface,
            (
                x + (ARMOUR_SLOT_SIZE - label_surface.get_width()) // 2,
                y + ARMOUR_SLOT_SIZE + 5,
            ),
        )
        armour_positions.append(rect)
    return inventory_positions, armour_positions


def handle_inventory_click(screen, mouse_pos, inventory_positions, armour_positions):
    """
    detect clicks on inventory boxes or armour slots and provide visual feedback, then return the selected inventory box index or armour slot index
    """
    selected_inventory_box = None
    selected_armour_slot = None
    for i, rect in enumerate(inventory_positions):
        if rect.collidepoint(mouse_pos):
            selected_inventory_box = i
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)
    for i, rect in enumerate(armour_positions):
        if rect.collidepoint(mouse_pos):
            selected_armour_slot = i
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)
    return selected_inventory_box, selected_armour_slot


def move_item_to_armour(inventory_index, armour_index):
    """
    move an item from the inventory to an armour slot
    """
    global INVENTORY_ITEMS_ARRAY, ARMOUR_SLOTS_ARRAY
    if INVENTORY_ITEMS_ARRAY[inventory_index]:
        ARMOUR_SLOTS_ARRAY[armour_index] = INVENTORY_ITEMS_ARRAY[inventory_index]
        INVENTORY_ITEMS_ARRAY[inventory_index] = None


def move_item_to_inventory(armour_index, inventory_index):
    """
    move an item from an armour slot back to the inventory
    """
    global INVENTORY_ITEMS_ARRAY, ARMOUR_SLOTS_ARRAY
    if ARMOUR_SLOTS_ARRAY[armour_index]:
        INVENTORY_ITEMS_ARRAY[inventory_index] = ARMOUR_SLOTS_ARRAY[armour_index]
        ARMOUR_SLOTS_ARRAY[armour_index] = None


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


def render_responsive_dragging(
    dragging_item, screen, inventory_positions, armour_positions
):
    """
    handles dragging animations resulting from the left mouse click within the inventory
    """
    if pygame.mouse.get_pressed()[0]:
        if not dragging_item:
            mouse_pos = pygame.mouse.get_pos()
            selected_inventory_box, selected_armour_slot = handle_inventory_click(
                screen, mouse_pos, inventory_positions, armour_positions
            )
            if selected_inventory_box is not None:
                dragging_item = True
                dragged_item = selected_inventory_box
                drag_start_pos = "inventory"
                print(f"inventory box {selected_inventory_box} clicked")
            elif selected_armour_slot is not None:
                dragging_item = True
                dragged_item = selected_armour_slot
                drag_start_pos = "armour"
                print(f"armour slot {selected_armour_slot} clicked")
            else:
                pass
        elif dragging_item:
            dragging_item = False
            dropped_inventory_box, dropped_armour_slot = handle_inventory_click(
                screen, mouse_pos, inventory_positions, armour_positions
            )
            if drag_start_pos == "inventory" and dropped_armour_slot is not None:
                move_item_to_armour(dragged_item, dropped_armour_slot)
            elif drag_start_pos == "armour" and dropped_armour_slot is None:
                move_item_to_inventory(dragged_item, dropped_inventory_box)
        else:
            pass
    if dragging_item and drag_start_pos == "inventory":
        render_dragged_item(screen, dragged_item, mouse_pos, inventory_positions)
    elif dragging_item and drag_start_pos == "armour":
        render_dragged_item(screen, dragged_item, mouse_pos, armour_positions)
