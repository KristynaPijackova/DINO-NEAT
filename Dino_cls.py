#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autor: Kristyna Pijackova
Project: Dino AI
Datum: 06/12/2019
"""
# =============================================================================
# class Dino for different Dino-behaviors / walk, jump, duck
# =============================================================================

import pygame
import os 

DINO_IMG = [pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'Dino' + str(x) + '.png')), (170,170)) for x in range(1,5)]
DINO_DUCK_IMG = [pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'Dino' + str(x) + '.png')), (540,230)) for x in range(5,7)]


class Dino:
    IMGS = DINO_IMG
    IMGS_DUCK = DINO_DUCK_IMG
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = self.x
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.is_jump = False
        self.jump_count = 15
        self.is_duck = False
        self.img_count_duck = 0
        self.duck_count = 0
        self.is_walk = False
        
    def dino_pos(self):       # returns Dino's position to Dino.py
        dino_y = self.y
        dino_x = self.x
        return dino_y, dino_x

    def jump(self):           # sets jump to True
        if not(self.is_jump):
            self.is_jump = True

    def duck(self):           # sets duck to True
        if not (self.is_duck):
            self.is_duck = True

    def walk(self):            # sets walk to True
        if not self.is_walk:
            self.is_walk = True

# =============================================================================
# If statemens in the draw function are based on the outputs from NEAT:
#   Walk ---> [1, 0, 0], [0, 0, 0]
#   Jump ---> [0, 1, 0], [1, 1, 0], [0, 1, 1], [0, 1, 1]
#   Duck ---> [0, 0, 1], [1, 0, 1]
# =============================================================================

    def draw(self, win, vel):   # animation for the outputs
        if (
            self.is_walk and not self.is_jump and not self.is_duck or
            not self.is_walk and not self.is_jump and not self.is_duck
            ):
            self.pos = self.x
            self.height = self.y
            if self.y != 510:
                self.height = 510
            # simulates running
            self.img_count += 1
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*2:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*4:
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME*5+1:
                self.img = self.IMGS[0]
                self.img_count = 0

        if (
            not self.is_walk and self.is_jump and not self.is_duck or
            self.is_walk and self.is_jump and not self.is_duck or
            self.is_walk and self.is_jump and self.is_duck or
            not self.is_walk and self.is_jump and self.is_duck
            ):
            self.vel = vel
            if self.jump_count >= -15:  # jumps fitted for game speed
                if self.vel < 25:
                    self.y -= 0.8*self.vel*((self.jump_count *abs(self.jump_count))*0.02)
                    self.jump_count -= 0.1*self.vel
            else: 
                self.is_jump = False
                self.jump_count = 15
                self.y = 510
            self.pos = self.x
            self.height = self.y
            self.img = self.IMGS[3]

        if (
            not self.is_walk and not self.is_jump and self.is_duck or
            self.is_walk and not self.is_jump and self.is_duck or 
            not self.is_walk and not self.is_jump and not self.is_duck
            ):
            self.is_walk = False        # prevents dino from freezing while [1,0,1]
            self.is_duck = True
            # simulates running
            self.img_count_duck += 0.5
            if self.img_count_duck < self.ANIMATION_TIME:
                self.img = self.IMGS_DUCK[0]
            elif self.img_count_duck < self.ANIMATION_TIME*2:
                self.img = self.IMGS_DUCK[1]
            elif self.img_count_duck < self.ANIMATION_TIME*3:
                self.img = self.IMGS_DUCK[0]
            elif self.img_count_duck < self.ANIMATION_TIME*4:
                self.img = self.IMGS_DUCK[1]
                self.img_count_duck = 0
            self.is_duck = False
            self.height = self.y - 7    # x, y positions fitted for the imgs
            self.pos = 6

        win.blit(self.img, (self.pos, self.height))
            
    def get_mask(self):             # mask of the Dino for collision detection
        return pygame.mask.from_surface(self.img)
