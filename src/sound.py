import pygame
import os


# A class to manage all sound effects in the game
class SoundManager:
    def __init__(self, base_path):
        pygame.mixer.init()

        # Define sounds with their filename and volume
        self.sounds = {
            "wa": self.load_sound(base_path, "wa.wav", 0.5),
            "ka": self.load_sound(base_path, "ka.wav", 0.5),
            "death": self.load_sound(base_path, "death.wav", 0.5),
            "siren": self.load_sound(base_path, "siren.wav", 0.4),
            "freight": self.load_sound(base_path, "freight.wav", 0.3),
            "eyes": self.load_sound(base_path, "eyes.wav", 0.4),
            "start": self.load_sound(base_path, "start.wav", 0.5),
            "eat_fruit": self.load_sound(base_path, "eat_fruit.wav", 0.5),
            "eat_ghost": self.load_sound(base_path, "eat_ghost.wav", 0.5),
            "highscore": self.load_sound(base_path, "highscore.wav", 0.5)
        }

        # Set channels for looping sound effects
        self.looping_channels = {}

    # Load an individual sound file given its filename and set its volume
    def load_sound(self, base_path, filename, volume):
        path = os.path.join(base_path, "assets", "sounds", filename)
        if os.path.exists(path):
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        return None

    # Play a sound by its key name (e.g., "wa", "ka")
    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    # Play a looping sound (siren and freight)
    def play_looping(self, name):
        sound = self.sounds.get(name)
        if not sound:
            return

        # If already playing, do nothing
        channel = self.looping_channels.get(name)
        if channel and channel.get_busy():
            return

        # Stop all other looping sounds
        for key in list(self.looping_channels.keys()):
            if key != name:
                self.stop_looping(key)

        # Start this sound
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(sound, loops=-1)
            self.looping_channels[name] = channel

    def stop_looping(self, name):
        channel = self.looping_channels.get(name)
        if channel:
            channel.stop()
            self.looping_channels[name] = None
