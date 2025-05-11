import random
from character.base import BaseChar
import pygame

class Cancer(BaseChar):
    def __init__(self, name, level):
        # Random HP and Attack based on monster type
        if name == "normal_cancer":
            super().__init__(name, level, random.randint(80, 100), random.randint(5, 10), 5)
        elif name == "high_cancer":
            super().__init__(name, level, random.randint(300, 400), random.randint(10, 15), 10)

    def attack_cancer(self, monster):
        # Monsters don't attack other monsters, so no implementation here
        pass
    def cancer_image(screen):
        cancer_image = pygame.image.load("assets/cancer.png")
        cancer_size = pygame.transform.scale(cancer_image,(550,550))
        screen.blit(cancer_size,(200,0))
        
    def attack(self, player):
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {player.get_name()} for {damage} damage!")
        player.set_hp(player.get_hp() - damage)
        return damage

    def is_alive(self):
        return self.get_hp() > 0

cancer_status = Cancer("normal cancer",1)
