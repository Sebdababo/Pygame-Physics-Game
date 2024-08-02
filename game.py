import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chaos Pendulum Simulation")

class Joint:
    def __init__(self, x, y, length, angle):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.angular_velocity = 0
        self.angular_acceleration = 0

class Pendulum:
    def __init__(self):
        self.joints = []
        self.gravity = 9.81
        self.damping = 0.995

    def add_joint(self, x, y):
        if not self.joints:
            length = 100
            angle = math.pi / 2
        else:
            prev_joint = self.joints[-1]
            dx = x - prev_joint.x
            dy = y - prev_joint.y
            length = math.sqrt(dx**2 + dy**2)
            angle = math.atan2(dy, dx)
        self.joints.append(Joint(x, y, length, angle))

    def remove_joint(self):
        if self.joints:
            self.joints.pop()

    def update(self):
        for i, joint in enumerate(self.joints):
            if i == 0:
                joint.x = WIDTH // 2
                joint.y = HEIGHT // 2
            else:
                prev_joint = self.joints[i-1]
                joint.x = prev_joint.x + joint.length * math.sin(joint.angle)
                joint.y = prev_joint.y + joint.length * math.cos(joint.angle)

            force = self.gravity * math.sin(joint.angle)
            joint.angular_acceleration = -force / joint.length
            joint.angular_velocity += joint.angular_acceleration
            joint.angular_velocity *= self.damping
            joint.angle += joint.angular_velocity

pendulum = Pendulum()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                pendulum.add_joint(x, y)
            elif event.button == 3:
                pendulum.remove_joint()

    pendulum.update()

    screen.fill((255, 255, 255))
    for joint in pendulum.joints:
        pygame.draw.circle(screen, (0, 0, 0), (int(joint.x), int(joint.y)), 5)
        if joint != pendulum.joints[0]:
            prev_joint = pendulum.joints[pendulum.joints.index(joint) - 1]
            pygame.draw.line(screen, (0, 0, 0), (prev_joint.x, prev_joint.y), (joint.x, joint.y), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()