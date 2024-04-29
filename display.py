import pygame
import os

names = ['bpawn', 'wpawn', 'bknight', 'wknight', 'bbishop',
         'wbishop', 'brook', 'wrook', 'bqueen', 'wqueen', 'bking', 'wking']


class Display:
    def __init__(self, game, sidebar, colors, SQUARE_SIZE=60):
        self.SQUARE_SIZE = SQUARE_SIZE 
        self.game = game
        self.sidebar = sidebar
        self.colors = colors
        
    def drawBoard(self, screen):
        screen.fill(self.colors["BROWN"])

        # screen_size = (width, height)
        screen_size = screen.get_size()
        self.SQUARE_SIZE = min(screen_size[1], screen_size[0] - self.sidebar.minWidth) // 8
        for row in range(self.game.ROWS):
            for col in range(self.game.COLS):
                square = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                square_rect = square.get_rect()
                if (self.game.game[row][col].clicked):
                    square.fill(self.colors["BLUE"])
                elif (self.game.game[row][col].possibleMove):
                    square.fill(self.colors["GREEN"])
                else:
                    square.fill(self.colors[self.game.game[row][col].color])
                if (self.game.game[row][col].piece != None):

                    img = pygame.image.load(
                        os.path.join(
                            'public', f'{names[self.game.game[row][col].piece]}.png')
                    )
                    img = pygame.transform.scale(
                        img, (self.SQUARE_SIZE, self.SQUARE_SIZE))

                    piece_rect = img.get_rect()
                    piece_rect.center = square_rect.center
                    square.blit(img, piece_rect.topleft)
                screen.blit(square, (col * self.SQUARE_SIZE,
                            row * self.SQUARE_SIZE))

    def drawSidebar(self, screen):
        # screen_size = (width, height)
    

        screen_size = screen.get_size()
        center_ypos = min(screen_size[1], screen_size[0] - self.sidebar.minWidth) + (screen_size[0] - self.SQUARE_SIZE * 8)//2
        center_xpos = 0.1 * screen_size[1]

        button_width = (screen_size[0] - self.SQUARE_SIZE * 8) * self.sidebar.widthPercent
        button_height = screen_size[1] * self.sidebar.heightPercent
        xpos = center_xpos - (button_height // 2)
        ypos = center_ypos - (button_width // 2) 
        
        for i in range(self.sidebar.numButton):
            self.sidebar.buttons[i].tlx = xpos + i * (button_height + self.sidebar.padding)
            self.sidebar.buttons[i].tly = ypos
            self.sidebar.buttons[i].width = button_width
            self.sidebar.buttons[i].height = button_height
            self.sidebar.buttons[i].draw_button(screen)
         





