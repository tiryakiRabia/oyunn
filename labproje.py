import pygame
import sys

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


pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Popping Game")
clock = pygame.time.Clock()

background = pygame.image.load("backgroundd.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Balon grubu
balloons = pygame.sprite.Group()

# Balonların konumlarını kendinize göre ayarlayın
balloon_positions = [
    (700, 420),  # Balon 1'in konumu
    (800, 420),  # Balon 2'nin konumu
    (900, 420),  # Balon 3'ün konumu
    (1000, 420),  # Balon 4'ün konumu
    (1100, 420),  # Balon 5'in konumu
]

# Her bir balon için belirtilen konumu kullanarak balonları ekleyin
for position in balloon_positions:
    balloon = Balloon(position[0], position[1])
    balloons.add(balloon)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse ile balona tıklanırsa patlat
            for balloon in balloons:
                if balloon.rect.collidepoint(event.pos):
                    if balloon.state == "normal":
                        balloon.pop()
                    elif balloon.state == "broken":
                        balloon.fall()

    balloons.update()

    screen.blit(background, (0, 0))
    balloons.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
