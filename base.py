import random
from abc import ABC, abstractmethod
import pygame
import basic_attack

# --- Abstract base Character class ---


    def get_energy(self):
        return self.__energy

    def set_energy(self, energy):
        self.__energy = max(0, min(energy, self.__max_energy))

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
        self.__hp = max(0, min(hp, self.__max_hp))

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
        return self.get_hp() > 0


# --- Player class ---
class Player(Character):
    def __init__(self, name):
        super().__init__(name, level=1, hp=100, attack=10, defense=10, max_hp=100, energy=100, max_energy=100)
        self.__experience = 0
        self.skill_energy_cost = {
            "basic_skill": 10,
            "special_attack": 50,
        }

    @staticmethod
    def player_image(screen):
        player_image = pygame.image.load("assets/player_image.png")
        player_image_size = pygame.transform.scale(player_image, (160, 160))
        screen.blit(player_image_size, (50, 420))

    def level_up(self):
        self.set_level(self.get_level() + 1)
        self.set_attack(self.get_attack() + 5)
        self.set_defense(self.get_defense() + 5)
        self.set_max_hp(self.get_max_hp() + 5)
        self.set_hp(self.get_max_hp())  # restore hp to max when level up
        self.set_max_energy(self.get_max_energy() + 10)
        self.set_energy(self.get_max_energy())  # fill energy to max when level up
        print(f"{self.get_name()} has leveled up to level {self.get_level()}!")

    def attack(self, cancer, screen=None):
        if screen:
            asset = "assets/slash_basic/warrior_skill1_frame"
            basic_attack.attack_animation(screen,10,asset)
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {cancer.get_name()} for {damage} damage!")
        cancer.set_hp(cancer.get_hp() - damage)
        return damage

    def use_skill(self, skill_name, target,screen):
        cost = self.skill_energy_cost.get(skill_name, None)
        if cost is None:
            print(f"Skill {skill_name} not found.")
            return False
        if self.get_energy() < cost:
            print("Not enough energy to use this skill.")
            return False

        self.set_energy(self.get_energy() - cost)

        if skill_name == "basic_skill":
            asset = "assets/slash_skill/warrior_skill4_frame"
            basic_attack.attack_animation(screen,7,asset)
            damage = self.get_attack() * 3
            target.set_hp(target.get_hp() - damage)
            print(f"Used skill {skill_name}, dealt {damage} damage.")
        elif skill_name == "special_attack":
            asset = "assets/slash_skill/warrior_skill4_frame"
            basic_attack.attack_animation(screen,7,asset)
            asset = "assets/slash_basic/warrior_skill1_frame"
            basic_attack.attack_animation(screen,10,asset)
            damage = self.get_attack() * 5
            target.set_hp(target.get_hp() - damage)
            print(f"Used skill {skill_name}, dealt {damage} damage.")

        return True

    def regenerate_energy(self, amount):
        self.set_energy(self.get_energy() + amount)

    def is_alive(self):
        return self.get_hp() > 0


# --- Cancer (Monster) class ---
class Cancer(Character):
    def __init__(self, cancer_type, level):
        if cancer_type == "normal_cancer":
            hp = random.randint(80, 100)
            attack = random.randint(5, 10)
            defense = 5
        elif cancer_type == "high_cancer":
            hp = random.randint(300, 400)
            attack = random.randint(10, 15)
            defense = 10
        else:
            hp = 100
            attack = 5
            defense = 5

        super().__init__(cancer_type.replace("_", " ").title(), level, hp, attack, defense, hp, energy=0, max_energy=0)

    @staticmethod
    def cancer_image(screen):
        cancer_image = pygame.image.load("assets/cancer.png")
        cancer_size = pygame.transform.scale(cancer_image, (550, 550))
        screen.blit(cancer_size, (200, 0))

    def attack(self, player,screen):
        asset = "assets/cancer_attack/warrior_skill5_frame"
        basic_attack.attack_animation(screen,7,asset)
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {player.get_name()} for {damage} damage!")
        player.set_hp(player.get_hp() - damage)
        return damage

    def is_alive(self):
        return self.get_hp() > 0
