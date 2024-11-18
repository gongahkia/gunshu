# ARCHIVED


def render_with_8_directions(screen, positions, sprites, animation_states, direction):
    """
    render the game state with player facing 8 possible directions, but note this function also rotates the literal sprite around its central axis which I want to avoid
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
            frame,
            (pos["x"] - PLAYER_SPRITE_SIZE // 2, pos["y"] - PLAYER_SPRITE_SIZE // 2),
        )
    pygame.display.flip()
