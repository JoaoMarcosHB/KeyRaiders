from pplay.sprite import *
from user_interface.shared_window import *
from math import radians, sin


class Boat(Sprite):

    def __init__(self, path: str, speed: float, oscillation=0.0, wave_size=0.0, frames=1, sequence_on="False"):
        self.__window = SharedWindow.instance
        if not self.__window:
            raise ValueError("The shared_window instance must be set before creating any boat.")

        super().__init__(path, frames)
        # Animation control (only if frames > 1)
        self._is_animated = frames > 1
        if self._is_animated:
            self.set_sequence(0, frames - 1)
            self.set_total_duration((10 ** 7.5) / (speed ** 2))

        self.speed = speed
        self.oscillation = oscillation
        self.wave_size = wave_size
        self.initial_y = self.y
        self.sequence_on = sequence_on

    def set_position(self, x, y):
        """Sobrescreve o método set_position para guardar a posição y inicial"""
        super().set_position(x, y)
        self.initial_y = y

    def _move(self):
        """Updates boat position and animation (if applicable)."""
        # Horizontal movement
        self.x -= self.speed * self.__window.delta_time()

        # Vertical wave effect
        if self.oscillation > 0:
            wave = sin(radians(self.x * self.oscillation)) * self.wave_size
            self.y = self.initial_y + wave

        # Update animation frames ONLY if animated
        if self._is_animated:
            self.update()
        self.draw()

    def __call__(self):
        self._move()
