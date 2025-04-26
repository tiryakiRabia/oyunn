import pygame
import sys

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Balon görselleri
        self.images = {
            "normal": pygame.transform.scale(pygame.image.load("sprites/balloon_normal.png"), (100, 130)),
            "broken": pygame.transform.scale(pygame.image.load("sprites/balloon_broken.png"), (100, 130)),
            "piece": pygame.transform.scale(pygame.image.load("sprites/balloon_piece.png"), (100, 130)),
        }

        self.image = self.images["normal"]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = "normal"  # Başlangıç durumu: normal

    def update(self):
        # Eğer balon 'piece' durumundaysa, balonun düşmesini sağla
        if self.state == "piece":
            if self.rect.bottom < 600:
                self.rect.y += 5
            else:
                self.rect.bottom = 600  # Havuz seviyesinde sabit

    def pop(self):
        # Normal balon patlatıldığında
        if self.state == "normal":
            self.image = self.images["broken"]
            self.state = "broken"

    def fall(self):
        # Patlayan balon yere düştüğünde
        if self.state == "broken":
            self.image = self.images["piece"]
            self.state = "piece"


class Archer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Okçu görselini yükle
        self.image = pygame.transform.scale(pygame.image.load("okcu.png"), (250, 350))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Okçuyu sol tarafta ortalayarak yerleştir

    def update(self):
        # Okçunun hareket etmesini istiyorsanız, buraya eklemeler yapabilirsiniz.
        pass


# Pygame başlatma
pygame.init()

# Ekran boyutları ve ayarları
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Popping Game")
clock = pygame.time.Clock()

# Arka plan resmi
background = pygame.image.load("backgroundd.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Balon grubu
balloons = pygame.sprite.Group()

# Okçuyu oluştur
archer = Archer(150, 450)  # Okçu sol tarafta
archer_group = pygame.sprite.Group()
archer_group.add(archer)

# Balonların konumlarını belirle
balloon_positions = [
    (650, 420),
    (770, 420),
    (890, 420),
    (1020, 420),
    (1140, 420),
]

# Balonları ekle
for position in balloon_positions:
    balloon = Balloon(position[0], position[1])
    balloons.add(balloon)

# Oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse ile balona tıklanırsa, balonu patlat veya patlatma sonrası düşmesini sağla
            for balloon in balloons:
                if balloon.rect.collidepoint(event.pos):
                    if balloon.state == "normal":
                        balloon.pop()
                    elif balloon.state == "broken":
                        balloon.fall()

    # Tüm sprite'ları güncelle
    balloons.update()
    archer_group.update()  # Okçuyu güncelle

    # Ekrana arka planı ve sprite'ları çiz
    screen.blit(background, (0, 0))
    balloons.draw(screen)
    archer_group.draw(screen)  # Okçuyu çiz

    # Ekranı güncelle
    pygame.display.update()

    # FPS (Frames Per Second) ayarı
    clock.tick(60)

# Pygame'i kapat
pygame.quit()
sys.exit()
