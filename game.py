import pygame
import os
from square import Square

WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
GREEN = (0, 0, 255)

names = ['bpawn', 'wpawn', 'bknight', 'wknight', 'bbishop',
         'wbishop', 'brook', 'wrook', 'bqueen', 'wqueen', 'bking', 'wking']


class Game:
    def __init__(self):
        self.ROWS = 8
        self.COLS = 8
        self.clicked = False
        self.squareClicked = None
        self.game = [[Square(WHITE if (i+j) % 2 == 0 else BLACK, None) for i in range(self.COLS)]
                     for j in range(self.ROWS)]
        self.SQUARE_SIZE = 60
        self.turn = 1
        # self.castle =  Black Queenside Castle, White Queenside Castle, Black Kingside Castle, White Kingside Castle
        self.castle = [True for _ in range(4)]
        self.lastMove = None

    def drawBoard(self, screen):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                square = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                square_rect = square.get_rect()
                square.fill(
                    self.game[row][col].color if not self.game[row][col].clicked else GREEN)
                if (self.game[row][col].piece != None):

                    img = pygame.image.load(
                        os.path.join(
                            'public', f'{names[self.game[row][col].piece]}.png')
                    )
                    img = pygame.transform.scale(
                        img, (self.SQUARE_SIZE, self.SQUARE_SIZE))

                    piece_rect = img.get_rect()
                    piece_rect.center = square_rect.center
                    square.blit(img, piece_rect.topleft)
                screen.blit(square, (col * self.SQUARE_SIZE,
                            row * self.SQUARE_SIZE))

    def addStartingPosition(self):
        for i in range(8):
            self.game[1][i].piece = 0
            self.game[6][i].piece = 1

            if (i < 4):
                if (i == 0):
                    for k in (0, 7):
                        self.game[0][k].piece = 6
                        self.game[7][k].piece = 7
                elif (i == 1):
                    for k in (1, 6):
                        self.game[0][k].piece = 2
                        self.game[7][k].piece = 3
                elif (i == 2):
                    for k in (2, 5):
                        self.game[0][k].piece = 4
                        self.game[7][k].piece = 5
                else:
                    self.game[0][3].piece = 8
                    self.game[7][3].piece = 9
                    self.game[0][4].piece = 10
                    self.game[7][4].piece = 11
