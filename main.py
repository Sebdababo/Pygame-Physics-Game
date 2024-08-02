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

ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

obstacles = []
for _ in range(5):
    obstacles.append(pygame.Rect(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 20), 100, 20))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= ball_radius or ball_y >= HEIGHT - ball_radius:
        ball_speed_y = -ball_speed_y

    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
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

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()