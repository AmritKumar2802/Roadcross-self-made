"""
Main – Roadcross with rescue animation and world transitions.

States:
  MENU → PLAYING → RESCUE (animation) → TRANSITIONING (scroll) → PLAYING
                 ↘ GAME_OVER
"""
import pygame, sys, math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, THEMES, PLAYER_START_Y
from road        import build_background
from player      import Player
from cars        import CarManager
from ui          import UI
from finish_scene import FinishScene, P_DONE
from endings     import WinScreen, GameOverCinematic
from stones      import StoneManager

WIN_LIMIT =1

# ── Init ───────────────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roadcross")
clock  = pygame.time.Clock()

all_bgs = [build_background(t) for t in THEMES]

player      = Player()
car_manager = CarManager()
stone_manager = StoneManager()
ui          = UI(SCREEN_WIDTH, SCREEN_HEIGHT)
scene       = FinishScene()

# ── States ─────────────────────────────────────────────────────────────────
S_MENU   = 0; S_PLAY = 1; S_RESCUE = 2; S_TRANS = 3; S_OVER = 4
S_WIN = 5; S_OVER_ANIM = 6
state    = S_MENU

win_screen  = None
over_anim   = None

# ── Transition vars ────────────────────────────────────────────────────────
TRANS_DUR  = 1.1
trans_t    = 0.0
old_bg     = all_bgs[0]
new_bg     = all_bgs[0]
player_y0  = 0.0        # player y at start of transition

# ── Flash vars ─────────────────────────────────────────────────────────────
FLASH_DUR = 0.6
flash_t   = 0.0
flashing  = False

def smooth(t):
    t = max(0.0, min(1.0, t))
    return t*t*(3-2*t)

def begin_transition():
    global state, trans_t, old_bg, new_bg, player_y0, flashing, flash_t
    nxt = (ui.theme_idx + 1) % len(THEMES)
    old_bg = all_bgs[ui.theme_idx % len(THEMES)]
    new_bg = all_bgs[nxt]
    ui.advance_theme()
    banner_text = THEMES[nxt]["name"]
    if ui.turtles_saved == 20:
        banner_text = "WARNING: 2-WAY TRAFFIC!"
    elif ui.turtles_saved == 40:
        banner_text = "WATCH FOR STONES!"
    ui.trigger_banner(banner_text)
    
    car_manager.level_up(ui.turtles_saved)
    if ui.turtles_saved >= 40:
        stone_manager.set_level(ui.turtles_saved)
    else:
        stone_manager.reset()
    car_manager.cars.empty()
    player_y0 = float(player.rect.centery)
    trans_t   = 0.0
    flashing  = True
    flash_t   = 0.0
    state     = S_TRANS

def begin_rescue():
    global state
    player.stop_all()
    car_manager.cars.empty()      # freeze cars
    scene.start_rescue(player)
    state = S_RESCUE

