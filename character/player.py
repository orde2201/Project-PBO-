from character.base import BaseChar
from character.cancer import Cancer
from character.player import PlayerMain
from character.base import Player
import random
import pygame
import basic_attack

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Skill Energy Demo")

    player = PlayerMain("Arthur")
    enemy = Cancer("normal_cancer", 1)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        player.player_image(screen)
        enemy.cancer_image(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pencet SPACE untuk pakai skill basic attack
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.use_skill("basic_attack", enemy, screen):
                        print("Skill basic attack berhasil digunakan.")
                    else:
                        print("Gagal menggunakan skill basic attack.")
                    print(f"Energi pemain sekarang: {player.get_energy()}")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()



class PlayerMain(Player):
    def __init__(self, name):
        super().__init__(name)
        # definisi energy cost tiap skill
        self.skill_energy_cost = {
            "basic_attack": 20,
            "special_attack": 50,
        }

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
        self.set_max_hp(self.get_max_hp() + 5)
        self.set_max_energy(self.get_max_energy() + 10)  # tambah max energy saat level up
        self.set_energy(self.get_max_energy())  # isi energi penuh saat level up
        print(f"{self.get_name()} has leveled up to level {self.get_level()}!")

    def use_skill(self, skill_name, target, screen):
        if skill_name not in self.skill_energy_cost:
            print("Skill tidak dikenal.")
            return False

        cost = self.skill_energy_cost[skill_name]
        if self.get_energy() < cost:
            print(f"Energi tidak cukup untuk menggunakan skill {skill_name}.")
            return False

        # Kurangi energi
        self.set_energy(self.get_energy() - cost)

        # Eksekusi efek skill
        if skill_name == "basic_attack":
            basic_attack.attack_animation(screen)
            damage = random.randint(self.get_attack() - 2, self.get_attack() + 2)
            print(f"{self.get_name()} uses {skill_name} on {target.get_name()} for {damage} damage!")
            target.set_hp(target.get_hp() - damage)
            return True

        elif skill_name == "special_attack":
            damage = random.randint(self.get_attack(), self.get_attack() + 10)
            print(f"{self.get_name()} uses {skill_name} on {target.get_name()} for {damage} damage!")
            target.set_hp(target.get_hp() - damage)
            return True

        return False

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

