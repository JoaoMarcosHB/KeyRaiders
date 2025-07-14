from .shared_window import *


class Grid:
    def __init__(self, layout: tuple[int, int], x_offset: float, y_offset: float):
        self.__window = SharedWindow.instance
        if not self.__window:
            raise ValueError("The shared_window instance must be set before creating any button.")

        self._columns, self._rows = layout
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._x_spacing = (self.__window.width - 2 * self._x_offset) / (self._columns + 1)
        self._y_spacing = (self.__window.height - 2 * self._y_offset) / (self._rows + 1)

    def get_points_position(self, *points_coordinates: tuple[int, int]) -> list[tuple[float, float]]:
        positions_list = []
        for coordinate in points_coordinates:
            if coordinate[0] > self._columns + 1 or coordinate[1] > self._rows + 1:
                raise ValueError("Invalid coordinates.")

            positions_list.append((coordinate[0] * self._x_spacing + self._x_offset,
                                   coordinate[1] * self._y_spacing + self._y_offset))
        return positions_list
