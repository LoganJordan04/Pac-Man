from constants import *


# Controls the alternation between scatter and chase modes based on time intervals.
class MainMode(object):
    def __init__(self):
        # Tracks time elapsed in current mode and starts in scatter mode
        self.timer = 0
        self.scatter()

    # Updates the internal timer and switches between scatter and chase
    # when the current mode's duration is complete.
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    # Switch to scatter mode, which sends ghosts to their corners.
    def scatter(self):
        self.mode = SCATTER

        # Duration of mode (in seconds)
        self.time = 7

        # Reset timer
        self.timer = 0

    # Switch to chase mode, which makes ghosts pursue Pac-Man.
    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0


# Manages the active mode for a specific ghost, including:
# - Main mode switching (scatter <-> chase)
# - Temporary override modes (freight, spawn)
class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None

        # Base scatter/chase timer logic
        self.mainmode = MainMode()

        # Currently active mode
        self.current = self.mainmode.mode

        # Reference to the ghost this controller manages
        self.entity = entity

    # Update mode logic every frame. Handles transitions for all ghost modes.
    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            # Stay in frightened mode until timer expires
            self.timer += dt
            if self.timer >= self.time:
                self.time = None

                # Restore normal speed and behavior
                self.entity.normal_mode()

                # Resume normal scatter/chase cycle
                self.current = self.mainmode.mode

        elif self.current in [SCATTER, CHASE]:
            # Mirror the current main mode if in standard mode
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            # Exit spawn mode if the ghost reaches the spawn node
            if self.entity.node == self.entity.spawnNode:
                self.entity.normal_mode()
                self.current = self.mainmode.mode

    # Transitions a ghost to spawn mode (used after being eaten).
    def set_spawn_mode(self):
        if self.current is FREIGHT:
            self.current = SPAWN

    # Transitions a ghost to freight mode.
    # Only works if currently in chase or scatter mode.
    def set_freight_mode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0

            # Duration of frightened state
            self.time = 7

            self.current = FREIGHT
        elif self.current is FREIGHT:
            # Restart the fright timer if already in frightened mode
            self.timer = 0
