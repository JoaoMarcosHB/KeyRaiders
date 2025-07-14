from pplay.sprite import Sprite
from math import pi, sin
from user_interface.shared_window import SharedWindow


class Sea:
    """Represents a moving sea/water background with wave-like oscillation effects."""

    def __init__(self, x_speed: float, y_speed: float):
        """Initializes the Sea object with movement parameters."""
        self.path = "images/scene.png"
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.max_offset = 5  # Máximo desvio vertical para as ondas
        self.oscillation = 0.32  # Frequência das ondas
        self.wave_size = 5  # Amplitude das ondas
        self.__window = SharedWindow.instance
        self.window_width = self.__window.width
        self.window_height = self.__window.height
        self._scene_in_screen = self._create_scene()
        self._counter = 0

    def _create_scene(self):
        x = y = 0
        scene_in_screen = []

        while y < self.window_height:
            line_scene = []
            while x < self.window_width:
                obj = Sprite(self.path)
                obj.set_position(x, y)
                line_scene.append(obj)
                x += obj.width
            x = 0
            y += line_scene[0].height
            scene_in_screen.append(line_scene)

        return scene_in_screen

    def _move_scene(self):
        self._counter += 1
        offset = sin(self._counter * self.oscillation) * self.max_offset

        for i, line in enumerate(self._scene_in_screen):
            for j, sprite in enumerate(line):
                sprite.x += self.x_speed
                sprite.y += self.y_speed

                # Aplicar oscilação senoidal por linha
                sprite.y += sin((sprite.x + self._counter * 5) * self.oscillation) * self.wave_size

    def _del_scene(self):
        # Remove linhas fora da tela
        if self._scene_in_screen and self._scene_in_screen[0][0].y + self._scene_in_screen[0][0].height < 0:
            self._scene_in_screen.pop(0)
        elif self._scene_in_screen and self._scene_in_screen[-1][0].y > self.window_height:
            self._scene_in_screen.pop(-1)

        # Remove colunas fora da tela
        for line in self._scene_in_screen:
            if line and line[0].x + line[0].width < 0:
                line.pop(0)
            if line and line[-1].x > self.window_width:
                line.pop(-1)

    def add_scene(self):
        # Adiciona linhas se necessário
        top_y = self._scene_in_screen[0][0].y
        bottom_y = self._scene_in_screen[-1][0].y + self._scene_in_screen[-1][0].height

        if top_y > 0:
            # Adiciona linha no topo
            new_line = []
            x = 0
            while x < self.window_width:
                obj = Sprite(self.path)
                obj.set_position(x, top_y - obj.height)
                new_line.append(obj)
                x += obj.width
            self._scene_in_screen.insert(0, new_line)

        if bottom_y < self.window_height:
            # Adiciona linha embaixo
            new_line = []
            x = 0
            while x < self.window_width:
                obj = Sprite(self.path)
                obj.set_position(x, bottom_y)
                new_line.append(obj)
                x += obj.width
            self._scene_in_screen.append(new_line)

        # Adiciona colunas laterais
        for line in self._scene_in_screen:
            left_x = line[0].x
            right_x = line[-1].x + line[-1].width

            if left_x > 0:
                obj = Sprite(self.path)
                obj.set_position(left_x - obj.width, line[0].y)
                line.insert(0, obj)

            if right_x < self.window_width:
                obj = Sprite(self.path)
                obj.set_position(right_x, line[0].y)
                line.append(obj)

    def _rend_scene(self):
        for line in self._scene_in_screen:
            for sprite in line:
                sprite.draw()

    def __call__(self):
        self._move_scene()
        self._del_scene()
        self.add_scene()
        self._rend_scene()
