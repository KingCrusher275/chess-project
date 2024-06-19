import pygame
from button import Button
class PlaySidebar:
    def __init__(self, context, new_game_callback, flip_board_callback, settings_callback, minWidth = 150, height = 20, heightPercent = 0.1, color="GRAY", hoverColor = "BLUE", textColor = "WHITE", padding=20, numButton = 3):

        self.context = context
        self.minWidth = minWidth
        self.widthPercent = 0.8
        self.height = height
        self.heightPercent = heightPercent
        self.numButton = numButton
        self.textColor = textColor

        self.buttons = [ 
            Button(0,0,0,0, self.context.colors[color], self.context.colors[hoverColor], self.context.colors[textColor], "arial", 20, "New Game", new_game_callback),
            Button(0,0,0,0, self.context.colors[color], self.context.colors[hoverColor], self.context.colors[textColor], "arial", 20, "Flip Board", flip_board_callback),
            Button(0,0,0,0, self.context.colors[color], self.context.colors[hoverColor], self.context.colors[textColor], "arial", 20, "Settings", settings_callback)
        ]
        self.padding = padding 
        self.color = color

    def handleEvent(self,event):
        for button in self.buttons:
            button.handleEvent(event)
