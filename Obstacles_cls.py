# =============================================================================
#     
# Class Obstacles for setting up the obstacles parameters and collision with 
# Dino
# =============================================================================

import pygame
import os 
import random

CACTUS_DIM = [140, 120, 160, 140, 150, 130]
CACTUS_IMG = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Kaktus" + str(x) + ".png")), (CACTUS_DIM[x]-20,CACTUS_DIM[x])) for x in range (1,6)]
PTERO_IMG = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Ptero" + str(x) + ".png")), (250,150)) for x in range (1,3)]


class Obstacles:
    VEL = 5
    ANIMATION_TIME = 5
    PTE = PTERO_IMG
    
    def __init__(self,x_ct, x_pt):
        self.x_ct = x_ct
        self.x_pt = x_pt
        self.height = 0
        self.PTERO = self.PTE[0]
        self.CACTUS = CACTUS_IMG[random.randrange(0,5)]
        self.CACTUS_HEIGHT = self.CACTUS.get_height()
        self.pt_index = random.randrange(0,3)
        self.y_pt = [380, 440, 550]
        self.pt_height = 0
        self.img_count = 0
        self.set_height()
        self.set_pt_height()
        self.passed = False

    def set_height(self):               # height of cactus based on width
        if self.CACTUS_HEIGHT == 120:
            self.height = 555
        if self.CACTUS_HEIGHT == 130:
            self.height = 545
        if self.CACTUS_HEIGHT == 140:
            self.height = 535
        if self.CACTUS_HEIGHT == 150:
            self.height = 530
        if self.CACTUS_HEIGHT == 160:
            self.height = 520
    
    def set_pt_height(self):            # choose 1 of 3 heights of ptero
        self.pt_height = self.y_pt[self.pt_index]

    def move(self, vel):                # obstacles velocity
        self.vel = vel
        self.x_ct -= vel
        self.x_pt -= vel
        
    def draw(self, win):
        # ptero animation 
        self.img_count+= 0.4
        if self.img_count < self.ANIMATION_TIME:
            self.PTERO = self.PTE[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.PTERO = self.PTE[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.PTERO = self.PTE[1]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.PTERO = self.PTE[0]
        elif self.img_count < self.ANIMATION_TIME*5:
            self.PTERO = self.PTE[1]
        elif self.img_count < self.ANIMATION_TIME*6:
            self.PTERO = self.PTE[1]
        elif self.img_count < self.ANIMATION_TIME*7:
            self.PTERO = self.PTE[0]
            self.img_count = 0
        win.blit(self.CACTUS, (self.x_ct, self.height))
        win.blit(self.PTERO, (self.x_pt, self.pt_height))

    def collide(self, dino):                # checks for collision with dino
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.CACTUS)
        ptero_mask = pygame.mask.from_surface(self.PTERO)
        cactus_offset = (round(self.x_ct - dino.pos), round(self.height - round(dino.y)))
        ptero_offset = (round(self.x_pt - dino.pos), round(self.pt_height - round(dino.y)))
        cactus_point = dino_mask.overlap(cactus_mask, cactus_offset)
        ptero_point = dino_mask.overlap(ptero_mask, ptero_offset)
        if cactus_point or ptero_point:
            return True
        else:
            return False

    def pos(self):                          # passes infos to Dino.py
        height = self.height
        pt_height = self.pt_height
        x_ct = self.x_ct
        x_pt = self.x_pt
        obst_height= 0
        if x_ct < 100:
            obst_height = pt_height
        elif x_ct > 100: 
            obst_height = height
        return x_ct, x_pt, obst_height
