import pygame
import shotchart
import numpy as np


class GUI:
    def __init__(self):
        pygame.init()

        # Create window
        window_size = (1280, 720)
        self.screen = pygame.display.set_mode(window_size)
        self.percentage_map = np.full((50, 42), -1.0)
        pygame.display.set_caption("Basketball Shooting Chart")
        self.input_box = TextBox(100, 100, 140, 32)

        self.percentage_map = shotchart.ShotChart('Stephen Curry', '2020-21').percentage_map

        self.court_created = False
        self.court = pygame.Surface((420, 500))

        self.heat_mode = True

        self.run()
        pygame.quit()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.input_box.handle_event(event)

            # Check for user input
            if self.input_box.is_chosen():
                name = self.input_box.return_name()
                self.percentage_map = shotchart.ShotChart(name, '2022-23').percentage_map
                self.input_box.after_chosen()
                self.court_created = False

            # Draw background
            self.screen.fill((255, 255, 255))

            # Draw text box
            self.input_box.update()

            self.input_box.draw(self.screen)

            if self.heat_mode:
                # Draw court image
                if not self.court_created:
                    self.court = self.create_court()
                    self.court_created = True
                self.screen.blit(self.court, (390, 300))

            else:
                pass
                # Draw tier list image
                # Write Names / Photos

            pygame.display.flip()

    def create_court(self):
        self.court = pygame.Surface((420, 500))
        # Overlay heat map
        for i in range(self.percentage_map.shape[0]):
            for j in range(self.percentage_map.shape[1]):
                percentage = self.percentage_map[i, j]
                color = (255, 255, 255)
                if percentage != -1:
                    green = int(255 * (1 - percentage))
                    color = (255, green, 0)

                pygame.draw.rect(self.court, color, (j * 10, i * 10, 10, 10))

        return pygame.transform.rotate(self.court, 90)


class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.chosen = False
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.chosen = True
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def return_name(self):
        return self.text

    def is_chosen(self):
        return self.chosen

    def after_chosen(self):
        self.chosen = False

