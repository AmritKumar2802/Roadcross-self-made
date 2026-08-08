"""
Shared constants and world themes for Roadcross.

Screen layout (700 x 600):
  y=0  ..  y=60  : top safe zone (finish/grass)
  y=60 .. y=540  : road  (480px, 6 lanes x 80px each)
  y=540.. y=600  : bottom safe zone (start/grass)

Lane centres: [100, 180, 260, 340, 420, 500]
"""

SCREEN_WIDTH  = 700
SCREEN_HEIGHT = 600

ROAD_TOP    = 60
ROAD_BOTTOM = 540
LANE_HEIGHT = 80          # (ROAD_BOTTOM - ROAD_TOP) / 6
NUM_LANES   = 6

LANE_CENTERS = [ROAD_TOP + LANE_HEIGHT * i + LANE_HEIGHT // 2
                for i in range(NUM_LANES)]   # [100, 180, 260, 340, 420, 500]

FINISH_LINE_Y  = ROAD_TOP - 10
PLAYER_START_Y = ROAD_BOTTOM + 30

# ── World themes ──────────────────────────────────────────────────────────
# Each theme has: name, grass, road, dash, kerb, finish, sky (HUD/menu)
THEMES = [
    {
        "name":   "Suburbs",
        "grass":  (67,  160,  71),
        "road":   (55,   55,  60),
        "dash":   (255, 255, 255),
        "kerb":   (220, 220, 220),
        "finish": (255, 215,   0),
        "sky":    (18,   22,  35),
        "ambient":(67,  160,  71),   # colour tint for HUD badge
    },
    {
        "name":   "Golden Hour",
        "grass":  (180,  95,  30),
        "road":   (75,   60,  45),
        "dash":   (255, 180,  60),
        "kerb":   (240, 160,  80),
        "finish": (255, 120,  20),
        "sky":    (80,   30,  10),
        "ambient":(200, 120,  30),
    },
    {
        "name":   "Night City",
        "grass":  (10,   30,  15),
        "road":   (18,   18,  28),
        "dash":   (80,  140, 255),
        "kerb":   (60,   60, 110),
        "finish": (0,   200, 255),
        "sky":    (5,    5,  20),
        "ambient":(30,   60, 180),
    },
    {
        "name":   "Desert",
        "grass":  (210, 175,  90),
        "road":   (130, 105,  65),
        "dash":   (255, 220, 140),
        "kerb":   (200, 155,  75),
        "finish": (255, 140,   0),
        "sky":    (90,   50,  10),
        "ambient":(200, 150,  60),
    },
    {
        "name":   "Arctic",
        "grass":  (210, 230, 245),
        "road":   (75,   85,  95),
        "dash":   (200, 220, 240),
        "kerb":   (180, 200, 220),
        "finish": (80,  200, 255),
        "sky":    (20,   40,  70),
        "ambient":(150, 200, 240),
    },
    {
        "name":   "Cyberpunk",
        "grass":  (10,    5,  25),
        "road":   (12,    8,  22),
        "dash":   (220,   0, 190),
        "kerb":   (0,   180, 200),
        "finish": (180,   0, 255),
        "sky":    (5,     0,  20),
        "ambient":(180,   0, 200),
    },
]
