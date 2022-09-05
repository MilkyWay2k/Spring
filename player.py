import pygame
import math

PI2 = math.pi+math.pi
SPEED = 1
ANGLE_SPEED = 0.1

class Player:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0)
        self.angle = 0

        self.o_points = [[0, -20],
                         [15, 20],
                         [0, 10],
                         [-15, 20]]
        self.t_points = None

        self.keys = {'forward': False,
                     'backward': False,
                     'left': False,
                     'right': False}

    def event_update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.keys['right'] = True
            elif event.key == pygame.K_a:
                self.keys['left'] = True
            elif event.key == pygame.K_w:
                self.keys['forward'] = True
            elif event.key == pygame.K_s:
                self.keys['backward'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.keys['right'] = False
            elif event.key == pygame.K_a:
                self.keys['left'] = False
            elif event.key == pygame.K_w:
                self.keys['forward'] = False
            elif event.key == pygame.K_s:
                self.keys['backward'] = False

    def collide_update(self, body, kt=1):
        if self.position.distance_squared_to(body.position) <= body.radius*body.radius:
            body.velocity += 65 * self.velocity * kt

    def update(self):
        global ANGLE_SPEED, SPEED, PI2

        if self.keys['right']:
            self.angle += ANGLE_SPEED
            if self.angle > PI2:
                self.angle -= PI2
        if self.keys['left']:
            self.angle -= ANGLE_SPEED
            if self.angle < 0:
                self.angle += PI2
        if self.keys['forward']:
            self.velocity.x += SPEED * math.sin(self.angle)
            self.velocity.y -= SPEED * math.cos(self.angle)
        if self.keys['backward']:
            self.velocity *= 0.9

        self.position += self.velocity
        self.velocity *= 0.9

    def draw(self, surface):
        self.t_points = []
        s = math.sin(self.angle)
        c = math.cos(self.angle)
        for p in self.o_points:
            self.t_points.append([self.position.x + p[0] * c - p[1] * s, self.position.y + p[0] * s + p[1] * c])
        pygame.draw.aalines(surface, (255, 255, 255), True, self.t_points, 2)


