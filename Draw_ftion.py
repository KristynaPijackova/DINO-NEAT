#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kristyna Pijackova
Project: Dino AI
Datum: 06/12/2019
"""

# =============================================================================
# Assemble the animation. 
# =============================================================================

import pygame

pygame.font.init()
STAT_FONT = pygame.font.Font(None, 50)

def draw_window(win, background, dinos, obstacles, ground, score, GEN, vel):
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    text2 = STAT_FONT.render("Generation: " + str(GEN), 1, (255,255,255))
    background.draw(win)
    win.blit(text, ((900, 15)))
    win.blit(text2, ((20, 15)))
    for obst in obstacles:
        obst.draw(win)
    ground.draw(win)
    for dino in dinos:
        dino.draw(win, vel)
    pygame.display.update()