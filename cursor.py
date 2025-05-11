import pygame
def cursor_menu():        
        menu_cursor_img = pygame.image.load("assets/main_cursor.png").convert_alpha()
        menu_cursor = pygame.transform.scale(menu_cursor_img, (100, 100))
        return menu_cursor
