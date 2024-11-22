import pygame


class Camera:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.world_width = 1600
        self.world_height = 1200
        self.width = width
        self.height = height

    def set_target(self, target):
        """
        set the specified target that the camera will follow
        """
        self.target = target

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

    def update(self, target_pos):
        """
        update the camera to follow a specified target
        """
        if self.target is None:
            raise ValueError(
                "Camera target not set, please use set_target() to assign a target"
            )
        x = -target_pos["x"] + int(self.width / 2)
        y = -target_pos["y"] + int(self.height / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)
