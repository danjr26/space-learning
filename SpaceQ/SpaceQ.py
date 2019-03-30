import pygame
import math
import random
import time
import copy
import multiprocessing
import itertools
import pygame
from pygame.locals import *
from Specimen import Specimen
from SpaceGame import SpaceGame

def get_fitness(specimen):
    return specimen.calc_fitness()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 800))

    #from SpaceGame import SpaceGame

    #game = SpaceGame()
    #print("Score: ", game.run())

    LEARN = True

    if LEARN:
        M=200
        pool = multiprocessing.Pool()


        generation = [Specimen() for i in range(M)]
        s = pool.map(get_fitness, generation)
        scores = {generation[i]:s[i] for i in range(len(generation))}
        count = 0
        while True:
            generation = sorted(scores, key=lambda k:scores[k], reverse=True)[0:M//2-1]
            if count % 5 == 0:
                generation[0].calc_fitness(doRender=True)
            t1 = time.time()
            for i in range(M//2):
                child = copy.deepcopy(generation[i])
                child.mutate()
                generation.append(child)
            s = pool.map(get_fitness, generation)
            scores = {generation[i]:s[i] for i in range(len(generation))}
            t2 = time.time()
            print(count, sum(sorted(scores.values(), reverse=True)[0:M//2]) / (M//2), round(t2-t1, 2), sep=", ")
            count += 1
    else:
        game = SpaceGame()
        print("Score: ", game.run())