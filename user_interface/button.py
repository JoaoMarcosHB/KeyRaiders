from pplay.sprite import *
from pplay.sound import *
from pplay.text import *
import time
from .shared_window import *
import pygame
from pplay.window import Window


class Button:
    _hover_path = None
    _hover_sound = None
    _click_path = None
    _click_sound = None
    __text_info = {}
    last_click = 0
    _delay = 0.5
    @classmethod
    def add_text_property(cls,
                            key,
                            font_name: str,
                            font_size: int,
                            default_position: tuple[float, float],
                            hover_position: tuple[float, float],
                            color: tuple[int, int, int]):

        font = pygame.font.SysFont(font_name, font_size)
        cls.__text_info[key] = (font, default_position, hover_position, color)

    @classmethod
    def set_sounds(cls, hover=None, click=None):
        if hover:
            cls._hover_path = hover
            cls._hover_sound = Sound(hover)
        if click:
            cls._click_path = click
            cls._click_sound = Sound(click)

    def __init__(self,
                 position: tuple[float, float],
                 paths: tuple[str, str],
                 function: callable,
                 key_text=("", ""),
                 size =60,
                 align_horizontal="center",
                 align_vertical="center"):

        self.__window = SharedWindow.instance
        if not self.__window:
            raise ValueError("The shared_window instance must be set before creating any button.")
        self._key = key_text[0]
        self._text = key_text[1]
        self.texto = key_text[1]
        self.font = pygame.font.Font("./fonts/CutePixel.ttf", size)
        self._text_enabled = True if self._key == 1 and self._text else False

        # Stores the function to be called when the button is clicked
        self.function = function
        self.mouse = Window.get_mouse()
        self._was_pressed_last_frame = False
        self._was_hovered = False

        default_image_path, hover_image_path = paths
        self.default_sprite = Sprite(default_image_path)
        self.hovered_sprite = Sprite(hover_image_path)

        x, y = position

        # Horizontal alignment
        if align_horizontal == "center":
            x -= self.default_sprite.width / 2
        elif align_horizontal == "right":
            x -= self.default_sprite.width
        # If align_horizontal is "left", no adjustment needed

        # Vertical alignment
        if align_vertical == "center":
            y -= self.default_sprite.height / 2
        elif align_vertical == "bottom":
            y -= self.default_sprite.height
        # If align_vertical is "top", no adjustment needed

        # Sets the final position for both sprites
        self.default_sprite.set_position(x, y)
        self.hovered_sprite.set_position(x, y)

    def is_released(self) -> bool:
        """
        Returns True only in the frame when the mouse button is released over the button.
        """
        currently_pressed = self.mouse.is_button_pressed(1)
        released = self._was_pressed_last_frame and not currently_pressed
        self._was_pressed_last_frame = currently_pressed
        return released

    def is_hovered(self) -> bool:
        """
        Returns True if the mouse is currently over the button.
        """
        return self.mouse.is_over_object(self.default_sprite)

    def is_clicked(self) -> bool:
        """
        Returns True if the mouse is over the button and the left mouse button was just released.
        """
        if self.is_hovered():
            if self.mouse.is_button_pressed(1):
                if time.time() - Button.last_click >= Button._delay:
                    Button.last_click = time.time()
                    if Button._click_sound:
                        Sound(Button._click_path).play()
                    return True
        return False

    def _display_text(self, default):
        if self._text_enabled:
            font_obj, default_position, hover_position, color = Button.__text_info[self._key]
            #x, y = default_position if default else hover_position
            sprite = self.default_sprite if default else self.hovered_sprite
            texto = self.font.render(self._text, True, color)

            x = sprite.x - texto.get_width()/2 + sprite.width/2
            y = sprite.y + sprite.height/3 - texto.get_height()/2
            if not default:
                y += sprite.height/7



            # text_surface = font_obj.render(self._text, True, color)
            # text_rect = text_surface.get_rect(center=(x, y))

            self.__window.screen.blit(texto, (x,y))

    def __call__(self):
        """
        Draws the button: shows the hover sprite if hovered, otherwise the default sprite.
        Plays the button audio.
        """
        if self.is_hovered():
            if not self._was_hovered and Button._hover_sound:
                Sound(Button._hover_path).play()
            self._was_hovered = True
            self.hovered_sprite.draw()
            self._display_text(False)
        else:
            self._was_hovered = False
            self.default_sprite.draw()
            self._display_text(True)
