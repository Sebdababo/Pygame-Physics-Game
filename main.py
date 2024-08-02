import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncy Ball")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

obstacles = []
for _ in range(5):
    obstacles.append(pygame.Rect(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 20), 100, 20))

points = []
for _ in range(5):
    points.append(pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20))

power_ups = []
power_up_timer = 0
is_invincible = False
invincibility_timer = 0

score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_x -= 5
    if keys[pygame.K_RIGHT]:
        ball_x += 5
    if keys[pygame.K_UP]:
        ball_y -= 5
    if keys[pygame.K_DOWN]:
        ball_y += 5

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= ball_radius or ball_y >= HEIGHT - ball_radius:
        ball_speed_y = -ball_speed_y

    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
    
    if not is_invincible:
        for obstacle in obstacles:
            if ball_rect.colliderect(obstacle):
                if abs(obstacle.top - ball_rect.bottom) < 10 and ball_speed_y > 0:
                    ball_speed_y = -ball_speed_y
                elif abs(obstacle.bottom - ball_rect.top) < 10 and ball_speed_y < 0:
                    ball_speed_y = -ball_speed_y
                elif abs(obstacle.left - ball_rect.right) < 10 and ball_speed_x > 0:
                    ball_speed_x = -ball_speed_x
                elif abs(obstacle.right - ball_rect.left) < 10 and ball_speed_x < 0:
                    ball_speed_x = -ball_speed_x

    for point in points[:]:
        if ball_rect.colliderect(point):
            points.remove(point)
            score += 1
            points.append(pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20))

    for power_up in power_ups[:]:
        if ball_rect.colliderect(power_up):
            power_ups.remove(power_up)
            is_invincible = True
            invincibility_timer = 300

    if is_invincible:
        invincibility_timer -= 1
        if invincibility_timer <= 0:
            is_invincible = False

    power_up_timer += 1
    if power_up_timer >= 300:
        power_up_timer = 0
        if len(power_ups) < 2:
            power_ups.append(pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20))

    screen.fill(BLACK)
    if is_invincible:
        pygame.draw.circle(screen, GREEN, (int(ball_x), int(ball_y)), ball_radius)
    else:
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)
    for point in points:
        pygame.draw.rect(screen, YELLOW, point)
    for power_up in power_ups:
        pygame.draw.rect(screen, GREEN, power_up)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()