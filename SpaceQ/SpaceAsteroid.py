import pygame, math, time, random, copy
import SpaceGame

texture = pygame.image.load("asteroid.png")


class Asteroid:
    def __init__(self, game:SpaceGame, position:pygame.Vector2, moveDirection:pygame.Vector2, size):
        self.game = game
        self.size = size
        self.position = position
        self.rotation = 0.0
        self.radius = 18.0 * 1.3**size
        self.scale = 0.20 * 1.3**size
        self.drawTexture = pygame.transform.rotozoom(texture, self.rotation, self.scale)
        self.moveDirection = moveDirection
        self.moveSpeed = 150 * 0.9**size * random.uniform(0.75, 1.0)
        self.game.add_asteroid(self)

    def update(self, dt):
        if self.moveDirection.length_squared() != 0:
            self.moveDirection.scale_to_length(self.moveSpeed)
        self.position += self.moveDirection * dt
        SpaceGame.wrap_coords(self.position)

    def render(self, surface:pygame.Surface):
        self.drawTexture = pygame.transform.rotozoom(texture, self.rotation, self.scale)
        surface.blit(self.drawTexture, self.position - pygame.Vector2(self.drawTexture.get_rect().size) / 2.0)

    def destroy(self):
        self.game.remove_asteroid(self)

    def split(self):
        rotateAmount = random.uniform(5, 15)
        Asteroid(self.game, copy.copy(self.position), self.moveDirection.rotate(rotateAmount), self.size - 1);
        Asteroid(self.game, copy.copy(self.position), self.moveDirection.rotate(-rotateAmount), self.size - 1);
        self.destroy()

    def get_hit(self):
        self.game.score += 10
        if self.size >= 1:
            self.split()
        self.destroy()

