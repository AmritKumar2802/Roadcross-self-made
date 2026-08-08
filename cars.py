"""
CarManager – cars drawn 100% programmatically.
No image files → no background squares, no rotation issues.
Each car type is a distinct shape drawn onto a per-Surface with transparency.
"""
import pygame
import random
from constants import SCREEN_WIDTH, LANE_CENTERS, LANE_HEIGHT

BASE_SPEED = 160
MAX_SPEED  = 520   # Cap: base + 9 increments of 40 (level-10 equivalent)


# ── Car drawing helpers ────────────────────────────────────────────────────

def _make_surface(w: int, h: int) -> pygame.Surface:
    """Transparent surface."""
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    return s


def draw_sedan(color: tuple) -> pygame.Surface:
    """Classic 4-door sedan silhouette (facing left, moving left)."""
    W, H = 96, 46
    s = _make_surface(W, H)
    body_color  = color
    roof_color  = tuple(max(0, c - 40) for c in color)
    glass_color = (140, 200, 230, 200)
    wheel_color = (30, 30, 30)
    rim_color   = (180, 180, 180)

    # body
    pygame.draw.rect(s, body_color, (4, 14, 88, 22), border_radius=5)
    # roof cabin
    pygame.draw.rect(s, roof_color, (24, 6, 46, 14), border_radius=4)
    # windscreens
    pygame.draw.rect(s, glass_color, (26, 7, 18, 12), border_radius=2)   # front
    pygame.draw.rect(s, glass_color, (52, 7, 16, 12), border_radius=2)   # rear
    # headlights (front = left side of image)
    pygame.draw.rect(s, (255, 255, 200), (4, 16, 8, 6), border_radius=2)
    # tail lights (rear = right side)
    pygame.draw.rect(s, (220, 50, 50), (84, 16, 8, 6), border_radius=2)
    # wheels
    for wx, wy in [(14, 32), (72, 32)]:
        pygame.draw.circle(s, wheel_color, (wx, wy), 10)
        pygame.draw.circle(s, rim_color,   (wx, wy),  5)
    return s


def draw_suv(color: tuple) -> pygame.Surface:
    """Tall SUV / pickup style."""
    W, H = 100, 50
    s = _make_surface(W, H)
    body_color  = color
    roof_color  = tuple(max(0, c - 50) for c in color)
    glass_color = (140, 200, 230, 200)
    wheel_color = (30, 30, 30)
    rim_color   = (200, 200, 200)

    pygame.draw.rect(s, body_color, (4, 10, 92, 28), border_radius=6)
    pygame.draw.rect(s, roof_color, (18, 3,  62, 14), border_radius=4)
    pygame.draw.rect(s, glass_color,(20, 4,  22, 12), border_radius=2)
    pygame.draw.rect(s, glass_color,(46, 4,  30, 12), border_radius=2)
    pygame.draw.rect(s, (255, 255, 180), (4, 14, 10, 8), border_radius=2)
    pygame.draw.rect(s, (220, 60, 60),   (86, 14, 10, 8), border_radius=2)
    for wx, wy in [(18, 36), (78, 36)]:
        pygame.draw.circle(s, wheel_color, (wx, wy), 11)
        pygame.draw.circle(s, rim_color,   (wx, wy),  5)
    return s


def draw_taxi(color=(240, 200, 0)) -> pygame.Surface:
    """Yellow taxi cab."""
    W, H = 94, 46
    s = _make_surface(W, H)
    pygame.draw.rect(s, color,           (4, 14, 86, 22), border_radius=5)
    pygame.draw.rect(s, (210, 170, 0),   (24, 6, 44, 14), border_radius=4)
    # taxi sign on roof
    pygame.draw.rect(s, (255, 255, 255), (35, 2, 22, 6),  border_radius=2)
    glass = (140, 200, 230, 200)
    pygame.draw.rect(s, glass, (26, 7, 16, 11), border_radius=2)
    pygame.draw.rect(s, glass, (50, 7, 16, 11), border_radius=2)
    pygame.draw.rect(s, (255, 255, 180), (4,  16, 8, 6), border_radius=2)
    pygame.draw.rect(s, (200, 50, 50),   (82, 16, 8, 6), border_radius=2)
    wc, rc = (30, 30, 30), (180, 180, 180)
    for wx, wy in [(14, 32), (72, 32)]:
        pygame.draw.circle(s, wc, (wx, wy), 10)
        pygame.draw.circle(s, rc, (wx, wy),  5)
    return s


def draw_truck(color=(60, 100, 200)) -> pygame.Surface:
    """Delivery / box truck — longer body."""
    W, H = 120, 52
    s = _make_surface(W, H)
    # cargo box
    pygame.draw.rect(s, color,          (36, 6, 80, 34), border_radius=3)
    # cab
    cab_color = tuple(max(0, c - 30) for c in color)
    pygame.draw.rect(s, cab_color,      (4, 12, 38, 28), border_radius=5)
    glass = (140, 200, 230, 200)
    pygame.draw.rect(s, glass,          (6, 14, 20, 14), border_radius=2)
    pygame.draw.rect(s, (255, 255, 180), (4, 18, 8, 8), border_radius=2)
    pygame.draw.rect(s, (200, 50, 50),  (108, 18, 8, 8), border_radius=2)
    wc, rc = (30, 30, 30), (190, 190, 190)
    for wx, wy in [(18, 40), (90, 40), (106, 40)]:
        pygame.draw.circle(s, wc, (wx, wy), 11)
        pygame.draw.circle(s, rc, (wx, wy),  5)
    return s


