import pygame
import random
from Constants.constants import width, height, NETWORKS_BASE, URLS_BASE, ACTIONS_BASE
from txt_rect import txt_rect, txt_rect_center

PADDING = 10

HEADER_HEIGHT = height // 6
CONFIRM_HEIGHT = 70

HEADER_RECT = pygame.Rect(PADDING, PADDING, width - 2 * PADDING, HEADER_HEIGHT)

CONFIRM_RECT = pygame.Rect(
    2 * PADDING, height - CONFIRM_HEIGHT - PADDING,
    width - 4 * PADDING, CONFIRM_HEIGHT
)

# Space between header and confirm button — all option cards live here
cards_top = HEADER_RECT.bottom + PADDING
cards_bot = CONFIRM_RECT.top - PADDING
cards_height = cards_bot - cards_top

# Phase 1: 4 network cards
NET_HEIGHT = (cards_height - 3 * PADDING) // 4

NET_RECTS = [

    pygame.Rect(
        2 * PADDING, cards_top + i * (NET_HEIGHT + PADDING),
        width - 4 * PADDING, NET_HEIGHT
    )

    for i in range(4)
]

# Phase 2: 2 URL cards
URL_HEIGHT = (cards_height - PADDING) // 2

URL_RECTS = [
    pygame.Rect(2 * PADDING,
                cards_top + i * (URL_HEIGHT + PADDING),
                width - 4 * PADDING, URL_HEIGHT)
    for i in range(2)
]

# Phase 3: 6 action rows — SAFE and RISKY buttons are right-aligned, full row height
ACT_HEIGHT = (cards_height - 5 * PADDING) // 6

ACT_BTN_WIDTH = 160

def make_action_rows():
    rows = []
    for i in range(6):
        y    = cards_top + i * (ACT_HEIGHT + PADDING)
        full = pygame.Rect(2 * PADDING, y, width - 4 * PADDING, ACT_HEIGHT)
        risk = pygame.Rect(full.right - ACT_BTN_WIDTH, y, ACT_BTN_WIDTH, ACT_HEIGHT)
        safe = pygame.Rect(risk.left - ACT_BTN_WIDTH - PADDING, y, ACT_BTN_WIDTH, ACT_HEIGHT)
        txt  = pygame.Rect(full.left + PADDING, y,
                           safe.left - full.left - 2 * PADDING, ACT_HEIGHT)
        rows.append((full, txt, safe, risk))
    return rows

ACTION_ROWS = make_action_rows()




retry_phase = 1   # setup() starts from this phase — set to 3 when phase 3 fails

phase         = 1
networks      = []
urls          = []
actions       = []

net_selected  = None
net_confirmed = False
url_selected  = None
url_confirmed = False
action_picks  = [None] * 6
result_text   = ""


def setup():
    global phase, networks, urls, actions
    global net_selected, net_confirmed
    global url_selected, url_confirmed
    global action_picks, result_text, retry_phase

    phase = retry_phase

    networks = NETWORKS_BASE.copy()
    random.shuffle(networks)

    urls = URLS_BASE.copy()
    random.shuffle(urls)

    actions = ACTIONS_BASE.copy()
    random.shuffle(actions)

    net_selected  = None
    net_confirmed = False
    url_selected  = None
    url_confirmed = False
    action_picks  = [None] * len(actions)
    result_text   = ""

    retry_phase = 1   # reset for next fresh game


