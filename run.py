import pygame
from pygame.locals import *
from constants import *


# Define the main GameController class which manages the game lifecycle
class GameController(object):
    def __init__(self):
        pygame.init()

        # Create the game screen with the size specified in constants.py
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)

        # Placeholder for background surface
        self.background = None

    # Create a surface for the background and fill it with black
    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    # Set up the initial background (more setup can be added later)
    def start_game(self):
        self.set_background()

    # Process input events and update the display every frame
    def update(self):
        self.check_events()
        self.render()

    # Poll for events, such as window close
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                # Exit the game if the window is closed
                exit()

    # Refresh the screen to reflect any updates
    def render(self):
        pygame.display.update()


# Start the game if this script is run directly
if __name__ == "__main__":
    game = GameController()
    game.start_game()

    # Run the game loop indefinitely
    while True:
        game.update()
