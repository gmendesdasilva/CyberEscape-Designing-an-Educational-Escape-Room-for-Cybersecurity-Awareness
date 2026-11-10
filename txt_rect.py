
import pygame




def txt_rect(surface, text, rect: pygame.Rect, padding, bold=False, color="white"):
   # test the biggest size that fits in rect from big to small
    for font_size in range(60, 6, -1):
        font = pygame.font.SysFont("Arial", font_size, bold)
        lines = wrap_txt(text, font, rect.width - 2 * padding)

        total_height = len(lines) * font.get_linesize() # number of lines times font height plus some padding

        if total_height <= rect.height:
            break # size fits so stop the loop

    y = rect.top + padding
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (rect.left + padding, y))
        y += font.get_linesize() # move down a line

def txt_rect_center(surface, text, rect: pygame.Rect, padding, bold=False, color="white"):
    # test the biggest size that fits in rect from big to small
    for font_size in range(60, 6, -1):
        font = pygame.font.SysFont("Arial", font_size, bold)
        lines = wrap_txt(text, font, rect.width - 2 * padding)

        total_height = len(lines) * font.get_linesize()  # number of lines times font height plus some padding

        if total_height <= rect.height:
            break  # size fits so stop the loop

    y = rect.top + (rect.height - total_height) // 2
    for line in lines:
        text_surface = font.render(line, True, color)
        total_width = text_surface.get_width()
        x = rect.left + (rect.width - total_width) // 2
        surface.blit(text_surface, (x, y))
        y += font.get_linesize()  # move down a line


def wrap_txt(text, font, max_width):
    lines = []
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        if paragraph == "":
            lines.append("")
            continue
        # check every word
        words = paragraph.split()
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            line_width = font.size(test_line)[0]


            # if the current_line fits in desired rect
            if line_width <= max_width:
                current_line = test_line

            else:
                if current_line:
                    lines.append(current_line.strip()) #append the line without the word
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip()) # last line in case non-empty

    return lines




