import pygame

class Button:
    def __init__(self, tlx, tly, width, height, color, hoverColor, textColor, font, fontSize, text, action): 
        self.tlx = tlx
        self.tly = tly
        self.width = width
        self.height = height
        self.color = color
        self.textColor = textColor
        self.hoverColor = hoverColor

        self.font = font
        self.fontSize = fontSize
        self.text = text  
        self.rect = pygame.Rect(self.tly, self.tlx, self.width, self.height)
        self.action = action
        self.curColor = color
    def draw_button(self, screen): 
        self.rect = pygame.Rect(self.tly, self.tlx, self.width, self.height)
        curFont = pygame.font.SysFont(self.font, self.fontSize)
        text = curFont.render(self.text, True, self.textColor)
        pygame.draw.rect(screen, self.curColor, self.rect)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handleEvent(self, event):
        if(event.type == pygame.MOUSEMOTION):
            mouse = event.pos
            if self.rect.collidepoint(mouse):
                self.curColor = self.hoverColor
            else:
                self.curColor = self.color
        elif(event.type == pygame.MOUSEBUTTONDOWN):
            mouse = event.pos
            if self.rect.collidepoint(mouse):
                self.action()

