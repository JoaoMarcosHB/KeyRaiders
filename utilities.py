from math import pi
from random import choice, uniform
from game_classes.boat import Boat
from game_classes.sea import Sea
from user_interface.shared_window import SharedWindow
import pygame


class Background:
    def __init__(self):
        self.window = SharedWindow.instance

        self._sea_object = Sea(0.0001, 0)

        # (path, speed, frames, oscillation, wave_size)
        self._objects_info = [
            ("images/boats/sized_boat.png", (100, 200), 5, 5, 4)
        ]

        self._objects_in_screen = []
        self.upper_half = True

        self.interval = 1
        self._time = 0

    def _add_object(self):
        self._time += self.window.delta_time()
        if self._time >= self.interval:
            info = choice(self._objects_info)
            path, speed_range, oscillation, wave_size, frames = info
            speed = uniform(*speed_range)
            obj = Boat(path, speed, oscillation, wave_size, frames)

            h = self.window.height
            if self.upper_half:
                y_position = uniform(0, h / 2)
            else:
                y_position = uniform(h / 2, h - obj.height)
            obj.set_position(self.window.width, y_position)
            self.upper_half = not self.upper_half

            # Inserts objects in correct draw order, so higher ones are drawn first and appear behind.
            for i, obj_in_list in enumerate(self._objects_in_screen):
                if obj.y >= obj_in_list.y:
                    self._objects_in_screen.insert(i, obj)
                    break
            else:
                self._objects_in_screen.append(obj)

            self._time = 0

    def _draw_objects(self):
        for i in range(len(self._objects_in_screen) - 1, -1, -1):
            obj = self._objects_in_screen[i]
            if obj.x + obj.width >= 0:
                obj()
            else:
                del self._objects_in_screen[i]

    def __call__(self):
        self._sea_object()
        self._draw_objects()
        self._add_object()


class Ranking:
    def __init__(self):
        # Access the shared game window/screen
        self.__window = SharedWindow.instance
        self.__screen = self.__window.screen

        # File path for saving scores
        self._file_path = "scores.txt"

        # Load saved scores from file
        self._best_scores = self._saved_scores()

        # Rectangle drawing settings
        self.rect_color = (0, 0, 0)
        self.rect_y_size = 70              # Height of each rectangle
        self.rect_x_size = 900             # Width of each rectangle
        self.top_y_offset = 50             # Top margin
        self.mid_y_offset = 15             # Vertical space between rectangles

        # Maximum number of entries in the ranking
        self.max_size = int((self.__window.height - self.top_y_offset) / (self.rect_y_size + self.mid_y_offset))

        # Text settings
        self.text_color = (0, 0, 0)
        self.text_font = "./fonts/CutePixel.ttf"
        self.text_size = 50
        self.text_x_pos = 20
        self.text_y_pos = 10

    def _saved_scores(self):
        """Load the scores from file and return a list of (name, score) tuples."""
        tuples_list = []
        try:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    lista = line.strip().split(' ')
                    name = ''
                    for i in range(len(lista)-1):
                        name = name + lista[i] + " "
                    name.strip()
                    score = lista[-1]

                    tuples_list.append((name, int(score)))
            return tuples_list
        except FileNotFoundError:
            return []

    def add_score(self, name: str, new_score: int):
        """Insert a new score in order, removing the lowest if the list exceeds max size."""
        entry = (name.strip(), new_score)
        for i, (_, score) in enumerate(self._best_scores):
            if new_score >= score:
                self._best_scores.insert(i, entry)
                break
        else:
            self._best_scores.append(entry)

        if len(self._best_scores) > self.max_size:
            del self._best_scores[-1]

        with open(self._file_path, 'w', encoding='utf-8') as file:
            for name, score in self._best_scores:
                file.write(f"{name} {score}\n")

    def __call__(self):
        """Draw the ranking on the screen."""
        y = self.top_y_offset
        x = self.__window.width / 2 - self.rect_x_size / 2

        font = pygame.font.Font(self.text_font, self.text_size)

        for name, score in self._best_scores:
            rect = pygame.Rect(x, y, self.rect_x_size, self.rect_y_size)
            pygame.draw.rect(self.__screen, self.rect_color, rect, 5)

            text_surface = font.render(f"{name}: {score}", False, self.text_color)
            self.__screen.blit(text_surface, (x + self.text_x_pos, y + self.text_y_pos))

            y += rect.height + self.mid_y_offset
