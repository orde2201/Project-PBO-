import random
from abc import ABC, abstractmethod
import pygame
import basic_attack
import text
import sys
import effect_animation

# --- Abstract base Character class ---
class Character(ABC):
    def __init__(self, name, level, hp, attack, max_hp, energy, max_energy, is_guarding):
        self.__name = name
        self.__level = level
        self.__hp = hp
        self.__attack = attack
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

    def get_is_guarding(self):
        return self.__is_guarding

    def set_is_guarding(self, is_guarding):
        self.__is_guarding = is_guarding

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
            max_hp=100,
            energy=100,
            max_energy=100,
            is_guarding=False
        )
        self.__experience = 0
        self.__skill_energy_cost = {
            "basic_skill": 10,
            "special_attack": 50,
            "crit_buff": 10
        }
        self.__crit_buff_turns = 0

    def is_crit_buff_active(self):
        return self.__crit_buff_turns > 0

    def decrement_crit_buff(self):
        if self.__crit_buff_turns > 0:
            self.__crit_buff_turns -= 1

    def use_crit_buff(self, screen):
        # Cek apakah buff sudah aktif
        if self.__crit_buff_turns > 0:
            text.font_animation("Crit Buff already active!", screen, random.randrange(270, 600),
                                random.randrange(100, 300), 40, "orange", fade_in=False)
            
            return False

        cost = self.get_skill_energy_cost("crit_buff")
        if self.get_energy() < cost:
            text.font_animation("Not enough energy for Crit Buff.", screen, random.randrange(270, 600),
                                random.randrange(100, 300), 40, "white", fade_in=False)
            return False
        self.set_hp(self.get_hp() + 20)
        self.set_energy(self.get_energy() - cost)
        self.__crit_buff_turns = 3
        text.font_animation("Crit Buff Activated!", screen, random.randrange(270, 600),
                            random.randrange(100, 300), 40, "yellow", fade_in=False)
        return True

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
        if self.get_level() < 10:
            self.set_level(self.get_level() + 1)
            self.set_attack(self.get_attack() + 2)
            self.set_max_hp(self.get_max_hp() + 20)
            self.set_hp(self.get_hp() + 50)  
            self.set_max_energy(self.get_max_energy() + 20)
            self.set_energy(self.get_energy() + 50)  # fill energy to max when level up
            print(f"{self.get_name()} has leveled up to level {self.get_level()}!")
        else:
            text.font_animation("Level Maximum!", screen, random.randrange(270, 600), random.randrange(100, 300), 40, "white", fade_in=False)

    def attack(self, cancer, screen=None):
        attack_sound = pygame.mixer.Sound("assets/sound/draw-sword1-44724.mp3")
        attack_sound.play()
        if screen:
            asset = "assets/slash_basic/warrior_skill1_frame"
            basic_attack.attack_animation(screen, 10, asset)

        crit = False
        base_damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)

        if self.is_crit_buff_active():
            if random.random() < 0.5:  # 40% chance crit saat buff aktif
                base_damage *= 2
                crit = True
            self.decrement_crit_buff()

        cancer.set_hp(cancer.get_hp() - base_damage)
        cancer.take_damage()
        cancer.cancer_image(screen, cancer)

        if crit:
            text.font_animation(f"{base_damage} CRIT!!", screen, random.randrange(270, 600),
                                random.randrange(100, 300), 40, "orange", fade_in=False)
        else:
            text.font_animation(f"{base_damage} damage!", screen, random.randrange(270, 600),
                                random.randrange(100, 300), 40, "white", fade_in=False)
        damage = base_damage
        return damage

    def use_skill(self, skill_name, target, screen):
        
        cost = self.__skill_energy_cost.get(skill_name)
        if cost is None:
            print(f"Skill {skill_name} not found.")
            return False

        if self.get_energy() < cost:
            print("Not enough energy to use this skill.")
            text.font_animation("Not enough energy to use this skill.", screen, random.randrange(270, 600), random.randrange(100, 300), 40, "white", fade_in=False)
            return False

        self.set_energy(self.get_energy() - cost)

        try:
            if skill_name == "basic_skill":
                attack_sound = pygame.mixer.Sound("assets/sound/draw-sword1-44724.mp3")
                attack_sound.play()
                asset = "assets/slash_skill/warrior_skill4_frame"
                basic_attack.attack_animation(screen, 7, asset)
                target.take_damage()
                target.cancer_image(screen, target)
                damage = self.get_attack() * 3
            elif skill_name == "special_attack":
                attack_sound = pygame.mixer.Sound("assets/sound/draw-sword1-44724.mp3")
                attack_sound.play()
                asset = "assets/slash_skill/warrior_skill4_frame"
                basic_attack.attack_animation(screen, 7, asset)
                asset = "assets/slash_basic/warrior_skill1_frame"
                basic_attack.attack_animation(screen, 10, asset)
                target.take_damage()
                target.cancer_image(screen, target)
                damage = self.get_attack() * 8
            else:
                return False

            crit = False
            if self.is_crit_buff_active():
                if random.random() < 0.5:  # 40% chance crit saat buff aktif
                    damage *= 2
                    crit = True
                self.decrement_crit_buff()

            if crit:
                text.font_animation(f"{damage} CRIT!!", screen, random.randrange(270, 600),
                                    random.randrange(100, 300), 40, "orange", fade_in=False)
            else:
                text.font_animation(f"{damage} damage!", screen, random.randrange(270, 600),
                                    random.randrange(100, 300), 40, "white", fade_in=False)

            target.set_hp(target.get_hp() - damage)
            return True
        except Exception as e:
            print(f"Error using skill {skill_name}: {e}")
            return False

    def guard(self):
        self.set_is_guarding(True)
        self.set_energy(min(self.get_energy() + 10, self.get_max_energy()))
        if self.is_crit_buff_active():
            self.decrement_crit_buff()

        print(f"{self.get_name()} is guarding and gained 10 energy!")

    def take_damage(self, amount, screen):
        try:
            chance = random.randint(1, 10)
            if self.get_is_guarding():
                if chance < 6:  # 60% chance to miss
                    amount = 0
                else:
                    amount = max(1, amount // 2)  # Ensure at least 1 damage

                self.set_is_guarding(False)

            self.set_hp(self.get_hp() - amount)
            effect_animation.effect_animation(screen, "assets/take_dmg.png")
            return amount
        except Exception as e:
            print(f"Error taking damage: {e}")
            return 0

    def regenerate_energy(self, amount):
        self.set_energy(min(self.get_energy() + amount, self.get_max_energy()))

    def is_alive(self):
        return self.get_hp() > 0


# --- Cancer (Monster) class ---
class Cancer(Character):
    def __init__(self, cancer_type, level):
        self.__blinking = False           # private
        self.__blink_timer = 0            # private

        try:
            if cancer_type == "normal_cancer":
                self.__cancer_img = pygame.image.load("assets/normal_cancer.png").convert_alpha()
                hp = random.randint(150, 250)
                attack = random.randint(7, 12)
                defense = 5
            elif cancer_type == "new_cancer":
                self.__cancer_img = pygame.image.load("assets/easy_cancer.png").convert_alpha()
                hp = random.randint(80, 100)
                attack = random.randint(3, 7)
                defense = 5
            elif cancer_type == "high_cancer":
                self.__cancer_img = pygame.image.load("assets/cancer.png").convert_alpha()  # private
                hp = random.randint(250, 350)
                attack = random.randint(12, 14)
                defense = 10
            else:
                raise ValueError(f"Invalid cancer type: {cancer_type}")

            super().__init__(
                cancer_type.replace("_", " ").title(),
                level,
                hp,
                attack,
                max_hp=hp,
                energy=0,
                max_energy=0,
                is_guarding=False
            )
        except pygame.error as e:
            print(f"Error loading cancer image: {e}")
            raise

    def reset_hp(self):
        self.hp = self.max_hp

    # Getter dan Setter (Opsional tergantung kebutuhan)
    def set_blinking(self, value: bool):
        self.__blinking = value

    def get_blinking(self):
        return self.__blinking

    def set_blink_timer(self, time_ms: int):
        self.__blink_timer = time_ms

    def get_blink_timer(self):
        return self.__blink_timer

    def cancer_image(self, screen, cancer):
        current_time = pygame.time.get_ticks()
        cancer_size = pygame.transform.scale(self.__cancer_img, (450, 420))
        clock = pygame.time.Clock()

        if self.__blinking:
            blink_interval = 80
            start_time = current_time

            while pygame.time.get_ticks() - start_time < (self.__blink_timer - start_time):
                current_time = pygame.time.get_ticks()
                blink_phase = (current_time % (blink_interval * 2)) < blink_interval

                if blink_phase:
                    try:
                        cancer_take_sound = pygame.mixer.Sound("assets/sound/monster damage.wav")
                        cancer_take_sound.play()
                    except pygame.error as e:
                        print(f"Error playing sound: {e}")

                    red_cancer = cancer_size.copy()
                    red_cancer.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                    screen.blit(red_cancer, (200, 0))
                else:
                    screen.blit(cancer_size, (200, 0))
                    self.__blinking = False

                pygame.display.flip()
            screen.blit(cancer_size, (200, 0))
            clock.tick(90)
            pygame.time.delay(100)
        else:
            screen.blit(cancer_size, (200, 0))

    def attack(self, player, screen):
        try:
            cancer_bite_sound = pygame.mixer.Sound("assets/sound/monster-bite-44538.mp3")
            cancer_bite_sound.play()
            asset = "assets/cancer_attack/warrior_skill5_frame"
            basic_attack.attack_animation(screen, 7, asset)

            damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)

            hit = player.take_damage(damage, screen)
            if hit != 0 or self.get_is_guarding():
                text.font_animation(f"{hit} damage!!", screen, random.randrange(270, 600), random.randrange(100, 300), 60, "red", fade_in=False)
            elif hit == 0:
                text.font_animation("Miss", screen, random.randrange(270, 600), random.randrange(100, 300), 60, "green", fade_in=False)

            return damage
        except Exception as e:
            print(f"Error during cancer attack: {e}")
            return 0

    def is_alive(self):
        return self.get_hp() > 0

    def take_damage(self):
       
        self.__blinking = True
        self.__blink_timer = pygame.time.get_ticks() + 300
        print("cancer take dmg")


def attack(target, attacker, screen):
    try:
        # Cek apakah attacker dan target merupakan subclass dari Character
        if not isinstance(attacker, Character):
            raise TypeError("Attacker must be a Character instance.")
        if not isinstance(target, Character):
            raise TypeError("Target must be a Character instance.")
        if screen is None:
            raise ValueError("Screen object is required.")

        # Panggil fungsi attack dari attacker
        return attacker.attack(target, screen)

    except Exception as e:
        print(f"Error during attack: {e}")
        text.font_animation(f"Attack failed: {str(e)}", screen, 300, 150, 30, "red", fade_in=False)
        return None
