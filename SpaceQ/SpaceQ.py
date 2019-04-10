import pygame, math, random, time, copy, multiprocessing, itertools, sys
import pygame
from pygame.locals import *
from Specimen import Specimen
from SpaceGame import SpaceGame

def get_fitness(specimen):
    return specimen.calc_fitness()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 800))

    args = sys.argv[1:]

    mode = ""
    genSize = 200
    saveBest = False
    saveFile = "brain.txt"
    loadFile = ""
    doDisplay = True
    displayMod = 10
    nThreads = 1

    while len(args):
        arg = args.pop(0)
        if arg == "--display-every":
            arg = args.pop(0)
            displayMod = int(arg)
        elif arg == "--no-display":
            doDisplay = False
        elif arg == "--save-best":
            saveBest = True
        elif arg == "--gen-size":
            arg = args.pop(0)
            genSize = int(arg)
        elif arg == "--save-file":
            arg = args.pop(0)
            saveFile = arg;
        elif arg == "--load-file":
            arg = args.pop(0)
            loadFile = arg;
        elif arg == "--num-threads":
            arg = args.pop(0)
            nThreads = int(arg)
        elif mode == "":
            mode = arg
        else:
            exit(-1)

    if mode == "learn":
        pool = multiprocessing.Pool(nThreads)

        halfSize = genSize//2
        generation = [Specimen() for i in range(genSize)]
        if loadFile != "":
            for specimen in generation:
                specimen.load(loadFile)
        s = pool.map(get_fitness, generation)
        scores = {generation[i]:s[i] for i in range(len(generation))}
        count = 0
        while True:
            generation = sorted(scores, key=lambda k:scores[k], reverse=True)[0:halfSize-1]

            if doDisplay and count % displayMod == 0:
                generation[0].calc_fitness(doRender=True)

            if saveBest:
                generation[0].save(saveFile)

            t1 = time.time()
            for i in range(genSize//2):
                child = copy.deepcopy(generation[i])
                child.mutate()
                generation.append(child)

            s = pool.map(get_fitness, generation)
            scores = {generation[i]:s[i] for i in range(len(generation))}
            t2 = time.time()

            print(count, max(sorted(scores.values(), reverse=True)), sum(sorted(scores.values(), reverse=True)[0:halfSize]) / halfSize, round(t2-t1, 2), sep=", ")
            count += 1

    elif mode == "playback":
        specimen = Specimen()
        specimen.load(loadFile)
        while True:
            print("Score: ", specimen.calc_fitness(doRender=True))

    elif mode == "play":
        game = SpaceGame()
        print("Score: ", game.run())

    elif mode == "":
        print("SpaceQ.py MODE [flags]")
        print("\tMODE = learn, play, playback")
        print("\tflags:")
        print("\t\t--no-display")
        print("\t\t--display-every N")
        print("\t\t--save-best")
        print("\t\t--gen-size N")
        print("\t\t--save-file FILE")
        print("\t\t--load-file FILE")
        print("\t\t--num-threads N")

    else:
        print("invalid mode:", mode)