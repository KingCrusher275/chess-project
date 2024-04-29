import pygame
from button import Button
class Sidebar:
    def __init__(self, colors, minWidth = 150, height = 20, heightPercent = 0.1, color="GRAY", hoverColor = "BLUE", textColor = "WHITE", padding=20, numButton = 3):
        self.minWidth = minWidth
        self.widthPercent = 0.8
        self.height = height
        self.heightPercent = heightPercent
        self.numButton = numButton
        self.colors = colors
        self.textColor = textColor

        self.buttons = [ 
            Button(0,0,0,0, self.colors[color], self.colors[hoverColor], self.colors[textColor], "arial", 20, "New Game"),
            Button(0,0,0,0, self.colors[color], self.colors[hoverColor], self.colors[textColor], "arial", 20, "Flip Board"),
            Button(0,0,0,0, self.colors[color], self.colors[hoverColor], self.colors[textColor], "arial", 20, "Settings")
        ]
        self.padding = padding 
        self.color = color

