from pplay.window import Window as PPlayWindow
import pygame


class SharedWindow(PPlayWindow):
    """
    This subclass holds a shared reference to the active window instance,
    allowing other components to access the window globally without needing
    to pass it explicitly.
    """
    instance = None

    def __init__(self, width, height, sound_channels=8):
        super().__init__(width, height, sound_channels)
        SharedWindow.instance = self


    def set_fullscreen(self):
        """
        Overrides the default fullscreen behavior to update the instance's
        width and height attributes with the actual screen resolution.
        This ensures that other components relying on SharedWindow.instance
        get the correct dimensions after entering fullscreen mode.
        """
        result = super().set_fullscreen()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        return result
