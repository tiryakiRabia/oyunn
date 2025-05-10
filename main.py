import pygame
import math
import sys

pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dairesel Dönen Yay ve Ok + Balon Sahnesi")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 48, bold=True)

# rotate_center fonksiyonu
def rotate_center(image, angle):
    rotated_image = pygame.transform.rotate(image, -math.degrees(angle))
    new_rect = rotated_image.get_rect(center=(0, 0))
    return rotated_image, new_rect

# simulate_trajectory fonksiyonu
def simulate_trajectory(x, y, angle, speed, gravity=0.2):
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    points = []
    for _ in range(100):
        x += vx
        vy += gravity
        y += vy
        if y > HEIGHT:
            break
        points.append((int(x), int(y)))
    return points

# --- Görsel tanımları ---
empty_heart = pygame.transform.scale(
    pygame.image.load("image/animation_characters/bos_kalp.png").convert_alpha(), (40, 40)
)
full_heart = pygame.transform.scale(
    pygame.image.load("image/animation_characters/dolu_kalp.png").convert_alpha(), (40, 40)
)
heart_states = [False] * 5

win_text_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/win_yazisi.png").convert_alpha(), (400, 120)
)
win_text_rect = win_text_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

win_heart_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/winkalp.png").convert_alpha(), (200, 200)
)
win_heart_rect = win_heart_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

lost_text_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/lost_yazisi.png").convert_alpha(), (300, 100)
)
lost_text_rect = lost_text_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

lost_heart_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/lostkalp.png").convert_alpha(), (200, 200)
)
lost_heart_rect = lost_heart_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

win_shown = False
win_start_time = None
lost_shown = False

background_img = pygame.transform.scale(
    pygame.image.load("image/backgroundd.png").convert(), (WIDTH, HEIGHT)
)

arrow_img_source = pygame.image.load("image/animation_characters/ok.png").convert_alpha()
narrow_img = pygame.transform.scale(arrow_img_source, (90, 30))
narrow_icon = pygame.transform.scale(arrow_img_source, (150, 50))

bow_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/acı_oku.png").convert_alpha(),
    (int(153 * 0.75), int(183 * 0.85)),
)

okcu_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/okcu.png").convert_alpha(),
    (int(WIDTH * 0.3), int(HEIGHT * 0.5)),
)

dial_img = pygame.transform.scale(
    pygame.image.load("image/animation_characters/hız_ibresi.png"), (250, 55)
)
line_image = pygame.transform.scale(
    pygame.image.load("image/animation_characters/ibre_altındaki_cizgi.png"), (250, 18)
)
pointer_image = pygame.transform.scale(
    pygame.image.load("image/animation_characters/ibre_belirtec.png"), (36, 36)
)

balloon_normal = pygame.transform.scale(
    pygame.image.load("image/animation_characters/balon1.png").convert_alpha(), (50, 140)
)
balloon_broken = pygame.transform.scale(
    pygame.image.load("image/animation_characters/balon2.png").convert_alpha(), (50, 140)
)
balloon_piece = pygame.transform.scale(
    pygame.image.load("image/animation_characters/balon3.png").convert_alpha(), (50, 140)
)

# --- Oyun durumu ---
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250
min_radius = radius - max(bow_img.get_width(), bow_img.get_height())
angle = math.pi

fired_angle = None
fired_x, fired_y = None, None
current_speed = 100
stage = "ready"
balloons = []
angle_locked = False
speed_locked = False
a_pressed = False
s_pressed = False
arrow_object = None
READY_DURATION = 3000
max_arrows = 10
remaining_arrows = max_arrows
start_time = pygame.time.get_ticks()

# --- Sınıflar ---
class MovingPointer:
    def __init__(self):
        self.arrow_rect = dial_img.get_rect(center=(150, 400))
        self.line_rect = line_image.get_rect(midtop=(self.arrow_rect.centerx, self.arrow_rect.bottom + 5))
        self.pointer_rect = pointer_image.get_rect(midtop=(self.line_rect.centerx, self.line_rect.top))
        self.start_x = self.line_rect.left
        self.end_x = self.line_rect.right
        self.direction = 1
        self.speed = 1.3
        self.running = True

    def update(self):
        if self.running:
            self.pointer_rect.x += self.direction * self.speed
            if self.pointer_rect.left <= self.start_x or self.pointer_rect.right >= self.end_x:
                self.direction *= -1

    def draw(self, surface):
        surface.blit(dial_img, self.arrow_rect)
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
        self.initial_y = y
        self.state = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 140)
        self.delay = delay
        self.animating = False
        self.last_change = 0
        self.change_interval = 300
        self.fall_speed = 1

    def update(self):
        if self.animating:
            now = pygame.time.get_ticks()
            if self.state == 1 and now - self.last_change > self.change_interval:
                self.state = 2
                self.animating = False
                for idx in range(len(heart_states)):
                    if not heart_states[idx]:
                        heart_states[idx] = True
                        break

        if self.state == 2:
            if self.y < self.initial_y + 30:
                self.y += self.fall_speed
                self.rect.y = self.y

    def draw(self, surface):
        if self.state == 0:
            surface.blit(balloon_normal, (self.x, self.y))
        elif self.state == 1:
            surface.blit(balloon_broken, (self.x, self.y))
        elif self.state == 2:
            surface.blit(balloon_piece, (self.x, self.y))

    def start_animation(self):
        self.state = 1
        self.animating = True
        self.last_change = pygame.time.get_ticks()

