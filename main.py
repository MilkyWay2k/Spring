import pygame
from body import Body
from spring import Spring
from player import Player
import math

pygame.font.init()
df = pygame.font.Font(None, 24)


def draw_spline(surface, points, color, width):
    p = []
    for i in range(len(points)):
        t = 0
        while t <= 1:
            tt = t * t
            ttt = tt * t
            q1 = -ttt + 2 * tt - t
            q2 = 3 * ttt - 5 * tt + 2
            q3 = -3 * ttt + 4 * tt + t
            q4 = ttt - tt
            x = 0.5 * (points[i - 1].position.x * q1 +
                       points[i].position.x * q2 +
                       points[(i + 1) % len(points)].position.x * q3 +
                       points[(i + 2) % len(points)].position.x * q4)
            y = 0.5 * (points[i - 1].position.y * q1 +
                       points[i].position.y * q2 +
                       points[(i + 1) % len(points)].position.y * q3 +
                       points[(i + 2) % len(points)].position.y * q4)
            p.append([x, y])
            t += 0.05

    pygame.draw.aalines(surface, color, True, p, width)


screen = pygame.display.set_mode((1600, 1000))
pygame.display.set_caption("Пружинка")

clock = pygame.time.Clock()
done = False

draw_bodies = False

player = Player(100, 100)

t = 6
kt = 1/t

bodies = []
fixing_bodies = []
springs = []
pi2 = math.pi * 2
n = 160
r = 400
cx = 800
cy = 450
K = 1
for k in range(n):
    bodies.append(Body(cx + r * math.sin(pi2 * k / n), cy - r * math.cos(pi2 * k / n)))
    fixing_bodies.append(Body(cx + r * math.sin(pi2 * k / n), cy - r * math.cos(pi2 * k / n), True))
    springs.append(Spring(bodies[-1], fixing_bodies[-1], K))

for k in range(n):
    springs.append(Spring(bodies[k], bodies[((k + 1) % n)], K))

if __name__ == '__main__':
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_y:
                draw_bodies = not draw_bodies
            for body in bodies:
                body.event_update(e)
            player.event_update(e)

        for i in range(t):
            for spring in springs:
                spring.update(kt)

            for body in bodies:
                body.update(kt)
                player.collide_update(body, kt)

            for body in fixing_bodies:
                body.update(kt)

        player.update()

        screen.fill((100, 100, 100))

        player.draw(screen)

        draw_spline(screen, bodies, (0, 0, 0), 2)

        if draw_bodies:
            for body in bodies:
                body.draw(screen)
            for spring in springs:
                spring.draw(screen)

        pygame.display.flip()
        clock.tick(70)
    pygame.quit()
