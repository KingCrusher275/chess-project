import sys
import pygame
import os
from game import Game
from collections import defaultdict
from playdisplay import PlayDisplay
from playsidebar import PlaySidebar

from sharedcontext import SharedContext
from menustate import MenuState 
from playstate import PlayState
from settingstate import SettingState
from menudisplay import MenuDisplay

pygame.init()
size = width, height = 650, 480
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

class GameStateMachine:
    def __init__(self, initial_state, context):
        self.context = context
        self.current_state = initial_state

        pldisplay = PlayDisplay(context)
        plsidebar = PlaySidebar(context, pldisplay.setNewGame, pldisplay.setFlipBoard, pldisplay.setSettings)

        menudisplay = MenuDisplay(context)
        self.states = {
                "menu": MenuState(context, menudisplay, self),
                "play": PlayState(context, pldisplay, plsidebar, self),
                "setting": SettingState(context, None, self)
                }
        self.context = context

    def handleEvent(self, event):
        self.current_state.handleEvent(event)
    def change_state(self, new_state):
        if self.current_state is not None:
            self.current_state.exit()
        self.current_state = self.states[new_state]
        self.current_state.enter()

    def update(self, delta_time):
        if self.current_state is not None:
            self.current_state.update(delta_time)

    def handle_input(self, input):
        if self.current_state is not None:
            self.current_state.handle_input(input)

if __name__ == "__main__":
    clock = pygame.time.Clock()
    context = SharedContext(screen)
    gameMachine = GameStateMachine(None, context)
    gameMachine.change_state("play")
    # gameMachine.change_state("menu")
    while True:
        for event in pygame.event.get():
            gameMachine.handleEvent(event)
        pygame.display.flip()
        clock.tick(10)
