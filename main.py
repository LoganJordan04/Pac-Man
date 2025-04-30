import pygame
import sys

# Initialize Pygame
pygame.init()

# Define dimensions for a 3:4 window (width:height)
width = 600
height = 800

# Create the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with black (optional)
    screen.fill((0, 0, 0))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


