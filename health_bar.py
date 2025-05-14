import pygame

class BarHp:
    @staticmethod
    def bar_hp(screen,x,y,width,height,color1,color2, hp=50, max_hp=100, ):
        ratio = hp / max_hp
        pygame.draw.rect(screen, color1, (x, y, width, height))
        pygame.draw.rect(screen, color2, (x, y, width * ratio, height))
