import pygame

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


def render_player_inventory(screen, font):
    """
    render the inventory overlay
    """
    for row in range(INVENTORY_GRID_SIZE):
        for col in range(INVENTORY_GRID_SIZE):
            x = INVENTORY_MARGIN + col * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            y = INVENTORY_MARGIN + row * (INVENTORY_BOX_SIZE + INVENTORY_MARGIN)
            pygame.draw.rect(
                screen, (200, 200, 200), (x, y, INVENTORY_BOX_SIZE, INVENTORY_BOX_SIZE)
            )
            pygame.draw.rect(
                screen, (50, 50, 50), (x, y, INVENTORY_BOX_SIZE, INVENTORY_BOX_SIZE), 2
            )
    armor_slot_names = ["Head", "Body", "Legs"]
    start_x = SCREEN_WIDTH - ARMOR_SLOT_SIZE - ARMOR_SLOT_PADDING
    start_y = (SCREEN_HEIGHT - 3 * ARMOR_SLOT_SIZE - 2 * ARMOR_SLOT_PADDING) // 2
    for i, slot in enumerate(armor_slot_names):
        x = start_x
        y = start_y + i * (ARMOR_SLOT_SIZE + ARMOR_SLOT_PADDING)
        pygame.draw.rect(
            screen, (180, 180, 180), (x, y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE)
        )
        pygame.draw.rect(
            screen, (50, 50, 50), (x, y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE), 2
        )
        label_surface = font.render(slot, True, (0, 0, 0))
        screen.blit(
            label_surface,
            (
                x + (ARMOR_SLOT_SIZE - label_surface.get_width()) // 2,
                y + ARMOR_SLOT_SIZE + 5,
            ),
        )
