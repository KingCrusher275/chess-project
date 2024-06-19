import pygame
import os
import sys
from button import Button
names = ['bpawn', 'wpawn', 'bknight', 'wknight', 'bbishop',
         'wbishop', 'brook', 'wrook', 'bqueen', 'wqueen', 'bking', 'wking']


class MenuDisplay:
    def __init__(self, context, color="GRAY", hoverColor = "BLUE", textColor = "WHITE", padding=20, widthPercent=0.2, heightPercent=0.1):
        self.context = context
        self.buttons = []
        self.buttons = [ 
            Button(0,0,0,0, self.context.colors[color], self.context.colors[hoverColor], self.context.colors[textColor], "arial", 20, "Single Player", self.singlePlayer),
            Button(0,0,0,0, self.context.colors[color], self.context.colors[hoverColor], self.context.colors[textColor], "arial", 20, "Two Player", self.twoPlayer)
        ]

        self.padding = padding
        self.widthPercent = widthPercent
        self.heightPercent = heightPercent
   
    def singlePlayer(self):
        print("single")
        pass
    def twoPlayer(self):
        print("double")
        pass
    def draw(self, screen):
        screen.fill(self.context.game_settings["bcolor"])
        # screen_size = (width, height)
        screen_size = screen.get_size()
        center_ypos = screen_size[0] // 2
        center_xpos = 0.3 * screen_size[1]

        button_width = screen_size[0] * self.widthPercent
        button_height = screen_size[1] * self.heightPercent
        xpos = center_xpos - (button_height // 2)
        ypos = center_ypos - (button_width // 2) 
        
        for i in range(len(self.buttons)):
            self.buttons[i].tlx = xpos + i * (button_height + self.padding)
            self.buttons[i].tly = ypos
            self.buttons[i].width = button_width
            self.buttons[i].height = button_height
            self.buttons[i].draw_button(screen)

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)



