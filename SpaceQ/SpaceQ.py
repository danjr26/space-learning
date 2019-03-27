import pygame
import math
import random
import time
import copy
from pygame.locals import *
from Specimen import Specimen
from SpaceGame import SpaceGame

pygame.init()
pygame.display.set_mode((800, 800))

#from SpaceGame import SpaceGame

#game = SpaceGame()
#print("Score: ", game.run())

LEARN = True

if LEARN:
    N=1
    M=100

    generation = [Specimen() for i in range(M)]
    scores = {specimen:sum(specimen.calc_fitness() for i in range(N))/N for specimen in generation}
    while True:
        generation = sorted(scores, key=lambda k:scores[k], reverse=True)[0:M//2-1]
        generation[0].calc_fitness(doRender=True)
        print(i, ', ', scores[generation[0]], end=', ', sep='')  
        for i in range(M//2):
            child = copy.deepcopy(generation[i])
            child.mutate()
            generation.append(child)
        scores = {specimen:sum(specimen.calc_fitness() for i in range(N))/N for specimen in generation}
        print(sum(value for key, value in scores.items()) / M)
else:
    game = SpaceGame()
    print("Score: ", game.run())