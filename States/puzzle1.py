import random
import pygame

from Constants.constants import width, height, EMAIL_DATA_POOL
from txt_rect import txt_rect, txt_rect_center

PADDING = 10
PREVIEW_WIDTH = width // 3
PREVIEW_HEIGHT = (height - PADDING * 6) // 5


EMAIL_FULL = pygame.Rect(
    PREVIEW_WIDTH + PADDING * 2, PADDING,
    width - PREVIEW_WIDTH - PADDING * 3, height - PADDING * 2
)

BUTTON_HEIGHT = 80
BUTTON_WIDTH = (EMAIL_FULL.width - PADDING * 3) // 2

phishing_bttn = pygame.Rect(EMAIL_FULL.left + PADDING, EMAIL_FULL.bottom - BUTTON_HEIGHT - PADDING,
                            BUTTON_WIDTH - PADDING, BUTTON_HEIGHT
)

safe_bttn = pygame.Rect(
    phishing_bttn.right + PADDING, phishing_bttn.top,
    BUTTON_WIDTH, BUTTON_HEIGHT
)

HEADER_RECT = pygame.Rect(
    EMAIL_FULL.left + PADDING, EMAIL_FULL.top + PADDING,
    EMAIL_FULL.width - PADDING * 2, height // 6
)

BODY_RECT = pygame.Rect(
    EMAIL_FULL.left + PADDING, HEADER_RECT.bottom + PADDING,
    EMAIL_FULL.width - PADDING * 2, phishing_bttn.top - HEADER_RECT.bottom - PADDING
)



class Email:
    def __init__(self, sender, recipient, title, txt, phishing, rect ):
        self.sender = sender
        self.recipient = recipient
        self.title = title
        self.txt = txt

        self.phishing = phishing
        self.flagged = None
        self.rect = rect





    def display_preview(self, screen, selected=False):
        pygame.draw.rect(screen, "blue", self.rect)

        if selected:
            border_color = "yellow"
        else:
            border_color = "black"

        pygame.draw.rect(screen, border_color, self.rect, 5)

        txt_rect(screen, f"{self.sender}\n\n{self.title}", self.rect, 5, True)


    def display_full(self, screen):
        header_text = (
            f"From: {self.sender}\n"
            f"To: {self.recipient}\n"
            f"Subject: {self.title}\n"
        )

        txt_rect(screen, header_text, HEADER_RECT, 10, True, "black")
        txt_rect(screen, self.txt, BODY_RECT, 10, False, "black")


    def handle_preview(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)

        return False


emails = []
selected_email = None


def setup():
    global emails, selected_email
    emails = []

    legit_pool = [e for e in EMAIL_DATA_POOL if not e["phishing"]]
    phishing_emails = [e for e in EMAIL_DATA_POOL if e["phishing"]]

    chosen_legit = random.sample(legit_pool, 3)
    round_data = chosen_legit + phishing_emails
    random.shuffle(round_data)

    for i, data in enumerate(round_data):
        rect = pygame.Rect(
            PADDING, PADDING + i * (PREVIEW_HEIGHT + PADDING),
            PREVIEW_WIDTH - PADDING * 2, PREVIEW_HEIGHT
        )

        emails.append(Email(
            data["sender"], data["recipient"],
            data["title"], data["txt"], data["phishing"],
            rect
        ))

    selected_email = emails[0]

def handle(event):
    global selected_email

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for email in emails:
            if email.handle_preview(event):
                selected_email = email
                return None
        if phishing_bttn.collidepoint(event.pos):
            selected_email.flagged = True
        elif safe_bttn.collidepoint(event.pos):
            selected_email.flagged = False

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        for email in emails:
            if email.flagged != email.phishing:
                return "retry"

        return "continue"

    return None


def draw(screen):
    for email in emails:
        email.display_preview(screen, selected= email is selected_email)

    pygame.draw.rect(screen, "white", EMAIL_FULL)
    pygame.draw.rect(screen, "black", EMAIL_FULL, 3)
    selected_email.display_full(screen)

    if selected_email.flagged is True:
        pygame.draw.rect(screen, "red", phishing_bttn)
        pygame.draw.rect(screen, "gold", phishing_bttn, 3)
        txt_rect_center(screen, "PHISHING", phishing_bttn, 10, True, "black")

        pygame.draw.rect(screen, "green", safe_bttn)
        pygame.draw.rect(screen, "black", safe_bttn, 3)
        txt_rect_center(screen, "SAFE", safe_bttn, 10, True, "black")

    elif selected_email.flagged is False:
        pygame.draw.rect(screen, "red", phishing_bttn)
        pygame.draw.rect(screen, "black", phishing_bttn, 3)
        txt_rect_center(screen, "PHISHING", phishing_bttn, 10, True, "black")

        pygame.draw.rect(screen, "green", safe_bttn)
        pygame.draw.rect(screen, "gold", safe_bttn, 3)
        txt_rect_center(screen, "SAFE", safe_bttn, 10, True, "black")

    elif selected_email.flagged is None:
        pygame.draw.rect(screen, "red", phishing_bttn)
        pygame.draw.rect(screen, "black", phishing_bttn, 3)
        txt_rect_center(screen, "PHISHING", phishing_bttn, 10, True, "black")

        pygame.draw.rect(screen, "green", safe_bttn)
        pygame.draw.rect(screen, "black", safe_bttn, 3)
        txt_rect_center(screen, "SAFE", safe_bttn, 10, True, "black")