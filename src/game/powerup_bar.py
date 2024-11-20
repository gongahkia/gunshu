# FUA add a function that takes in the player's current inventory or powerup as an array and displays their powerup sprites, including a numbered count of each powerup

import pygame
import json
from collections import Counter


def update_player_powerup(player_powerup_array):
    """
    updates the player's powerup array

    FUA
    add code to update the player's powerup array when they collide with a powerup sprite
    """
    return None


def render_powerup_bar(screen, font, player_powerup_array, powerup_json_filepath):
    """
    render the player's powerup bar on the top right of the screen
    """

    padding = 10
    sprite_size = 40

    try:
        with open(powerup_json_filepath, "r") as file:
            powerup_json = json.load(file)
    except:
        print("Error: Unable to load the JSON filepath")
        return False

    powerup_counts = Counter(player_powerup_array)

    x = screen.get_width() - sprite_size - padding
    y = padding

    for powerup_name, count in powerup_counts.items():

        if powerup_name not in powerup_json:

            print(f"Warning: Powerup '{powerup_name}' not found in the JSON file")
            continue

        sprite_path = f'./sprite/item/{powerup_json[powerup_name].get("filename")}'

        if not sprite_path:
            print(f"Warning: Sprite filename missing for powerup '{powerup_name}'")
            continue

        try:

            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))

        except pygame.error as e:
            print(f"Error: Error loading sprite for powerup '{powerup_name}': {e}")
            return False

        screen.blit(sprite, (x, y))

        if count > 1:
            count_text = font.render(str(count), True, (255, 255, 255))
            text_rect = count_text.get_rect(
                bottomright=(x + sprite_size, y + sprite_size)
            )
            pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
            screen.blit(count_text, text_rect)
        y += sprite_size + padding

    return True
