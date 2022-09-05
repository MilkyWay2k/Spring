import pygame

R = 10

class Body:
    def __init__(self, x, y, static=False):
        global R

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0)
        self.static = static

        self.radius = R

        self.dragging = None
        self.last_rel = False
        self.drag_offset = None

    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.position.distance_squared_to(event.pos) <= self.radius ** 2:
            self.dragging = True
            self.drag_offset = event.pos - self.position
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            self.velocity.x = self.last_rel[0]
            self.velocity.y = self.last_rel[1]
            self.velocity *= 0.75
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.position = event.pos - self.drag_offset
            self.last_rel = event.rel

    def update(self, kt=1):
        if self.static or self.dragging:
            return

        self.position += self.velocity * kt
        self.velocity *= 0.9**kt

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.position, self.radius)
