import pygame
import sys

# Başlangıç ayarları
pygame.init()
WIDTH, HEIGHT = 1152, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perfectly Centered Pointer on Line")
clock = pygame.time.Clock()

# Görselleri yükle ve ölçekle
background = pygame.image.load("backgroundd.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

speed_arrow = pygame.image.load("hız_ibresi.png")
speed_arrow = pygame.transform.scale(speed_arrow, (300, 80))

line_image = pygame.image.load("ibre_altındaki_cizgi.png")
line_image = pygame.transform.scale(line_image, (300, 20))

pointer_image = pygame.image.load("ibre_belirtec.png")
pointer_image = pygame.transform.scale(pointer_image, (50, 50))

# İbre sınıfı
class MovingPointer:
    def __init__(self):
        # Hız ibresi (üstteki renkli oklar)
        self.arrow_rect = speed_arrow.get_rect(center=(WIDTH // 2, HEIGHT - 200))
        
        # Gri çizgi
        self.line_rect = line_image.get_rect(midtop=(self.arrow_rect.centerx, self.arrow_rect.bottom + 5))

        # Belirteç: çizginin üstünde, tam ortalanmış
        self.pointer_rect = pointer_image.get_rect(midtop=(self.line_rect.centerx, self.line_rect.top))

        self.start_x = self.line_rect.left
        self.end_x = self.line_rect.right

        self.direction = 1  # 1 = sağa, -1 = sola
        self.speed = 4
        self.running = True

    def update(self):
        if self.running:
            self.pointer_rect.x += self.direction * self.speed

            # Buraya dikkat: belirtecin sol ve sağ kenarlarını kontrol ediyoruz
            if self.pointer_rect.left <= self.start_x or self.pointer_rect.right >= self.end_x:
                self.direction *= -1

    def draw(self, surface):
        surface.blit(background, (0, 0))
        surface.blit(speed_arrow, self.arrow_rect)
        surface.blit(line_image, self.line_rect)
        surface.blit(pointer_image, self.pointer_rect)

    def stop(self):
        self.running = False

# Nesne oluştur
pointer = MovingPointer()

# Oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pointer.stop()

    pointer.update()
    pointer.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
