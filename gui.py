import pygame
import numpy as np
from shotchart import ShotChart
from buttons import Button, TextBox
import sorting


class GUI:
    def __init__(self):
        pygame.init()

        # Create window
        window_size = (1280, 720)
        self.screen = pygame.display.set_mode(window_size)
        self.percentage_map = np.full((50, 42), -1.0)
        pygame.display.set_caption("Basketball Shooting Chart")

        # UI elements
        self.input_box = TextBox(540, 50, 200, 40)
        self.all = Button(100, 140, 200, 50, "All")
        self.threes = Button(400, 140, 200, 50, "Threes")
        self.midrange = Button(700, 140, 200, 50, "Mid-Range")
        self.paint = Button(1000, 140, 200, 50, "Paint")

        self.merge_buttons = []
        self.heap_buttons = []

        # Court
        image = pygame.image.load('nba_court_image.jpg')
        self.scaled_image = pygame.transform.scale(image, (500, 425))
        self.court_created = False
        self.court = pygame.Surface((420, 500))

        # Defaults
        self.name = 'Lebron James'
        self.percentage_map = ShotChart(self.name, '2022-23', 'all').percentage_map

        self.run()
        pygame.quit()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                # User exits or types in text box
                if event.type == pygame.QUIT:
                    running = False
                self.input_box.handle_event(event)

                # User clicks button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.all.is_over(pos):
                        self.percentage_map = ShotChart(self.name, '2022-23', 'all').percentage_map
                        self.court_created = False
                        self.add_sorting(0)
                    elif self.threes.is_over(pos):
                        self.percentage_map = ShotChart(self.name, '2022-23', 'threes').percentage_map
                        self.court_created = False
                        self.add_sorting(1)
                    elif self.midrange.is_over(pos):
                        self.percentage_map = ShotChart(self.name, '2022-23', 'midrange').percentage_map
                        self.court_created = False
                    elif self.paint.is_over(pos):
                        self.percentage_map = ShotChart(self.name, '2022-23', 'paint').percentage_map
                        self.court_created = False

            # Check for user input
            if self.input_box.is_chosen():
                self.name = self.input_box.return_name()
                self.percentage_map = ShotChart(self.name, '2022-23', 'all').percentage_map

                self.input_box.after_chosen()
                self.court_created = False

            # Draw background
            self.screen.fill((245, 245, 245))

            # Draw UI elements
            self.input_box.update()
            self.input_box.draw(self.screen)
            self.threes.draw(self.screen)
            self.midrange.draw(self.screen)
            self.paint.draw(self.screen)
            self.all.draw(self.screen)

            # Draw sorting buttons
            for button in self.merge_buttons:
                button.draw(self.screen)
            for button in self.heap_buttons:
                button.draw(self.screen)

            # Draw court image
            self.screen.blit(self.scaled_image, (390, 270))

            if not self.court_created:
                self.court = self.create_court()
                self.court_created = True
            self.screen.blit(self.court, (390, 300))

            pygame.display.flip()

    def create_court(self):
        # Dimensions of NBA half-court is 42x50 feet
        self.court = pygame.Surface((420, 500))
        self.court.set_alpha(150)

        # Overlay heat map (red to yellow)
        for i in range(self.percentage_map.shape[0]):
            for j in range(self.percentage_map.shape[1]):
                percentage = self.percentage_map[i, j]
                color = (255, 255, 255)
                if percentage != -1:
                    green = int(255 * (1 - percentage))
                    color = (255, green, 0)

                pygame.draw.rect(self.court, color, (j * 10, i * 10, 10, 10))

        # Rotate so it looks like half court
        return pygame.transform.rotate(self.court, 90)

    def add_sorting(self, n):
        merge_list, merge_time = sorting.descending(n)
        heap_list, heap_time = sorting.ascending(n)
        for num in range(5):
            name = merge_list[num]
            button = Button(100, 100 + 100*num, 200, 50, name)
            self.merge_buttons.append(button)

        for num2 in range(5):
            name2 = heap_list[num]
            button2 = Button(800, 100 + 100*num, 200, 50, name2)
            self.heap_buttons.append(button2)

        print("merge: ", merge_time)
        print("heap: ", heap_time)
