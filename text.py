import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Font Fade In-Out Example")
clock = pygame.time.Clock()

# --- METHOD FONT MILIKMU, TIDAK DIUBAH ---
def font(text, screen, x, y, size):  
    start_font = pygame.font.Font("assets/HelpMe.ttf", size)
    start_text = start_font.render(text, True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(x, y))
    screen.blit(start_text, start_rect)
    return start_rect

# --- FONT ANIMATION DENGAN FADING ---
def font_animation(text, screen, x, y, size,color, fade_in=True, speed=5, delay=40):
    temp_font = pygame.font.Font("assets/HelpMe.ttf", size)
    
    # Create a surface with per-pixel alpha
    text_surface = temp_font.render(text, True, color).convert_alpha()
    text_rect = text_surface.get_rect(center=(x, y))
    
    # Create a copy of the current screen content behind the text
    background = screen.copy()
    
    alpha = 0 if fade_in else 255
    direction = 1 if fade_in else -1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Restore the background without the text
        screen.blit(background, (0, 0))
        
        # Apply current alpha to text
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()

        alpha += speed * direction
        alpha = max(0, min(255, alpha))

        if (fade_in and alpha >= 255) or (not fade_in and alpha <= 0):
            running = False

        clock.tick(delay)