# ── Main loop ──────────────────────────────────────────────────────────────
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # ── Events ─────────────────────────────────────────────────────────────
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        if ev.type == pygame.KEYDOWN:
            if state == S_PLAY:
                if ev.key == pygame.K_UP:    player.move_up    = True
                if ev.key == pygame.K_DOWN:  player.move_down  = True
                if ev.key == pygame.K_LEFT:  player.move_left  = True
                if ev.key == pygame.K_RIGHT: player.move_right = True
            if ev.key == pygame.K_SPACE:
                if state == S_MENU: state = S_PLAY
                elif state == S_OVER:
                    player.go_to_start(); car_manager.reset(); stone_manager.reset()
                    ui.reset(); scene.reset()
                    old_bg = all_bgs[0]; flashing = False
                    state = S_PLAY
                elif state == S_WIN and win_screen:
                    win_screen.handle_key(ev.key)
                    if win_screen.done:
                        player.go_to_start(); car_manager.reset(); stone_manager.reset()
                        ui.reset(); scene.reset()
                        old_bg = all_bgs[0]; flashing = False
                        win_screen = None; state = S_MENU
                elif state == S_OVER_ANIM and over_anim:
                    over_anim.handle_key(ev.key)
                    if over_anim.done:
                        player.go_to_start(); car_manager.reset(); stone_manager.reset()
                        ui.reset(); scene.reset()
                        old_bg = all_bgs[0]; flashing = False
                        over_anim = None; state = S_MENU

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_UP:    player.move_up    = False
            if ev.key == pygame.K_DOWN:  player.move_down  = False
            if ev.key == pygame.K_LEFT:  player.move_left  = False
            if ev.key == pygame.K_RIGHT: player.move_right = False

    # ── Update ─────────────────────────────────────────────────────────────
    ui.update(dt)

    if state == S_PLAY:
        player.update(dt)
        car_manager.update(dt)
        if flashing:
            flash_t += dt
            if flash_t >= FLASH_DUR: flashing = False

        # Collision → game over cinematic
        for car in car_manager.cars:
            if player.hitbox.colliderect(car.rect.inflate(-16,-10)):
                player.stop_all()
                over_anim = GameOverCinematic(SCREEN_WIDTH, SCREEN_HEIGHT, ui.turtles_saved)
                state = S_OVER_ANIM

        if stone_manager.check_collision(player.hitbox):
            player.stop_all()
            over_anim = GameOverCinematic(SCREEN_WIDTH, SCREEN_HEIGHT, ui.turtles_saved)
            state = S_OVER_ANIM

        if player.is_at_finish_line():
            begin_rescue()

    elif state == S_RESCUE:
        scene.update(dt, player)
        if scene.is_done:
            ui.save_turtle()
            scene.reset()
            # Check win condition
            if ui.turtles_saved >= WIN_LIMIT:
                win_screen = WinScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
                state = S_WIN
            else:
                begin_transition()

    elif state == S_WIN and win_screen:
        win_screen.update(dt)

    elif state == S_OVER_ANIM and over_anim:
        over_anim.update(dt)

    elif state == S_TRANS:
        trans_t += dt
        s = smooth(trans_t / TRANS_DUR)
        player.rect.centery = int(player_y0 + s*(PLAYER_START_Y - player_y0))
        if flashing:
            flash_t += dt
            if flash_t >= FLASH_DUR: flashing = False
        if trans_t >= TRANS_DUR:
            player.go_to_start()
            state = S_PLAY

    # ── Render ─────────────────────────────────────────────────────────────
    if state == S_MENU:
        ui.draw_start_menu(screen)

    elif state == S_WIN and win_screen:
        win_screen.draw(screen)

    elif state == S_OVER_ANIM and over_anim:
        over_anim.draw(screen)

    elif state == S_TRANS:
        scroll = int(smooth(trans_t/TRANS_DUR) * SCREEN_HEIGHT)
        screen.blit(old_bg, (0, -scroll))
        screen.blit(new_bg, (0,  SCREEN_HEIGHT-scroll))
        stone_manager.draw(screen)
        screen.blit(player.image, player.rect)
        if flashing: ui.draw_level_up_flash(screen, flash_t/FLASH_DUR)
        ui.draw_hud(screen)
        ui.draw_banner(screen)

    else:  # PLAY, RESCUE, OVER
        bg = all_bgs[ui.theme_idx % len(THEMES)]
        screen.blit(bg, (0,0))

        if state != S_RESCUE:
            car_manager.cars.draw(screen)

        stone_manager.draw(screen)
        scene.draw(screen)           # alien/child/UFO always drawn
        screen.blit(player.image, player.rect)

        if flashing: ui.draw_level_up_flash(screen, flash_t/FLASH_DUR)
        ui.draw_hud(screen)
        ui.draw_banner(screen)

        if state == S_OVER:
            ui.draw_game_over(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()