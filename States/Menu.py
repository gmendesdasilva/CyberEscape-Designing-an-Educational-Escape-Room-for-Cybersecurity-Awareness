from Constants.constants import *
from txt_rect import txt_rect_center, txt_rect

start_bttn = pygame.Rect((width // 2) - 400, height * 4 // 5 - 250, 350, 250)
quit_bttn = pygame.Rect(width // 2 + 50, height * 4 // 5 - 250, 350, 250)
intro_txt = ("You will face three real-world cybersecurity scenarios:\n\n"
            "Checkpoint 1: Identify phishing emails in your inbox\n\n"
            "Checkpoint 2: Discover why personal passwords are dangerous\n\n"
            "Checkpoint 3: Navigate safely on a public Wi-Fi network")

title_font = pygame.font.SysFont("Arial", 60, True)
info_rect = pygame.Rect(20, height // 7, width - 40, 400)

footer_font = pygame.font.SysFont("Arial", 25, True)
footer_txt = footer_font.render("Guilherme Mendes da Silva - University of Luxembourg", True, "white")


def draw(screen):
    screen.fill("blue")
    pygame.draw.rect(screen, "green", start_bttn)
    pygame.draw.rect(screen, "black", start_bttn, 5)
    txt_rect_center(screen, "Start", start_bttn, 20, True)

    pygame.draw.rect(screen, "red", quit_bttn)
    pygame.draw.rect(screen, "black", quit_bttn, 5)
    txt_rect_center(screen, "Quit", quit_bttn, 20, True)

    txt = title_font.render("CyberEscape", True, "white")
    screen.blit(txt, ((width - txt.get_width()) // 2, height // 15))
    txt_rect(screen, intro_txt, info_rect, 20, False)

    screen.blit(footer_txt, (width - footer_txt.get_width() - 20, height - footer_txt.get_height() - 5))


def handle(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if start_bttn.collidepoint(event.pos):
             return "puzzle1_intro"
        elif quit_bttn.collidepoint(event.pos):
            return "quit"
    return None
