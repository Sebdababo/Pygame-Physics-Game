import pygame
import math
import colorsys

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Chaos Pendulum Simulation")

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
        self.max_trail_length = 500
        self.selected_joint = None
        self.hue = 0
        self.trail_color = (255, 255, 255)
        self.joint_color = (128, 128, 128)
        self.selected_color = (255, 0, 0)

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
            self.selected_joint = None
            self.trail.clear()

    def update(self):
        for i, joint in enumerate(self.joints):
            if i == 0:
                continue
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
                self.selected_joint.x = x
                self.selected_joint.y = y
            else:
                prev_joint = self.joints[index - 1]
                dx = x - prev_joint.x
                dy = y - prev_joint.y
                self.selected_joint.length = math.sqrt(dx**2 + dy**2)
                self.selected_joint.angle = math.atan2(dy, dx)
            self.update_joint_positions()

    def update_joint_positions(self):
        for i, joint in enumerate(self.joints):
            if i == 0:
                continue
            prev_joint = self.joints[i-1]
            joint.x = prev_joint.x + joint.length * math.sin(joint.angle)
            joint.y = prev_joint.y + joint.length * math.cos(joint.angle)

    def change_color(self):
        self.hue = (self.hue + 0.1) % 1
        rgb = colorsys.hsv_to_rgb(self.hue, 1, 1)
        self.trail_color = tuple(int(x * 255) for x in rgb)

pendulum = Pendulum()
clock = pygame.time.Clock()
running = True
paused = False

font = pygame.font.Font(None, 36)

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
            elif event.key == pygame.K_c:
                pendulum.change_color()
            elif event.key == pygame.K_UP:
                pendulum.gravity += 0.1
            elif event.key == pygame.K_DOWN:
                pendulum.gravity = max(0, pendulum.gravity - 0.1)
            elif event.key == pygame.K_RIGHT:
                pendulum.damping = min(1, pendulum.damping + 0.001)
            elif event.key == pygame.K_LEFT:
                pendulum.damping = max(0, pendulum.damping - 0.001)
            elif event.key == pygame.K_r:
                pendulum = Pendulum()
                paused = False

    if not paused:
        pendulum.update()
    else:
        pendulum.update_joint_positions()

    screen.fill((0, 0, 0))

    if len(pendulum.trail) > 1:
        pygame.draw.lines(screen, pendulum.trail_color, False, pendulum.trail, 2)

    for joint in pendulum.joints:
        color = pendulum.selected_color if joint == pendulum.selected_joint else pendulum.joint_color
        pygame.draw.circle(screen, color, (int(joint.x), int(joint.y)), 5)
        if joint != pendulum.joints[0]:
            prev_joint = pendulum.joints[pendulum.joints.index(joint) - 1]
            pygame.draw.line(screen, pendulum.trail_color, (prev_joint.x, prev_joint.y), (joint.x, joint.y), 2)

    info_text = f"Gravity: {pendulum.gravity:.2f} | Damping: {pendulum.damping:.3f} | {'Paused' if paused else 'Running'}"
    text_surface = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    controls_text = "Space (Pause/Resume) | C (Change Color) | Up/Down (Gravity) | Left/Right (Damping) | R (Reset)"
    controls_surface = font.render(controls_text, True, (200, 200, 200))
    screen.blit(controls_surface, (10, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()