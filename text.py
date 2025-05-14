import pygame
#modul untuk font
def font(text,screen,x,y,size):  
    start_font = pygame.font.Font("assets/HelpMe.ttf", size)
    start_text = start_font.render(text, True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(x, y))
    screen.blit(start_text, start_rect)
    return start_rect
    