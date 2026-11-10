import pygame

from Constants.constants import width, height, states
from txt_rect import txt_rect_center, txt_rect



title_font = pygame.font.SysFont("Arial", 60, True)
bttn = pygame.Rect(width // 2 - 200, height * 4 // 5, 400, height // 7)
info_rect = pygame.Rect(20, height // 15 + 80, width - 40, height - (height // 15 + 80) - (height - bttn.top) - 43)


WAIT_TIME = 5
start = None
count_font = pygame.font.SysFont("Arial", 20)


def handle(event, current_state: str):
    elapsed = (pygame.time.get_ticks() - start) / 1000
    if elapsed < WAIT_TIME:
        return None

    if current_state != "summary3":
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if bttn.collidepoint(event.pos):
                return states[states.index(current_state) + 1]

    if current_state == "summary3":
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if bttn.collidepoint(event.pos):
                return "quit"

    return None


def draw(screen, title_txt: str, info_txt: str, current_state: str):

    if current_state != "summary3":
        box_txt = "CONTINUE"
        box_colour = "green"
    else:
        box_txt = "QUIT"
        box_colour = "red"

    screen.fill("blue")
    txt = title_font.render(title_txt, True, "white")
    screen.blit(txt, ((width - txt.get_width()) // 2, height // 15))
    txt_rect(screen, info_txt, info_rect, 20, False)

    elapsed = (pygame.time.get_ticks() - start) / 1000
    left = WAIT_TIME - elapsed

    if left > 0:
        pygame.draw.rect(screen, "grey", bttn)
        pygame.draw.rect(screen, "black", bttn, 5)
        txt_rect_center(screen, box_txt, bttn, 20, True)

        count_txt = count_font.render(f" {int(left) + 1} seconds left", True, "white")
        x = bttn.centerx - count_txt.get_width() // 2
        y = bttn.top - count_txt.get_height() - 5
        screen.blit(count_txt, (x, y))
    else:
        pygame.draw.rect(screen, box_colour, bttn)
        pygame.draw.rect(screen, "black", bttn, 5)
        txt_rect_center(screen, box_txt, bttn, 20, True)
