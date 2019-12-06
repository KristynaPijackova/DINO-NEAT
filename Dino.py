#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autor: Kristyna Pijackova
Project: Dino AI
Datum: 06/12/2019
"""
# =============================================================================
# Dino with implemented NEAT
# =============================================================================

from Ground_cls import Ground
from Background_cls import Background
from Obstacles_cls import Obstacles
from Dino_cls import Dino
from Draw_ftion import draw_window
import Visualize
import pygame
import random
import os
import pickle
import neat

GEN = 0
WIN_WIDTH = 1184
WIN_HEIGHT = 768

def main(genomes, config):
    global GEN                      # passing the number of current generation
    GEN += 1
    # needed for NEAT setup
    nets = []
    ge = []
    dinos = []
    for _, g in genomes:            # set up genomes
        #net = neat.nn.recurrent.RecurrentNetwork.create(g, config)
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(50,510))
        g.fitness = 0
        ge.append(g)
    #print(genomes)
    #print()
    print(g)
    # NN input variables:
    obst_height = 0
    x_ct = 0
    x_pt = 0
    vel = 5                         # game velocity
    jump_vel = vel                  # jump velocity
    speed = 55                      # ticks
    dino_y = 510                    # initial dino y position
    dino_x = 50
    count = 0                       # help var to count score
    score = 0
    reward = 0
    ground = Ground(500)
    background = Background(0)
    obstacles = [Obstacles(-200,1400)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()

    # Load the genome of previous/best try
    try:
        with open('winner.pkl', 'rb') as input_file:
            g = pickle.load(input_file)
    except:
        pass
    
# game loop
    pygame.init()
    run = True
    while run:
    #end game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.quit()
        clock.tick(speed)                   # frames speed

    # checks if there are dinos - count score and velocity/break game loop
        if len(dinos) > 0:
            count_score = pygame.time.get_ticks()/200
            if count_score > 0:
                count += 0.05
                score = (round(count))
            if score % 40 == 0 and vel < 25:
                vel = vel + 0.005
                if vel % 4 != 0:
                    jump_vel = vel - vel % 2
                else: jump_vel = vel
        elif len(dinos)==0:
            run = False
            break

    # NN inputs, outputs and fitness
        for x, dino in enumerate(dinos):
            ge[x].fitness = score + reward
            output = nets[x].activate((obst_height, x_ct, x_pt, vel, dino_x))
            if output[0] == 1:
                dino.walk()
            if output[1] == 1:
                dino.jump()
            if output[2] == 1:
                dino.duck()
            if output[2] == 1 and output[1] == 0:
                reward += 0.0001

        ground.move(vel)
        rem_obst = []
        add_obst = False

        for din in dinos:
            for obst in obstacles:
        # collision?
                if obst.collide(din):
                    ge[dinos.index(din)].fitness -= 4
                    nets.pop(dinos.index(din))
                    ge.pop(dinos.index(din))
                    dinos.pop(dinos.index(din))
        # remove/add obstacles?
                if obst.x_ct + obst.CACTUS.get_width() < 0 and obst.x_pt + obst.PTERO.get_width() < 0:
                    rem_obst.append(obst)
                    ge[dinos.index(din)].fitness += 5
                if not obst.passed and obst.x_ct < -200 and obst.x_pt < -200:
                    obst.passed = True
                    if obst.passed and obst_height < 430 and output[1] == 0 and dino.duck():
                        reward += 5
                    if obst.passed:
                        reward += 0.2
                    add_obst = True

        obst.move(vel)
        background.move(vel)
    # add obstacles to "random" positions
        if add_obst:
            x_cact = random.randrange(1200,2150,800)
            x_ptero = x_cact + random.randrange(450,600,10)
            obstacles.append(Obstacles(x_cact, x_ptero))
    # remove passed obstacles
        for r in rem_obst:
            obstacles.remove(r)
    # passed variables from Obstacles_cls.py and Dino_cls.py
        x_ct, x_pt, obst_height = obst.pos()
        dino_y, dino_x = dino.dino_pos()
    # calling draw function for animation
        draw_window(win, background, dinos, obstacles, ground, score, GEN, jump_vel)
        
        if score == 100:
            pickle.dump(nets[0],open("best100.pickle", "wb"))
        if score == 200:
            pickle.dump(nets[0],open("best200.pickle", "wb"))
        if score == 400:
            pickle.dump(nets[0],open("best400.pickle", "wb"))

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main,10)
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)
        
    node_names = {-1:'Obst height', -2: 'X cactus', -3: 'X Ptero', -4: 'Speed', -5: 'X dino', 0: 'Walk', 1: 'Jump', 2: 'Duck'}
    Visualize.draw_net(config, winner, True, node_names=node_names)
    Visualize.plot_stats(stats, ylog=False, view=True)
    Visualize.plot_species(stats, view=True)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward3.txt")
    run(config_path)
