import pygame
import os


# A class to manage all sound effects in the game
class SoundManager:
    def __init__(self, base_path):
        pygame.mixer.init()

        # Load sounds into a dictionary for easy access by name
        self.sounds = {
            "wa": self.load_sound(base_path, "wa.wav"),
            "ka": self.load_sound(base_path, "ka.wav"),
            # "eat_ghost": self.load_sound(base_path, "eat_ghost.wav"),
            # "death": self.load_sound(base_path, "death.wav"),
            # "fruit": self.load_sound(base_path, "eat_fruit.wav"),
            # "power_pellet": self.load_sound(base_path, "power_pellet.wav"),
            # "start": self.load_sound(base_path, "start.wav"),
        }

        # Set common volume level
        for sound in self.sounds.values():
            sound.set_volume(0.5)

    # Load an individual sound file given its filename
    def load_sound(self, base_path, filename):
        path = os.path.join(base_path, "assets", "sounds", filename)
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None

    # Play a sound by its key name (e.g., "wa", "ka")
    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()
