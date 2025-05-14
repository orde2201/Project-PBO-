import random
from abc import ABC, abstractmethod
import pygame
import time
import basic_attack
#import assets

# --- Kelas Abstrak Character ---
class Character(ABC):
    def __init__(self, name, level, hp, attack, defense, max_hp, energy, max_energy):
        self.__name = name
        self.__level = level
        self.__hp = hp
        self.__attack = attack
        self.__defense = defense
        self.__max_hp = max_hp
        self.__energy = energy
        self.__max_energy = max_energy

    def get_energy(self):
        return self.__energy

    def set_energy(self, energy):
        self.__energy = energy

    def get_max_energy(self):
        return self.__max_energy

    def set_max_energy(self, max_energy):
        self.__max_energy = max_energy

    def get_max_hp(self):
        return self.__max_hp

    def set_max_hp(self, max_hp):
        self.__max_hp = max_hp

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_level(self):
        return self.__level

    def set_level(self, level):
        self.__level = level

    def get_hp(self):
        return self.__hp

    def set_hp(self, hp):
        self.__hp = hp

    def get_attack(self):
        return self.__attack

    def set_attack(self, attack):
        self.__attack = attack

    def get_defense(self):
        return self.__defense

    def set_defense(self, defense):
        self.__defense = defense

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def is_alive(self):
        pass

# --- Kelas Player ---
class Player(Character):
    def __init__(self, name):
        super().__init__(name, 1, 100, 10, 10, 100, 100, 100)
        self.__experience = 0

    @staticmethod
    def player_image(screen):
        player_image = pygame.image.load("assets/player_image.png")
        player_image_size = pygame.transform.scale(player_image, (200, 200))
        screen.blit(player_image_size, (10, 400))

    def level_up(self):
        self.set_level(self.get_level() + 1)
        self.set_attack(self.get_attack() + 5)
        self.set_defense(self.get_defense() + 5)
        self.set_hp(self.get_hp() + 5)
        print(f"{self.get_name()} has leveled up to level {self.get_level()}!")

    def attack(self, cancer,screen):
        basic_attack.attack_animation(screen)
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {cancer.get_name()} for {damage} damage!")
        blink_interval = 500
        cancer.set_hp(cancer.get_hp() - damage)
        # Delay 0.5 detik
        return damage

    def is_alive(self):
        return self.get_hp() > 0

# --- Kelas Monster ---
class Cancer(Character):
    def __init__(self, cancer_type, level):
        random_hp = random.randint(80, 100)
        random_hp_high = random.randint(300,400)
        self.type = cancer_type
        if cancer_type == "normal_cancer":
            super().__init__("Normal Cancer", level,random_hp , random.randint(5, 10), 5, random_hp, 0, 0)
        else:
            super().__init__("High Cancer", level, random_hp_high, random.randint(5, 10), 10,random_hp_high, 0, 0)
        self.__image = None

    @staticmethod
    def cancer_image(screen):
        cancer_image = pygame.image.load("assets/cancer.png")
        cancer_size = pygame.transform.scale(cancer_image, (550, 550))
        screen.blit(cancer_size, (200, 0))

    def attack(self, player):
        
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {player.get_name()} for {damage} damage!")
        player.set_hp(player.get_hp() - damage)
        # Delay 0.5 detik
        return damage

    def is_alive(self):
        return self.get_hp() > 0
