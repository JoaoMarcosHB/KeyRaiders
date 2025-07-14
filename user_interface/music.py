from pplay.sound import *


class Music:
    """
    Class responsible for managing music. Allows setting a main shared music or a custom music for each instance.
    """
    _main_music = None
    _currently_playing = None
    volume = 30
    def __init__(self):
        self.custom_music = None
        self._music_defined = False
        self.customvolume = Music.volume

    @classmethod
    def set_main_music(cls, music_path):
        """
        Sets the main (default) music shared by all instances.
        """
        cls._main_music = Sound(music_path) if music_path else None

        if cls._main_music is not None:
            cls._main_music.set_volume(cls.volume)
    @classmethod
    def set_volume(cls, volume):
        if 0 <= volume <= 100:
            amount = volume - cls.volume
            cls.volume = volume
            if cls._main_music is not None:
                cls._main_music.increase_volume(amount)

    def check_volume_change(self):
        if self.customvolume != Music.volume:
            amount = Music.volume - self.customvolume
            self.customvolume = Music.volume
            if self.current_music is not None:
                self.current_music.increase_volume(amount)

    def set_custom_music(self, music_path):
        """
        Sets a custom music for this specific instance.
        If None is passed, it disables music for this instance.
        """
        self._music_defined = True
        self.custom_music = Sound(music_path) if music_path else None
        if self.custom_music is not None:
            self.custom_music.set_volume(Music.volume)


    @property
    def current_music(self):
        """
        Returns the music to be played: custom if defined, otherwise the main one.
        """
        return self.custom_music if self._music_defined else Music._main_music

    def play(self):
        """
        Plays the current music if it's not already playing.
        Stops the previous music if different.
        """
        #self.check_volume_change()
        music = self.current_music
        if music is not Music._currently_playing:
            if Music._currently_playing:
                Music._currently_playing.stop()
            if music:
                music.play()
                Music._currently_playing = music
            else:
                Music._currently_playing = None
