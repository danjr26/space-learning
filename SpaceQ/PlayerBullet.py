import pygame
import math
import time
import SpaceGame

texture = pygame.image.load("player_bullet.png")

class PlayerBullet:
    def __init__(self, game, position:pygame.Vector2, moveDirection:pygame.Vector2):
        self.game = game
        self.position = position
        self.rotation = 0.0
        self.radius = 2.0
        self.scale = 0.5
        self.drawTexture = pygame.transform.rotozoom(texture, self.rotation, self.scale)
        self.moveDirection = moveDirection
        self.moveSpeed = 500
        self.passedTime = 0.0
        self.lifeTime = 0.5
        self.game.add_player_bullet(self)

    def update(self, dt):
        if self.moveDirection.length_squared() != 0:
            self.moveDirection.scale_to_length(self.moveSpeed)
        self.position += self.moveDirection * dt
        SpaceGame.wrap_coords(self.position)
        self.passedTime += dt
        if self.passedTime >= self.lifeTime: self.destroy()

    def render(self, surface:pygame.Surface):
        self.drawTexture = pygame.transform.rotozoom(texture, self.rotation, self.scale)
        surface.blit(self.drawTexture, self.position - pygame.Vector2(self.drawTexture.get_rect().size) / 2.0)

    def destroy(self):
        self.game.remove_player_bullet(self)

    def get_hit(self):
        self.destroy()