def draw_sportscar(color: tuple) -> pygame.Surface:
    """Low, wide sports car."""
    W, H = 98, 42
    s = _make_surface(W, H)
    pygame.draw.rect(s, color,          (4, 16, 90, 18), border_radius=8)
    roof_color = tuple(max(0, c - 60) for c in color)
    # Sleek low roof polygon
    roof_pts = [(28, 16), (68, 16), (62, 6), (34, 6)]
    pygame.draw.polygon(s, roof_color, roof_pts)
    glass = (140, 200, 230, 200)
    pygame.draw.polygon(s, glass, [(30, 15), (46, 15), (44, 7), (32, 7)])
    pygame.draw.polygon(s, glass, [(52, 15), (66, 15), (60, 7), (50, 7)])
    pygame.draw.rect(s, (255, 255, 150), (4,  18, 10, 6), border_radius=2)
    pygame.draw.rect(s, (255, 60, 60),   (84, 18, 10, 6), border_radius=2)
    wc, rc = (25, 25, 25), (200, 200, 200)
    for wx, wy in [(16, 30), (76, 30)]:
        pygame.draw.circle(s, wc, (wx, wy), 10)
        pygame.draw.circle(s, rc, (wx, wy),  5)
    return s


# ── Palette of car types ───────────────────────────────────────────────────
CAR_PALETTE = [
    # (draw_fn, *extra_args_or_color)
    (draw_sedan,    (220, 50,  50)),   # red sedan
    (draw_sedan,    (50,  100, 220)),  # blue sedan
    (draw_sedan,    (50,  180, 80)),   # green sedan
    (draw_sedan,    (160, 60,  200)),  # purple sedan
    (draw_suv,      (230, 120, 30)),   # orange SUV
    (draw_suv,      (30,  150, 150)),  # teal SUV
    (draw_taxi,),                      # yellow taxi (uses default color)
    (draw_truck,),                     # blue truck  (uses default color)
    (draw_truck,    (80,  160, 80)),   # green truck
    (draw_sportscar,(240, 30,  30)),   # red sports
    (draw_sportscar,(240, 200, 20)),   # gold sports
    (draw_sportscar,(20,  20,  200)),  # blue sports
]


class CarManager:
    def __init__(self):
        self.cars = pygame.sprite.Group()
        self.base_speed    = BASE_SPEED
        self.spawn_timer   = 0.0
        self.spawn_interval= 0.85
        self.both_dirs     = False   # cars from both left AND right

        # Pre-render RTL (right-to-left, facing left) surfaces
        self._rtl: list[pygame.Surface] = []
        for entry in CAR_PALETTE:
            fn, *args = entry
            self._rtl.append(fn(*args))

        # LTR = horizontally flipped RTL (facing right)
        self._ltr = [pygame.transform.flip(s, True, False) for s in self._rtl]

    # ─── public API ───────────────────────────────────────────────────

    def update(self, dt: float):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self._create_car()
        for car in list(self.cars):
            car.rect.x += car.direction * self.base_speed * dt
            # Kill if off either edge
            if car.rect.right < -20 or car.rect.left > SCREEN_WIDTH + 20:
                car.kill()

    def level_up(self, turtles_saved: int):
        # Speed cap at level 10 equivalent
        if self.base_speed < MAX_SPEED:
            self.base_speed = min(self.base_speed + 40, MAX_SPEED)
        self.spawn_interval = max(0.25, self.spawn_interval * 0.88)

        # Reset speed after saving turtle #40
        if turtles_saved == 40:
            self.base_speed     = BASE_SPEED
            self.spawn_interval = 0.85

        # Enable bidirectional traffic at every multiple-of-20 save
        self.both_dirs = (turtles_saved > 0 and turtles_saved % 20 == 0)

    def reset(self):
        self.cars.empty()
        self.base_speed     = BASE_SPEED
        self.spawn_interval = 0.85
        self.spawn_timer    = 0.0
        self.both_dirs      = False

    # ─── internal ────────────────────────────────────────────────────────

    def _create_car(self):
        """Spawn a car centred in a random lane, from left or right."""
        car = pygame.sprite.Sprite()
        idx = random.randrange(len(self._rtl))
        lane_y = random.choice(LANE_CENTERS)

        # Decide direction
        go_ltr = self.both_dirs and random.random() < 0.45  # ~45 % from left when bi-dir

        if go_ltr:
            car.image     = self._ltr[idx]
            car.rect      = car.image.get_rect()
            car.rect.midright = (-10, lane_y)   # spawn left edge
            car.direction = +1                   # moves right
        else:
            car.image     = self._rtl[idx]
            car.rect      = car.image.get_rect()
            car.rect.midleft = (SCREEN_WIDTH + 10, lane_y)  # spawn right edge
            car.direction = -1                               # moves left

        self.cars.add(car)