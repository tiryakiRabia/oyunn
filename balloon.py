import pygame

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {
            "normal": pygame.transform.scale(pygame.image.load("sprites/balloon_normal.png"), (80, 100)),
            "broken": pygame.transform.scale(pygame.image.load("sprites/balloon_broken.png"), (80, 100)),
            "piece": pygame.transform.scale(pygame.image.load("sprites/balloon_piece.png"), (80, 100))
        }

        self.image = self.images["normal"]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = "normal"  # normal, broken, piece

    def update(self):
        if self.state == "piece":
            if self.rect.bottom < 600:  # Havuza ulaşana kadar düş
                self.rect.y += 5
            else:
                self.rect.bottom = 600  # Havuz seviyesinde sabitle

    def pop(self):
        if self.state == "normal":
            self.image = self.images["broken"]
            self.state = "broken"

    def fall(self):
        if self.state == "broken":
            self.image = self.images["piece"]
            self.state = "piece"
