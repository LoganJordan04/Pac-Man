import pygame
import json
import os
from pygame.locals import *
from constants import *
from vector import Vector2
from text import Text


class HighScore:
    def __init__(self, filename="highscore.json"):
        self.filename = filename
        self.high_score = self.load_high_score()

    # Load high score from file, return 0 if file doesn't exist
    def load_high_score(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except (json.JSONDecodeError, IOError):
            pass
        return 0

    # Save high score to file if it's a new record
    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.filename, 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
                # New high score
                return True
            except IOError:
                pass
        # Not a new high score
        return False

    def get_high_score(self):
        return self.high_score


class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.high_score_manager = HighScore()
        self.setup_text()
        self.blink_timer = 0
        # Blink every 1 second
        self.blink_speed = 1
        self.show_start_text = True

    # Create all menu text elements
    def setup_text(self):
        self.texts = []

        # load your logo.png from the same folder as menu.py
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        self.logo_image = pygame.image.load(logo_path).convert_alpha()
        # optional: scale it to fit (e.g. width=12 tiles, height=3 tiles)
        logo_w = int(12 * TILEWIDTH)
        logo_h = int(3 * TILEHEIGHT)
        self.logo_image = pygame.transform.scale(self.logo_image, (logo_w, logo_h))
        # position it at 8.5 tiles over, 6 tiles down
        self.logo_pos = (8.5 * TILEWIDTH, 6 * TILEHEIGHT)

        # 2) High Score (already in your original)
        high_score = self.high_score_manager.get_high_score()
        self.texts.append(Text("HIGH SCORE", WHITE, 9 * TILEWIDTH, 9 * TILEHEIGHT, TILEHEIGHT))
        self.texts.append(Text(str(high_score).zfill(8), WHITE, 9 * TILEWIDTH, 10.5 * TILEHEIGHT, TILEHEIGHT))

        # 3) Character / Nickname header
        self.texts.append(Text("CHARACTER / NICKNAME", WHITE, 6 * TILEWIDTH, 13 * TILEHEIGHT, int(TILEHEIGHT * 0.8)))

        # 4) Ghost names updated to original Japanese
        ghost_y = 15 * TILEHEIGHT
        self.texts.append(Text("OIKAKE", RED,    7 * TILEWIDTH,  ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"AKABEI"', RED,  15 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))

        ghost_y += 1.5 * TILEHEIGHT
        self.texts.append(Text("MACHIBUSE", PINK, 7 * TILEWIDTH,  ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"PINKY"', PINK,   15 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))

        ghost_y += 1.5 * TILEHEIGHT
        self.texts.append(Text("KIMAGURE", TEAL,   7 * TILEWIDTH,  ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"AOSUKE"', TEAL,   15 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))

        ghost_y += 1.5 * TILEHEIGHT
        self.texts.append(Text("OTOBOKE", ORANGE,  7 * TILEWIDTH,  ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"GUZUTA"', ORANGE, 15 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))

        # 5) Point values
        points_y = 22 * TILEHEIGHT
        self.texts.append(Text("10 PTS", WHITE,  7 * TILEWIDTH,  points_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text("50 PTS", WHITE, 15 * TILEWIDTH,  points_y, int(TILEHEIGHT * 0.8)))

        # 6) namco credit at very bottom, centered
        self.texts.append(Text(
            "namco", PINK,
            (NCOLS / 2) * TILEWIDTH, 28 * TILEHEIGHT,
            int(TILEHEIGHT * 1)
        ))

        # 7) Blinking “PRESS SPACEBAR” prompt (replaces CREDIT 0)
        self.start_text = Text(
            "PRESS SPACEBAR", YELLOW,
            (NCOLS / 2) * TILEWIDTH, 28 * TILEHEIGHT,
            int(TILEHEIGHT * 0.9)
        )

    # Update menu animations
    def update(self, dt):
        # Update blinking text
        self.blink_timer += dt
        if self.blink_timer >= self.blink_speed:
            self.blink_timer = 0
            self.show_start_text = not self.show_start_text

        # Update all text objects
        for text in self.texts:
            text.update(dt)
        self.start_text.update(dt)

    # Update the displayed high score
    def update_high_score(self, score):
        new_record = self.high_score_manager.save_high_score(score)
        if new_record:
            self.texts[2].set_text(str(self.high_score_manager.get_high_score()).zfill(8))
        return new_record

    # Render the menu screen
    def render(self):
        # Clear screen with black
        self.screen.fill(BLACK)

        # 2) draw your logo
        self.screen.blit(self.logo_image, self.logo_pos)

        # Draw all text
        for text in self.texts:
            text.render(self.screen)

        # Draw blinking start text
        if self.show_start_text:
            self.start_text.render(self.screen)

    # Handle menu input events
    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Start game
                return True
        return False


# Simple state manager for menu/game transitions
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    HIGH_SCORE = 3

    def __init__(self):
        self.current_state = self.MENU
        self.previous_state = self.MENU

    def set_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state = new_state

    def is_menu(self):
        return self.current_state == self.MENU

    def is_playing(self):
        return self.current_state == self.PLAYING

    def is_game_over(self):
        return self.current_state == self.GAME_OVER

    def is_high_score(self):
        return self.current_state == self.HIGH_SCORE


# Screen shown when player gets a new high score
class HighScoreScreen:
    def __init__(self, screen, new_score):
        self.screen = screen
        self.new_score = new_score
        self.timer = 0
        self.display_time = 3.0  # Show for 3 seconds
        self.setup_text()

    def setup_text(self):
        self.texts = []
        self.texts.append(Text("NEW HIGH SCORE!", YELLOW, 6 * TILEWIDTH, 12 * TILEHEIGHT, int(TILEHEIGHT * 1.2)))
        self.texts.append(
            Text(str(self.new_score).zfill(8), WHITE, 9 * TILEWIDTH, 16 * TILEHEIGHT, int(TILEHEIGHT * 1.5)))
        self.texts.append(Text("CONGRATULATIONS!", WHITE, 6.5 * TILEWIDTH, 20 * TILEHEIGHT, TILEHEIGHT))

    def update(self, dt):
        self.timer += dt
        for text in self.texts:
            text.update(dt)
        return self.timer >= self.display_time

    def render(self):
        self.screen.fill(BLACK)
        for text in self.texts:
            text.render(self.screen)