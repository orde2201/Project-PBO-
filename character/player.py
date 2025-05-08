from character.base import BaseChar
import pygame
class Arthur(BaseChar) :
    #gambar character player

    def __init__(self,health_poin,deffend,demage) :
        super().__init__(health_poin,deffend,demage)
        self.set_name("nigger")
        self.arthur_char_img = pygame.image.load("assets/main_cursor.png")
        self.size_gambar = pygame.transform.scale(self.arthur_char_img,(100,100))
        #koordinat player
        self.x = 0
        self.y = 0

        self.y_point= 0
        self.x_point= 0
        
    def draw(self,screen):
        screen.blit(self.size_gambar,(self.x_point,self.y_point))
    
    def attack(self):
        pass
    def guard(self):
        pass
    def skill(self):
        pass

       

player_main = Arthur(200, 0, 21)

