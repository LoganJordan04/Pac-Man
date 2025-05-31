import pygame
import json
import os
from pygame.locals import *
from constants import *
from vector import Vector2
from text import Text
from sprites import Spritesheet


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
        # Blink every 0.5 seconds
        self.blink_speed = 0.5
        self.show_start_text = True

    # Create all menu text elements
    def setup_text(self):
        self.texts = []

        # Load the spritesheet once so we can render the ghosts
        self.spritesheet = Spritesheet()

        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        self.logo_image = pygame.image.load(logo_path).convert_alpha()
        logo_w = int(18 * TILEWIDTH)
        logo_h = int(4 * TILEHEIGHT)
        self.logo_image = pygame.transform.scale(self.logo_image, (logo_w, logo_h))
        self.logo_pos = (4.75 * TILEWIDTH, 2 * TILEHEIGHT)

        self.texts.append(Text("CHARACTER / NICKNAME", WHITE, 7.25 * TILEWIDTH, 8.5 * TILEHEIGHT, int(TILEHEIGHT * 0.8)))

        ghost_y = 10.5 * TILEHEIGHT
        self.texts.append(Text("-SHADOW", RED, 8 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"BLINKY"', RED, 16 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        blinky_img = self.spritesheet.get_image(0, 10, 2 * TILEWIDTH, 2 * TILEHEIGHT)

        ghost_y += 2.2 * TILEHEIGHT
        self.texts.append(Text("-SPEEDY", PINK, 8 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"PINKY"', PINK, 16 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        pinky_img = self.spritesheet.get_image(2, 10, 2 * TILEWIDTH, 2 * TILEHEIGHT)

        ghost_y += 2.2 * TILEHEIGHT
        self.texts.append(Text("-BASHFUL", TEAL, 8 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"INKY"', TEAL, 16 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        inky_img  = self.spritesheet.get_image(4, 10, 2 * TILEWIDTH, 2 * TILEHEIGHT)

        ghost_y += 2.2 * TILEHEIGHT
        self.texts.append(Text("-POKEY", ORANGE, 8 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        self.texts.append(Text('"CLYDE"', ORANGE, 16 * TILEWIDTH, ghost_y, int(TILEHEIGHT * 0.8)))
        clyde_img = self.spritesheet.get_image(6, 10, 2 * TILEWIDTH, 2 * TILEHEIGHT)

        # Store all ghost images alongside their Y-coordinates
        self.ghost_sprites = [
            (blinky_img, (5 * TILEWIDTH, 9.75 * TILEHEIGHT)),
            (pinky_img, (5 * TILEWIDTH, 11.95 * TILEHEIGHT)),
            (inky_img, (5 * TILEWIDTH, 14.15 * TILEHEIGHT)),
            (clyde_img, (5 * TILEWIDTH, 16.35 * TILEHEIGHT)),
        ]

        points_y = 20 * TILEHEIGHT
        self.texts.append(Text("10 PTS", WHITE, 8 * TILEWIDTH, points_y, int(TILEHEIGHT * 0.75)))
        self.texts.append(Text("50 PTS", WHITE, 16 * TILEWIDTH, points_y, int(TILEHEIGHT * 0.75)))

        high_score = self.high_score_manager.get_high_score()
        self.texts.append(Text("HIGH SCORE", WHITE, 9 * TILEWIDTH, 24 * TILEHEIGHT, TILEHEIGHT))
        self.texts.append(Text(str(high_score).zfill(8), WHITE, 10 * TILEWIDTH, 25.25 * TILEHEIGHT, TILEHEIGHT))

        self.start_text = Text(
            "PRESS SPACEBAR", YELLOW, 5.75 * TILEWIDTH, 29 * TILEHEIGHT, int(TILEHEIGHT * 1.2)
        )

        self.texts.append(Text(
            "PROFESSIONAL BODYBUILDERS", PINK, 4.75 * TILEWIDTH, 33 * TILEHEIGHT, int(TILEHEIGHT * 0.8)
        ))

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

        # Draw the logo
        self.screen.blit(self.logo_image, self.logo_pos)

        # Draw ghost sprites
        for ghost_img, pos in self.ghost_sprites:
            self.screen.blit(ghost_img, pos)

        # Draw all text
        for text in self.texts:
            text.render(self.screen)

        # Draw the pellets for points
        points_y = 20.35 * TILEHEIGHT
        pygame.draw.circle(self.screen, WHITE, (7.25 * TILEWIDTH, points_y), int(2 * TILEWIDTH / 16))
        pygame.draw.circle(self.screen, WHITE, (14.75 * TILEWIDTH, points_y), int(8 * TILEWIDTH / 16))

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
            Text(str(self.new_score).zfill(8), WHITE, 8.5 * TILEWIDTH, 16 * TILEHEIGHT, int(TILEHEIGHT * 1.5)))
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