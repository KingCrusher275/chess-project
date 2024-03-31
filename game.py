import pygame
import os
from square import Square
from collections import defaultdict
import sys

WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

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
        self.end = False

    def drawBoard(self, screen):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                square = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                square_rect = square.get_rect()
                if (self.game[row][col].clicked):
                    square.fill(BLUE)
                elif (self.game[row][col].possibleMove):
                    square.fill(GREEN)
                else:
                    square.fill(self.game[row][col].color)
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

    def promotion(self, x, y, fx, fy, cur):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_q or event.key == pygame.K_r or event.key == pygame.K_k or event.key == pygame.K_b):
                        if (event.key == pygame.K_q):
                            self.game[fx][fy].piece = 8 + cur
                            self.game[x][y].piece = None
                        elif (event.key == pygame.K_r):
                            self.game[fx][fy].piece = 6 + cur
                            self.game[x][y].piece = None
                        elif (event.key == pygame.K_b):
                            self.game[fx][fy].piece = 4 + cur
                            self.game[x][y].piece = None
                        elif (event.key == pygame.K_b):
                            self.game[fx][fy].piece = 2 + cur
                            self.game[x][y].piece = None

                        return

    def togglePossibleMoves(self, x, y):
        validMoves = self.generateMove(x, y)
        for move in validMoves:
            self.game[move[0]][move[1]
                               ].possibleMove = not self.game[move[0]][move[1]].possibleMove

    def inCheck(self, color):
        moves = defaultdict(list)
        px, py = -1, -1
        for i in range(8):
            for j in range(8):
                if (self.game[i][j].piece != None and self.game[i][j].piece % 2 != color):
                    if (self.game[i][j].piece == 0 or self.game[i][j].piece == 1):
                        moves[(i, j)] += self.pawnMove(i, j)
                    if (self.game[i][j].piece == 2 or self.game[i][j].piece == 3):
                        moves[(i, j)] += self.knightMove(i, j)
                    if (self.game[i][j].piece == 4 or self.game[i][j].piece == 5 or self.game[i][j].piece == 8 or self.game[i][j].piece == 9):
                        moves[(i, j)] += self.bishopMove(i, j)
                    if (self.game[i][j].piece == 6 or self.game[i][j].piece == 7 or self.game[i][j].piece == 8 or self.game[i][j].piece == 9):
                        moves[(i, j)] += self.rookMove(i, j)
                elif (self.game[i][j].piece == 10 or self.game[i][j].piece == 11 and self.game[i][j].piece % 2 == color):
                    px, py = i, j

        for mov in moves.values():
            if ((px, py) in mov):
                return True
        return False

    def makeMove(self, x, y, fx, fy):
        cur = self.game[x][y].piece
        # print(cur)
        self.lastMove = ((x, y), (fx, fy))
        if ((cur == 0 or cur == 1) and (abs(fx - x) == 1 and abs(fy - y) == 1 and self.game[fx][fy].piece == None)):
            self.game[fx][fy].piece = self.game[x][y].piece
            self.game[x][y].piece = None
            self.game[x][fy].piece = None
        elif ((cur == 0 or cur == 1) and (fx == 0 or fx == 7)):
            self.promotion(x, y, fx, fy, cur)
        elif ((cur == 10 or cur == 11) and (abs(fy-y) > 1)):
            if (fy - y > 1):
                mult = 1
            else:
                mult = -1
            if (cur == 10):
                rank = 0
            else:
                rank = 7
            self.game[rank][4+2*mult].piece = self.game[rank][4].piece
            self.game[rank][4].piece = None
            if (fy - y > 1):
                self.game[rank][5].piece = self.game[rank][7].piece
                self.game[rank][7].piece = None
            else:
                self.game[rank][3].piece = self.game[rank][0].piece
                self.game[rank][0].piece = None
        else:
            self.game[fx][fy].piece = self.game[x][y].piece
            self.game[x][y].piece = None

        if (cur == 10 or cur == 11):
            self.castle[cur % 2] = False
            self.castle[2 + cur % 2] = False
        if ((x == 0 and y == 0) or (fx == 0 and fy == 0)):
            self.castle[0] = False
        if ((x == 0 and y == 7) or (fx == 0 and fy == 7)):
            self.castle[2] = False
        if ((x == 7 and y == 0) or (fx == 7 and fy == 0)):
            self.castle[1] = False
        if ((x == 7 and y == 7) or (fx == 7 and fy == 7)):
            self.castle[3] = False

    def validateMove(self, x, y, fx, fy):
        moves = self.generateMove(x, y)
        if ((fx, fy) in moves):
            return True
        else:
            return False

    def generateMove(self, x, y):
        moves = []
        cur = self.game[x][y].piece
        if (cur == 0 or cur == 1):
            moves += self.pawnMove(x, y)
        if (cur == 2 or cur == 3):
            moves += self.knightMove(x, y)
        if (cur == 4 or cur == 5 or cur == 8 or cur == 9):
            moves += self.bishopMove(x, y)
        if (cur == 6 or cur == 7 or cur == 8 or cur == 9):
            moves += self.rookMove(x, y)
        if (cur == 10 or cur == 11):
            moves += self.kingMove(x, y)

        validmoves = []
        for (fx, fy) in moves:
            if ((cur == 0 or cur == 1) and (abs(fx - x) == 1 and abs(fy - y) == 1 and self.game[fx][fy].piece == None)):
                tmp = self.game[x][fy].piece
                self.game[fx][fy].piece = self.game[x][y].piece
                self.game[x][y].piece = None
                self.game[x][fy].piece = None

                if (not self.inCheck(cur % 2)):
                    validmoves.append((fx, fy))

                self.game[x][y].piece = self.game[fx][fy].piece
                self.game[fx][fy].piece = None
                self.game[x][fy].piece = tmp
            elif ((cur == 10 or cur == 11) and (abs(fy-y) > 1)):
                if (fy - y > 1):
                    mult = 1
                else:
                    mult = -1
                if (cur == 10):
                    rank = 0
                else:
                    rank = 7

                works = True
                for i in range(3):
                    tmp = self.game[rank][4+i*mult].piece
                    if (self.inCheck(cur % 2)):

                        self.game[rank][4+i*mult].piece = None
                        self.game[rank][4].piece = tmp

                        works = False
                        break
                    if (i == 2):
                        self.game[rank][4+i*mult].piece = None
                        self.game[rank][4].piece = tmp

                        break
                    self.game[rank][4+(i+1) *
                                    mult].piece = self.game[rank][4+i*mult].piece
                    self.game[rank][4+i*mult].piece = None
                if (works):
                    validmoves.append((fx, fy))
            else:
                tmp = self.game[fx][fy].piece
                self.game[fx][fy].piece = self.game[x][y].piece
                self.game[x][y].piece = None
                if (not self.inCheck(cur % 2)):
                    validmoves.append((fx, fy))

                self.game[x][y].piece = self.game[fx][fy].piece
                self.game[fx][fy].piece = tmp
        return validmoves

    def gameEnd():
        pass

    def bishopMove(self, x, y):
        moves = []
        dx = [-1, 1, -1, 1]
        dy = [1, -1, -1, 1]
        for dxx, dyy in zip(dx, dy):
            mult = 1
            while (x + dxx * mult >= 0 and x + dxx * mult < 8 and y + dyy * mult >= 0 and y + dyy * mult < 8):
                if (self.game[x+dxx*mult][y+dyy*mult].piece == None):
                    moves.append((x+dxx*mult, y+dyy*mult))
                elif (self.game[x+dxx*mult][y+dyy*mult].piece % 2 != self.game[x][y].piece % 2):
                    moves.append((x+dxx*mult, y+dyy*mult))
                    break
                else:
                    break
                mult += 1

        return moves

    def rookMove(self, x, y):
        moves = []
        d = [-1, 1]
        for i in d:
            mult = 1
            while (x + i * mult >= 0 and x + i * mult < 8):
                if (self.game[x+i*mult][y].piece == None):
                    moves.append((x+i*mult, y))
                elif (self.game[x+i*mult][y].piece % 2 != self.game[x][y].piece % 2):
                    moves.append((x+i*mult, y))
                    break
                else:
                    break
                mult += 1
            mult = 1
            while (y + i * mult >= 0 and y + i * mult < 8):
                if (self.game[x][y+i*mult].piece == None):
                    moves.append((x, y+i*mult))
                elif (self.game[x][y+i*mult].piece % 2 != self.game[x][y].piece % 2):
                    moves.append((x, y+i*mult))
                    break
                else:
                    break
                mult += 1

        return moves

    def knightMove(self, x, y):
        moves = []
        dx = [2, 1]
        dy = [1, 2]
        for i in range(2):
            for j in (-dx[i], dx[i]):
                for k in (-dy[i], dy[i]):
                    if (x + j < 8 and x + j >= 0 and y + k < 8 and y + k >= 0):
                        if (self.game[x+j][y+k].piece == None or self.game[x+j][y+k].piece % 2 != self.game[x][y].piece % 2):
                            moves.append((x+j, y+k))

        return moves

    def kingMove(self, x, y):
        moves = []
        dx = [-1, 0, 1]
        dy = [-1, 0, 1]
        for i in dx:
            for j in dy:
                if (x + i < 8 and x + i >= 0 and y + j >= 0 and y + j < 8):
                    if (self.game[x+i][y+j].piece == None or self.game[x+i][y+j].piece % 2 != self.game[x][y].piece % 2):
                        moves.append((x+i, y+j))
        rank = 0
        ix = 0
        if (self.game[x][y].piece % 2 == 1):
            rank = 7
            ix = 1
        if (self.castle[ix+2]):
            if (self.game[rank][5].piece == None and self.game[rank][6].piece == None):
                moves.append((rank, 6))
        if (self.castle[ix]):
            if (self.game[rank][1].piece == None and self.game[rank][2].piece == None and self.game[rank][3].piece == None):
                moves.append((rank, 2))
        return moves

    def pawnMove(self, x, y):
        moves = []
        if (self.game[x][y].piece % 2 == 0):
            mult = 1
            rank = 1
        else:
            mult = -1
            rank = 6
        if (self.game[x+mult][y].piece == None):
            moves.append((x+mult, y))
            if (x == rank and self.game[x+2*mult][y].piece == None):
                moves.append((x+2*mult, y))

        if ((y < 7 and self.game[x+mult][y+1].piece != None and self.game[x+mult][y+1].piece % 2 != self.game[x][y].piece % 2)
            or (y < 7 and self.game[x][y+1].piece != None and self.game[x][y+1].piece % 2 != self.game[x][y].piece % 2 and
                (self.game[x][y+1].piece == 0 or self.game[x][y+1].piece == 1) and self.lastMove[1] == (x, y+1) and
                self.lastMove[1][0] - self.lastMove[0][0] == -2 * mult)):
            moves.append((x+mult, y+1))
        if ((y > 0 and self.game[x+mult][y-1].piece != None and self.game[x+mult][y-1].piece % 2 != self.game[x][y].piece % 2)
            or (y > 0 and self.game[x][y-1].piece != None and self.game[x][y-1].piece % 2 != self.game[x][y].piece % 2 and
                (self.game[x][y-1].piece == 0 or self.game[x][y-1].piece == 1) and
                self.lastMove[1] == (x, y-1) and self.lastMove[1][0] - self.lastMove[0][0] == -2 * mult)):
            moves.append((x+mult, y-1))

        return moves
