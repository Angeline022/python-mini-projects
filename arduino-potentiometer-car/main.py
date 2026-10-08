import pygame
import serial
import time
import random

# =========================
# ARDUINO
# =========================

arduino = serial.Serial("COM3", 9600)
time.sleep(2)

# =========================
# PYGAME SETUP
# =========================

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arduino Car Game")

clock = pygame.time.Clock()

# =========================
# ROAD
# =========================

ROAD_LEFT = 150
ROAD_RIGHT = 650

ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# =========================
# PLAYER CAR
# =========================

CAR_WIDTH = 50
CAR_HEIGHT = 90

car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - 130

# =========================
# OBSTACLES
# =========================

obstacles = []

obstacle_timer = 0
obstacle_delay = 60

obstacle_width = 50
obstacle_height = 90

# =========================
# GAME
# =========================

score = 0
game_over = False

font = pygame.font.Font(None, 40)

running = True

while running:

    # -------------------------
    # EVENTS
    # -------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Restart
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and game_over:
                obstacles.clear()
                score = 0
                game_over = False

    # =========================
    # GAME LOGIC
    # =========================

    if not game_over:

        # -------------------------
        # READ POTENTIOMETER
        # -------------------------

        if arduino.in_waiting:

            try:
                data = arduino.readline().decode().strip()
                pot_value = int(data)

                # Map potentiometer to road position
                target_x = ROAD_LEFT + (
                    pot_value / 1023
                ) * (ROAD_WIDTH - CAR_WIDTH)

                # Smooth steering
                car_x += (target_x - car_x) * 0.2

            except:
                pass

        # -------------------------
        # CREATE OBSTACLES
        # -------------------------

        obstacle_timer += 1

        if obstacle_timer >= obstacle_delay:

            obstacle_timer = 0

            x = random.randint(
                ROAD_LEFT,
                ROAD_RIGHT - obstacle_width
            )

            obstacle = pygame.Rect(
                x,
                -obstacle_height,
                obstacle_width,
                obstacle_height
            )

            obstacles.append(obstacle)

        # -------------------------
        # MOVE OBSTACLES
        # -------------------------

        for obstacle in obstacles:
            obstacle.y += 7

        # -------------------------
        # REMOVE OLD OBSTACLES
        # -------------------------

        obstacles = [
            obstacle for obstacle in obstacles
            if obstacle.y < HEIGHT
        ]

        # -------------------------
        # COLLISION
        # -------------------------

        car_rect = pygame.Rect(
            int(car_x),
            car_y,
            CAR_WIDTH,
            CAR_HEIGHT
        )

        for obstacle in obstacles:

            if car_rect.colliderect(obstacle):
                game_over = True

        # -------------------------
        # SCORE
        # -------------------------

        score += 1

    # =========================
    # DRAW
    # =========================

    # Grass
    screen.fill((40, 150, 40))

    # Road
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (
            ROAD_LEFT,
            0,
            ROAD_WIDTH,
            HEIGHT
        )
    )

    # -------------------------
    # ROAD EDGE
    # -------------------------

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (ROAD_LEFT, 0, 5, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (ROAD_RIGHT - 5, 0, 5, HEIGHT)
    )

    # -------------------------
    # ROAD CENTER LINE
    # -------------------------

    for y in range(-40, HEIGHT, 80):

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                WIDTH // 2 - 5,
                y,
                10,
                40
            )
        )

    # -------------------------
    # PLAYER CAR
    # -------------------------

    pygame.draw.rect(
        screen,
        (220, 30, 30),
        car_rect,
        border_radius=8
    )

    # Windshield
    pygame.draw.rect(
        screen,
        (100, 200, 230),
        (
            int(car_x) + 8,
            car_y + 12,
            CAR_WIDTH - 16,
            25
        ),
        border_radius=5
    )

    # -------------------------
    # OBSTACLES
    # -------------------------

    for obstacle in obstacles:

        pygame.draw.rect(
            screen,
            (30, 80, 220),
            obstacle,
            border_radius=8
        )

        # Windshield
        pygame.draw.rect(
            screen,
            (100, 200, 230),
            (
                obstacle.x + 8,
                obstacle.y + 12,
                obstacle.width - 16,
                25
            ),
            border_radius=5
        )

    # -------------------------
    # SCORE
    # -------------------------

    score_text = font.render(
        f"Score: {score // 10}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    # =========================
    # GAME OVER
    # =========================

    if game_over:

        game_over_text = font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 - 100,
                HEIGHT // 2 - 30
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - 120,
                HEIGHT // 2 + 20
            )
        )

    pygame.display.flip()

    clock.tick(60)

# =========================
# CLEANUP
# =========================

arduino.close()
pygame.quit()