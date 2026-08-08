"""endings.py – Win screen (100 turtles) and Game-Over cinematic."""
import pygame, math, random

def _f(sz, bold=False):
    for n in ["Segoe UI","Arial","DejaVu Sans"]:
        try: return pygame.font.SysFont(n, sz, bold=bold)
        except: pass
    return pygame.font.Font(None, sz)

def _wrap(font, text, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if font.size(test)[0] <= max_w: cur = test
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

# ─── tiny turtle helper ───────────────────────────────────────────────────
def _mini_turtle(surf, cx, cy, r=9, happy=False):
    sc = (40, 160, 65)
    pygame.draw.ellipse(surf, sc, (cx-r+1, cy-r+1, (r-1)*2, (r-1)*2))
    hc = (70, 200, 90)
    pygame.draw.ellipse(surf, hc, (cx-r-4, cy-3, 9, 7))
    pygame.draw.circle(surf, (0,0,0), (cx-r-1, cy-1), 1)
    if happy:
        pygame.draw.arc(surf, (0,100,0), (cx-r-5,cy+1,7,4), math.pi, 2*math.pi, 1)

# ─── large happy turtle (win screen centre) ──────────────────────────────
def _big_turtle(surf, cx, cy, size=110, tick=0.0):
    r = size // 2
    # shell
    shell = (35, 155, 65)
    pygame.draw.ellipse(surf, shell, (cx-r+6, cy-r+6, (r-6)*2, (r-6)*2))
    patch = (25, 120, 45)
    for ang, pr in [(90,r//2),(30,r//2),(150,r//2),(270,r//2),(210,r//2),(330,r//2)]:
        a = math.radians(ang)
        pygame.draw.circle(surf, patch, (int(cx+pr*math.cos(a)), int(cy-pr*math.sin(a))), r//5)
    pygame.draw.ellipse(surf, (15,100,35), (cx-r+6, cy-r+6, (r-6)*2, (r-6)*2), 2)
    # head
    hy = int(4*math.sin(tick*3))
    pygame.draw.ellipse(surf, (65, 210, 85), (cx-22, cy-r-18+hy, 44, 36))
    # eyes
    for ex in [-9, 9]:
        pygame.draw.circle(surf, (0,0,0), (cx+ex, cy-r-6+hy), 7)
        pygame.draw.circle(surf, (255,255,255), (cx+ex-2, cy-r-9+hy), 3)
    # smile
    pygame.draw.arc(surf, (0,120,30), (cx-14, cy-r+hy, 28, 18), math.pi, 2*math.pi, 3)
    # rosy cheeks
    chk = pygame.Surface((16,10), pygame.SRCALPHA)
    pygame.draw.ellipse(chk, (255,150,150,120), (0,0,16,10))
    surf.blit(chk, (cx-22, cy-r-1+hy)); surf.blit(chk, (cx+6, cy-r-1+hy))
    # legs
    leg = (65, 195, 80)
    for lx,ly,lw,lh in [(-r+2,10,18,14),(r-18,10,18,14),(-r+6,r-16,16,12),(r-20,r-16,16,12)]:
        pygame.draw.ellipse(surf, leg, (cx+lx, cy+ly, lw, lh))

# ─── WinScreen ────────────────────────────────────────────────────────────
HEART_PTS = []
for _td in range(0, 360, 8):
    _t = math.radians(_td)
    _x = 16*(math.sin(_t)**3)
    _y = -(13*math.cos(_t) - 5*math.cos(2*_t) - 2*math.cos(3*_t) - math.cos(4*_t))
    HEART_PTS.append((_x*11, _y*11))   # scale 11 → ~350px wide

class WinScreen:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.tick   = 0.0
        self.reveal = 0.0   # 0→len(HEART_PTS): turtles appear one by one
        self.parts  = []
        self.done   = False
        self.fT = _f(62, True); self.fS = _f(32, True); self.fP = _f(24)
        # spawn celebration particles after reveal
        self._spawned = False

    def update(self, dt):
        self.tick += dt
        self.reveal = min(self.reveal + dt*18, len(HEART_PTS))
        if self.reveal >= len(HEART_PTS) and not self._spawned:
            self._spawned = True
            for _ in range(120):
                self.parts.append({
                    'x': self.W//2 + random.randint(-160,160),
                    'y': self.H//2 + random.randint(-120,120),
                    'vx': random.uniform(-110,110), 'vy': random.uniform(-180,-30),
                    'life': 1.0,
                    'col': random.choice([(255,215,0),(80,220,100),(255,100,200),(100,200,255)])
                })
        for p in self.parts:
            p['x']+=p['vx']*dt; p['y']+=p['vy']*dt
            p['vy']+=200*dt; p['life']-=dt*0.6
        self.parts=[p for p in self.parts if p['life']>0]

    def handle_key(self, key):
        if key == pygame.K_SPACE:
            self.done = True

    def draw(self, surf):
        # Sand background
        surf.fill((238, 210, 150))
        # Wavy sand lines
        for i in range(0, self.H, 18):
            c = (220,195,130) if (i//18)%2==0 else (245,220,165)
            pygame.draw.line(surf, c, (0,i), (self.W,i), 1)

        # Heart of turtles
        cx, cy = self.W//2, self.H//2 + 10
        n = int(self.reveal)
        for i in range(n):
            hx, hy = HEART_PTS[i % len(HEART_PTS)]
            _mini_turtle(surf, int(cx+hx), int(cy+hy), r=9, happy=True)

        # Big turtle in centre (after all turtles placed)
        if self.reveal >= len(HEART_PTS):
            _big_turtle(surf, cx, cy, size=100, tick=self.tick)

        # Particles
        for p in self.parts:
            a = int(255*p['life']); sz = max(1, int(8*p['life']))
            ps = pygame.Surface((sz*2,sz*2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p['col'],a), (sz,sz), sz)
            surf.blit(ps, (int(p['x']-sz), int(p['y']-sz)))

        # Title
        pulse = 1+0.04*math.sin(self.tick*3)
        raw = self.fT.render("100 TURTLES SAVED!", True, (60,140,60))
        sc2 = pygame.transform.smoothscale(raw,(int(raw.get_width()*pulse),int(raw.get_height()*pulse)))
        shd = pygame.transform.smoothscale(self.fT.render("100 TURTLES SAVED!",True,(0,0,0)),
                                           (int(raw.get_width()*pulse),int(raw.get_height()*pulse)))
        r = sc2.get_rect(center=(self.W//2, 52)); surf.blit(shd,r.move(3,3)); surf.blit(sc2,r)

        sub = self.fS.render("You saved every child turtle!", True, (90,60,20))
        surf.blit(sub, sub.get_rect(center=(self.W//2, 108)))

        if self.reveal >= len(HEART_PTS):
            a2 = int(155+100*math.sin(self.tick*3.5))
            pr = self.fP.render("Press SPACE to Play Again", True, (80,50,10))
            pr.set_alpha(a2); surf.blit(pr, pr.get_rect(center=(self.W//2, self.H-36)))

# ─── GameOverCinematic ────────────────────────────────────────────────────
ALIEN_LINES  = ["Mwahahaha! You FAILED!", "This little turtle is MINE now!", "Forever and ever! HA HA HA!"]
TURTLE_LINES = ["Please... help me...", "I miss my family so much...", "Is anyone out there?  😢"]

def _draw_big_alien(surf, cx, cy, tick=0.0, smug=True):
    bc = (55, 200, 75)
    # body
    pygame.draw.ellipse(surf, bc, (cx-28, cy, 56, 80))
    # head
    pygame.draw.circle(surf, bc, (cx, cy), 38)
    pygame.draw.circle(surf, (30,140,45), (cx, cy), 38, 2)
    # eyes
    for ex in [-14, 14]:
        pygame.draw.ellipse(surf, (10,10,10), (cx+ex-14, cy-16, 28, 22))
        pygame.draw.circle(surf, (255,255,255), (cx+ex-5, cy-8), 8)
        pygame.draw.circle(surf, (10,10,10), (cx+ex-4, cy-8), 4)
    # smug mouth
    if smug:
        pygame.draw.arc(surf, (20,100,30), (cx-18,cy+12,36,16), 0, math.pi, 3)
    # antenna
    pygame.draw.line(surf, bc, (cx, cy-38), (cx+12, cy-60), 3)
    pygame.draw.circle(surf, (255,40,40), (cx+12, cy-60), 6)
    # arms
    pygame.draw.line(surf, bc, (cx-28,cy+20),(cx-55,cy+8),3)
    pygame.draw.line(surf, bc, (cx+28,cy+20),(cx+55,cy+8),3)
    # legs
    pygame.draw.line(surf, bc, (cx-14,cy+80),(cx-18,cy+110),3)
    pygame.draw.line(surf, bc, (cx+14,cy+80),(cx+18,cy+110),3)

def _draw_big_child(surf, cx, cy, tick=0.0):
    r = 34
    sc = (200,130,30)
    pygame.draw.ellipse(surf,(sc),(cx-r+2,cy-r+2,(r-2)*2,(r-2)*2))
    pygame.draw.ellipse(surf,tuple(max(0,c-30) for c in sc),(cx-r+2,cy-r+2,(r-2)*2,(r-2)*2),2)
    pygame.draw.circle(surf,tuple(max(0,c-20) for c in sc),(cx,cy),r//2)
    hc=(90,185,85)
    pygame.draw.ellipse(surf,hc,(cx-r-14,cy-12,26,20))
    pygame.draw.circle(surf,(0,0,0),(cx-r-6,cy-3),4)
    # sad mouth
    pygame.draw.arc(surf,(120,60,0),(cx-r-16,cy+6,20,10),0,math.pi,2)
    # tear
    tear_y = cy-3+int(4*((tick*2)%1))
    pygame.draw.ellipse(surf,(100,180,255),(cx-r-4,tear_y,5,8))
    # legs
    leg=(90,175,80)
    for lx,ly in [(-r+2,r-8),(r-14,r-8),(-r+4,r+4),(r-12,r+4)]:
        pygame.draw.ellipse(surf,leg,(cx+lx,cy+ly,14,10))

def _draw_bubble(surf, rect, lines, font, col, tail_left=True):
    bg = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(bg, (255,255,255,230), bg.get_rect(), border_radius=14)
    pygame.draw.rect(bg, (*col,220), bg.get_rect(), 2, border_radius=14)
    surf.blit(bg, rect.topleft)
    for i,ln in enumerate(lines):
        t = font.render(ln, True, (30,30,30))
        surf.blit(t, (rect.x+10, rect.y+8+i*22))
    # tail triangle
    tx = rect.x-10 if tail_left else rect.right+10
    ty = rect.centery
    pts = [(rect.x if tail_left else rect.right, ty-6),
           (rect.x if tail_left else rect.right, ty+6),
           (tx, ty)]
    pygame.draw.polygon(surf, (255,255,255), pts)
    pygame.draw.polygon(surf, col, pts, 2)

class GameOverCinematic:
    def __init__(self, W, H, saved):
        self.W,self.H,self.saved = W,H,saved
        self.tick   = 0.0
        self.phase  = 0   # 0=alien talks, 1=turtle responds, 2=await input
        self.a_chars= 0
        self.t_chars= 0
        self.type_t = 0.0
        self.spd    = 0.045
        self.done   = False
        self.fT = _f(64,True); self.fD = _f(19); self.fS = _f(26,True); self.fP = _f(22)
        self.a_full = " ".join(ALIEN_LINES)
        self.t_full = " ".join(TURTLE_LINES)

    def update(self, dt):
        self.tick += dt; self.type_t += dt
        if self.phase == 0:
            self.a_chars = min(int(self.type_t/self.spd), len(self.a_full))
            if self.a_chars >= len(self.a_full): self.phase=1; self.type_t=0
        elif self.phase == 1:
            self.t_chars = min(int(self.type_t/self.spd), len(self.t_full))
            if self.t_chars >= len(self.t_full): self.phase=2

    def handle_key(self, key):
        if key == pygame.K_SPACE:
            if self.phase < 2:
                self.a_chars=len(self.a_full); self.t_chars=len(self.t_full); self.phase=2
            else: self.done=True

    def draw(self, surf):
        # Dark alien-world background
        surf.fill((12, 8, 28))
        # Stars
        for i in range(100):
            sx=(i*137+7)%self.W; sy=(i*91+13)%self.H
            br=int(120+80*math.sin(self.tick*1.5+i))
            pygame.draw.circle(surf,(br,br,br+30),(sx,sy),1)
        # Nebula blobs
        for cx2,cy2,col2 in [(150,200,(60,0,80,40)),(550,350,(0,40,80,40))]:
            nb=pygame.Surface((180,120),pygame.SRCALPHA)
            pygame.draw.ellipse(nb,col2,(0,0,180,120)); surf.blit(nb,(cx2-90,cy2-60))

        # Title
        raw=self.fT.render("GAME  OVER",True,(220,35,35))
        sh=self.fT.render("GAME  OVER",True,(80,0,0))
        tr=raw.get_rect(center=(self.W//2,58)); surf.blit(sh,tr.move(4,4)); surf.blit(raw,tr)
        sc=self.fS.render(f"Turtles Saved:  {self.saved} / 100",True,(255,200,50))
        surf.blit(sc,sc.get_rect(center=(self.W//2,120)))

        # Characters
        _draw_big_alien(surf,175,230,tick=self.tick)
        _draw_big_child(surf,525,270,tick=self.tick)

        # Alien bubble
        if self.a_chars>0:
            lines=_wrap(self.fD,self.a_full[:self.a_chars],300)[:4]
            bh=16+len(lines)*22
            _draw_bubble(surf,pygame.Rect(220,200,310,bh),lines,self.fD,(180,20,180),tail_left=True)

        # Turtle bubble
        if self.t_chars>0:
            lines=_wrap(self.fD,self.t_full[:self.t_chars],260)[:4]
            bh=16+len(lines)*22
            _draw_bubble(surf,pygame.Rect(360,370,280,bh),lines,self.fD,(40,160,80),tail_left=False)

        # Prompt
        if self.phase>=2:
            a2=int(155+100*math.sin(self.tick*3.5))
            pr=self.fP.render("SPACE – Return to Menu",True,(200,200,200))
            pr.set_alpha(a2); surf.blit(pr,pr.get_rect(center=(self.W//2,self.H-36)))
