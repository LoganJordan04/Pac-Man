import pygame
import os
from vector import Vector2
from constants import *


# Represents a single on-screen text element
class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setup_font("PressStart2P-Regular.ttf")
        self.create_label()

    # Loads a font file at the given path with the configured size
    def setup_font(self, fontpath):
        font_path = os.path.join(base_path, "assets", "fonts", fontpath)
        self.font = pygame.font.Font(font_path, self.size)

    # Renders the text string into a Pygame surface
    def create_label(self):
        self.label = self.font.render(self.text, 1, self.color)

    # Changes the displayed text and re-renders the label
    def set_text(self, newtext):
        self.text = str(newtext)
        self.create_label()

    # If the text has a limited lifespan, track its display time
    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None

                # Mark for removal
                self.destroy = True

    # Draws the text label to the screen, if visible
    def render(self, screen):
        if self.visible:
            x, y = self.position.as_tuple()
            screen.blit(self.label, (x, y))


# Manages all on-screen text elements as a group
class TextGroup(object):
    def __init__(self):
        # Used to assign unique IDs for new text objects
        self.nextid = 10

        # Dictionary of all text objects (id → Text)
        self.alltext = {}

        # Preload fixed labels (score, level, status)
        self.setup_text()

        # Start by showing the "READY!" message
        self.show_text(READYTXT)

    # Dynamically creates a new text object with optional lifespan
    def add_text(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    # Deletes a text object by its ID
    def remove_text(self, id):
        self.alltext.pop(id)

    # Predefined static labels and positions for score, level, and messages
    def setup_text(self):
        size = TILEHEIGHT
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23 * TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25 * TILEWIDTH, 20 * TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625 * TILEWIDTH, 20 * TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10 * TILEWIDTH, 20 * TILEHEIGHT, size, visible=False)

        # Add small top labels for clarity
        self.add_text("SCORE", WHITE, 0, 0, size)
        self.add_text("LEVEL", WHITE, 23 * TILEWIDTH, 0, size)

    # Updates all text elements; removes expired ones
    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.remove_text(tkey)

    # Shows a specific message (READY, PAUSED, GAMEOVER)
    def show_text(self, id):
        self.hide_text()
        self.alltext[id].visible = True

    # Hides all major status messages
    def hide_text(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    # Updates the displayed score with zero-padding (8 digits)
    def update_score(self, score):
        self.update_text(SCORETXT, str(score).zfill(8))

    # Updates the displayed level (zero-padded to 3 digits, levels are 1-based)
    def update_level(self, level):
        self.update_text(LEVELTXT, str(level + 1).zfill(3))

    # Changes the text content of an existing label
    def update_text(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].set_text(value)

    # Renders all visible text labels to the screen
    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
