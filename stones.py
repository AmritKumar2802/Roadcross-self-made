"""stones.py – Static stone obstacles on the road, repositioned each level."""
import pygame, random
from constants import SCREEN_WIDTH, LANE_CENTERS

def _draw_stone(cx, cy, rx, ry, col) -> pygame.Surface:
    w, h = rx*2+6, ry*2+6
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    # Main body
    pygame.draw.ellipse(s, col, (3, 3, rx*2, ry*2))
    # Highlight
    hi = tuple(min(255, c+50) for c in col)
    pygame.draw.ellipse(s, hi, (5, 4, rx, ry//2+2))
    # Outline
    dk = tuple(max(0, c-40) for c in col)
    pygame.draw.ellipse(s, dk, (3, 3, rx*2, ry*2), 2)
    return s

STONE_COLS = [(120,115,108),(100,95,88),(140,128,115),(105,100,92)]

class StoneManager:
    def __init__(self):
        self.stones: list[tuple[pygame.Surface, pygame.Rect]] = []

    def set_level(self, turtles_saved: int):
        """Regenerate stones deterministically for this level number."""
        self.stones.clear()
        if turtles_saved == 0:
            return
        rng = random.Random(turtles_saved * 31 + 17)
        n = rng.randint(3, 5)
        # Avoid the same lane twice in a row
        used_lanes = []
        for _ in range(n):
            available = [l for l in LANE_CENTERS if l not in used_lanes[-1:]]
            lane_y = rng.choice(available)
            used_lanes.append(lane_y)
            x  = rng.randint(80, SCREEN_WIDTH - 80)
            rx = rng.randint(18, 30)
            ry = rng.randint(11, 20)
            col = rng.choice(STONE_COLS)
            surf = _draw_stone(0, 0, rx, ry, col)
            rect = surf.get_rect(center=(x, lane_y))
            self.stones.append((surf, rect))

    def draw(self, surf: pygame.Surface):
        for stone_surf, stone_rect in self.stones:
            surf.blit(stone_surf, stone_rect)

    def check_collision(self, player_hitbox: pygame.Rect) -> bool:
        for _, rect in self.stones:
            if player_hitbox.colliderect(rect.inflate(-6, -4)):
                return True
        return False

    def reset(self):
        self.stones.clear()
