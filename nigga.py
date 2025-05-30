import sys
import pygame
import random
import cursor
import base
import text
from health_bar import BarHp

# Fungsi bantu load gambar dengan error handling
def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error as e:
        print(f"Gagal memuat gambar {path}: {e}")
        placeholder = pygame.Surface(size if size else (50, 50))
        placeholder.fill((255, 0, 255))  # warna magenta sebagai placeholder
        return placeholder

# Fungsi bantu load suara dengan error handling
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Gagal memuat suara {path}: {e}")
        return None

# Inisialisasi pygame
pygame.init()
pygame.mixer.init()
battle_bgm_channel = pygame.mixer.Channel(0)  # channel 0 khusus untuk musik battle

# Menyembunyikan kursor mouse
pygame.mouse.set_visible(False)

# Ukuran layar utama
screen = pygame.display.set_mode((1000, 600))

class CancerHunter:
    def __init__(self):
        self._cursor_x = -40
        self._cursor_y = 40
        self._base_structure = 1  # 1=menu, 2=pilih mode, 3=explore, 4=battle
        self._selected_mode = None
        self._player = None
        self._cancer = None
        self._cancers = []
        self._camera = [0, 0]
        self._player_pos = [1000, 600]
        self._cancer_type = None
        
        # Load sound dengan error handling
        self._click_sound = load_sound("assets/sound/click-button-166324.mp3")
        self._backsound = load_sound("assets/sound/horror-thriller-2-336734.mp3")
        if self._backsound:
            self._backsound.play(-1)

    # Getter dan Setter
    def get_cursor_pos(self):
        return (self._cursor_x, self._cursor_y)
    
    def get_base_structure(self):
        return self._base_structure
    
    def get_selected_mode(self):
        return self._selected_mode
    
    def set_base_structure(self, value):
        self._base_structure = value
    
    def set_cursor_pos(self, x, y):
        self._cursor_x = x
        self._cursor_y = y
    
    def set_selected_mode(self, mode):
        self._selected_mode = mode

    def menu(self, screen, event):
        try:
            menu_background = load_image("assets/menu_background.png")
            screen.blit(menu_background, (0, 0))
        except Exception as e:
            print("Error saat load menu background:", e)
            screen.fill((0, 0, 0))

        typing = "START"
        start_rect = text.font(typing, screen, 500, 200, 200)
        
        if event and event.type == pygame.MOUSEMOTION:
            self.set_cursor_pos(*event.pos)

        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                if self._click_sound:
                    self._click_sound.play()
                self.set_base_structure(2)

        screen.blit(cursor.cursor_menu(), (self._cursor_x - 50, self._cursor_y - 50))

    def mode_select(self, screen, event):
        screen.fill((0, 0, 0))
        try:
            font = pygame.font.Font("assets/HelpMe.ttf", 100)
        except Exception as e:
            print("Gagal load font HelpMe.ttf, pakai default font:", e)
            font = pygame.font.Font(None, 100)
        
        texts = ["Easy", "Medium", "Hard"]
        positions = [150, 300, 450]
        option_rects = []

        for text_label, y in zip(texts, positions):
            rendered = font.render(text_label, True, (255, 255, 255))
            rect = rendered.get_rect(center=(500, y))
            screen.blit(rendered, rect)
            option_rects.append((text_label.lower(), rect))

        if event and event.type == pygame.MOUSEMOTION:
            self.set_cursor_pos(*event.pos)

        if event and event.type == pygame.MOUSEBUTTONDOWN:
            for label, rect in option_rects:
                if rect.collidepoint(event.pos):
                    print(f"{label.capitalize()} mode selected")
                    if self._click_sound:
                        self._click_sound.play()
                    self.set_selected_mode(label)
                    self.set_base_structure(3)

        screen.blit(cursor.cursor_menu(), (self._cursor_x - 50, self._cursor_y - 50))

    def explore_mode(self, screen):
        # Load map dengan error handling
        map_img = load_image("assets/map1.png", (2000, 1200))

        # Load player dan cancer image dengan error handling
        player_img = load_image("assets/main_cursor.png", (50, 50))
        cancer_img = load_image("assets/player.png", (50, 50))

        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_w]:
            self._player_pos[1] -= speed
        if keys[pygame.K_s]:
            self._player_pos[1] += speed
        if keys[pygame.K_a]:
            self._player_pos[0] -= speed
        if keys[pygame.K_d]:
            self._player_pos[0] += speed

        map_rect = map_img.get_rect()

        player_width, player_height = 50, 50
        self._player_pos[0] = max(player_width//2, min(self._player_pos[0], map_rect.width - player_width//2))
        self._player_pos[1] = max(player_height//2, min(self._player_pos[1], map_rect.height - player_height//2))

        screen_width, screen_height = screen.get_size()
        self._camera[0] = self._player_pos[0] - screen_width // 2
        self._camera[1] = self._player_pos[1] - screen_height // 2

        self._camera[0] = max(0, min(self._camera[0], map_rect.width - screen_width))
        self._camera[1] = max(0, min(self._camera[1], map_rect.height - screen_height))

        screen.blit(map_img, (-self._camera[0], -self._camera[1]))

        # Tentukan jumlah kanker sesuai mode
        if self._selected_mode == "easy":
            sum_cancer = 5
        elif self._selected_mode == "medium":
            sum_cancer = 10
        elif self._selected_mode == "hard":
            sum_cancer = 15
        else:
            sum_cancer = 5  # default

        if not self._cancers:
            for _ in range(sum_cancer):
                x = random.randint(100, map_rect.width - 100)
                y = random.randint(100, map_rect.height - 100)
                self._cancers.append({'x': x, 'y': y, 'visible': False})

        # Tangani event secara lokal (ambil dari pygame.event.get())
        events = pygame.event.get()
        interact_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    interact_pressed = True

        for cancer in self._cancers[:]:
            distance = ((self._player_pos[0] - cancer['x'])**2 + (self._player_pos[1] - cancer['y'])**2) ** 0.5

            if distance < 100:
                cancer['visible'] = True
                screen.blit(cancer_img, (cancer['x'] - self._camera[0] - 25, cancer['y'] - self._camera[1] - 25))
                if distance < 20 and interact_pressed:
                    self.set_base_structure(4)  # Masuk battle
                    self._cancers.remove(cancer)
                    break
            else:
                cancer['visible'] = False

        player_draw_x = self._player_pos[0] - self._camera[0]
        player_draw_y = self._player_pos[1] - self._camera[1]
        screen.blit(player_img, (player_draw_x - 25, player_draw_y - 25))

        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Cancers remaining: {len(self._cancers)}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        if len(self._cancers) == 0:
            font = pygame.font.Font(None, 72)
            text_surface = font.render("VICTORY! All cancers defeated!", True, (255, 255, 255))
            screen.blit(text_surface, (100, 300))

    def battle_mode(self, screen, event):
        pygame.mouse.set_visible(True)

        # Pastikan player dan cancer sudah diinisialisasi
        if not self._player:
            try:
                self._player = base.Player("arthur")
            except Exception as e:
                print("Error ininisialisasi player:", e)
                return None
        if not self._cancer:
            try:
                self._cancer_type = random.choices(["normal_cancer", "high_cancer"], weights=[80, 20], k=1)[0]
                self._cancer = base.Cancer(self._cancer_type, 1)
            except Exception as e:
                print("Error ininisialisasi cancer:", e)
                return None

        # Load gambar background dengan error handling
        background = load_image("assets/battle_background.png")
        background_size_battle = pygame.transform.scale(background, (1000, 1000))
        screen.blit(background_size_battle, (0, -300))

        text_cancer = load_image("assets/cancer_stats_back.png", (300, 300))
        screen.blit(text_cancer, (700, 0))

        try:
            self._cancer.cancer_image(screen, self._cancer)
        except Exception as e:
            print("Error saat gambar kanker:", e)

        text_background = load_image("assets/text_background.png", (1000, 1000))
        screen.blit(text_background, (100, 0))

        try:
            base.Player.player_image(screen)
        except Exception as e:
            print("Error gambar player:", e)

        # Tampilkan stats player dan cancer dengan pengecekan
        try:
            lvl = self._player.get_level()
            hp_now = self._player.get_hp()
            hp_max = self._player.get_max_hp()
            text.font(f"level {lvl}", screen, 100, 560, 30)
            BarHp.bar_hp(screen, 0, 350, 200, 20, "red", "green", hp_now, hp_max)

            energy_now = self._player.get_energy()
            energy_max = self._player.get_max_energy()
            BarHp.bar_hp(screen, 0, 380, 200, 20, "red", "blue", energy_now, energy_max)

            name_cancer = self._cancer.get_name()
            text.font(name_cancer, screen, 800, 50, 30)
            hp_now_cancer = self._cancer.get_hp()
            hp_max_cancer = self._cancer.get_max_hp()
            text.font(f"HP : {hp_now_cancer}/{hp_max_cancer}", screen, 820, 170, 30)
            BarHp.bar_hp(screen, 700, 90, 200, 30, "red", "green", hp_now_cancer, hp_max_cancer)
        except Exception as e:
            print("Error saat tampilkan stats:", e)

        attack_rect = text.font("Attack", screen, 400, 465, 40)
        guard_rect = text.font("Guard", screen, 400, 540, 40)
        skill_rect = text.font("Skill", screen, 600, 465, 40)
        ultimate_rect = text.font("ultimate", screen, 650, 540, 40)

        if event and event.type == pygame.MOUSEMOTION:
            self.set_cursor_pos(*event.pos)

        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if attack_rect.collidepoint(event.pos):
                self._player.attack(self._cancer, screen)
                if not self._cancer.is_alive():
                    print("win")
                    self._player.level_up()
                    self._cancer = None
                    return 2

                text.font_animation("Cancer attack", screen, random.randrange(270, 600), random.randrange(100, 300), 60, "green", fade_in=False)
                self._cancer.attack(self._player, screen)
                if not self._player.is_alive():
                    print("game over")
                    return True

            if guard_rect.collidepoint(event.pos):
                self._player.guard()
                self._cancer.attack(self._player, screen)
                if not self._player.is_alive():
                    print("game over")
                    return True

            if skill_rect.collidepoint(event.pos):
                energy_empty = self._player.use_skill("basic_skill", self._cancer, screen)
                if energy_empty:
                    if not self._cancer.is_alive():
                        print("win")
                        self._player.level_up()
                        self._cancer = None
                        return 2

                    self._cancer.attack(self._player, screen)
                    if not self._player.is_alive():
                        print("game over")
                        return True

            if ultimate_rect.collidepoint(event.pos):
                energy_empty = self._player.use_skill("special_attack", self._cancer, screen)
                if energy_empty:
                    if not self._cancer.is_alive():
                        print("win")
                        self._player.level_up()
                        self._cancer = None
                        return 2

                    self._cancer.attack(self._player, screen)
                    if not self._player.is_alive():
                        print("game over")
                        return True

        return None


def main():
    game = CancerHunter()
    clock = pygame.time.Clock()

    while True:
        game.set_base_structure(1)

        done = False
        while not done:
            event = None
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                event = e

            if game.get_base_structure() == 1:
                game.menu(screen, event)
            elif game.get_base_structure() == 2:
                game.mode_select(screen, event)
            elif game.get_base_structure() == 3:
                game.explore_mode(screen)
            elif game.get_base_structure() == 4:
                condition = game.battle_mode(screen, event)
                if condition == True:
                    print("Game Over")
                    pygame.time.delay(2000)
                    done = True
                    game._player = None
                    game._cancer = None
                    game._cancers = []
                    game._camera = [0, 0]
                elif condition == 2:
                    game.set_base_structure(3)
                    game._cancer = None

            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    main()