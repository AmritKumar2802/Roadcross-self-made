"""
finish_scene.py – alien kidnapper scene + rescue animation state machine.
Positions: top-right safe zone. Alien at ~(595, 38), child at (548, 40), UFO at (630, 16).
"""
import pygame, math, random

# ── Scene anchor positions ────────────────────────────────────────────────
UFO_X,   UFO_Y   = 630, 16
ALIEN_X, ALIEN_Y = 595, 38
CHILD_X, CHILD_Y = 548, 40

# ── Animation phases ───────────────────────────────────────────────────────
P_IDLE       = "idle"
P_WALK_IN    = "walk_in"
P_PUNCH      = "punch"
P_FLEE       = "flee"
P_JOIN       = "join"
P_CELEBRATE  = "celebrate"
P_DONE       = "done"

DURATIONS = {P_WALK_IN: 0.5, P_PUNCH: 0.6, P_FLEE: 0.8, P_JOIN: 0.55, P_CELEBRATE: 0.7}


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ── Primitive drawing helpers ──────────────────────────────────────────────

def _draw_ufo(surf, cx, cy, beam_alpha=110):
    # Beam
    if beam_alpha > 0:
        bm = pygame.Surface((52, 55), pygame.SRCALPHA)
        pygame.draw.polygon(bm, (210, 255, 80, beam_alpha), [(8,0),(44,0),(52,55),(0,55)])
        surf.blit(bm, (cx - 26, cy + 12))
    # Saucer body
    pygame.draw.ellipse(surf, (110, 120, 140), (cx-38, cy+6,  76, 18))
    pygame.draw.ellipse(surf, (180, 195, 215), (cx-30, cy+7,  60,  9))  # sheen
    # Dome
    pygame.draw.ellipse(surf, (40, 100, 190),  (cx-20, cy-10, 40, 24))
    pygame.draw.ellipse(surf, (80, 160, 255),  (cx-12, cy-5,  18, 12))  # highlight
    # Rim lights
    for i, ang in enumerate(range(0, 360, 60)):
        lx = int(cx + 32*math.cos(math.radians(ang)))
        ly = int(cy + 12 + 6*math.sin(math.radians(ang)))
        c  = [(255,220,0),(0,255,160),(255,80,0),(0,200,255),(255,0,160),(120,255,0)][i]
        pygame.draw.circle(surf, c, (lx, ly), 3)


def _draw_alien(surf, cx, cy, flash=False, shake=0):
    cx = cx + shake
    bc = (200, 30, 30) if flash else (55, 200, 75)
    dk = (100, 15, 15) if flash else (30, 140, 45)
    # Body
    pygame.draw.ellipse(surf, bc,  (cx-9,  cy+6,  18, 24))
    # Head
    pygame.draw.circle(surf, bc,   (cx, cy),  13)
    pygame.draw.circle(surf, dk,   (cx, cy),  13, 1)
    # Eyes
    pygame.draw.ellipse(surf, (10,10,10),  (cx-11, cy-5, 10, 8))
    pygame.draw.ellipse(surf, (10,10,10),  (cx+1,  cy-5, 10, 8))
    pygame.draw.circle(surf,  (255,255,255), (cx-7, cy-2), 3)
    pygame.draw.circle(surf,  (255,255,255), (cx+5, cy-2), 3)
    pygame.draw.circle(surf,  (0,0,0),       (cx-6, cy-2), 1)
    pygame.draw.circle(surf,  (0,0,0),       (cx+6, cy-2), 1)
    # Mouth (smug line)
    pygame.draw.arc(surf, (10,80,20), (cx-6, cy+3, 12, 6), math.pi, 2*math.pi, 2)
    # Antenna
    pygame.draw.line(surf, bc, (cx, cy-13), (cx+5, cy-24), 2)
    pygame.draw.circle(surf, (255,40,40), (cx+5, cy-24), 3)
    # Arms
    pygame.draw.line(surf, bc, (cx-9, cy+10), (cx-22, cy+6), 2)
    pygame.draw.line(surf, bc, (cx+9, cy+10), (cx+22, cy+6), 2)
    # Legs
    pygame.draw.line(surf, bc, (cx-4, cy+30), (cx-6, cy+40), 2)
    pygame.draw.line(surf, bc, (cx+4, cy+30), (cx+6, cy+40), 2)


