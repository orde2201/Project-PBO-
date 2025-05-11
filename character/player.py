from character.base import BaseChar
import pygame
class PlayerMain(BaseChar) :
    def __init__(self, name):
        super().__init__(name, 1, 100, 10, 10)  # Set initial values for player
        self.__experience = 0
    def player_image(screen):
        player_image = pygame.image.load("assets/player_image.png")
        player_image_size = pygame.transform.scale(player_image,(200,200))
        screen.blit(player_image_size,(10,400))
        
    def level_up(self):
        self.set_level(self.get_level() + 1)
        self.set_attack(self.get_attack() + 5)
        self.set_defense(self.get_defense() + 5)
        self.set_hp(self.get_hp() + 5)
        print(f"{self.get_name()} has leveled up to level {self.get_level()}!")

    def attack(self, monster):
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {monster.get_name()} for {damage} damage!")
        monster.set_hp(monster.get_hp() - damage)
        return damage

    def attack_player(self, player):
        # Player doesn't attack other players directly, so no implementation here
        pass

    def is_alive(self):
        return self.get_hp() > 0



player_main = PlayerMain("Arthur")

