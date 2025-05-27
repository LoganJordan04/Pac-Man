class Pause(object):
    def __init__(self, paused=False):
        # Flag to indicate if the game is currently paused
        self.paused = paused

        self.timer = 0

        # Duration for which the game should remain paused (in seconds)
        self.pauseTime = None

        # Optional function to call after the pause ends
        self.func = None

    # Should be called every frame. Tracks pause duration and resumes gameplay
    # when the timer expires. If a function was provided via set_pause, returns it when the pause ends.
    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                # Time to resume the game
                self.timer = 0
                self.paused = False
                self.pauseTime = None

                # # Trigger follow-up function if any
                return self.func
        return None

    # Initiates a pause. You can specify:
    # - playerPaused: Manual pause triggered by player (e.g. key press)
    # - pauseTime: Duration of timed pause in seconds
    # - func: Optional callback to execute once pause ends
    def set_pause(self, playerPaused=False, pauseTime=None, func=None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime

        # Toggle pause state
        self.flip()

    # Reverses the paused state: pause if running, resume if paused.
    def flip(self):
        self.paused = not self.paused
