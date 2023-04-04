"""Test user-defined events"""

import pygame
from pygame.locals import *

class PygView(object):

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800,800), pygame.DOUBLEBUF)
        self.user_typevent = None
        # Creates new userevent
        self.create_event()

    def create_event(self):
        self.user_typevent = pygame.event.Event(pygame.USEREVENT)

    def run(self):
        running = True

        while(running):
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event == self.user_typevent:
                    print("Userevent happened.")
                elif event.type == KEYDOWN:
                    pygame.event.post(self.user_typevent)

        pygame.quit()


PygView().run()
