import pygame, math, time, random
import PlayerBullet
import PlayerShip
import SpaceAsteroid
import ScoreText
from pygame.locals import *

def get_user_rotation(ship):
    toMouse = pygame.mouse.get_pos() - ship.position
    angle = math.atan2(toMouse.y, toMouse.x)
    return -math.degrees(angle)

def get_user_move_direction(ship):
    direction = pygame.Vector2(0, 0)
    
    keys = pygame.key.get_pressed()

    if(keys[K_w]): direction.y -= 1
    if(keys[K_s]): direction.y += 1
    if(keys[K_a]): direction.x -= 1
    if(keys[K_d]): direction.x += 1

    return direction

def get_user_shoot(ship):
    return pygame.key.get_pressed()[K_SPACE]

def circles_collide(pos1:pygame.Vector2, radius1, pos2:pygame.Vector2, radius2):
    return pos1.distance_squared_to(pos2) <= (radius1 + radius2)**2

def wrap_coords(point):
    dim = (800, 800)
    while point.x < 0: point.x += dim[0]
    while point.x > dim[0]: point.x -= dim[0]
    while point.y < 0: point.y += dim[1]
    while point.y > dim[1]: point.y -= dim[1]
    return point

class SpaceGame:
    def __init__(self):
        self.playerShip = PlayerShip.PlayerShip(self)
        self.scoreText = ScoreText.ScoreText(self)
        self.playerBullets = []
        self.asteroids = []
        self.score = 0
        self.specimen = None
        self.doRender = True
        self.isPlaying = True
        self.playTime = 0.0
        self.tAccum = 0.0
        self.spawnAccum = 0.0

    def run(self, specimen=None, doRender=True):
        self.specimen = specimen
        self.doRender = doRender
        for i in range(5): self.spawn_asteroid(0)
        for i in range(4): self.spawn_asteroid(1)
        for i in range(2): self.spawn_asteroid(2)
        renderSurface = pygame.display.get_surface()
        t1 = time.time()
        while(self.isPlaying):
            t2 = time.time()
            dt = t2 - t1
            t1 = t2

            if self.specimen:
                dt = 0.02

            self.check_events()
            self.apply_input()
            self.update(dt)
            self.check_collisions()
            self.spawn_asteroids(dt)
            if self.doRender:
                self.render(renderSurface)
                pygame.display.flip()
                pygame.display.get_surface().fill((0, 0, 0))

        return self.score

    def check_events(self):
        event = pygame.event.poll()
        while(event.type != NOEVENT):
            if(event.type == QUIT): 
                exit()
            event = pygame.event.poll()

    def apply_input(self):
        if self.specimen:
            self.specimen.apply_input(self)
        else:
            self.playerShip.moveDirection = get_user_move_direction(self.playerShip)
            self.playerShip.rotation = get_user_rotation(self.playerShip)
            self.playerShip.isShooting = get_user_shoot(self.playerShip)

    def update(self, dt):
        self.playerShip.update(dt)
        for playerBullet in self.playerBullets:
            playerBullet.update(dt)
        for asteroid in self.asteroids:
            asteroid.update(dt)
        self.playTime += dt
        self.tAccum += dt
        while self.tAccum > 1.0:
            self.tAccum -= 1.0
            self.score += 1
        if self.score < 0: self.score = 0

    def check_collisions(self):
        toHit = set()
        for asteroid in self.asteroids:
            for playerBullet in self.playerBullets:
                if circles_collide(asteroid.position, asteroid.radius, playerBullet.position, playerBullet.radius):
                    toHit.add(asteroid)
                    toHit.add(playerBullet)
            if circles_collide(asteroid.position, asteroid.radius, self.playerShip.position, self.playerShip.radius):
                toHit.add(self.playerShip)
        for thing in toHit:
            thing.get_hit()

    def spawn_asteroids(self, dt):
        period = 1.0
        size = 0
        if self.playTime <= 20:
            period = 2.0
            size = 1
        elif self.playTime <= 40:
            period = 2.5
            size = 2
        elif self.playTime <= 60:
            period = 4.0
            size = 3
        elif self.playTime <= 80:
            period = 7.0
            size = 4
        else:
            period = 6.0
            size = 4
        self.spawnAccum += dt
        if self.spawnAccum > period:
            self.spawnAccum -= period
            self.spawn_asteroid(size)

    def spawn_asteroid(self, size):
        position = pygame.Vector2(0, 0)
        if bool(random.randint(0, 1)):
            if bool(random.randint(0, 1)): position = pygame.Vector2(random.uniform(0, 800), 0)
            else: position = pygame.Vector2(random.uniform(0, 800), 800)
        else:
            if bool(random.randint(0, 1)): position = pygame.Vector2(0, random.uniform(0, 800))
            else: position = pygame.Vector2(800, random.uniform(0, 800))

        moveDirection = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        SpaceAsteroid.Asteroid(self, position, moveDirection, size)

    def render(self, surface:pygame.Surface):
        self.playerShip.render(surface)
        for playerBullet in self.playerBullets:
            playerBullet.render(surface)
        for asteroid in self.asteroids:
            asteroid.render(surface)
        self.scoreText.render(surface)

    def add_player_bullet(self, bullet):
        self.playerBullets.append(bullet)

    def remove_player_bullet(self, bullet) :
        if(bullet in self.playerBullets):
            self.playerBullets.remove(bullet)

    def add_asteroid(self, asteroid):
        self.asteroids.append(asteroid)

    def remove_asteroid(self, asteroid):
        if asteroid in self.asteroids: 
            self.asteroids.remove(asteroid)

    def lose(self):
        self.isPlaying = False

