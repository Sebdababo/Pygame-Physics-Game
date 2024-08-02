import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1200, 800
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
        self.gravity = 1
        self.damping = 1
        self.trail = []
        self.max_trail_length = 100
        self.selected_joint = None

    def add_joint(self, x, y):
        if not self.joints:
            length = 500
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
            self.selected_joint = None

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

        if self.joints:
            last_joint = self.joints[-1]
            self.trail.append((last_joint.x, last_joint.y))
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)

    def select_joint(self, x, y):
        for joint in self.joints:
            if math.sqrt((joint.x - x)**2 + (joint.y - y)**2) < 10:
                self.selected_joint = joint
                return True
        return False

    def move_selected_joint(self, x, y):
        if self.selected_joint:
            index = self.joints.index(self.selected_joint)
            if index == 0:
                return
            prev_joint = self.joints[index - 1]
            dx = x - prev_joint.x
            dy = y - prev_joint.y
            self.selected_joint.length = math.sqrt(dx**2 + dy**2)
            self.selected_joint.angle = math.atan2(dy, dx)

pendulum = Pendulum()
clock = pygame.time.Clock()
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                if not pendulum.select_joint(x, y):
                    pendulum.add_joint(x, y)
            elif event.button == 3:
                pendulum.remove_joint()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pendulum.selected_joint = None
        elif event.type == pygame.MOUSEMOTION:
            if pendulum.selected_joint:
                x, y = pygame.mouse.get_pos()
                pendulum.move_selected_joint(x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        pendulum.update()

    screen.fill((0, 0, 0))

    if len(pendulum.trail) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, pendulum.trail, 1)

    for joint in pendulum.joints:
        color = (255, 0, 0) if joint == pendulum.selected_joint else (128, 128, 128)
        pygame.draw.circle(screen, color, (int(joint.x), int(joint.y)), 5)
        if joint != pendulum.joints[0]:
            prev_joint = pendulum.joints[pendulum.joints.index(joint) - 1]
            pygame.draw.line(screen, (255, 255, 255), (prev_joint.x, prev_joint.y), (joint.x, joint.y), 2)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()