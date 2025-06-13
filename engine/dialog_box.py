import pygame


class DialogBox:
    def __init__(self, x, y, width, height, font, text_color=(255, 255, 255), box_color=(50, 50, 50), border_color=(255, 255, 255), border_radius=10, padding = 7, stroke_width = 3):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.padding = padding
        self.stroke_width = stroke_width
        self.pages = []
        self.current_page = 0
        self.visible = False

    #Prepare text to use
    def set_text(self, text):
        lines = self.split_text_to_lines(text)
        self.split_to_pages(lines)

    #Show dialog box
    def show(self):
        self.visible = True

    #Hide dialog box
    def hide(self):
        self.visible = False

    #Clear text from the box
    def clear(self):
        self.pages.clear()
        self.current_page = 0

    #Check if page has next page
    def has_next_page(self):
        return self.current_page < len(self.pages) - 1

    #Go to the next page
    def next_page(self):
        if self.has_next_page():
            self.current_page += 1

    #Draw the current page
    def draw(self, surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, self.box_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, self.rect, self.stroke_width, border_radius=self.border_radius)

        for i, line in enumerate(self.pages[self.current_page]):
            rendered = self.font.render(line, True, self.text_color)
            surface.blit(rendered, (self.rect.x + self.padding + self.stroke_width, self.rect.y + self.padding + self.stroke_width + i * self.font.get_linesize()))

    #Split text to lines depends on the size of box and font
    def split_text_to_lines(self, text):
        words = text.split()
        lines = []
        current_line = ""

        max_width = self.rect.width - 2 * (self.padding + self.stroke_width)

        for word in words:
            if self.font.size(word)[0] > max_width:
                while self.font.size(word)[0] > max_width:
                    part_word = self.split_word(word, current_line)
                    current_line += part_word
                    word = word[len(part_word):]
                    lines.append(current_line)
                    current_line = ""
                test_line = word
            else:
                test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                 lines.append(current_line.strip())
                 current_line = word + " "
        lines.append(current_line.strip())
        return lines

    #Split that word can fill in line with the current line already
    def split_word(self, word, current_line):
        max_width = self.rect.width - 2 * (self.padding + self.stroke_width)
        if self.font.size(word)[0] <= max_width:
            return word
        else:
            for i in range(len(word)):
                test_line = current_line + word[:i]
                if self.font.size(test_line)[0] > max_width:
                    return word[:i-1]
            return word

    # Split to pages depends on the size of box and font
    def split_to_pages(self, lines):
        max_lines_per_stage = (self.rect.height - self.stroke_width * 2) // self.font.get_linesize()
        self.pages = [lines[i:i + max_lines_per_stage] for i in range(0, len(lines), max_lines_per_stage)]