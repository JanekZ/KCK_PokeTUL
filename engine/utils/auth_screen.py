import pygame
import sys

from database.utils.auth import Auth
from engine.utils.login_session import save_session

pygame.init()

FONT = pygame.font.SysFont("arial", 28)
SMALL_FONT = pygame.font.SysFont("arial", 22)

COLOR_INACTIVE = pygame.Color('gray')
COLOR_ACTIVE = pygame.Color(128, 35, 29)
COLOR_TEXT = pygame.Color('white')
COLOR_BG = pygame.Color(40, 40, 40)
COLOR_BUTTON = pygame.Color(128, 35, 29)
COLOR_BUTTON_HOVER = pygame.Color(107, 27, 22)
COLOR_ERROR = pygame.Color('red')

auth = Auth()

class InputBox:
    """A single input box with optional password masking."""

    def __init__(self, x: int, y: int, w: int, h: int, is_password: bool = False) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.txt_surface = FONT.render('', True, COLOR_TEXT)
        self.active = False
        self.is_password = is_password

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process events relevant to input (mouse clicks and key presses)."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                self.active = False
                self.color = COLOR_INACTIVE
            else:
                self.text += event.unicode

            display_text = '*' * len(self.text) if self.is_password else self.text
            self.txt_surface = FONT.render(display_text, True, COLOR_TEXT)

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Draw input box and its text."""
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 7))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        """Check if mouse is over the input box."""
        return self.rect.collidepoint(mouse_pos)

def draw_text(surface: pygame.surface.Surface, text: str, pos: tuple[int, int], font=FONT, color=COLOR_TEXT) -> None:
    """Render text on given surface at given position."""
    txt_surf = font.render(text, True, color)
    surface.blit(txt_surf, pos)

def draw_button(surface: pygame.surface.Surface, center_pos: tuple[int, int], text: str, mouse_pos: tuple[int, int]) -> tuple[bool, pygame.rect.Rect]:
    """Draw button with hover effect and return (hovered, rect)."""
    txt_surf = FONT.render(text, True, COLOR_TEXT)
    padding_x, padding_y = 20, 10
    rect = txt_surf.get_rect()
    rect.inflate_ip(padding_x * 2, padding_y * 2)
    rect.center = center_pos

    hovered = rect.collidepoint(mouse_pos)
    color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON

    pygame.draw.rect(surface, color, rect, border_radius=5)
    surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))

    return hovered, rect

def login_screen(display: pygame.surface.Surface, clock: pygame.time.Clock) -> str:
    """Main login screen loop, returns session_id on success."""
    screen_w, screen_h = display.get_size()
    center_x = screen_w // 2
    start_y = screen_h // 2 - 140

    username_box = InputBox(center_x - 150, start_y + 70, 300, 40)
    password_box = InputBox(center_x - 150, start_y + 140, 300, 40, is_password=True)

    error_message = ''
    current_cursor = pygame.SYSTEM_CURSOR_ARROW

    while True:
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

            username_box.handle_event(event)
            password_box.handle_event(event)

        display.fill(COLOR_BG)
        draw_text(display, "Zaloguj się", (center_x - 100, start_y), font=pygame.font.SysFont("arial", 36, bold=True))
        draw_text(display, "Indeks Gracza:", (username_box.rect.x, username_box.rect.y - 30), font=SMALL_FONT)
        draw_text(display, "Hasło:", (password_box.rect.x, password_box.rect.y - 30), font=SMALL_FONT)

        username_box.draw(display)
        password_box.draw(display)

        mouse_pos = pygame.mouse.get_pos()
        login_hover, login_rect = draw_button(display, (center_x, password_box.rect.y + 70), "Zaloguj się", mouse_pos)
        register_hover, register_rect = draw_button(display, (center_x, password_box.rect.y + 130), "Zarejestruj się", mouse_pos)

        if error_message:
            draw_text(display, error_message, (center_x - 150, register_rect.bottom + 15), font=SMALL_FONT, color=COLOR_ERROR)

        desired_cursor = pygame.SYSTEM_CURSOR_ARROW

        if username_box.is_hovered(mouse_pos) or password_box.is_hovered(mouse_pos):
            desired_cursor = pygame.SYSTEM_CURSOR_IBEAM
        elif login_hover or register_hover:
            desired_cursor = pygame.SYSTEM_CURSOR_HAND

        if current_cursor != desired_cursor:
            pygame.mouse.set_cursor(desired_cursor)
            current_cursor = desired_cursor

        if mouse_click:
            if login_hover:
                try:
                    player_id = int(username_box.text.strip())
                    password = password_box.text

                    success, result = auth.login(player_id, password)

                    if success:
                        save_session(result)
                        return result
                    else:
                        error_message = result
                except ValueError:
                    error_message = "Indeks jest niepoprawny"

            elif register_hover:
                if registration_screen(display, clock):
                    username_box.text = ''
                    username_box.txt_surface = FONT.render('', True, COLOR_TEXT)
                    password_box.text = ''
                    password_box.txt_surface = FONT.render('', True, COLOR_TEXT)
                    error_message = ''
                else:
                    error_message = ''

        pygame.display.flip()
        clock.tick(60)

def registration_screen(display: pygame.surface.Surface, clock: pygame.time.Clock) -> bool:
    """Registration screen loop, returns True on successful registration."""
    screen_w, screen_h = display.get_size()
    center_x = screen_w // 2
    start_y = screen_h // 2 - 180

    id_box = InputBox(center_x - 150, start_y + 70, 300, 40)
    name_box = InputBox(center_x - 150, start_y + 140, 300, 40)
    password_box = InputBox(center_x - 150, start_y + 210, 300, 40, is_password=True)

    error_message = ''
    current_cursor = pygame.SYSTEM_CURSOR_ARROW

    while True:
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

            id_box.handle_event(event)
            name_box.handle_event(event)
            password_box.handle_event(event)

        display.fill(COLOR_BG)
        draw_text(display, "Rejestracja", (center_x - 100, start_y), font=pygame.font.SysFont("arial", 36, bold=True))
        draw_text(display, "Indeks Gracza:", (id_box.rect.x, id_box.rect.y - 30), font=SMALL_FONT)
        draw_text(display, "Imię Gracza:", (name_box.rect.x, name_box.rect.y - 30), font=SMALL_FONT)
        draw_text(display, "Hasło:", (password_box.rect.x, password_box.rect.y - 30), font=SMALL_FONT)

        id_box.draw(display)
        name_box.draw(display)
        password_box.draw(display)

        mouse_pos = pygame.mouse.get_pos()
        register_hover, register_rect = draw_button(display, (center_x, password_box.rect.y + 70), "Zarejestruj", mouse_pos)
        back_hover, back_rect = draw_button(display, (center_x, password_box.rect.y + 130), "Powrót do logowania", mouse_pos)

        if error_message:
            draw_text(display, error_message, (center_x - 150, back_rect.bottom + 15), font=SMALL_FONT, color=COLOR_ERROR)

        desired_cursor = pygame.SYSTEM_CURSOR_ARROW

        if id_box.is_hovered(mouse_pos) or name_box.is_hovered(mouse_pos) or password_box.is_hovered(mouse_pos):
            desired_cursor = pygame.SYSTEM_CURSOR_IBEAM
        elif register_hover or back_hover:
            desired_cursor = pygame.SYSTEM_CURSOR_HAND

        if current_cursor != desired_cursor:
            pygame.mouse.set_cursor(desired_cursor)
            current_cursor = desired_cursor

        if mouse_click:
            if register_hover:
                try:
                    user_id = int(id_box.text.strip())
                    username = name_box.text.strip()

                    password = password_box.text

                    if not username or not password:
                        error_message = "Wypełnij wszystkie pola"
                    else:
                        success, message = auth.register(user_id, username, password)
                        if success:
                            return True
                        error_message = message
                except ValueError:
                    error_message = "ID użytkownika musi być liczbą"

            elif back_hover:
                return False

        pygame.display.flip()
        clock.tick(60)
