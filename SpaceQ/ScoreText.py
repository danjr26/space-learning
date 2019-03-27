import pygame

pygame.init()
displayFont = pygame.font.Font(pygame.font.match_font("Consolas,Lucida Console,Mono,Monospace,Sans"), 20)


class ScoreText:
    def __init__(self, game):
        self.game = game
        pass

    def render(self, surface:pygame.Surface):
        text = str(self.game.score).rjust(6)
        textImage = displayFont.render(text, True, (255, 255, 255))
        surface.blit(textImage, pygame.Vector2(0, 0))
        pass