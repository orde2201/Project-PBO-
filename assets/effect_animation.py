import pygame
import sys

def effect_animation(screen, image_path, speed=5, delay=40):
    """
    Menampilkan gambar yang perlahan memudar (fade out)
    
    Parameters:
        screen (pygame.Surface): Layar target
        image_path (str): Path ke file gambar
        speed (int): Kecepatan fade (1-255)
        delay (int): Delay antar frame (ms)
    """
    # Load dan scale gambar
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, screen.get_size())
    
    # Simpan background awal
    background = screen.copy()
    
    # Nilai alpha awal (penuh)
    alpha = 255

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Kembalikan background tanpa gambar
        screen.blit(background, (0, 0))
        
        # Atur transparansi gambar
        image.set_alpha(alpha)
        screen.blit(image, (0, 0))
        
        pygame.display.flip()

        # Kurangi alpha untuk fade out
        alpha = max(0, alpha - speed)  # Pastikan tidak kurang dari 0

        # Berhenti ketika gambar sepenuhnya transparan
        if alpha <= 0:
            running = False

        clock.tick(delay)
        
import time

def blinking():
    # Inisialisasi Pygame
    pygame.init()

    # Set ukuran layar
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Gambar Berkedip 2 Kali")

    # Warna
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Muat gambar
    try:
        image = pygame.image.load("assets/normal_cancer.png")  # Ganti dengan path gambar Anda
        image = pygame.transform.scale(image, (200, 200))  # Sesuaikan ukuran jika perlu
    except:
        # Jika gambar tidak ditemukan, buat gambar placeholder
        image = pygame.Surface((200, 200))
       # image.fill((255, 0, 0))  # Kotak merah sebagai placeholder
        font = pygame.font.SysFont(None, 36)
        text = font.render("Gambar", True, WHITE)
        image.blit(text, (50, 80))

    # Posisi gambar
    image_rect = image.get_rect(center=(width//2, height//2))

    # Variabel untuk kedipan
    blink_count = 0
    max_blinks = 2  # Jumlah kedipan maksimal
    blink_interval = 100  # Waktu kedip dalam milidetik (500ms = 0.5 detik)
    last_blink_time = pygame.time.get_ticks()
    show_image = True

    # Clock untuk mengatur FPS
    clock = pygame.time.Clock()

    # Loop utama
    running = True
    while running and blink_count < max_blinks * 2:
        # Tangani event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update kedipan
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_interval:
            show_image = not show_image
            last_blink_time = current_time
            blink_count += 1
        
        # Gambar latar belakang
        screen.fill(BLACK)
        
        # Gambar gambar jika show_image True
        if show_image:
            screen.blit(image, image_rect)
        
        # Update layar
        pygame.display.flip()
        
        # Batasi FPS
        clock.tick(60)

    # Tampilkan gambar terakhir (jika berhenti dalam keadaan tidak terlihat)
    if not show_image and blink_count >= max_blinks * 2:
        
        screen.blit(image, image_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # Tampilkan selama 1 detik sebelum keluar

    # Tunggu sebentar sebelum keluar
    pygame.time.delay(1000)
    

 # Panggil fungsi blinking untuk menjalankan animasi