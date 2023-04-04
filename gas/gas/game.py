"""This is the main module of the game. It provides a PyG class that runs the
graphics and the events"""

import pygame
from pygame.locals import *
# Ball and Walls are not directly callable
from engine import Mechanics
from pygame.math import Vector2

class Pyg(object):

    def __init__(self, width, height, fps):
        pygame.init()
        self.running = None
        self.screen = pygame.display.set_mode((width, height), DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.mechanics = Mechanics(width, height)

    def trace_balls(self):
        """Draws every ball at every frame, tracing its movement."""
        # This is a graphical method so it only draws balls, it doesn't
        # update the position, Mechanics does
        for ball in self.mechanics.ball_list:
            # blitting straight on ball.position would shift the surface away
            self.screen.blit(ball.surf, ball.position +
                                        Vector2(- ball.radius, - ball.radius))

    def event_manager(self):
        """Manages all events in the game"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                else:
                    self.mechanics.generate_ball()
            elif event == self.mechanics.collision:
                # Play a short audio clip (yet to script)
                pass

    def run(self):
        """Runs the main loop."""
        self.running = True
        while(self.running):
            self.screen.blit(self.background, (0, 0))
            self.mechanics.manage_collisions()
            self.event_manager()
            self.mechanics.move_balls(self.clock.tick(self.fps))
            self.trace_balls()
            pygame.display.flip()

        pygame.quit()

Pyg(800, 800, 30).run()