def handle(event):
    global phase
    global net_selected, net_confirmed
    global url_selected, url_confirmed
    global action_picks, result_text, retry_phase

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:


        if phase == 1:

            for i, rect in enumerate(NET_RECTS):
                if rect.collidepoint(event.pos):
                    net_selected  = i
                    net_confirmed = False
                    result_text   = ""
                    return None

            if CONFIRM_RECT.collidepoint(event.pos):
                # Check confirmed FIRST (same fix as puzzle2)
                if net_confirmed:
                    phase         = 2
                    net_confirmed = False
                    result_text   = ""

                elif net_selected is not None:
                    net = networks[net_selected]
                    if net["secure"]:
                        net_confirmed = True
                        result_text   = (
                            "Correct! Password-protected networks encrypt your "
                            "traffic so others nearby cannot read it. "
                            "Click Continue to move to Step 2."
                        )
                    else:
                        result_text  = net["reason"]
                        net_selected = None

        elif phase == 2:

            for i, rect in enumerate(URL_RECTS):
                if rect.collidepoint(event.pos):
                    url_selected  = i
                    url_confirmed = False
                    result_text   = ""
                    return None

            if CONFIRM_RECT.collidepoint(event.pos):
                if url_confirmed:
                    phase         = 3
                    url_confirmed = False
                    result_text   = ""

                elif url_selected is not None:
                    url = urls[url_selected]
                    result_text = url["feedback"]
                    if url["secure"]:
                        url_confirmed = True
                    else:
                        url_selected = None

        elif phase == 3:

            for i, (full, txt_r, safe_r, risk_r) in enumerate(ACTION_ROWS):
                if safe_r.collidepoint(event.pos):
                    action_picks[i] = True
                    return None
                if risk_r.collidepoint(event.pos):
                    action_picks[i] = False
                    return None

            all_picked = all(p is not None for p in action_picks)
            if CONFIRM_RECT.collidepoint(event.pos) and all_picked:
                all_correct = all(
                    action_picks[i] == actions[i]["safe"]
                    for i in range(len(actions))
                )
                if all_correct:
                    return "continue"
                else:
                    retry_phase = 3   # restart from phase 3, not from 1
                    return "retry"

    return None


def draw(screen):

    # Background colour changes per phase
    if phase == 1:
        screen.fill((30, 80, 160))
    elif phase == 2:
        screen.fill("white")
    else:
        screen.fill((220, 230, 245))

    pygame.draw.rect(screen, "white", HEADER_RECT)
    pygame.draw.rect(screen, "black", HEADER_RECT, 2)

    # If there is feedback, show it in the header instead of the instruction
    if result_text:
        txt_rect(screen, result_text, HEADER_RECT, 5, False, "black")
    else:
        if phase == 1:
            header_text = (
                "Step 1 of 3 - Choose a Safe Wi-Fi Network\n"
                ""
                "Four networks are available. "
                "Which one is safe to use if you want to log in to an account?"
            )
        elif phase == 2:
            header_text = (
                "Step 2 of 3 - Check the Website Address\n"
                ""
                "You are connected. Before entering your login details, "
                "look carefully at the address bar. Which address is safe?"
            )
        else:
            header_text = (
                "Step 3 of 3 - What is Safe to Do Online?\n"
                ""
                "Even on a safer network, some actions are riskier than others. "
                "Mark each action as Safe or Risky."
            )
        txt_rect(screen, header_text, HEADER_RECT, 5, False, "black")


    if phase == 1:
        draw_networks(screen)
    elif phase == 2:
        draw_urls(screen)
    else:
        draw_actions(screen)

    draw_confirm(screen)


def draw_networks(screen):
    for i, (net, rect) in enumerate(zip(networks, NET_RECTS)):
        pygame.draw.rect(screen, "white", rect)

        border_col = "gold" if i == net_selected else "black"
        border_w = 4 if i == net_selected else 2
        pygame.draw.rect(screen, border_col, rect, border_w)

        # [LOCK] / [OPEN] right-aligned
        ind_text = "[LOCK]" if net["secure"] else "[OPEN]"
        ind_col = (0, 150, 0) if net["secure"] else (180, 0, 0)
        f_ind = pygame.font.SysFont("Arial", 15, bold=True)
        ind_surf = f_ind.render(ind_text, True, ind_col)
        screen.blit(ind_surf, (rect.right - ind_surf.get_width() - PADDING,
                               rect.top   + PADDING))

        # Name and detail in remaining left space
        inner = pygame.Rect(
            rect.left + PADDING, rect.top,
            rect.width - ind_surf.get_width() - 3 * PADDING, rect.height
        )
        txt_rect(screen, f"{net['name']}\n{net['detail']}", inner, 10, True, "black")


