"""
UI – HUD shows "TURTLES SAVED" instead of level.
"""
import pygame, math, random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, THEMES


class UI:
    COL_BG      = (18,  22,  35)
    COL_TEXT    = (240, 245, 255)
    COL_SUBTEXT = (160, 175, 200)
    COL_ACCENT  = (80,  220, 100)
    COL_GOLD    = (255, 200,  50)
    COL_DANGER  = (230,  60,  60)

    def __init__(self, w, h):
        self.W, self.H = w, h
        pygame.font.init()

        def _f(sz, bold=False):
            for name in ["Segoe UI", "Arial", "DejaVu Sans"]:
                try: return pygame.font.SysFont(name, sz, bold=bold)
                except: pass
            return pygame.font.Font(None, sz)

        self.f_huge   = _f(76, True)
        self.f_title  = _f(54, True)
        self.f_large  = _f(36, True)
        self.f_medium = _f(26)
        self.f_small  = _f(20)
        self.f_tiny   = _f(16)

        self.turtles_saved = 0
        self.theme_idx     = 0
        self._tick         = 0.0
        self._banner_alpha = 0
        self._banner_text  = ""
        self._banner_timer = 0.0
        self._banner_dur   = 2.2

        # UFO intro animation (start menu)
        # Each UFO: {x, y, speed, veering, parked}
        self._intro_ufos    = []
        self._ufo_spawn_t   = 0.0
        self._ufo_wave_gap  = 7.0  # seconds between waves
        self._parked_x      = SCREEN_WIDTH - 80
        self._parked_y      = 30
        self._parked_hov    = 0.0
        self._stopper_done  = False
        self._spawn_ufo_wave()   # trigger first wave immediately

    @property
    def current_theme(self): return THEMES[self.theme_idx % len(THEMES)]

    def update(self, dt):
        self._tick += dt
        self._parked_hov += dt
        if self._banner_alpha > 0:
            self._banner_timer += dt
            t, d = self._banner_timer, self._banner_dur
            if   t < 0.3:         self._banner_alpha = int(255 * t / 0.3)
            elif t < d - 0.5:     self._banner_alpha = 255
            else:                 self._banner_alpha = int(255 * max(0, (d-t)/0.5))
            if t >= d:            self._banner_alpha = 0

        # UFO intro: spawn waves
        self._ufo_spawn_t += dt
        if self._ufo_spawn_t >= self._ufo_wave_gap:
            self._ufo_spawn_t = 0.0
            self._spawn_ufo_wave()

        # Update flying UFOs
        for u in list(self._intro_ufos):
            if u.get('parked'):
                continue
            u['x'] -= u['speed'] * dt
            # Stopper UFO veers toward parked position
            if u.get('stopper'):
                target_y = self._parked_y
                u['y'] += (target_y - u['y']) * 3.0 * dt
                # Check if close enough to park
                if u['x'] <= self._parked_x + 5 and abs(u['y'] - target_y) < 8:
                    u['x'] = self._parked_x
                    u['y'] = self._parked_y
                    u['parked'] = True
                    self._stopper_done = True
            else:
                # Remove regular UFOs that went off screen
                if u['x'] < -120:
                    self._intro_ufos.remove(u)

    # ── Panel helper ───────────────────────────────────────────────────────
    def _panel(self, surf, rect, r=16, col=(20,26,48,215)):
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s, col, s.get_rect(), border_radius=r)
        surf.blit(s, rect.topleft)

    def _shadow_text(self, surf, font, text, col, center):
        sh = font.render(text, True, (0,0,0))
        surf.blit(sh, sh.get_rect(center=(center[0]+3, center[1]+3)))
        img = font.render(text, True, col)
        surf.blit(img, img.get_rect(center=center))

    def _outlined(self, surf, font, text, col, outline, center, thick=2):
        base = font.render(text, True, outline)
        r    = base.get_rect(center=center)
        for dx in range(-thick, thick+1):
            for dy in range(-thick, thick+1):
                if dx or dy: surf.blit(base, r.move(dx,dy))
        surf.blit(font.render(text, True, col), r)

    # ── UFO intro helpers ───────────────────────────────────────────────────
    def _spawn_ufo_wave(self):
        """Spawn 3 UFOs from right side; last one is the stopper."""
        # Remove any old non-parked UFOs
        self._intro_ufos = [u for u in self._intro_ufos if u.get('parked')]
        lanes_y = [160, 250, 340]
        random.shuffle(lanes_y)
        for i, y in enumerate(lanes_y):
            is_stopper = (i == len(lanes_y) - 1)
            start_x    = SCREEN_WIDTH + 60 + i * 80
            self._intro_ufos.append({
                'x': start_x, 'y': float(y),
                'speed': random.randint(130, 190),
                'stopper': is_stopper,
                'parked': False,
                'scale': 0.85 if not is_stopper else 1.0,
            })

    def _draw_ufo_simple(self, surf, cx, cy, scale=1.0, beam=False):
        """Minimal UFO drawn with pygame.draw — no imports needed."""
        w = int(60 * scale); h = int(15 * scale)
        # Body ellipse
        pygame.draw.ellipse(surf, (110, 120, 140), (cx-w//2, cy+4, w, h))
        pygame.draw.ellipse(surf, (190, 205, 225), (cx-w//2+4, cy+5, w-8, h-4))
        # Dome
        dw = int(28*scale); dh = int(18*scale)
        pygame.draw.ellipse(surf, (40, 100, 200), (cx-dw//2, cy-dh+4, dw, dh))
        pygame.draw.ellipse(surf, (80, 160, 255), (cx-dw//4, cy-dh+7, dw//2, dh//2))
        # Lights
        for ang in range(0, 360, 60):
            lx = int(cx + (w//2-4)*math.cos(math.radians(ang)))
            ly = int(cy + 8 + 4*math.sin(math.radians(ang)))
            pygame.draw.circle(surf, (255,220,0), (lx,ly), max(2, int(3*scale)))
        # Beam
        if beam:
            bm = pygame.Surface((int(48*scale), 55), pygame.SRCALPHA)
            bw2 = int(48*scale)
            pygame.draw.polygon(bm, (210,255,80,90),
                                [(6,0),(bw2-6,0),(bw2,55),(0,55)])
            surf.blit(bm, (cx - bw2//2, cy + h + 2))

    def _draw_menu_ufos(self, surf):
        """Draw all intro UFOs (flying + parked) on the menu screen."""
        # Always show parked UFO at top-right (once established)
        if self._stopper_done:
            hy = self._parked_y + int(3*math.sin(self._parked_hov * 2.2))
            self._draw_ufo_simple(surf, self._parked_x, hy, scale=1.0, beam=True)
        for u in self._intro_ufos:
            if u.get('parked'):
                continue  # handled above
            self._draw_ufo_simple(surf, int(u['x']), int(u['y']), scale=u['scale'])

    # ── Start menu ─────────────────────────────────────────────────────────
    def draw_start_menu(self, surf):
        surf.fill(self.COL_BG)
        self._draw_menu_road(surf)
        self._draw_menu_ufos(surf)  # UFOs fly across then one parks top-right
        pw, ph = 490, 340
        px, py = (self.W-pw)//2, (self.H-ph)//2
        self._panel(surf, pygame.Rect(px, py, pw, ph), r=22, col=(18,24,44,228))
        pygame.draw.rect(surf, (*self.COL_ACCENT,160), (px,py,pw,ph), 2, border_radius=22)

        pulse = 1.0 + 0.035*math.sin(self._tick*2.8)
        raw   = self.f_title.render("ROADCROSS", True, self.COL_ACCENT)
        w2,h2 = int(raw.get_width()*pulse), int(raw.get_height()*pulse)
        sc    = pygame.transform.smoothscale(raw,(w2,h2))
        sh    = pygame.transform.smoothscale(self.f_title.render("ROADCROSS",True,(0,0,0)),(w2,h2))
        tr    = sc.get_rect(center=(self.W//2, py+85))
        surf.blit(sh, tr.move(4,5)); surf.blit(sc, tr)

        sub = self.f_medium.render("Cross the road. Rescue the turtles. Beat the aliens.", True, self.COL_SUBTEXT)
        surf.blit(sub, sub.get_rect(center=(self.W//2, py+158)))

        pygame.draw.line(surf, (*self.COL_ACCENT,110), (px+40,py+182),(px+pw-40,py+182), 1)

        for i,(k,v) in enumerate([("↑ ↓ ← →","Move"),("Reach finish","Save the turtle!")]):
            ks = self.f_small.render(f"{k}  –  {v}", True, self.COL_SUBTEXT)
            surf.blit(ks, ks.get_rect(center=(self.W//2, py+205+i*22)))

        a = int(155+100*math.sin(self._tick*3.5))
        btn = self.f_large.render("Press  SPACE  to Play", True, self.COL_GOLD)
        btn.set_alpha(a); surf.blit(btn, btn.get_rect(center=(self.W//2, py+296)))

    def _draw_menu_road(self, surf):
        rh = 220; ry = (self.H-rh)//2
        rs = pygame.Surface((self.W,rh),pygame.SRCALPHA); rs.fill((35,38,48,148)); surf.blit(rs,(0,ry))
        dw,gap,lh = 40,20,55
        for i in range(3):
            y = ry+lh*i+lh//2
            off = int(self._tick*110)%(dw+gap)
            x = -off
            while x<self.W:
                pygame.draw.line(surf,(88,90,105),(x,y),(min(x+dw,self.W),y),2); x+=dw+gap

    # ── HUD ────────────────────────────────────────────────────────────────
    def draw_hud(self, surf):
        th  = self.current_theme
        amb = th.get("ambient",(80,200,100))

        # Turtles saved (top-left) — turtle emoji + count
        bw,bh = 220,52
        self._panel(surf, pygame.Rect(10,10,bw,bh), r=12, col=(10,14,30,218))
        pygame.draw.rect(surf,(*amb,155),(10,10,bw,bh),1,border_radius=12)
        lbl = self.f_tiny.render("TURTLES SAVED", True, self.COL_SUBTEXT)
        surf.blit(lbl, lbl.get_rect(midleft=(26,25)))
        num = self.f_large.render(f"🐢  {self.turtles_saved}", True, self.COL_GOLD)
        surf.blit(num, num.get_rect(midleft=(22,42)))

        # Area name (top-center)
        aname = th["name"]
        aw = max(160, self.f_small.size(aname)[0]+30)
        ax = (self.W-aw)//2
        self._panel(surf, pygame.Rect(ax,10,aw,38), r=10, col=(10,14,30,205))
        pygame.draw.rect(surf,(*amb,115),(ax,10,aw,38),1,border_radius=10)
        at = self.f_small.render(aname.upper(), True, amb)
        surf.blit(at, at.get_rect(center=(self.W//2,29)))

        # (Speed bars removed — was covering the alien/turtle/UFO scene)

    # ── Banner ─────────────────────────────────────────────────────────────
    def trigger_banner(self, text):
        self._banner_text = text; self._banner_alpha = 1; self._banner_timer = 0.0

    def draw_banner(self, surf):
        if self._banner_alpha <= 0: return
        th  = self.current_theme
        amb = th.get("ambient",(80,200,100))
        pw,ph = 500,72; ps = pygame.Surface((pw,ph),pygame.SRCALPHA)
        pygame.draw.rect(ps,(*th.get("sky",(10,14,30)),210),ps.get_rect(),border_radius=36)
        pygame.draw.rect(ps,(*amb,200),ps.get_rect(),2,border_radius=36)
        ps.set_alpha(self._banner_alpha); surf.blit(ps,((self.W-pw)//2,(self.H-ph)//2))
        e = self.f_tiny.render("ENTERING", True, self.COL_SUBTEXT); e.set_alpha(self._banner_alpha)
        surf.blit(e, e.get_rect(center=(self.W//2,self.H//2-8)))
        n = self.f_large.render(self._banner_text.upper(), True, amb); n.set_alpha(self._banner_alpha)
        surf.blit(n, n.get_rect(center=(self.W//2,self.H//2+18)))

    # ── Level-up flash ─────────────────────────────────────────────────────
    def draw_level_up_flash(self, surf, progress):
        alpha = int(255*(1.0-progress))
        th    = self.current_theme
        fl    = pygame.Surface((self.W,self.H),pygame.SRCALPHA)
        fl.fill((*th.get("ambient",(80,200,100)),min(110,alpha)))
        surf.blit(fl,(0,0))

    # ── Game over ──────────────────────────────────────────────────────────
    def draw_game_over(self, surf):
        ov = pygame.Surface((self.W,self.H),pygame.SRCALPHA); ov.fill((0,0,0,165)); surf.blit(ov,(0,0))
        pw,ph = 500,330; px,py = (self.W-pw)//2,(self.H-ph)//2
        self._panel(surf,pygame.Rect(px,py,pw,ph),r=22,col=(22,8,8,238))
        pygame.draw.rect(surf,self.COL_DANGER,(px,py,pw,ph),2,border_radius=22)
        self._outlined(surf,self.f_huge,"WASTED",self.COL_DANGER,(80,8,8),(self.W//2,py+95),thick=3)
        area = self.f_medium.render(f"Last area:  {self.current_theme['name']}", True, self.COL_SUBTEXT)
        surf.blit(area, area.get_rect(center=(self.W//2,py+185)))
        lvl = self.f_large.render(f"Turtles Saved:  {self.turtles_saved}", True, self.COL_GOLD)
        surf.blit(lvl, lvl.get_rect(center=(self.W//2,py+228)))
        a = int(155+100*math.sin(self._tick*3.5))
        rs = self.f_medium.render("Press  SPACE  to Restart", True, self.COL_TEXT); rs.set_alpha(a)
        surf.blit(rs, rs.get_rect(center=(self.W//2,py+290)))

    # ── Mutations ──────────────────────────────────────────────────────────
    def save_turtle(self):    self.turtles_saved += 1
    def advance_theme(self):  self.theme_idx += 1
    def reset(self):
        self.turtles_saved  = 0
        self.theme_idx      = 0
        self._intro_ufos    = []
        self._ufo_spawn_t   = 0.0
        self._stopper_done  = False
