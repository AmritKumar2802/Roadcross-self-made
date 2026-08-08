"""
Road background drawn 100% programmatically.
Accepts a theme dict from constants.THEMES so each level looks different.
"""
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT,
                        ROAD_TOP, ROAD_BOTTOM, LANE_HEIGHT, NUM_LANES)


def build_background(theme: dict) -> pygame.Surface:
    """Return a pre-rendered Surface of the full background for the given theme."""
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # ── Grass zones ────────────────────────────────────────────────────────
    surf.fill(theme["grass"])

    # ── Subtle grass texture lines ─────────────────────────────────────────
    dark = tuple(max(0, c - 18) for c in theme["grass"])
    for zone_top, zone_bot in [(0, ROAD_TOP), (ROAD_BOTTOM, SCREEN_HEIGHT)]:
        y = zone_top
        while y < zone_bot:
            pygame.draw.line(surf, dark, (0, y), (SCREEN_WIDTH, y), 1)
            y += 8

    # ── Road body ─────────────────────────────────────────────────────────
    road_rect = pygame.Rect(0, ROAD_TOP, SCREEN_WIDTH, ROAD_BOTTOM - ROAD_TOP)
    pygame.draw.rect(surf, theme["road"], road_rect)

    # ── Road surface texture (very subtle horizontal bands) ────────────────
    light = tuple(min(255, c + 6) for c in theme["road"])
    for y in range(ROAD_TOP, ROAD_BOTTOM, 16):
        pygame.draw.line(surf, light, (0, y), (SCREEN_WIDTH, y), 1)

    # ── Kerb lines (top & bottom of road) ─────────────────────────────────
    pygame.draw.rect(surf, theme["kerb"], (0, ROAD_TOP - 6,    SCREEN_WIDTH, 6))
    pygame.draw.rect(surf, theme["kerb"], (0, ROAD_BOTTOM,     SCREEN_WIDTH, 6))

    # ── Lane dividers (dashed lines) ──────────────────────────────────────
    dash_w, gap = 40, 22
    for i in range(1, NUM_LANES):
        y = ROAD_TOP + LANE_HEIGHT * i
        x = 0
        while x < SCREEN_WIDTH:
            end_x = min(x + dash_w, SCREEN_WIDTH)
            pygame.draw.line(surf, theme["dash"], (x, y), (end_x, y), 2)
            x += dash_w + gap

    # ── Finish line (checkered/striped at top kerb) ────────────────────────
    stripe_w = 18
    x = 0
    alt = False
    while x < SCREEN_WIDTH:
        color = theme["finish"] if alt else theme["kerb"]
        pygame.draw.rect(surf, color, pygame.Rect(x, ROAD_TOP - 6, stripe_w, 6))
        x += stripe_w
        alt = not alt

    # ── Start zone indicator (dashed line at bottom kerb) ─────────────────
    x = 0
    while x < SCREEN_WIDTH:
        end_x = min(x + 30, SCREEN_WIDTH)
        pygame.draw.line(surf, theme["kerb"], (x, ROAD_BOTTOM + 3), (end_x, ROAD_BOTTOM + 3), 2)
        x += 30 + 14

    return surf
