# --- SAMPLE CODE FOR A SCREENSHAKE EFFECT ---

import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

shake_duration = 0
shake_intensity = 10
shake_decay = 0.05
shake_offset_x = 0
shake_offset_y = 0

player_pos = [400, 300]

camera_offset_x = 0
camera_offset_y = 0


def start_screen_shake(duration, intensity):
    global shake_duration, shake_intensity, shake_offset_x, shake_offset_y
    shake_duration = duration
    shake_intensity = intensity
    shake_offset_x = random.randint(-shake_intensity, shake_intensity)
    shake_offset_y = random.randint(-shake_intensity, shake_intensity)


def update_screen_shake():
    global shake_duration, shake_intensity, shake_offset_x, shake_offset_y
    if shake_duration > 0:
        shake_duration -= 16
        shake_intensity -= shake_decay
        if shake_intensity <= 0:
            shake_intensity = 0
            shake_duration = 0
        int_shake_intensity = int(shake_intensity)
        shake_offset_x = random.randint(-int_shake_intensity, int_shake_intensity)
        shake_offset_y = random.randint(-int_shake_intensity, int_shake_intensity)


def draw_game():
    global camera_offset_x, camera_offset_y
    temp_offset_x = camera_offset_x + shake_offset_x
    temp_offset_y = camera_offset_y + shake_offset_y
    temp_offset_x = max(min(temp_offset_x, 0), -SCREEN_WIDTH + shake_intensity)
    temp_offset_y = max(min(temp_offset_y, 0), -SCREEN_HEIGHT + shake_intensity)
    screen.fill((0, 0, 0))
    shake_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    shake_surface.fill((255, 255, 255))
    pygame.draw.rect(
        shake_surface, (255, 0, 0), (player_pos[0], player_pos[1], 100, 100)
    )
    screen.blit(shake_surface, (temp_offset_x, temp_offset_y))


def main():
    global camera_offset_x, camera_offset_y
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen_shake(500, 20)
        update_screen_shake()
        camera_offset_x = 0
        camera_offset_y = 0
        draw_game()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
