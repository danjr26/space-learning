import numpy as np
import pygame
import math
import time

import PlayerBullet
import SpaceGame

texture = pygame.image.load("ship.png")

class PlayerShip:
    def __init__(self, game):
        self.game = game
        self.position = pygame.Vector2(400, 400)
        self.rotation = 45.0
        self.radius = 18.0
        self.scale = 0.5
        self.drawTexture = pygame.transform.rotozoom(texture, self.rotation, self.scale)
        self.moveDirection = pygame.Vector2(0, 0)
        self.moveSpeed = 100
        self.isShooting = False
        self.shootAccum = 0.0
        self.shootPeriod = 0.25

    def update(self, dt):
        if(self.moveDirection.length_squared() != 0):
            self.moveDirection.scale_to_length(self.moveSpeed)
        self.position += self.moveDirection * dt
        SpaceGame.wrap_coords(self.position)
        self.shootAccum += dt
        self.fire()

    def fire(self):
        if not self.isShooting or self.shootAccum < self.shootPeriod: return False
        self.shootAccum -= self.shootPeriod
        shootDirection = pygame.Vector2(math.cos(math.radians(self.rotation)), -math.sin(math.radians(self.rotation)))
        bullet = PlayerBullet.PlayerBullet(self.game, self.position + shootDirection * self.radius, shootDirection)
        self.game.score -= 2
        return True

    def render(self, surface:pygame.Surface):
        self.drawTexture = pygame.transform.rotozoom(texture, self.rotation, self.scale)
        surface.blit(self.drawTexture, self.position - pygame.Vector2(self.drawTexture.get_rect().size) / 2.0)

    def get_hit(self):
        self.game.lose()
