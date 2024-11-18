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
