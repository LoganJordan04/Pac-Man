from constants import *


# Manages frame-based animations by cycling through a list of frames over time.
class Animator(object):
    def __init__(self, frames=[], speed=20, loop=True):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False

    # Resets the animation to the first frame and re-enables playback.
    def reset(self):
        self.current_frame = 0
        self.finished = False

    # Updates the current frame based on elapsed time (dt).
    # If the animation finishes and is non-looping, it freezes on the last frame.
    def update(self, dt):
        if not self.finished:
            self.next_frame(dt)

        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                # Stay on the last valid frame
                self.current_frame -= 1

        return self.frames[self.current_frame]

    # Advances to the next frame if enough time (1/speed) has passed.
    # Resets time accumulator after each frame change.
    def next_frame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0
