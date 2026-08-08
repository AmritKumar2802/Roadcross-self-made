"""
Player – drawn programmatically. Supports 4-directional movement.
"""
import pygame, math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_START_Y, FINISH_LINE_Y, ROAD_TOP, ROAD_BOTTOM


def build_player_surface(size=44) -> pygame.Surface:
    s  = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    r  = size // 2 - 2

    # Shell
    pygame.draw.ellipse(s, (30, 160, 60), (cx-r+4, cy-r+4, (r-4)*2, (r-4)*2))
    patch = (20, 130, 45)
    for ang, pr in [(90,9),(30,9),(150,9),(270,9),(210,9),(330,9)]:
        a = math.radians(ang)
        pygame.draw.circle(s, patch, (int(cx+pr*math.cos(a)), int(cy-pr*math.sin(a))), 5)
    pygame.draw.ellipse(s, (15, 100, 35), (cx-r+4, cy-r+4, (r-4)*2, (r-4)*2), 2)

    # Head (up)
    pygame.draw.ellipse(s, (60, 200, 80), (cx-6, 0, 12, 10))
    pygame.draw.circle(s, (0,0,0),       (cx-3, 3), 2)
    pygame.draw.circle(s, (0,0,0),       (cx+3, 3), 2)
    pygame.draw.circle(s, (255,255,255), (cx-3, 2), 1)
    pygame.draw.circle(s, (255,255,255), (cx+3, 2), 1)

    # Legs
    leg = (60, 190, 70)
    pygame.draw.ellipse(s, leg, (0,        cy-7,  8, 12))
    pygame.draw.ellipse(s, leg, (size-8,   cy-7,  8, 12))
    pygame.draw.ellipse(s, leg, (2,        cy+4,  8, 10))
    pygame.draw.ellipse(s, leg, (size-10,  cy+4,  8, 10))
    # Tail
    pygame.draw.ellipse(s, leg, (cx-4, size-8, 8, 8))
    return s


class Player:
    SPEED = 220   # px / second

    def __init__(self):
        self.image   = build_player_surface(44)
        self.rect    = self.image.get_rect()
        self.go_to_start()

        self.move_up    = False
        self.move_down  = False
        self.move_left  = False
        self.move_right = False

    # ── Update (called every frame during STATE_PLAYING) ───────────────────
    def update(self, dt: float):
        dx, dy = 0, 0
        if self.move_up:    dy -= self.SPEED * dt
        if self.move_down:  dy += self.SPEED * dt
        if self.move_left:  dx -= self.SPEED * dt
        if self.move_right: dx += self.SPEED * dt

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # Clamp to screen bounds
        self.rect.left   = max(0, self.rect.left)
        self.rect.right  = min(SCREEN_WIDTH, self.rect.right)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)
        # Don't clamp top — going past FINISH_LINE_Y triggers rescue

    def go_to_start(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery  = PLAYER_START_Y

    def stop_all(self):
        self.move_up = self.move_down = self.move_left = self.move_right = False

    def is_at_finish_line(self) -> bool:
        return self.rect.top < FINISH_LINE_Y

    @property
    def hitbox(self) -> pygame.Rect:
        return self.rect.inflate(-12, -12)