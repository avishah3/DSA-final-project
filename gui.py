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

        # UI elements
        self.input_box = TextBox(100, 100, 140, 32)
        self.all = Button(50, 0, 200, 50, "All")
        self.threes = Button(50, 100, 200, 50, "Threes")
        self.midrange = Button(50, 200, 200, 50, "Mid-Range")
        self.paint = Button(50, 300, 200, 50, "Paint")

        self.mode = 'all'
        self.name = 'Lebron James'

        self.percentage_map = shotchart.ShotChart(self.name, '2022-23', 'all').percentage_map

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.all.is_over(pos):
                        self.percentage_map = shotchart.ShotChart(self.name, '2022-23', 'all').percentage_map
                        self.court_created = False
                    elif self.threes.is_over(pos):
                        self.percentage_map = shotchart.ShotChart(self.name, '2022-23', 'threes').percentage_map
                        self.court_created = False
                    elif self.midrange.is_over(pos):
                        self.percentage_map = shotchart.ShotChart(self.name, '2022-23', 'midrange').percentage_map
                        self.court_created = False
                    elif self.paint.is_over(pos):
                        self.percentage_map = shotchart.ShotChart(self.name, '2022-23', 'paint').percentage_map
                        self.court_created = False

            # Check for user input
            if self.input_box.is_chosen():
                self.name = self.input_box.return_name()
                self.percentage_map = shotchart.ShotChart(self.name, '2022-23', 'all').percentage_map

                self.input_box.after_chosen()
                self.court_created = False

            # Draw background
            self.screen.fill((255, 255, 255))

            # Draw UI elements
            self.input_box.update()
            self.input_box.draw(self.screen)
            self.threes.draw(self.screen)
            self.midrange.draw(self.screen)
            self.paint.draw(self.screen)
            self.all.draw(self.screen)

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


class Button:
    def __init__(self, x, y, width, height, text):
        self.color = (0, 0, 255)  # Blue color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        # Draw the button rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        # Draw the button text
        font = pygame.font.SysFont(None, 40)
        text = font.render(self.text, True, (255, 255, 255))  # White color
        win.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

    def is_over(self, pos):
        # Check if mouse is over the button
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
