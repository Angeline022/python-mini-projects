import pygame, random

pygame.init()
W, H = 400, 600
ROAD_L, ROAD_R = 50, 350
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

def reset():
    return pygame.Rect(W // 2 - 20, 500, 40, 70), [], 0, 0

def get_steer():
    # the ONLY function we'll change later to read the wheel
    keys = pygame.key.get_pressed()
    return float(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])   # -1..1

car, enemies, score, dash = reset()
alive, spawn_timer = True, 0
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r and not alive:
            car, enemies, score, dash = reset()
            alive = True

    if alive:
        speed = 5 + score // 500
        car.x += int(get_steer() * 8)
        car.x = max(ROAD_L, min(ROAD_R - car.width, car.x))

        spawn_timer -= 1
        if spawn_timer <= 0:
            enemies.append(pygame.Rect(random.randint(ROAD_L, ROAD_R - 40), -80, 40, 70))
            spawn_timer = random.randint(30, 60)
        for en in enemies:
            en.y += speed
        enemies = [en for en in enemies if en.y < H]

        if any(car.colliderect(en) for en in enemies):
            alive = False
        score += 1
        dash = (dash + speed) % 40

    screen.fill((30, 120, 30))
    pygame.draw.rect(screen, (60, 60, 60), (ROAD_L, 0, ROAD_R - ROAD_L, H))
    for y in range(-40, H, 40):
        pygame.draw.rect(screen, (230, 230, 230), (W // 2 - 3, y + dash, 6, 20))
    for en in enemies:
        pygame.draw.rect(screen, (200, 50, 50), en)
    pygame.draw.rect(screen, (50, 120, 255), car)
    screen.blit(font.render(f"Score {score // 10}", True, (255, 255, 255)), (10, 10))
    if not alive:
        screen.blit(font.render("Crashed! Press R", True, (255, 255, 0)), (100, H // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()