def _draw_child_turtle(surf, cx, cy, happy=False, scared=False):
    r = 10
    sc = (200, 130, 30) if not happy else (60, 220, 90)
    # Shell
    pygame.draw.ellipse(surf, sc, (cx-r+1, cy-r+1, (r-1)*2, (r-1)*2))
    pygame.draw.ellipse(surf, tuple(max(0,c-30) for c in sc), (cx-r+1, cy-r+1, (r-1)*2, (r-1)*2), 1)
    # Shell patch
    pygame.draw.circle(surf, tuple(max(0,c-20) for c in sc), (cx, cy), 5)
    # Head (facing left)
    hc = (80, 200, 100) if happy else (90, 180, 80)
    pygame.draw.ellipse(surf, hc, (cx-r-6, cy-4, 12, 9))
    # Eye
    pygame.draw.circle(surf, (0,0,0), (cx-r-2, cy-1), 2)
    if scared:
        pygame.draw.arc(surf, (80,0,0), (cx-r-7, cy+2, 8, 5), 0, math.pi, 1)   # sad mouth
    elif happy:
        pygame.draw.arc(surf, (0,100,0), (cx-r-7, cy+2, 8, 5), math.pi, 2*math.pi, 1)
    # Legs
    leg = (80, 180, 90)
    pygame.draw.ellipse(surf, leg, (cx-r-1, cy+r-4, 7, 5))   # back leg left
    pygame.draw.ellipse(surf, leg, (cx+r-5, cy+r-4, 7, 5))   # back leg right


def _draw_pow(surf, cx, cy, alpha):
    """Comic-book POW! star."""
    pts = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        rad   = 26 if i % 2 == 0 else 12
        pts.append((cx + rad*math.cos(angle), cy + rad*math.sin(angle)))
    star = pygame.Surface((70, 60), pygame.SRCALPHA)
    center_s = (35, 30)
    pts_s = [(int(p[0]-cx+35), int(p[1]-cy+30)) for p in pts]
    pygame.draw.polygon(star, (255, 220, 0, alpha), pts_s)
    pygame.draw.polygon(star, (255, 140, 0, alpha), pts_s, 2)
    font = pygame.font.SysFont("Arial", 15, bold=True)
    t = font.render("POW!", True, (200, 0, 0))
    t.set_alpha(alpha)
    star.blit(t, t.get_rect(center=center_s))
    surf.blit(star, (cx - 35, cy - 30))


# ── Main class ────────────────────────────────────────────────────────────

