import pygame
import random
from character import player

# Inisialisasi pygame
pygame.init()

#menyembunyikan kursor mouse agar yang bergerak hanya gambar menu_cursor.png
pygame.mouse.set_visible(False)

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
        """Menampilkan menu utama dengan tombol START"""
        #mengakses base_structure global
        global base_structure

        # Load background dan cursor
        menu_background = pygame.image.load("assets/menu_background.png")
        menu_cursor_img = pygame.image.load("assets/main_cursor.png")
        menu_cursor = pygame.transform.scale(menu_cursor_img, (100, 100))

        # Tampilkan Background
        screen.blit(menu_background, (0, 0))

        # Tampilkan tombol START
        start_font = pygame.font.Font(None, 200)
        start_text = start_font.render("START", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(490, 200))
        screen.blit(start_text, start_rect)
        
        # Update posisi kursor
        if event and event.type == pygame.MOUSEMOTION:
            cursor_x, cursor_y = event.pos

        # Deteksi klik pada tombol START
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                base_structure = 2  # Pindah ke menu pemilihan mode

        # Tampilkan kursor
        screen.blit(menu_cursor, (cursor_x - 50, cursor_y - 50))
        return cursor_x, cursor_y

    @staticmethod
    def mode_select(screen, event):
        """Menampilkan menu pemilihan tingkat kesulitan"""
        global cursor_x, cursor_y, base_structure, selected_mode

        screen.fill((0, 0, 0))  # Bersihkan layar

        # Load cursor
        menu_cursor_img = pygame.image.load("assets/main_cursor.png")
        menu_cursor = pygame.transform.scale(menu_cursor_img, (100, 100))

        # Daftar mode dan posisi tombol
        font = pygame.font.Font(None, 150)
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
        screen.blit(menu_cursor, (cursor_x - 50, cursor_y - 50))

    @staticmethod
    def explore_mode():
        """Menampilkan map dan menyiapkan jumlah cancer sesuai mode"""
        global selected_mode

        # Tampilkan map
        map_img = pygame.image.load("assets/map1.png")
        size_map = pygame.transform.scale(map_img, (1000, 600))
        screen.blit(size_map, (0, 0))

        # Jumlah musuh berdasarkan mode
        if selected_mode == "easy":
            sum_cancer = 5
        elif selected_mode == "medium":
            sum_cancer = 10
        elif selected_mode == "hard":
            sum_cancer = 15

        # Cetak jumlah untuk debugging
        print(f"Explore Mode: {selected_mode}, cancer count: {sum_cancer}")

    @staticmethod
    def battle_mode():
        """Mode pertarungan (belum diimplementasikan)"""
        pass


# Ambil objek player dari modul karakter
player_main = player.player_main

# Loop utama game
done = False
clock = pygame.time.Clock()

while not done:
    event = None
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        event = e  # Simpan event terakhir (untuk mouse click/move)

    # Gerakan player berdasarkan input keyboard
    

    # Cek status game dan panggil fungsi sesuai struktur
    if base_structure == 1:
        cursor_x, cursor_y = CancerHunter.menu(screen, event, cursor_x, cursor_y)
    elif base_structure == 2:
        CancerHunter.mode_select(screen, event)
    elif base_structure == 3:
        CancerHunter.explore_mode()
    elif base_structure == 4:
        CancerHunter.battle_mode()

    # Tampilkan player di layar

    # Update tampilan layar
    pygame.display.flip()
    clock.tick(60)  # Batasi ke 60 FPS
