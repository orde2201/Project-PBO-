import sys
import pygame
import random
import cursor
import base
import text
from health_bar import BarHp
import effect_animation

# Inisialisasi pygame
try:
    pygame.init()
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame or Mixer: {e}")
    sys.exit()

# Channel untuk musik
battle_bgm_channel = pygame.mixer.Channel(0)  # channel 0 khusus untuk musik battle
main_bgm_channel = pygame.mixer.Channel(1)    # channel 1 untuk musik utama

# Menyembunyikan kursor mouse
pygame.mouse.set_visible(False)

# Ukuran layar utama
screen = pygame.display.set_mode((1000, 600))

# Class utama untuk semua fitur game
class CancerHunter:
    def __init__(self):
        self._cursor_x = -40  
        self._cursor_y = 40   # Private attribute
        self._base_structure = 1  # 1=menu, 2=pilih mode, 3=explore, 4=battle
        self._selected_mode = None
        self._player = None
        self._cancer = None
        self._cancers = []
        self._camera = [0, 0]
        self._player_pos = [1000, 600]
        self._cancer_type = None
        self._current_bgm = None  # Untuk melacak musik yang sedang diputar
        
        # Sound effects
        try:
            self._click_sound = pygame.mixer.Sound("assets/sound/click-button-166324.mp3")
            self._backsound = pygame.mixer.Sound("assets/sound/horror-thriller-2-336734.mp3")
            self._battle_sound = pygame.mixer.Sound("assets/sound/battle-march-action-loop-6935.mp3")
        except pygame.error as e:
            print(f"Error loading sound files: {e}")
            sys.exit()
        
        # Mulai main BGM
        self._play_main_bgm()

    def _play_main_bgm(self):
        """Memutar musik utama (non-battle)"""
        if self._current_bgm != "main":
            main_bgm_channel.stop()
            battle_bgm_channel.stop()
            main_bgm_channel.play(self._backsound, loops=-1)
            self._current_bgm = "main"

    def _play_battle_bgm(self):
        """Memutar musik battle"""
        if self._current_bgm != "battle":
            main_bgm_channel.stop()
            battle_bgm_channel.stop()
            battle_bgm_channel.play(self._battle_sound, loops=-1)
            self._current_bgm = "battle"

    # Getter methods
    def get_cursor_pos(self):
        return (self._cursor_x, self._cursor_y)
    
    def get_base_structure(self):
        return self._base_structure
    
    def get_selected_mode(self):
        return self._selected_mode
    
    # Setter methods
    def set_base_structure(self, value):
        self._base_structure = value
    
    def set_cursor_pos(self, x, y):
        self._cursor_x = x
        self._cursor_y = y
    
    def set_selected_mode(self, mode):
        self._selected_mode = mode

    def menu(self, screen, event):
        self._play_main_bgm()
        """Handle menu screen"""
        try:
            # Load background
            menu_background = pygame.image.load("assets/menu_background.png").convert()
            screen.blit(menu_background, (0, 0))
        except pygame.error as e:
            print(f"Error loading menu background: {e}")
            return
        
        # Tampilkan tombol START
        typing = "START"
        start_rect = text.font(typing, screen, 500, 200, 200)
        
        # Update posisi kursor
        if event and event.type == pygame.MOUSEMOTION:
            self.set_cursor_pos(*event.pos)

        # Deteksi klik pada tombol START
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                self._click_sound.play()
                self.set_base_structure(2)  # Pindah ke menu pemilihan mode

        # Tampilkan kursor
        screen.blit(cursor.cursor_menu(), (self._cursor_x - 50, self._cursor_y - 50))

    def mode_select(self, screen, event):
        """Menampilkan menu pemilihan tingkat kesulitan"""
        screen.fill((0, 0, 0))  # Bersihkan layar

        # Daftar mode dan posisi tombol
        font = pygame.font.Font("assets/HelpMe.ttf", 100)
        texts = ["Easy", "Medium", "Hard"]
        positions = [150, 300, 450]
        option_rects = []

        # Tampilkan tombol masing-masing mode
        for text, y in zip(texts, positions):
            rendered = font.render(text, True, (255, 255, 255))
            rect = rendered.get_rect(center=(500, y))
            screen.blit(rendered, rect)
            option_rects.append((text.lower(), rect))  # lower agar konsisten

        # Update posisi kursor
        if event and event.type == pygame.MOUSEMOTION:
            self.set_cursor_pos(*event.pos)

        # Deteksi klik dan simpan mode yang dipilih
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            for label, rect in option_rects:
                if rect.collidepoint(event.pos):
                    print(f"{label.capitalize()} mode selected")
                    self.set_selected_mode(label)
                    self._click_sound.play()
                    self.set_base_structure(3)  # Masuk ke explore mode

        # Tampilkan kursor
        screen.blit(cursor.cursor_menu(), (self._cursor_x - 50, self._cursor_y - 50))

    def explore_mode(self, screen):
        """Handle exploration gameplay"""
        try:
            # Load map
            map_img = pygame.image.load("assets/map1.png").convert()
            map_img = pygame.transform.scale(map_img, (2000, 1200))
            map_rect = map_img.get_rect()
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            return
        
        # Load cursor / karakter
        try:
            player_img = pygame.image.load("assets/main_cursor.png")
            player_img = pygame.transform.scale(player_img, (50, 50))

            cancer_img = pygame.image.load("assets/player.png")
            cancer_img = pygame.transform.scale(cancer_img, (50, 50))
        except pygame.error as e:
            print(f"Error loading player or cancer images: {e}")
            return

        # Event
        keys = pygame.key.get_pressed()

        # Update posisi karakter (dunia)
        speed = 5
        if keys[pygame.K_w]:
            self._player_pos[1] -= speed
        if keys[pygame.K_s]:
            self._player_pos[1] += speed
        if keys[pygame.K_a]:
            self._player_pos[0] -= speed
        if keys[pygame.K_d]:
            self._player_pos[0] += speed

        # Batasi dalam map
        player_width, player_height = 50, 50
        self._player_pos[0] = max(player_width//2, min(self._player_pos[0], map_rect.width - player_width//2))
        self._player_pos[1] = max(player_height//2, min(self._player_pos[1], map_rect.height - player_height//2))

        # Update kamera mengikuti karakter
        screen_width, screen_height = screen.get_size()
        self._camera[0] = self._player_pos[0] - screen_width // 2
        self._camera[1] = self._player_pos[1] - screen_height // 2

        # Pastikan kamera tidak keluar dari batas map
        self._camera[0] = max(0, min(self._camera[0], map_rect.width - screen_width))
        self._camera[1] = max(0, min(self._camera[1], map_rect.height - screen_height))

        # Blit map
        screen.blit(map_img, (-self._camera[0], -self._camera[1]))
        sum_cancer = 20
        # Jumlah musuh berdasarkan mode
        if self._selected_mode == "easy":
            self._cancer_type = "new_cancer"
        elif self._selected_mode == "medium":
            self._cancer_type = "normal_cancer"
        elif self._selected_mode == "hard":
            self._cancer_type = "high_cancer"
        
        # Inisialisasi kanker jika belum ada
        if not self._cancers:
            for _ in range(sum_cancer):
                x = random.randint(100, map_rect.width - 100)
                y = random.randint(100, map_rect.height - 100)
                self._cancers.append({'x': x, 'y': y, 'visible': False})

        # Event klik
        events = pygame.event.get()
        interact_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    interact_pressed = True

        # Proses kanker
        for cancer in self._cancers[:]:
            distance = ((self._player_pos[0] - cancer['x'])**2 +
                       (self._player_pos[1] - cancer['y'])**2)**0.5

            if distance < 100:
                cancer['visible'] = True
                screen.blit(cancer_img, (cancer['x'] - self._camera[0] - 25,
                                       cancer['y'] - self._camera[1] - 25))
                if distance < 20 and interact_pressed:
                    self.set_base_structure(4)  # Masuk battle
                    self._cancers.remove(cancer)
                    break
            else:
                cancer['visible'] = False

        # Gambar karakter di tengah layar
        player_draw_x = self._player_pos[0] - self._camera[0]
        player_draw_y = self._player_pos[1] - self._camera[1]
        screen.blit(player_img, (player_draw_x - 25, player_draw_y - 25))

        # Info sisa musuh
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Cancers remaining: {len(self._cancers)}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        if len(self._cancers) == 0:
            font = pygame.font.Font("assets/HelpMe.ttf", 72)
            text_surface = font.render("VICTORY! All cancers defeated!", True, (255, 255, 255))
            screen.blit(text_surface, (100, 300))
            pygame.display.flip()  # Tampilkan pesan sebelum delay
            pygame.time.delay(4000)  # Tunggu 4 detik
            return True
            
    def battle_mode(self, screen, event):
        self._play_battle_bgm()
        """Handle battle gameplay"""
        pygame.mouse.set_visible(True)
        
        # Initialize player and cancer if not exists
        if not self._player:
            self._player = base.Player("hunter")
        if not self._cancer:
            self._cancer = base.Cancer(self._cancer_type, 1)

        # Layout
        try:
            background = pygame.image.load("assets/battle_background.png")
            background_size_battle = pygame.transform.scale(background, (1000, 1000))
            screen.blit(background_size_battle, (0, -300))

            text_cancer = pygame.image.load("assets/cancer_stats_back.png")
            text_cancer_size = pygame.transform.scale(text_cancer, (300, 300))
            screen.blit(text_cancer_size, (700, 0))

            self._cancer.cancer_image(screen, self._cancer)

            text_background = pygame.image.load("assets/text_background.png")
            text_background_size = pygame.transform.scale(text_background, (1000, 1000))
            screen.blit(text_background_size, (100, 0))

            # Player image
            base.Player.player_image(screen)
        except pygame.error as e:
            print(f"Error loading battle images: {e}")
            return

        # Stats player
        lvl = self._player.get_level()
        hp_now = self._player.get_hp()
        hp_max = self._player.get_max_hp()
        text.font(f"level {lvl}", screen, 100, 560, 30)
        BarHp.bar_hp(screen, 0, 350, 200, 20, "red", "green", hp_now, hp_max)

        energy_now = self._player.get_energy()
        energy_max = self._player.get_max_energy()
        BarHp.bar_hp(screen, 0, 380, 200, 20, "red", "blue", energy_now, energy_max)
    
        # Stats cancer
        name_cancer = self._cancer.get_name()
        text.font(name_cancer, screen, 800, 50, 30)
        hp_now_cancer = self._cancer.get_hp()
        hp_max_cancer = self._cancer.get_max_hp()
        text.font(f"HP : {hp_now_cancer}/{hp_max_cancer}", screen, 820, 170, 30)
        BarHp.bar_hp(screen, 700, 90, 200, 30, "red", "green", hp_now_cancer, hp_max_cancer)

        # Battle options
        attack_rect = text.font("Attack", screen, 400, 465, 40)
        guard_rect = text.font("Guard", screen, 400, 540, 40)
        skill_rect = text.font("Skill", screen, 600, 465, 40)
        ultimate_rect = text.font("ultimate", screen, 650, 540, 40)
        buff_rect = text.font("Buff", screen, 750, 465, 40)

        if event and event.type == pygame.MOUSEMOTION:
            self.set_cursor_pos(*event.pos)
            
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            # Basic attack
            if attack_rect.collidepoint(event.pos):
                base.attack(self._cancer,self._player, screen)
                if not self._cancer.is_alive():
                    print("win")
                    self._player.level_up()
                    # Reset cancer for next battle
                    self._cancer = None
                    return 2
                
                text.font_animation("Cancer attack", screen, random.randrange(270, 600), 
                                  random.randrange(100, 300), 60, "green", fade_in=False)
                base.attack(self._player,self._cancer, screen)
                if not self._player.is_alive():
                    print("game over")
                    return True
            
            # Guard
            if guard_rect.collidepoint(event.pos):
                self._player.guard()
                self._cancer.attack(self._player, screen)
                if not self._player.is_alive():
                    print("game over")
                    return True

            # Skill
            if skill_rect.collidepoint(event.pos):
                energy_empty = self._player.use_skill("basic_skill", self._cancer, screen)
                if energy_empty:
                    if not self._cancer.is_alive():
                        print("win")
                        self._player.level_up()
                        # Reset cancer for next battle
                        self._cancer = None
                        return 2
                    
                    self._cancer.attack(self._player, screen)
                    if not self._player.is_alive():
                        print("game over")
                        return True
            
            # Ultimate
            if ultimate_rect.collidepoint(event.pos):
                energy_empty = self._player.use_skill("special_attack", self._cancer, screen)
                if energy_empty:
                    if not self._cancer.is_alive():
                        print("win")
                        self._player.level_up()
                        # Reset cancer for next battle
                        self._cancer = None
                        return 2
                    
                    self._cancer.attack(self._player, screen)
                    if not self._player.is_alive():
                        print("game over")
                        return True
            # Buff
            if buff_rect.collidepoint(event.pos):
                buff_status = self._player.use_crit_buff(screen)
                if buff_status:
                    base.attack(self._player, self._cancer, screen)
                    if not self._player.is_alive():
                        print("game over")
                        return True
        return None


# Main game loop
def main():
    game = CancerHunter()
    clock = pygame.time.Clock()
    
    while True:
        try:
            # Reset game state
            game.set_base_structure(1)
            done = False
            while not done:
                event = None
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    event = e  # Simpan event terakhir
                # Game structure
                if game.get_base_structure() == 1:
                    game.menu(screen, event)
                elif game.get_base_structure() == 2:
                    game.mode_select(screen, event)
                elif game.get_base_structure() == 3:
                    explore_status = game.explore_mode(screen)
                    if explore_status:
                        game.set_base_structure(1)
                elif game.get_base_structure() == 4:
                    condition = game.battle_mode(screen, event)
                    if condition == True:  # player kalah
                        # Tampilkan gambar game over selama 7 detik
                        game_over_img = pygame.image.load("assets/game_over_vignet.png").convert()
                        game_over_img = pygame.transform.scale(game_over_img, (1000, 600))
                        
                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 7000:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            screen.blit(game_over_img, (0, 0))
                            pygame.display.flip()
                            clock.tick(30)

                        # Reset ke menu
                        game.set_base_structure(1)
                        game._player = None
                        game._cancer = None
                        game._cancers = []
                        game._camera = [0, 0]
                    elif condition == 2:  # player menang
                        game.set_base_structure(3)
                        # Reset cancer stats for next battle
                        game._cancer = None
                # Update display
                pygame.display.flip()
                clock.tick(30)
        except Exception as e:
            print(f"An error occurred: {e}")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
