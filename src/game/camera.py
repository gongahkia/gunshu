import pygame


class Camera:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.world_width = 1600
        self.world_height = 1200
        self.width = width
        self.height = height

    def apply(self, entity):
        """
        apply the camera's view to the entity
        """
        return entity.rect.move(self.camera.topleft)

    def apply_position(self, position):
        """
        translate a world position into camera-space coordinates
        """
        return position[0] - self.camera.x, position[1] - self.camera.y

    def update(self, target):
        """
        update the camera to follow a specified target
        """
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_width - self.width), x)
        y = max(-(self.world_height - self.height), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
