import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dairesel Dönen Yay ve Ok + Balon Sahnesi")
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

# Balon görselleri
balloon_normal = pygame.image.load("image/animation_characters/balon1.png").convert_alpha()
balloon_broken = pygame.image.load("image/animation_characters/balon2.png").convert_alpha()
balloon_piece = pygame.image.load("image/animation_characters/balon3.png").convert_alpha()

balloon_normal = pygame.transform.scale(balloon_normal, (50, 140))
balloon_broken = pygame.transform.scale(balloon_broken, (50, 140))
balloon_piece = pygame.transform.scale(balloon_piece, (50, 140))

# Yay parametreleri
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250
angle = math.pi

bow_width, bow_height = bow_img.get_width(), bow_img.get_height()
min_radius = radius - max(bow_width, bow_height)

start_time = pygame.time.get_ticks()

fired_angle = None
fired_x, fired_y = None, None
current_speed = 100

stage = "aiming"
balloons = []

angle_locked = False
speed_locked = False

a_pressed = False
s_pressed = False
balloon_animation_started = False

def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, -math.degrees(angle))
    new_rect = rotated_image.get_rect(center=(0, 0))
    return rotated_image, new_rect

class MovingPointer:
    def __init__(self):
        self.arrow_rect = speed_arrow.get_rect(center=(150, 400))
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
        return self.pointer_rect.centerx

class Balloon:
    def __init__(self, x, y, delay=0):
        self.x = x
        self.y = y
        self.state = 0
        self.last_change = pygame.time.get_ticks()
        self.change_interval = 500
        self.visible = True  # Başta hep görünür
        self.delay = delay
        self.animating = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.animating and self.state < 2 and current_time - self.last_change > self.change_interval:
            self.state += 1
            self.last_change = current_time

    def draw(self, surface):
        if self.state == 0:
            surface.blit(balloon_normal, (self.x, self.y))
        elif self.state == 1:
            surface.blit(balloon_broken, (self.x, self.y))
        elif self.state == 2:
            surface.blit(balloon_piece, (self.x, self.y))

    def start_animation(self):
        self.animating = True
        self.state = 1  # Başlangıçta kırık balonla başla
        self.last_change = pygame.time.get_ticks()

pointer = MovingPointer()

# Balonlar her zaman sahnede olacak şekilde en başta oluşturuluyor
balloon_spacing = 30
balloon_width = 50
total_width = 5 * balloon_width + 4 * balloon_spacing
start_x = WIDTH - total_width - 30
start_y = HEIGHT - 310

for i in range(5):
    x = start_x + i * (balloon_width + balloon_spacing)
    y = start_y
    balloons.append(Balloon(x, y, delay=i * 500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and not angle_locked:
                fired_angle = angle
                fired_x = center_x - 215 + min_radius * math.cos(fired_angle)
                fired_y = center_y + 300 + min_radius * math.sin(fired_angle)
                angle_locked = True
                a_pressed = True

            if (event.key == pygame.K_s or event.key == pygame.K_SPACE) and not speed_locked:
                pointer.stop()
                pointer_position = pointer.get_pointer_position()
                current_speed = (pointer_position / 2.5) if 25 < pointer_position < 250 else (10 if pointer_position <= 25 else 100)
                speed_locked = True
                s_pressed = True

            if angle_locked and speed_locked and stage != "balloon_show":
                stage = "balloon_show"

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    screen.blit(background_img, (0, 0))

    if stage == "aiming":
        if elapsed_time < 3000:
            screen.blit(okcu_img, (50, HEIGHT - okcu_img.get_height() - 150))
        else:
            if fired_angle is None:
                angle += 0.01
                if angle > 2 * math.pi:
                    angle = math.pi
                x = center_x - 215 + min_radius * math.cos(angle)
                y = center_y + 300 + min_radius * math.sin(angle)
                rotated_bow, bow_rect = rotate_center(bow_img, angle + math.pi / 2)
                bow_rect.center = (x, y)
                screen.blit(rotated_bow, bow_rect)
            else:
                rotated_bow, bow_rect = rotate_center(bow_img, fired_angle + math.pi / 2)
                bow_rect.center = (fired_x, fired_y)
                screen.blit(rotated_bow, bow_rect)
            pointer.update()
            pointer.draw(screen)

    if stage == "balloon_show" and not balloon_animation_started and a_pressed and s_pressed:
        for balloon in balloons:
            balloon.start_animation()
        balloon_animation_started = True

    for balloon in balloons:
        balloon.update()
        balloon.draw(screen)

    pygame.display.flip()
    clock.tick(60)





