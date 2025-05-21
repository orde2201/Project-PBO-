import random
from abc import ABC, abstractmethod
import pygame
import basic_attack

# --- Abstract base Character class ---
class Character(ABC):
    def __init__(self, name, level, hp, attack, defense, max_hp, energy, max_energy, is_guarding):
        self._name = name
        self._level = level
        self._hp = hp
        self._attack = attack
        self._defense = defense
        self._max_hp = max_hp
        self._energy = energy
        self._max_energy = max_energy
        self.is_guarding = is_guarding

    def get_energy(self):
        return self._energy

    def set_energy(self, energy):
        self._energy = max(0, min(energy, self._max_energy))

    def get_max_energy(self):
        return self._max_energy

    def set_max_energy(self, max_energy):
        self._max_energy = max_energy

    def get_max_hp(self):
        return self._max_hp

    def set_max_hp(self, max_hp):
        self._max_hp = max_hp

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_level(self):
        return self._level

    def set_level(self, level):
        self._level = level

    def get_hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = max(0, min(hp, self._max_hp))

    def get_attack(self):
        return self._attack

    def set_attack(self, attack):
        self._attack = attack

    def get_defense(self):
        return self._defense

    def set_defense(self, defense):
        self._defense = defense

    @abstractmethod
    def guard(self, attacker, logs=None):
        pass

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def is_alive(self):
        return self.get_hp() > 0


# --- Player class ---
class Player(Character):
    def __init__(self, name):
        super().__init__(
            name,
            level=1,
            hp=100,
            attack=10,
            defense=10,
            max_hp=100,
            energy=100,
            max_energy=100,
            is_guarding=False
        )
        self.__experience = 0
        self.skill_energy_cost = {
            "basic_skill": 10,
            "special_attack": 50,
        }
        self.is_guarding = False

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
            basic_attack.attack_animation(screen, 10, asset)
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {cancer.get_name()} for {damage} damage!")
        cancer.set_hp(cancer.get_hp() - damage)
        return damage

    def use_skill(self, skill_name, target, screen):
        cost = self.skill_energy_cost.get(skill_name)
        if cost is None:
            print(f"Skill {skill_name} not found.")
            return False
        if self.get_energy() < cost:
            print("Not enough energy to use this skill.")
            return False

        self.set_energy(self.get_energy() - cost)

        if skill_name == "basic_skill":
            asset = "assets/slash_skill/warrior_skill4_frame"
            basic_attack.attack_animation(screen, 7, asset)
            damage = self.get_attack() * 3
        elif skill_name == "special_attack":
            asset = "assets/slash_skill/warrior_skill4_frame"
            basic_attack.attack_animation(screen, 7, asset)
            asset = "assets/slash_basic/warrior_skill1_frame"
            basic_attack.attack_animation(screen, 10, asset)
            damage = self.get_attack() * 5
        else:
            return False

        target.set_hp(target.get_hp() - damage)
        print(f"Used skill {skill_name}, dealt {damage} damage.")
        return True

    def guard(self):
        self.is_guarding = True

    def take_damage(self, amount):
        chance = random.random()
        if self.is_guarding:
            if chance < 0.7:  # 70% chance musuh miss attack
                print(f"{self.get_name()} guarded and the attack missed!")
            amount = 0
        else:
            amount = amount // 2
            print(f"Guarding! Damage reduced to {amount}")
            self.is_guarding = False 
        self.set_hp(self.get_hp() - amount)
        print(f"{self.get_name()} takes {amount} damage. HP now {self.get_hp()}")

    def regenerate_energy(self, amount):
        self.set_energy(min(self.get_energy() + amount, self.get_max_energy()))

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

        super().__init__(
        cancer_type.replace("_", " ").title(),
        level,
        hp,
        attack,
        defense,
        max_hp=hp,
        energy=0,
        max_energy=0,
        is_guarding=False)

    @staticmethod
    def cancer_image(screen):
        cancer_image = pygame.image.load("assets/cancer.png")
        cancer_size = pygame.transform.scale(cancer_image, (550, 550))
        screen.blit(cancer_size, (200, 0))

    def attack(self, player, screen):
        asset = "assets/cancer_attack/warrior_skill5_frame"
        basic_attack.attack_animation(screen, 7, asset)

        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        print(f"{self.get_name()} attacks {player.get_name()} for {damage} damage!")
        player.take_damage(damage)

        return damage

    def guard(self, attacker, logs=None):
        self.is_guarding = True
        print(f"{self.get_name()} is guarding!")

    def is_alive(self):
        return self.get_hp() > 0