def draw_urls(screen):
    for i, (url, rect) in enumerate(zip(urls, URL_RECTS)):
        pygame.draw.rect(screen, "white", rect)

        border_col = "gold" if i == url_selected else "black"
        border_w = 4 if i == url_selected else 2
        pygame.draw.rect(screen, border_col, rect, border_w)

        # Fake browser address bar in the upper half of the card
        bar = pygame.Rect(
            rect.left + PADDING, rect.top  + PADDING,
            rect.width - 2 * PADDING, rect.height // 2 - PADDING
        )
        pygame.draw.rect(screen, (215, 215, 215), bar, border_radius=4)
        pygame.draw.rect(screen, "black", bar, 1, border_radius=4)

        f_url    = pygame.font.SysFont("Courier", 16, bold=True)
        url_surf = f_url.render(url["bar"], True, url["bar_col"])
        screen.blit(url_surf, (bar.left + PADDING,
                               bar.centery - url_surf.get_height() // 2))

        # Short description below the bar
        desc_rect = pygame.Rect(
            rect.left + PADDING, bar.bottom + PADDING,
            rect.width - 2 * PADDING, rect.bottom - bar.bottom - PADDING * 2
        )
        desc_col = (0, 120, 0) if url["secure"] else (160, 0, 0)
        txt_rect(screen, url["detail"], desc_rect, 13, False, desc_col)


def draw_actions(screen):
    for i, (full, txt_r, safe_r, risk_r) in enumerate(ACTION_ROWS):
        pick = action_picks[i]

        # Row background
        pygame.draw.rect(screen, "white", full)
        pygame.draw.rect(screen, "black", full, 1)

        # Action text
        txt_rect(screen, actions[i]["text"], txt_r, 13, False, "black")

        # SAFE button — light green background, gold border if picked
        pygame.draw.rect(screen, (195, 235, 195), safe_r)
        safe_bc = "gold" if pick is True  else "black"
        safe_bw = 4 if pick is True  else 1
        pygame.draw.rect(screen, safe_bc, safe_r, safe_bw)
        txt_rect_center(screen, "SAFE", safe_r, 10, True, "black")

        # RISKY button — light red background, gold border if picked
        pygame.draw.rect(screen, (235, 195, 195), risk_r)
        risk_bc = "gold" if pick is False else "black"
        risk_bw = 4 if pick is False else 1
        pygame.draw.rect(screen, risk_bc, risk_r, risk_bw)
        txt_rect_center(screen, "RISKY", risk_r, 14, True, "black")


def draw_confirm(screen):
    if phase == 1:
        if net_confirmed:
            col, label = (50, 180, 80), "Continue to Step 2 ->"
        elif net_selected is not None:
            col, label = (50, 180, 80), "Confirm"
        else:
            col, label = (160, 160, 160), "Select a network first"

    elif phase == 2:
        if url_confirmed:
            col, label = (50, 180, 80), "Continue to Step 3 ->"
        elif url_selected is not None:
            col, label = (50, 180, 80), "Confirm"
        else:
            col, label = (160, 160, 160), "Select an address first"

    else:
        all_picked = all(p is not None for p in action_picks)
        if all_picked:
            col, label = (50, 180, 80), "Submit Answers"
        else:
            remaining  = action_picks.count(None)
            col, label = (160, 160, 160), f"{remaining} actions still to mark"

    pygame.draw.rect(screen, col,     CONFIRM_RECT, border_radius=6)
    pygame.draw.rect(screen, "black", CONFIRM_RECT, 2, border_radius=6)
    txt_rect_center(screen, label, CONFIRM_RECT, 14, True, "white")