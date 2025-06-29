import pygame
import sys
import math

from engine.utils.fix_path import fix_path

pygame.init()

def splash_screen(display: pygame.surface.Surface, path: str, duration: float = 0.5) -> None:
    logo = pygame.image.load(fix_path(path)).convert_alpha()
    original_rect = logo.get_rect()

    screen_w, screen_h = display.get_size()

    start_width = int(screen_w * 0.25)
    scale_factor = start_width / original_rect.width
    start_height = int(original_rect.height * scale_factor)

    target_width = int(start_width * 2)
    target_height = int(start_height * 2)

    overshoot_scale = 1.15
    bounce_duration = 0.35
    total_duration = duration + bounce_duration

    start_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000.0

        if elapsed_time > total_duration:
            break

        if elapsed_time <= duration:
            progress = elapsed_time / duration
            ease_progress = progress ** 2  # ease-in
        else:
            bounce_phase = (elapsed_time - duration) / bounce_duration
            ease_progress = 1 + (overshoot_scale - 1) * math.sin(math.pi * (1 - bounce_phase)) * (1 - bounce_phase)

        current_width = int(start_width + (target_width - start_width) * ease_progress)
        current_height = int(start_height + (target_height - start_height) * ease_progress)

        scaled_logo = pygame.transform.smoothscale(logo, (current_width, current_height))
        centered_rect = scaled_logo.get_rect(center=(screen_w // 2, screen_h // 2))

        display.fill((0, 0, 0))
        display.blit(scaled_logo, centered_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)

    pygame.time.delay(300)
