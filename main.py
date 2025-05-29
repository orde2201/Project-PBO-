import random
from abc import ABC, abstractmethod
import pygame
import basic_attack
import text
import test
import sys

#pygame.mixer.init()

# --- Abstract base Character class ---
class Character(ABC):
    def __init__(self, name, level, hp, attack, defense, max_hp, energy, max_energy, is_guarding):
        self.__name = name
        self.__level = level
        self.__hp = hp
        self.__attack = attack
        self.__defense = defense
        self.__max_hp = max_hp
        self.__energy = energy
        self.__max_energy = max_energy
        self.__is_guarding = is_guarding

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

    def get_is_guarding(self):
        return self.__is_guarding

    def set_is_guarding(self, is_guarding):
        self.__is_guarding = is_guarding

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
        self.__skill_energy_cost = {
            "basic_skill": 10,
            "special_attack": 50,
        }

    def get_experience(self):
        return self.__experience

    def set_experience(self, experience):
        self.__experience = experience

    def get_skill_energy_cost(self, skill_name):
        return self.__skill_energy_cost.get(skill_name)

    @staticmethod
    def player_image(screen):
        player_image = pygame.image.load("assets/player_image.png")
        player_image_size = pygame.transform.scale(player_image, (160, 160))
        screen.blit(player_image_size, (50, 420))

    def level_up(self):
        
        if self.set_level != 10 :
            self.set_level(self.get_level() + 1)
        else :
             text.font_animation("Level Maximum!", screen, random.randrange(270,600), random.randrange(100,300), 40,"white", fade_in=False)
        self.set_attack(self.get_attack() + 2)
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

        cancer.set_hp(cancer.get_hp() - damage)
        cancer.take_damage()
        cancer.cancer_image(screen,cancer)
        print("works")
        text.font_animation(f"{damage} damage!", screen, random.randrange(270,600), random.randrange(100,300), 40,"white", fade_in=False)
       
        return damage
   
    def use_skill(self, skill_name, target, screen):
        cost = self.__skill_energy_cost.get(skill_name)
        if cost is None:
            print(f"Skill {skill_name} not found.")
            return False
        if self.get_energy() < cost:
            print("Not enough energy to use this skill.")
            text.font_animation("Not enough energy to use this skill.", screen, random.randrange(270,600), random.randrange(100,300), 40,"white", fade_in=False)
            return False

        self.set_energy(self.get_energy() - cost)

        if skill_name == "basic_skill":
            asset = "assets/slash_skill/warrior_skill4_frame"
            basic_attack.attack_animation(screen, 7, asset)
            target.take_damage()
            target.cancer_image(screen,target)
            damage = self.get_attack() * 3
        elif skill_name == "special_attack":
            asset = "assets/slash_skill/warrior_skill4_frame"
            basic_attack.attack_animation(screen, 7, asset)
            asset = "assets/slash_basic/warrior_skill1_frame"
            basic_attack.attack_animation(screen, 10, asset)
            target.take_damage()
            target.cancer_image(screen,target)
            damage = self.get_attack() * 8
        else:
            return False

        target.set_hp(target.get_hp() - damage)
        text.font_animation(f"{damage} damage!", screen, random.randrange(270,600), random.randrange(100,300), 40, "white",fade_in=False)

        return True

    def guard(self):
        self.set_is_guarding(True)
        self.set_energy(min(self.get_energy() + 10, self.get_max_energy()))
        print(f"{self.get_name()} is guarding and gained 10 energy!")

    def take_damage(self, amount, screen):
        chance = random.randint(1,10)
        if self.get_is_guarding():
            if chance < 5:  # 60% chance to miss
                
                amount = 0
            else:
                amount = max(1, amount // 2)  # Ensure at least 1 damage
                
            self.set_is_guarding(False)
        
        self.set_hp(self.get_hp() - amount)
        
        return amount

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

        self.blinking = False
        self.blink_timer = 0

    def cancer_image(self, screen, cancer):
        current_time = pygame.time.get_ticks()
        cancer_img = pygame.image.load("assets/cancer.png").convert_alpha()
        cancer_size = pygame.transform.scale(cancer_img, (450, 420))
        clock = pygame.time.Clock()
        
        if self.blinking:
            # Hitung waktu blink (0.1 detik = 100 milidetik)
            blink_interval = 80  # ms
            start_time = current_time
            
            # Loop blocking selama waktu blink
            while pygame.time.get_ticks() - start_time < (self.blink_timer - start_time):
                current_time = pygame.time.get_ticks()
                blink_phase = (current_time % (blink_interval * 2)) < blink_interval
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                # Clear screen (gunakan background color game Anda)
                
                # Gambar cancer sesuai fase
                if blink_phase:  # Fase merah
                    cancer_take_sound = pygame.mixer.Sound("assets/sound/monster damage.wav")
                    cancer_take_sound.play()
                    red_cancer = cancer_size.copy()
                    red_cancer.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                    screen.blit(red_cancer, (200, 0))
                else:  # Fase normal
                    screen.blit(cancer_size, (200, 0))
                    
                pygame.display.flip()
            clock.tick(60)  # 60 FPS
            self.blinking = False
            pygame.time.delay(100)
        else:
            # Gambar normal jika tidak blinking
            screen.blit(cancer_size, (200, 0))
                    
    
    def attack(self, player, screen):
        cancer_bite_sound = pygame.mixer.Sound("assets/sound/monster-bite-44538.mp3")
        cancer_bite_sound.play()
        asset = "assets/cancer_attack/warrior_skill5_frame"
        basic_attack.attack_animation(screen, 7, asset)
        
        
        damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
        
        print(f"{self.get_name()} attacks {player.get_name()} for {damage} damage!")
        hit = player.take_damage(damage, screen)
        if hit != 0 and self.get_is_guarding:
            text.font_animation(f"{hit} damage!!", screen, random.randrange(270,600), random.randrange(100,300), 60,"red", fade_in=False)
        if hit == 0 :
            text.font_animation("Miss", screen, random.randrange(270,600), random.randrange(100,300), 60,"green", fade_in=False)

        return damage

    def guard(self, attacker, logs=None):
        self.set_is_guarding(True)
        print(f"{self.get_name()} is guarding!")

    def is_alive(self):
        return self.get_hp() > 0
    
    def take_damage(self):
        # Setelah cancer menerima damage
        self.blinking = True
        self.blink_timer = pygame.time.get_ticks() + 300  # kedip selama 300 ms
        print("cancer take dmg")
        pass
