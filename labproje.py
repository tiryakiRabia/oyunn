import pygame
import math
import sys

# ------------------- BALLOON SINIFI -------------------
class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {
            "normal": pygame.transform.scale(pygame.image.load("balon1.png"), (100, 130)),
            "broken": pygame.transform.scale(pygame.image.load("balon2.png"), (100, 130)),
            "piece": pygame.transform.scale(pygame.image.load("balon3.png"), (100, 130)),
        }
        self.image = self.images["normal"]
        self.rect = self.image.get_rect(center=(x, y))
        self.state = "normal"
        self.broken_time = None
        self.pop_sound = pygame.mixer.Sound("balonpatlatma.mp3")  # Balon patlama sesi

    def update(self):
        if self.state == "piece":
            if self.rect.bottom < 600:
                self.rect.y += 5
            else:
                self.rect.bottom = 600

        if self.state == "broken" and self.broken_time:
            now = pygame.time.get_ticks()
            if now - self.broken_time > 150:
                self.fall()

    def pop(self):
        if self.state == "normal":
            self.image = self.images["broken"]
            self.state = "broken"
            self.broken_time = pygame.time.get_ticks()
            self.pop_sound.play()  # Patlama sesi çal

    def fall(self):
        if self.state == "broken":
            self.image = self.images["piece"]
            self.state = "piece"


# ------------------- OK SINIFI -------------------
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load("ok.png"), (120, 120))
        self.image = pygame.transform.rotate(self.original_image, 45)
        self.rect = self.image.get_rect(center=(x, y))

        self.angle = math.radians(angle)
        self.speed = 10
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()


# ------------------- BAŞLANGIÇ -------------------
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Popping Game")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("backgroundd.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

balloons = pygame.sprite.Group()
balloon_positions = [(650, 420), (770, 420), (890, 420), (1020, 420), (1140, 420)]
for pos in balloon_positions:
    balloons.add(Balloon(*pos))

# Balon sayısı
balloon_count = len(balloons)

# Okçu sadece bir kere gösterilecek
archer_image = pygame.transform.scale(pygame.image.load("okcu.png"), (250, 350))
archer_rect = archer_image.get_rect(center=(150, 450))
show_archer = True
archer_display_time = 1500  # milisaniye
archer_start_time = pygame.time.get_ticks()

arrows = pygame.sprite.Group()

# Yay + ok birleşik görsel
bow_img = pygame.transform.scale(pygame.image.load("acı_oku.png"), (150, 150))
bow_angle = 0
bow_center = [archer_rect.right - 20, archer_rect.centery - 30]

# Arka plan müziği
pygame.mixer.music.load("arkaplan.mp3")  # Arka plan müziği
pygame.mixer.music.play(-1, 0.0)  # Sonsuz döngüde çalsın

# Germe sesi
germe = pygame.mixer.Sound("germe.mp3")  # Germe sesi
germe.set_volume(0.2)

# ------------------- OYUN DÖNGÜSÜ -------------------
running = True
while running:
    screen.blit(background, (0, 0))

    current_time = pygame.time.get_ticks()
    if show_archer and current_time - archer_start_time > archer_display_time:
        show_archer = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # SPACE ile ok fırlat
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                arrow = Arrow(*bow_center, bow_angle)
                arrows.add(arrow)

    # Yay açısı ayarlama
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        bow_angle -= 1
        germe.play()  # Yay germe sesi çal
    if keys[pygame.K_DOWN]:
        bow_angle += 1
        germe.play()  # Yay germe sesi çal

    # Güncellemeler
    arrows.update()
    balloons.update()

    # Çarpışma kontrolü
    for arrow in arrows:
        hit_balloons = pygame.sprite.spritecollide(arrow, balloons, False)
        for balloon in hit_balloons:
            if balloon.state == "normal":
                balloon.pop()  # Balon patlatma
                arrow.kill()  # Oku öldür
                balloon_count -= 1  # Balon sayısını azalt

    # Eğer balonlar bitmişse oyunu bitir
    if balloon_count <= 0:
        # Kazanma müziği çal
        pygame.mixer.music.stop()  # Oyun başlama müziğini durdur
        pygame.mixer.music.load("oyunukazandı.mp3")  # Kazanma müziği
        pygame.mixer.music.play(0, 0.0)  # Bir kere çalsın

        # Kazanma ekranı
        win_girl = pygame.transform.scale(pygame.image.load("win_girl.png"), (500, 500))
        screen.blit(win_girl,
                    (SCREEN_WIDTH // 2 - win_girl.get_width() // 2, SCREEN_HEIGHT // 2 - win_girl.get_height() // 2))



        pygame.display.update()
        pygame.time.delay(2000)  # 2 saniye bekle, ardından çık
        running = False

    # Çizimler
    balloons.draw(screen)
    arrows.draw(screen)

    if show_archer:
        screen.blit(archer_image, archer_rect)
    else:
        rotated_bow = pygame.transform.rotate(bow_img, -bow_angle)
        bow_rect = rotated_bow.get_rect(center=bow_center)
        screen.blit(rotated_bow, bow_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
