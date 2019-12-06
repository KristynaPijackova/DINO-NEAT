#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:06:37 2019

@author: kristyna
"""

# =============================================================================
# Class Background for moving sky
# =============================================================================

import pygame
import os 

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Nebe.png")), (1200,700))


class Background:
    BG_WIDTH = BG_IMG.get_width()
    BG_IMG = BG_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.BG_WIDTH
        
    def move(self, vel):
        self.vel = vel
        self.x1 -= vel/5
        self.x2 -= vel/5
        if self.x1 + self.BG_WIDTH < 0:
            self.x1 = self.x2 + self.BG_WIDTH
        if self.x2 + self.BG_WIDTH < 0:
            self.x2 = self.x1 + self.BG_WIDTH

    def draw(self, win):
        win.blit(self.BG_IMG, (self.x1, self.y))
        win.blit(self.BG_IMG, (self.x2, self.y))