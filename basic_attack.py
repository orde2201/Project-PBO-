import pygame

def attack_animation(screen, fram, asset):
    fram = int(fram) if not isinstance(fram, int) else fram

    # Tentukan rect area animasi
    anim_rect = pygame.Rect(250, 0, 500, 450)

    # Simpan snapshot background di area animasi
    background_snapshot = screen.subsurface(anim_rect).copy()

    # Load semua frame animasi
    frames = []
    for i in range(1, fram):
        img = pygame.image.load(f"{asset}{i}.png")
        img = pygame.transform.scale(img, (500, 500))
        # Buat surface dengan alpha untuk transparansi
        frame_surface = pygame.Surface((600, 600), pygame.SRCALPHA)
        frame_surface.blit(img, (0, 0))
        frames.append(frame_surface)

    # Loop animasi
    for img in frames:
        # Kembalikan background di area animasi
        screen.blit(background_snapshot, anim_rect.topleft)

        # Gambar frame baru dengan transparansi
        screen.blit(img, anim_rect.topleft)

        # Update hanya area animasi
        pygame.display.update(anim_rect)

        # Delay antar frame
        pygame.time.delay(40)
    
    # Setelah animasi selesai, kembalikan background asli
    screen.blit(background_snapshot, anim_rect.topleft)
    pygame.display.update(anim_rect)
