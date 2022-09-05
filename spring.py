import pygame

H = 5  # Ширина пружины
N = 5  # Число витков пружины


class Spring:
    def __init__(self, b1, b2, k):
        self.body1 = b1
        self.body2 = b2
        self.initial_length = self.body1.position.distance_to(self.body2.position)
        self.k = k

    def update(self, kt=1):
        l = self.body1.position.distance_to(self.body2.position)
        if l == 0: return

        F = self.k * (l - self.initial_length)

        dx = self.body1.position.x - self.body2.position.x
        dx /= l

        dy = self.body1.position.y - self.body2.position.y
        dy /= l

        self.body1.velocity.x -= F * dx * kt
        self.body1.velocity.y -= F * dy * kt

        self.body2.velocity.x += F * dx * kt
        self.body2.velocity.y += F * dy * kt

    def draw(self, surface, fast=False):
        global H, N

        if fast:
            pygame.draw.line(surface, (0, 0, 0), self.body1.position, self.body2.position, 2)
            return

        l = self.body1.position.distance_to(self.body2.position)
        if l == 0: return
        h = H * 0.5
        dx = (self.body1.position.x - self.body2.position.x)
        dy = (self.body1.position.y - self.body2.position.y)
        ddx = -h * dy / l
        ddy = h * dx / l
        p = [[self.body1.position.x, self.body1.position.y]]
        for k in range(1, N):
            x = self.body1.position.x - k / N * dx
            y = self.body1.position.y - k / N * dy
            if k % 2 == 0:
                x += ddx
                y += ddy
            else:
                x -= ddx
                y -= ddy
            p.append([x, y])
        p.append([self.body2.position.x, self.body2.position.y])

        pygame.draw.lines(surface, (0, 0, 0), False, p, 2)