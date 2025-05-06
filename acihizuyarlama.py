import pygame
import math
import sys

# Başlangıç
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dairesel Dönen Yay ve Ok + İbre Göstergesi")
clock = pygame.time.Clock()

# Arka plan görseli
background_img = pygame.image.load("image/backgroundd.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Yay ve ok görseli
bow_img = pygame.image.load("image/animation_characters/acı_oku.png").convert_alpha()
bow_img = pygame.transform.scale(bow_img, (int(bow_img.get_width() * 0.15), int(bow_img.get_height() * 0.15)))

# Okçu görseli
okcu_img = pygame.image.load("image/animation_characters/okcu.png").convert_alpha()
okcu_img = pygame.transform.scale(okcu_img, (int(WIDTH * 0.3), int(HEIGHT * 0.5)))

# Hız ibresi, çizgi ve belirteç görselleri
speed_arrow = pygame.image.load("image/animation_characters/hız_ibresi.png")
speed_arrow = pygame.transform.scale(speed_arrow, (250, 55))

line_image = pygame.image.load("image/animation_characters/ibre_altındaki_cizgi.png")
line_image = pygame.transform.scale(line_image, (250, 18))

pointer_image = pygame.image.load("image/animation_characters/ibre_belirtec.png")
pointer_image = pygame.transform.scale(pointer_image, (36, 36))

# Merkez ve hareket parametreleri
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250
angle = math.pi  # Başlangıç açısı: 180 derece

bow_width, bow_height = bow_img.get_width(), bow_img.get_height()
min_radius = radius - max(bow_width, bow_height)

# Zamanlayıcı
start_time = pygame.time.get_ticks()

# A tuşuna basıldığında yay sabitlenir
fired_angle = None
fired_x, fired_y = None, None

# Hız değişkeni
current_speed = 100  # Başlangıç hızı

# Görsel döndürme fonksiyonu
def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, -math.degrees(angle))
    new_rect = rotated_image.get_rect(center=(0, 0))
    return rotated_image, new_rect

# İbre sınıfı
class MovingPointer:
    def __init__(self):  # Düzeltildi
        self.arrow_rect = speed_arrow.get_rect(center=(150, 350))  # Konumu biraz daha aşağıya kaydırdık
        self.line_rect = line_image.get_rect(midtop=(self.arrow_rect.centerx, self.arrow_rect.bottom + 5))
        self.pointer_rect = pointer_image.get_rect(midtop=(self.line_rect.centerx, self.line_rect.top))
        self.start_x = self.line_rect.left
        self.end_x = self.line_rect.right
        self.direction = 1
        self.speed = 2
        self.running = True

    def update(self):
        if self.running:
            self.pointer_rect.x += self.direction * self.speed
            if self.pointer_rect.left <= self.start_x or self.pointer_rect.right >= self.end_x:
                self.direction *= -1

    def draw(self, surface):
        surface.blit(speed_arrow, self.arrow_rect)
        surface.blit(line_image, self.line_rect)
        surface.blit(pointer_image, self.pointer_rect)

    def stop(self):
        self.running = False

    def get_pointer_position(self):
        # Pointer'ın konumunu döndürme
        return self.pointer_rect.centerx

# Pointer nesnesi
pointer = MovingPointer()

# Ana döngü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # A tuşuna bir kere basıldığında açıyı sabitler
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and fired_angle is None:
                fired_angle = angle
                fired_x = center_x - 215 + min_radius * math.cos(fired_angle)
                fired_y = center_y + 300 + min_radius * math.sin(fired_angle)
                print(f"Atış açısı: {math.degrees(fired_angle)} derece")

            # Belirteci durdurmak için SPACE veya S tuşu
            if event.key == pygame.K_SPACE or event.key == pygame.K_s:
                pointer.stop()

                # Hızı, ibre belirtecinin mevcut konumuna göre hesapla
                pointer_position = pointer.get_pointer_position()

                # Hızın, 25 ile 250 arasında orantılı olarak ayarlanması
                if pointer_position <= 25:
                    current_speed = 10
                elif pointer_position >= 250:
                    current_speed = 100
                else:
                    # Oran-orantı mantığıyla hız hesaplama
                    current_speed = (pointer_position / 2.5)

                print(f"Yeni hız: {current_speed}")

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    screen.blit(background_img, (0, 0))

    if elapsed_time < 3000:
        # İlk 3 saniyede sadece okçu görünür
        screen.blit(okcu_img, (50, HEIGHT - okcu_img.get_height() - 150))
    else:
        # Yay döner veya sabit kalır
        if fired_angle is None:
            angle += 0.01
            if angle > 2 * math.pi:
                angle = math.pi

            x = center_x - 215 + min_radius * math.cos(angle)
            y = center_y + 300 + min_radius * math.sin(angle)
            rotation_angle = angle + math.pi / 2
            rotated_bow, bow_rect = rotate_center(bow_img, rotation_angle)
            bow_rect.center = (x, y)
            screen.blit(rotated_bow, bow_rect)
        else:
            rotation_angle = fired_angle + math.pi / 2
            rotated_bow, bow_rect = rotate_center(bow_img, rotation_angle)
            bow_rect.center = (fired_x, fired_y)
            screen.blit(rotated_bow, bow_rect)

        # Okçu gittikten sonra ibre gösterimi
        pointer.update()
        pointer.draw(screen)

    pygame.display.flip()
    clock.tick(60)




























