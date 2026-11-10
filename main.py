import time

import pygame, sys
from pygame.locals import *



pygame.init()

import States.Menu as Menu
import States.checkpoints as checkpoint
from States import puzzle1, puzzle2, puzzle3
from Constants.constants import *
from txt_rect import *


screen = pygame.display.set_mode(SIZE)
screen_rect = pygame.Rect(0, 0, SIZE[0], SIZE[1])
clock = pygame.time.Clock()

current_state = "intro"
previous_state = None
retry_start = None

timer_start = None
time_left = duration
timer_font = pygame.font.SysFont("Arial", 36, True)

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False


#events
        if current_state == "intro":
            result = Menu.handle(event)
            if result == "puzzle1_intro":
                current_state = "puzzle1_intro"
                timer_start = pygame.time.get_ticks()
                checkpoint.start = pygame.time.get_ticks()
            elif result == "quit":
                running = False

        elif current_state == "puzzle1_intro":
            result = checkpoint.handle(event, current_state)

            if result == "puzzle1":
                current_state = "puzzle1"
                puzzle1.setup()


        elif current_state == "puzzle1":
            result = puzzle1.handle(event)

            if result == "continue":
                current_state = "puzzle2_intro"
                checkpoint.start = pygame.time.get_ticks()
                puzzle2.setup()

            elif result == "retry":
                puzzle1.setup()
                previous_state = "puzzle1"
                current_state = "retry"
                retry_start = pygame.time.get_ticks()

        elif current_state == "puzzle2_intro":
            result = checkpoint.handle(event, current_state)

            if result == "puzzle2":
                current_state = "puzzle2"

        elif current_state == "puzzle2":
            result = puzzle2.handle(event)

            if result == "continue":
                puzzle3.setup()
                current_state = "puzzle3_intro"
                checkpoint.start = pygame.time.get_ticks()

            elif result == "retry":
                puzzle2.setup()
                previous_state = "puzzle2"
                current_state = "retry"
                retry_start = pygame.time.get_ticks()


        elif current_state == "puzzle3_intro":
            result = checkpoint.handle(event, current_state)
            if result == "puzzle3":
                current_state = "puzzle3"

        elif current_state == "puzzle3":
            result = puzzle3.handle(event)

            if result == "continue":
                current_state = "summary1"
                checkpoint.start = pygame.time.get_ticks()

            elif result == "retry":
                puzzle3.setup()
                previous_state = "puzzle3"
                current_state = "retry"
                retry_start = pygame.time.get_ticks()

        elif current_state == "summary1":
            result = checkpoint.handle(event, current_state)

            if result == "summary2":
                current_state = "summary2"
                checkpoint.start = pygame.time.get_ticks()

        elif current_state == "summary2":
            result = checkpoint.handle(event, current_state)

            if result == "summary3":
                current_state = "summary3"
                checkpoint.start = pygame.time.get_ticks()

        elif current_state == "summary3":
            result = checkpoint.handle(event, current_state)

            if result == "quit":
                running = False



    screen.fill("black")

#draw
    if current_state == "intro":
        Menu.draw(screen)

    elif current_state == "puzzle1_intro":
        checkpoint.draw(screen, intro1_title, intro1_txt, current_state)

    elif current_state == "puzzle1":
        puzzle1.draw(screen)

    elif current_state == "puzzle2_intro":
        checkpoint.draw(screen, intro2_title, intro2_txt, current_state)

    elif current_state == "puzzle2":
        puzzle2.draw(screen)

    elif current_state == "puzzle3_intro":
        checkpoint.draw(screen, intro3_title, intro3_txt, current_state)

    elif current_state == "puzzle3":
        puzzle3.draw(screen)

    elif current_state == "summary1":
        checkpoint.draw(screen, summary1_title, summary1_txt, current_state)

    elif current_state == "summary2":
        checkpoint.draw(screen, summary2_title, summary2_txt, current_state)

    elif current_state == "summary3":
        checkpoint.draw(screen, summary3_title, summary3_txt, current_state)

    elif current_state == "retry":
        pygame.draw.rect(screen, "red", (0, 0, SIZE[0], SIZE[1]))
        txt_rect_center(screen, "RETRY", screen_rect, 10, True, "black")

        if pygame.time.get_ticks() - retry_start >= 3000:
            current_state = previous_state




    if current_state in states[1:len(states) - 5] and timer_start != None:
        elapsed = (pygame.time.get_ticks() - timer_start) // 1000

        time_left = duration - elapsed

        timer_text = f"{time_left // 60:02}:{time_left % 60:02}"

        colour = "black" if current_state == "puzzle1" else "white"

        timer_surface = timer_font.render(timer_text, True, colour)
        screen.blit(timer_surface, (width - timer_surface.get_width() - 20, 25))

        if time_left <= 0:
            current_state = "summary1"
            timer_start = None

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
sys.exit()