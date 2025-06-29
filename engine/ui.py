import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

MINIMAP_WIDTH = 200
MINIMAP_HEIGHT = 200

MENU_WIDTH = 150
MENU_HEIGHT = 100

def draw_menu(surface, visible=True):
    if not visible:
        return
    menu_rect = pygame.Rect(surface.get_width() - MENU_WIDTH - 10, 10, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(surface, BLACK, menu_rect)
    pygame.draw.rect(surface, WHITE, menu_rect, 2)

    font = pygame.font.SysFont("Arial", 16)
    text1 = font.render("[M] Menu", True, WHITE)
    text2 = font.render("[ESC] Exit", True, WHITE)
    surface.blit(text1, (menu_rect.x + 10, menu_rect.y + 10))
    surface.blit(text2, (menu_rect.x + 10, menu_rect.y + 40))

def draw_ui(surface, player_pos, show_menu=False):
    draw_menu(surface, visible=show_menu)
