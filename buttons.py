import pygame


class TextBox:
    def __init__(self, x, y, w, h, text='Lebron James'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.chosen = False
        self.text = text
        self.txt_surface = pygame.font.Font(None, 40).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the textbox
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change color if selected
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')

        if event.type == pygame.KEYDOWN:
            if self.active:
                # If user enters a player's name
                if event.key == pygame.K_RETURN:
                    self.chosen = True
                    print(self.text)
                # Interactive typing
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = pygame.font.Font(None, 40).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    # Some get/set functions
    def return_name(self):
        return self.text

    def is_chosen(self):
        return self.chosen

    def after_chosen(self):
        self.chosen = False


class Button:
    def __init__(self, x, y, width, height, text):
        self.color = (80, 80, 255)  # Blue color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = str(text)

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        # Draw the button text
        font = pygame.font.SysFont(None, 40)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

    def is_over(self, pos):
        # Check if mouse is over the button
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.color = (0, 0, 255)
            return True
        self.color = (80, 80, 255)
        return False


class PlayerButton:
    def __init__(self, x, y, width, height, text):
        self.color = (245, 245, 245)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = str(text)

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        # Draw the button text
        font = pygame.font.SysFont(None, 30)
        text = font.render(self.text, True, (40, 40, 40))
        win.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))


class Text:
    def __init__(self, x, y, width, height, text):
        self.color = (245, 245, 245)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = str(text)

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        # Draw the button text
        font = pygame.font.SysFont(None, 40)
        text = font.render(self.text, True, (100, 40, 100))
        win.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

