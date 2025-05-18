import pygame
import random
import cursor
import base
import text
from health_bar import BarHp
from character.cancer import Cancer
from character.player import PlayerMain

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
# Inisialisasi pygame
pygame.init()

#menyembunyikan kursor mouse agar yang bergerak hanya gambar menu_cursor.png
pygame.mouse.set_visible(False)

# variabel global untuk log
battle_log = ""

# Posisi awal kursor,kursor awalnya diletakan di luar screen agar tidak terlihat
cursor_x = -40
cursor_y = +40

# Ukuran layar utama
screen = pygame.display.set_mode((1000, 600))

# Status game: 1=menu, 2=pilih mode, 3=explore, 4=battle
base_structure = 1

# Menyimpan mode yang dipilih (easy/medium/hard)
selected_mode = None

# Class utama untuk semua fitur game
class CancerHunter():
    #tempat kode menu start
    @staticmethod
    def menu(screen, event, cursor_x, cursor_y):
        #mengakses base_structure global
        global base_structure
        # Load background dan cursor
        menu_background = pygame.image.load("assets/menu_background.png").convert()
        # Tampilkan Background
        screen.blit(menu_background, (0, 0))
        # Tampilkan tombol START
        typing = "START"
        start_rect = text.font(typing,screen,500,200,200)
        
        # Update posisi kursor
        if event and event.type == pygame.MOUSEMOTION:
            cursor_x, cursor_y = event.pos

        # Deteksi klik pada tombol START
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                base_structure = 2  # Pindah ke menu pemilihan mode

        # Tampilkan kursor
        screen.blit(cursor.cursor_menu(), (cursor_x - 50, cursor_y - 50))
        return cursor_x, cursor_y

    @staticmethod
    def mode_select(screen, event):
        """Menampilkan menu pemilihan tingkat kesulitan"""
        global cursor_x, cursor_y, base_structure, selected_mode

        screen.fill((0, 0, 0))  # Bersihkan layar

        # Load cursor
        cursor.cursor_menu()
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
            cursor_x, cursor_y = event.pos

        # Deteksi klik dan simpan mode yang dipilih
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            for label, rect in option_rects:
                if rect.collidepoint(event.pos):
                    print(f"{label.capitalize()} mode selected")
                    selected_mode = label
                    base_structure = 3  # Masuk ke explore mode

        # Tampilkan kursor
        screen.blit(cursor.cursor_menu(), (cursor_x - 50, cursor_y - 50))
  
    @classmethod
    def explore_mode(cls):
        global base_structure, selected_mode,cancers
        

        # Load map
        map_img = pygame.image.load("assets/map1.png").convert()
        map_img = pygame.transform.scale(map_img, (2000, 1200))  # Ukuran map diperbesar
        map_rect = map_img.get_rect()

        # Load cursor / karakter
        player_img = pygame.image.load("assets/main_cursor.png")
        player_img = pygame.transform.scale(player_img, (50, 50))

        # Event
        keys = pygame.key.get_pressed()

        # Inisialisasi posisi karakter dan kamera
        if not hasattr(CancerHunter, 'player_pos'):
            CancerHunter.player_pos = [1000, 600]  # posisi di dunia besar
        if not hasattr(CancerHunter, 'camera'):
            CancerHunter.camera = [0, 0]

        # Update posisi karakter (dunia)
        speed = 5
        if keys[pygame.K_w]:
            CancerHunter.player_pos[1] -= speed
        if keys[pygame.K_s]:
            CancerHunter.player_pos[1] += speed
        if keys[pygame.K_a]:
            CancerHunter.player_pos[0] -= speed
        if keys[pygame.K_d]:
            CancerHunter.player_pos[0] += speed

        # Batasi dalam map dengan mempertimbangkan ukuran player
        player_width, player_height = 50, 50
        CancerHunter.player_pos[0] = max(player_width//2, min(CancerHunter.player_pos[0], map_rect.width - player_width//2))
        CancerHunter.player_pos[1] = max(player_height//2, min(CancerHunter.player_pos[1], map_rect.height - player_height//2))

        # Update kamera mengikuti karakter
        screen_width, screen_height = screen.get_size()
        CancerHunter.camera[0] = CancerHunter.player_pos[0] - screen_width // 2
        CancerHunter.camera[1] = CancerHunter.player_pos[1] - screen_height // 2

        # Pastikan kamera tidak keluar dari batas map
        CancerHunter.camera[0] = max(0, min(CancerHunter.camera[0], map_rect.width - screen_width))
        CancerHunter.camera[1] = max(0, min(CancerHunter.camera[1], map_rect.height - screen_height))

        # Blit map
        screen.blit(map_img, (-CancerHunter.camera[0], -CancerHunter.camera[1]))

        # Jumlah musuh berdasarkan mode
        if selected_mode == "easy":
            sum_cancer = 5
        elif selected_mode == "medium":
            sum_cancer = 10
        elif selected_mode == "hard":
            sum_cancer = 15

        # Inisialisasi kanker jika belum ada
        if not hasattr(CancerHunter, 'cancers'):
            CancerHunter.cancers = []
            for _ in range(sum_cancer):
                x = random.randint(100, map_rect.width - 100)
                y = random.randint(100, map_rect.height - 100)
                CancerHunter.cancers.append({'x': x, 'y': y, 'visible': False})

        # Event klik
        events = pygame.event.get()
        interact_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    interact_pressed = True
                elif event.key == pygame.K_RETURN:  # Tambah deteksi Enter key
                    interact_pressed = True

        # Proses kanker
        for cancer in CancerHunter.cancers[:]:
            distance = ((CancerHunter.player_pos[0] - cancer['x'])**2 +
                        (CancerHunter.player_pos[1] - cancer['y'])**2)**0.5

            if distance < 100:
                cancer['visible'] = True
                cancer_img = pygame.image.load("assets/player.png")
                cancer_img = pygame.transform.scale(cancer_img, (50, 50))
                # Gambar dengan kamera offset
                screen.blit(cancer_img, (cancer['x'] - CancerHunter.camera[0] - 25,
                                        cancer['y'] - CancerHunter.camera[1] - 25))
                if distance <20:
                    if interact_pressed:
                        base_structure = 4  # Masuk battle
                        CancerHunter.cancers.remove(cancer)
                        break
            else:
                cancer['visible'] = False

        # Gambar karakter di tengah layar
        player_draw_x = CancerHunter.player_pos[0] - CancerHunter.camera[0]
        player_draw_y = CancerHunter.player_pos[1] - CancerHunter.camera[1]
        screen.blit(player_img, (player_draw_x - 25, player_draw_y - 25))  # -25 agar titik tengah pas
        
        # Info sisa musuh
        font = pygame.font.Font(None, 36)
        text = font.render(f"Cancers remaining: {len(CancerHunter.cancers)}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        if len(CancerHunter.cancers) == 0:
            font = pygame.font.Font(None, 72)
            text = font.render("VICTORY! All cancers defeated!", True, (255, 255, 255))
            screen.blit(text, (100, 300))

    cancer_type = None
    @staticmethod
    def battle_mode():
        global cursor_x, cursor_y, base_structure, selected_mode
        pygame.mouse.set_visible(True)
        #membuat object player
    
        if not hasattr(CancerHunter, 'player'):
            CancerHunter.player = base.Player("arthur")
        if not hasattr(CancerHunter, 'cancer'):
            CancerHunter.cancer_type = random.choices(["normal_cancer","high_cancer"],weights=[80,20],k=1)[0]
            print(CancerHunter.cancer_type)
            CancerHunter.cancer = base.Cancer(CancerHunter.cancer_type, 1)

        player = CancerHunter.player
        cancer = CancerHunter.cancer
        #layout
        background = pygame.image.load("assets/battle_background.png")
        background_size_battle = pygame.transform.scale(background,(1000,1000))
        screen.blit(background_size_battle,(0,-300))

        text_cancer = pygame.image.load("assets/cancer_stats_back.png")
        text_cancer_size = pygame.transform.scale(text_cancer,(300,300))
        screen.blit(text_cancer_size,(700,0))


        base.Cancer.cancer_image(screen)


        text_background = pygame.image.load("assets/text_background.png")
        text_background_size = pygame.transform.scale(text_background,(1000,1000))
        screen.blit(text_background_size,(100,0))

        #player image
        base.Player.player_image(screen)

        #stats player
        ##stats hp
        hp_now = (player.get_hp())
        hp_max = (player.get_max_hp())
        #hp = text.font(f"HP : {hp_now}/{hp_max}",screen,400,450,20)
        BarHp.bar_hp(screen,0,350,200,20,"red","green",hp_now,hp_max)

        ##stats energy
        energy_now = (player.get_energy())
        energy_max = (player.get_max_energy())
        #hp = text.font(f"Energy : {energy_now}/{energy_max}",screen,800,450,20)
        BarHp.bar_hp(screen,0,380,200,20,"red","blue",energy_now,energy_max)
    
        #stats cancer
        ##stats hp
        name_cancer = (cancer.get_name())
        name = text.font(name_cancer,screen,800,50,30)
        hp_now_cancer = (cancer.get_hp())
        hp_max_cancer = (cancer.get_max_hp())
        hp = text.font(f"HP : {hp_now_cancer}/{hp_max_cancer}",screen,800,200,40)
        BarHp.bar_hp(screen,700,80,200,30,"red","green",hp_now_cancer,hp_max_cancer)


        #battle
        typing = "Attack"
        attack_cancer = text.font(typing,screen,400,550,50)

        typing = "Guard"
        guard_from_cancer = text.font(typing,screen,600,550,50)

        typing = "Skill"
        skill_cancer = text.font(typing,screen,800,550,50)

        if event and event.type == pygame.MOUSEMOTION:
            cursor_x, cursor_y = event.pos
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if attack_cancer.collidepoint(event.pos):
                player.attack(cancer,screen)
                cancer.attack(player)
                
                condition_player = player.is_alive()
                condition_cancer = cancer.is_alive()
                if condition_player != True :
                    print("game over")
                    return True
                if condition_cancer != True :
                    print("win")
                    return 2
                
                
            if guard_from_cancer.collidepoint(event.pos):
                print("guard")
            if skill_cancer.collidepoint(event.pos):
                print("skill")


        #screen.blit(cursor.cursor_menu(), (cursor_x - 50, cursor_y - 50))


# Loop utama game
clock = pygame.time.Clock()


while True :
    base_structure = 1  # kembali ke menu
    if hasattr(CancerHunter, 'player'):
        del CancerHunter.player
    if hasattr(CancerHunter, 'camera'):
        del CancerHunter.camera
    if hasattr(CancerHunter, 'cancers'):
        del CancerHunter.cancers
        del CancerHunter.cancer

    done = False
    while not done:
        event = None
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            event = e  # Simpan event terakhir

        # Struktur permainan
        if base_structure == 1:
            cursor_x, cursor_y = CancerHunter.menu(screen, event, cursor_x, cursor_y)
        elif base_structure == 2:
            CancerHunter.mode_select(screen, event)
        elif base_structure == 3:
            CancerHunter.explore_mode()
        elif base_structure == 4:
            condition = CancerHunter.battle_mode()
            if condition == True:  # player kalah
                print("Game Over")
                pygame.time.delay(2000)  # Delay 2 detik sebelum reset
                done = True
            if condition == 2:
                base_structure = 3
                if hasattr(CancerHunter, 'cancers'):
                    del CancerHunter.cancer
        # Update layar
        pygame.display.flip()
        clock.tick(30)
