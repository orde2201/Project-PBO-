import random
from abc import ABC, abstractmethod
import pygame
import basic_attack

# --- Abstract base Character class ---


   


# --- Player class ---


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

    

    def is_alive(self):
        return self.get_hp() > 0