class Arrow:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.image = narrow_img
        self.active = True
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        self.gravity = 0.2

    def update(self):
        if self.active:
            self.vy += self.gravity
            self.x += self.vx
            self.y += self.vy
            if self.x < -100 or self.x > WIDTH + 100 or self.y > HEIGHT + 100:
                self.active = False

    def draw(self, surface):
        current_angle = math.atan2(self.vy, self.vx)
        rotated_arrow = pygame.transform.rotate(self.image, -math.degrees(current_angle))
        arrow_rect = rotated_arrow.get_rect(center=(self.x, self.y))
        surface.blit(rotated_arrow, arrow_rect)

# --- Oyun Nesneleri Başlat ---
pointer = MovingPointer()

balloon_spacing = 30
balloon_width = 50
total_width = 5 * balloon_width + 4 * balloon_spacing
start_x = WIDTH - total_width - 30
start_y = HEIGHT - 310
for i in range(5):
    x = start_x + i * (balloon_width + balloon_spacing)
    y = start_y
    balloons.append(Balloon(x, y, delay=i * 500))

# --- Oyun Döngüsü ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not win_shown and not lost_shown:
                if event.key == pygame.K_a and not angle_locked and remaining_arrows > 0:
                    fired_angle = angle
                    fired_x = center_x - 215 + min_radius * math.cos(fired_angle)
                    fired_y = center_y + 300 + min_radius * math.sin(fired_angle)
                    angle_locked = True
                    a_pressed = True

                if (event.key == pygame.K_s or event.key == pygame.K_SPACE) and not speed_locked and angle_locked and remaining_arrows > 0:
                    pointer.stop()
                    pointer_position = pointer.get_pointer_position()
                    current_speed = (pointer_position / 3.5) if 25 < pointer_position < 250 else (10 if pointer_position <= 25 else 100)
                    speed_locked = True
                    s_pressed = True
                    arrow_object = Arrow(fired_x, fired_y, fired_angle + math.pi / 2, current_speed / 5)

    if all(heart_states) and win_start_time is None:
        win_start_time = pygame.time.get_ticks()

    if win_start_time and pygame.time.get_ticks() - win_start_time >= 1000:
        win_shown = True

    screen.blit(background_img, (0, 0))

    for i in range(max_arrows):
        if i < remaining_arrows:
            row = i // 5
            col = i % 5
            x = 10 + col * 80
            y = 10 + row * 35
            screen.blit(narrow_icon, (x, y))

    for i in range(5):
        img = full_heart if heart_states[i] else empty_heart
        x = WIDTH - (i + 1) * 45 - 10
        y = 10
        screen.blit(img, (x, y))

    if win_shown:
        screen.blit(win_text_img, win_text_rect)
        screen.blit(win_heart_img, win_heart_rect)
        pygame.display.flip()
        clock.tick(60)
        continue

    if lost_shown:
        screen.blit(lost_text_img, lost_text_rect)
        screen.blit(lost_heart_img, lost_heart_rect)
        pygame.display.flip()
        clock.tick(60)
        continue

    elapsed_time = pygame.time.get_ticks() - start_time

    if stage == "ready":
        if elapsed_time < READY_DURATION:
            screen.blit(okcu_img, (50, HEIGHT - okcu_img.get_height() - 150))
            remaining_time = max(0, int((READY_DURATION - elapsed_time) / 1000) + 1)
            text_surface = font.render(f"ARE YOU READY? {remaining_time}", True, (0, 0, 128))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 200))
            screen.blit(text_surface, text_rect)
        else:
            stage = "aiming"

    elif stage == "aiming":
        if not a_pressed and remaining_arrows == max_arrows:
            helper_font = pygame.font.SysFont("Arial", 24, bold=True)
            inst1 = helper_font.render('Yayı durdurmak için "A" tuşuna basınız.', True, (255, 0, 0))
            inst2 = helper_font.render('Hızı belirlemek için "S" tuşuna basınız.', True, (255, 0, 0))
            inst1_rect = inst1.get_rect(center=(WIDTH // 2, 100))
            inst2_rect = inst2.get_rect(center=(WIDTH // 2, 130))
            screen.blit(inst1, inst1_rect)
            screen.blit(inst2, inst2_rect)

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

        if angle_locked and not speed_locked:
            preview_speed = (pointer.get_pointer_position() / 3.5)
            corrected_angle = fired_angle + math.pi / 2
            points = simulate_trajectory(fired_x, fired_y, corrected_angle, preview_speed / 5)
            for pt in points:
                pygame.draw.circle(screen, (180, 180, 180), pt, 2)

    if arrow_object:
        arrow_object.update()
        if arrow_object.active:
            arrow_object.draw(screen)
            for balloon in balloons:
                if balloon.state == 0 and balloon.rect.collidepoint(arrow_object.x, arrow_object.y):
                    balloon.start_animation()
                    arrow_object.active = False
                    break
        else:
            if remaining_arrows > 0:
                remaining_arrows -= 1

            if remaining_arrows == 0 and not all(heart_states):
                lost_shown = True

            arrow_object = None
            angle_locked = False
            speed_locked = False
            a_pressed = False
            s_pressed = False
            pointer = MovingPointer()
            fired_angle = None
            stage = "aiming"

    for balloon in balloons:
        balloon.update()
        balloon.draw(screen)

    pygame.display.flip()
    clock.tick(60)
