import pygame
import random

from Constants.constants import width, height, STRONG_OPTIONS, PASSWORD_POOL, SARAH_BIO, SARAH_NAME, SARAH_HANDLE
from txt_rect import txt_rect, txt_rect_center

PADDING = 10

PROFILE_WIDTH = width // 3 -  2 * PADDING
PROFILE_HEIGHT = height - 2 * PADDING

# Left panel: Sarah's profile
PROFILE_PANEL = pygame.Rect(
    PADDING, PADDING,
    PROFILE_WIDTH, PROFILE_HEIGHT
)


# Right panel: puzzle content
RIGHT_PANEL = pygame.Rect(
    width // 3 + PADDING, PADDING,
    width - (width // 3) - PADDING, height - PADDING
)

# Avatar circle position and radius (top-left of right panel)
AVATAR_R  = 45
AVATAR_CX = 2 * PADDING + AVATAR_R + 25
AVATAR_CY = 2 * PADDING + AVATAR_R + 25

NAME_HANDLE_rect = pygame.Rect(
    PADDING, AVATAR_CY + AVATAR_R + 2 * PADDING,
    PROFILE_WIDTH, 125
)

# Bio area sits below the avatar
BIO_RECT = pygame.Rect(
    PADDING, NAME_HANDLE_rect.bottom + PADDING,
    PROFILE_PANEL.width - PADDING, height - PADDING - NAME_HANDLE_rect.height - AVATAR_CY - 2 * AVATAR_R
)

font_av = pygame.font.SysFont("Arial", 36, bold=True)
initial = font_av.render("S", True, (30, 80, 160))

title_A = "PART 1: Guess Sarah's Password"
instr_A = "Which of these is she most likely using?"

title_B = "PART 2: Pick the Strong Password"
instr_B = "Now help Sarah choose a password an attacker cannot guess."


def pick_part_a():
    personal     = [p for p in PASSWORD_POOL if p["personal"]]
    non_personal = [p for p in PASSWORD_POOL if not p["personal"]]
    chosen = random.sample(personal, 3) + random.sample(non_personal, 3)
    random.shuffle(chosen)
    return chosen


def pick_part_b():
    strong = [p for p in STRONG_OPTIONS if p["strong"]]
    weak   = [p for p in STRONG_OPTIONS if not p["strong"]]
    chosen = random.sample(strong, 1) + random.sample(weak, 3)
    random.shuffle(chosen)
    return chosen

instr_rect = pygame.Rect(
    RIGHT_PANEL.left + PADDING, PADDING,
    RIGHT_PANEL.width - 2 * PADDING, height // 4 - 2 * PADDING
)

FEEDBACK_RECT = pygame.Rect(
    RIGHT_PANEL.left + PADDING, height // 4,
    RIGHT_PANEL.width - 2 * PADDING, height // 4 - PADDING
)

CONTINUE_BUTTON_HEIGHT = 80
BUTTON_WIDTH = RIGHT_PANEL.width - 2 * PADDING
CONTINUE_BUTTON = pygame.Rect(
    RIGHT_PANEL.left + PADDING, height - CONTINUE_BUTTON_HEIGHT - PADDING,
    BUTTON_WIDTH, CONTINUE_BUTTON_HEIGHT
)

bttn_start = height // 2 + PADDING
bbtn_end = CONTINUE_BUTTON.top - PADDING
bttn_height = bbtn_end - bttn_start


BUTTON_HEIGHT_A = (bttn_height - PADDING * 5) //  6
BUTTON_HEIGHT_B = (bttn_height - PADDING * 3) // 4


def make_option_rects(phase):

    rects = []
    start_y = 0

    if phase == "A":
        for i in range(6):
            rects.append(pygame.Rect(
                RIGHT_PANEL.left + PADDING, height // 2 + PADDING + start_y * (BUTTON_HEIGHT_A + PADDING),
                BUTTON_WIDTH, BUTTON_HEIGHT_A
            ))

            start_y += 1

    else:
        for i in range(4):
            rects.append(pygame.Rect(
                RIGHT_PANEL.left + PADDING, height // 2 + PADDING + start_y * (BUTTON_HEIGHT_B + PADDING),
                BUTTON_WIDTH, BUTTON_HEIGHT_B
            ))

            start_y += 1

    return rects



phase          = "A"        # "A" = guess Sarah's password  |  "B" = pick strong pwd
candidates_a   = []         # list of dicts for part A
candidates_b   = []         # list of dicts for part B
option_rects   = []         # pygame.Rect for each current option button
selected_idx   = None       # which option the player has selected
confirmed      = False      # player has clicked Confirm
result_text    = ""         # feedback shown after confirming




def setup():
    global phase, candidates_a, candidates_b, option_rects
    global selected_idx, confirmed, result_text

    phase = "A"
    candidates_a = pick_part_a()
    candidates_b = pick_part_b()
    selected_idx = None
    confirmed    = False
    result_text  = ""

    # Build option rects for part A (6 options)
    option_rects = make_option_rects("A")


def current_candidates():
    return candidates_a if phase == "A" else candidates_b


def handle(event):
    global selected_idx, confirmed, result_text, phase, option_rects

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

        for i, rect in enumerate(option_rects):
            if rect.collidepoint(event.pos):
                selected_idx = i
                confirmed    = False   # reset confirmation if they change selection
                result_text  = ""
                return None

        if CONTINUE_BUTTON.collidepoint(event.pos):

            if confirmed:
                if phase == "A":
                    phase = "B"
                    selected_idx = None
                    confirmed = False
                    result_text = ""
                    option_rects = make_option_rects("B")
                else:
                    return "continue"

            elif selected_idx is not None:
                confirmed = True
                candidates = current_candidates()
                chosen = candidates[selected_idx]

                if phase == "A":
                    if chosen["personal"]:
                        result_text = (
                            "Correct! You guessed it from her profile.\n"
                            f"Why: {chosen['why']}\n\n"
                            "An attacker could do this in seconds.\n"
                            "Click Continue to go to Part 2."
                        )
                    else:
                        result_text = (
                            f"Not quite. {chosen['why']}\n\n"
                            "Try a password that uses information\n"
                            "visible on her profile."
                        )
                        confirmed = False
                        selected_idx = None

                else:
                    if chosen["strong"]:
                        result_text = (
                            "Correct!\n"
                            f"{chosen['why']}\n\n"
                            "Click Continue to finish this checkpoint."
                        )
                    else:
                        result_text = (
                            f"Not strong enough.\n{chosen['why']}\n\n"
                            "Look for the longest, most random option."
                        )
                        confirmed = False
                        selected_idx = None

        return None



def draw(screen):
    global initial

    pygame.draw.rect(screen, "blue", PROFILE_PANEL)          # blue bg
    pygame.draw.rect(screen, "black", PROFILE_PANEL, 5)

    # Avatar circle
    pygame.draw.circle(screen, (200, 220, 255), (AVATAR_CX, AVATAR_CY), AVATAR_R)
    pygame.draw.circle(screen, "black", (AVATAR_CX, AVATAR_CY), AVATAR_R, 2)

    # Initial inside avatar

    screen.blit(initial, (AVATAR_CX - initial.get_width() // 2,
                           AVATAR_CY - initial.get_height() // 2))

    # Name and handle below avatar
    txt_rect(screen, f"{SARAH_NAME}\n {SARAH_HANDLE}", NAME_HANDLE_rect, 10, False, "white")


    # Bio text
    txt_rect(screen, SARAH_BIO, BIO_RECT, 13, False, "white")

    pygame.draw.rect(screen, "white", RIGHT_PANEL)
    pygame.draw.rect(screen, "black", RIGHT_PANEL, 3)

    # Phase title and instruction
    if phase == "A":
        txt_rect(screen, f"{title_A}\n {instr_A}", instr_rect, 10, True, "black")
    else:
        txt_rect(screen, f"{title_B}\n {instr_B}", instr_rect, 10, True, "black")


    if result_text:
        pygame.draw.rect(screen, (220, 240, 220), FEEDBACK_RECT, border_radius=6)
        pygame.draw.rect(screen, "black", FEEDBACK_RECT, 1, border_radius=6)
        txt_rect(screen, result_text, FEEDBACK_RECT, 12, False, "black")


    # Option buttons
    candidates = current_candidates()
    for i, (rect, cand) in enumerate(zip(option_rects, candidates)):
        if i == selected_idx:
            bg_col     = (50, 120, 220)
            text_col   = "white"
            border_col = "gold"
        else:
            bg_col     = "white"
            text_col   = "black"
            border_col = "black"

        pygame.draw.rect(screen, bg_col, rect, border_radius=6)
        pygame.draw.rect(screen, border_col, rect, 2, border_radius=6)
        txt_rect_center(screen, cand["pwd"], rect, 13, True, text_col)



    # Confirm button
    if selected_idx is not None or confirmed:
        confirm_col = (50, 180, 80)
        label = "Continue ->" if confirmed else "Confirm"
    else:
        confirm_col = (160, 160, 160)
        label = "Confirm"

    pygame.draw.rect(screen, confirm_col, CONTINUE_BUTTON, border_radius=6)
    pygame.draw.rect(screen, "black", CONTINUE_BUTTON, 2, border_radius=6)
    txt_rect_center(screen, label, CONTINUE_BUTTON, 15, True, "white")