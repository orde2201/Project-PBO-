import pygame

#modul untuk buat animasi per frame
def attack_animation(screen):
    frame = []
    for i in range(1,7):
        img = pygame.image.load(f"assets/slash_basic/warrior_skill4_frame{i}.png")
        img_size = pygame.transform.scale(img,(600,600))
        frame.append(img_size)
    for img in frame:
        screen.blit(img, (230, -30))
        pygame.display.flip()
        pygame.time.delay(50)