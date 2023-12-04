import pygame
import numpy as np
from shotchart import ShotChart
from buttons import Button, TextBox, PlayerButton, Text
import heapq
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

        self.buttons = []

        # Court
        image = pygame.image.load('nba_court_image.jpg')
        self.scaled_image = pygame.transform.scale(image, (500, 425))
        self.court_created = False
        self.court = pygame.Surface((420, 500))

        # Defaults
        self.name = 'Lebron James'
        self.mode = 'all'
        self.percentage_map = ShotChart(self.name, '2022-23', self.mode).percentage_map

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
                        self.mode = 'all'
                        self.percentage_map = ShotChart(self.name, '2022-23', self.mode).percentage_map
                        self.court_created = False
                        self.add_sorting(0)
                    elif self.threes.is_over(pos):
                        self.mode = 'threes'
                        self.percentage_map = ShotChart(self.name, '2022-23', self.mode).percentage_map
                        self.court_created = False
                        self.add_sorting(1)
                    elif self.midrange.is_over(pos):
                        self.mode = 'midrange'
                        self.percentage_map = ShotChart(self.name, '2022-23', self.mode).percentage_map
                        self.court_created = False
                        self.add_sorting(0)
                    elif self.paint.is_over(pos):
                        self.mode = 'paint'
                        self.percentage_map = ShotChart(self.name, '2022-23', self.mode).percentage_map
                        self.court_created = False
                        self.add_sorting(0)

            # Check for user input
            if self.input_box.is_chosen():
                self.name = self.input_box.return_name()
                self.mode = 'all'
                self.percentage_map = ShotChart(self.name, '2022-23', self.mode).percentage_map

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
            for button in self.buttons:
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
        self.buttons.clear()
        merge_list, merge_time = sorting.descending(n)
        heap, heap_time = sorting.ascending(n)

        # Add buttons (0 -> FG, 1 -> 3FG)
        if n == 0:
            text = Text(100, 250, 200, 50, 'Best FG%')
            self.buttons.append(text)
            text2 = Text(1000, 250, 200, 50, 'Worst FG%')
            self.buttons.append(text2)
            string = 'merge sort: ' + str(round(merge_time, 3)) + ' s'
            text3 = Text(100, 600, 200, 50, string)
            self.buttons.append(text3)
            string2 = 'min heap: ' + str(round(heap_time, 3)) + ' s'
            text4 = Text(1000, 600, 200, 50, string2)
            self.buttons.append(text4)
        else:
            text = Text(100, 250, 200, 50, 'Best 3FG%')
            self.buttons.append(text)
            text2 = Text(1000, 250, 200, 50, 'Worst 3FG%')
            self.buttons.append(text2)
            string = 'merge sort: ' + str(round(heap_time, 3)) + ' s'
            text3 = Text(100, 600, 200, 50, string)
            self.buttons.append(text3)
            string2 = 'min heap: ' + str(round(heap_time, 3)) + ' s'
            text4 = Text(1000, 600, 200, 50, string2)
            self.buttons.append(text4)

        # Place player buttons on the left
        for num in range(5):
            name = merge_list[num][0]
            button = PlayerButton(100, 320 + 50*num, 200, 50, name)
            self.buttons.append(button)

        # Place player buttons on the right
        for num2 in range(5):
            name2 = heapq.heappop(heap)[1]
            button2 = PlayerButton(1000, 320 + 50*num2, 200, 50, name2)
            self.buttons.append(button2)