class FinishScene:
    def __init__(self):
        self.phase        = P_IDLE
        self.phase_timer  = 0.0
        self.is_done      = False
        self._reset_anims()

    def _reset_anims(self):
        self.alien_x       = float(ALIEN_X)
        self.alien_y       = float(ALIEN_Y)
        self.ufo_x         = float(UFO_X)
        self.ufo_y         = float(UFO_Y)
        self.child_x       = float(CHILD_X)
        self.child_y       = float(CHILD_Y)
        self.alien_visible = True
        self.beam_alpha    = 110
        self.alien_flash   = False
        self.alien_shake   = 0
        self.pow_alpha     = 0
        self.child_happy   = False
        self.particles     = []
        self._player_start_x = 0
        self._player_start_y = 0
        self._tick         = 0.0

    def reset(self):
        self.phase       = P_IDLE
        self.phase_timer = 0.0
        self.is_done     = False
        self._reset_anims()

    def start_rescue(self, player):
        self._player_start_x = float(player.rect.centerx)
        self._player_start_y = float(player.rect.centery)
        self.phase       = P_WALK_IN
        self.phase_timer = 0.0
        self.is_done     = False

    # ── Update ─────────────────────────────────────────────────────────────
    def update(self, dt, player):
        self._tick += dt

        if self.phase == P_IDLE:
            self.ufo_y = UFO_Y + 3 * math.sin(self._tick * 2.2)
            return

        self.phase_timer += dt
        dur = DURATIONS.get(self.phase, 0.5)
        t   = self.phase_timer / dur
        s   = _smooth(min(t, 1.0))

        if self.phase == P_WALK_IN:
            tx = ALIEN_X - 36
            player.rect.centerx = int(self._player_start_x + s*(tx - self._player_start_x))
            player.rect.centery = int(self._player_start_y + s*(ALIEN_Y - self._player_start_y))
            self.ufo_y = UFO_Y + 3 * math.sin(self._tick * 2.2)
            if t >= 1.0: self._next(P_PUNCH)

        elif self.phase == P_PUNCH:
            shake_mag       = int(6 * math.sin(t * math.pi * 10))
            self.alien_shake = shake_mag
            self.alien_flash = (int(t * 12) % 2 == 0)
            self.pow_alpha   = int(255 * min(1.0, t * 3))
            if t >= 1.0:
                self.alien_flash = False
                self.alien_shake = 0
                self.pow_alpha   = 0
                self._next(P_FLEE)

        elif self.phase == P_FLEE:
            if t < 0.45:
                sub = _smooth(t / 0.45)
                self.alien_x  = ALIEN_X + sub * (UFO_X - ALIEN_X)
                self.alien_y  = ALIEN_Y
                self.beam_alpha = int(110 * (1 - sub))
            else:
                self.alien_visible = False
                sub = _smooth((t - 0.45) / 0.55)
                self.ufo_y = UFO_Y - sub * 180
            if t >= 1.0: self._next(P_JOIN)

        elif self.phase == P_JOIN:
            tx = player.rect.centerx + 28
            ty = player.rect.centery
            self.child_x = CHILD_X + s * (tx - CHILD_X)
            self.child_y = CHILD_Y + s * (ty - CHILD_Y)
            if t >= 1.0:
                self.child_happy = True
                self._next(P_CELEBRATE)

        elif self.phase == P_CELEBRATE:
            # Burst particles
            if len(self.particles) < 50:
                for _ in range(4):
                    self.particles.append({
                        'x': player.rect.centerx + random.randint(-20, 20),
                        'y': player.rect.centery + random.randint(-20, 20),
                        'vx': random.uniform(-90, 90),
                        'vy': random.uniform(-130, -30),
                        'life': 1.0,
                        'col': random.choice([(255,215,0),(80,220,100),(255,100,200),(100,200,255),(255,140,30)]),
                        'sz': random.randint(4, 10)
                    })
            for p in self.particles:
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
                p['vy'] += 210 * dt
                p['life'] -= dt * 1.8
            self.particles = [p for p in self.particles if p['life'] > 0]
            if t >= 1.0:
                self.phase   = P_DONE
                self.is_done = True

    def _next(self, phase):
        self.phase       = phase
        self.phase_timer = 0.0

    # ── Draw ───────────────────────────────────────────────────────────────
    def draw(self, surf):
        # UFO
        if self.ufo_y > -100:
            _draw_ufo(surf, int(self.ufo_x), int(self.ufo_y), beam_alpha=self.beam_alpha)

        # Alien
        if self.alien_visible:
            _draw_alien(surf, int(self.alien_x), int(self.alien_y),
                        flash=self.alien_flash, shake=self.alien_shake)

        # Child turtle
        _draw_child_turtle(surf, int(self.child_x), int(self.child_y),
                           happy=self.child_happy, scared=not self.child_happy)

        # POW!
        if self.pow_alpha > 0:
            _draw_pow(surf, int(self.alien_x) - 20, int(self.alien_y) - 30, self.pow_alpha)

        # Particles
        for p in self.particles:
            a  = int(255 * p['life'])
            sz = max(1, int(p['sz'] * p['life']))
            ps = pygame.Surface((sz*2, sz*2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p['col'], a), (sz, sz), sz)
            surf.blit(ps, (int(p['x']-sz), int(p['y']-sz)))

        # "TURTLE SAVED!" banner during celebrate
        if self.phase == P_CELEBRATE:
            font = pygame.font.SysFont("Arial", 28, bold=True)
            txt = font.render("🐢  TURTLE SAVED!  🐢", True, (255, 215, 0))
            surf.blit(txt, txt.get_rect(center=(350, 300)))
