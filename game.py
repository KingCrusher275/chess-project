import pygame
import os
from square import Square
from collections import defaultdict
import sys
symbolToIx = {'p':0, 'P':1, 'n':2, 'N':3, 'b':4, 'B':5, 'r':6, 'R':7, 'q':8, 'Q':9, 'k':10, 'K':11}
symbolToCastle = {'k':2, 'q':0, 'Q':1, 'K':3}
ixToSymbol = dict([(value, key) for key, value in symbolToIx.items()])
castleToSymbol = dict([(value, key) for key, value in symbolToCastle.items()])
ixToFile = dict([(i, chr(97+i)) for i in range(8)])
startingPosition = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" 
class Game:
    def __init__(self, fen=startingPosition):
        self.ROWS = 8
        self.COLS = 8
        self.clicked = False
        self.squareClicked = None
        self.game = [[Square("WHITE" if (i+j) % 2 == 0 else "BLACK", None) for i in range(self.COLS)]
                     for j in range(self.ROWS)]
        self.turn = 1
        # self.castle =  Black Queenside Castle, White Queenside Castle, Black Kingside Castle, White Kingside Castle
        self.castle = [False for _ in range(4)]
        self.lastMove = None
        self.end = False
        self.moveNumber = 0
        self.fiftyMove = 0
        self.load_fen(fen)
        
    def export_fen(self):
        fen_string = ""
        for i in range(8):
            cur = 0
            for j in range(8):
                if(self.game[i][j].piece != None):
                    if(cur != 0):
                        fen_string += str(cur)
                    fen_string += ixToSymbol[self.game[i][j].piece]
                    cur = 0
                else:
                    cur += 1
            if(cur != 0):
                fen_string += str(cur)
            if(i < 7):
                fen_string += "/"
        
        fen_string += " "
        if(self.turn == 1):
            fen_string += "w"
        else:
            fen_string += "b"

        fen_string += " "
        if(sum(self.castle) == 0):
            fen_string += "-"
        else:
            for i in [3, 1, 2, 0]: 
                if(self.castle[i]):
                    fen_string += castleToSymbol[i]
        fen_string += " "
        if(self.lastMove == None):
           fen_string += "-" 
        else:
            if(self.game[self.lastMove[1][1]][self.lastMove[1][0]].piece == 0):
                if(self.lastMove[0][0] == 1 and self.lastMove[1][0] - self.lastMove[0][0] == 2):
                    fen_string += f"{ixToFile[self.lastMove[0][1]]}3"
                else:
                    fen_string += "-"
            elif(self.game[self.lastMove[1][1]][self.lastMove[1][0]].piece == 1):
                if(self.lastMove[0][0] == 6 and self.lastMove[1][0] - self.lastMove[0][0] == -2):
                    fen_string += "{ixToFile[self.lastMove[0][1]]}6"
                else:
                    fen_string += "-"
            else:
                fen_string += "-"

        fen_string += f" {self.fiftyMove} {self.moveNumber}"
        return fen_string
    def load_fen(self, position):
        parts = position.split(' ')
        for i in range(len(parts)):
            if(i == 0):
                ranks = parts[i].split('/')
                for j in range(len(ranks)):
                    cur = 0
                    for k in ranks[j]:
                        val = ord(k)
                        if(val >= 49 and val <= 56):
                            val -= 48
                            cur += val
                        else:
                            self.game[j][cur].piece = symbolToIx[k]
                            cur += 1
            elif(i == 1):
                if(parts[i] == 'w'):
                    self.turn = 1
                else:
                    self.turn = 0
            elif(i == 2):
                for j in parts[i]:
                    if(j == 'K'):
                        self.castle[3] = True
                    elif(j == 'Q'):
                        self.castle[1] = True
                    elif(j == 'k'):
                        self.castle[2] = True
                    elif(j == 'q'):
                        self.castle[0] = True
            elif(i == 3):
                if(parts[i] != '-'):
                    file = ord(parts[i][0]) - 97
                    rank = int(parts[i][1]) - 1
                    if(rank == 3):
                        self.lastMove = ((6, file), (4, file))
                    else:
                        self.lastMove = ((1, file), (3, file))
            elif(i == 4):
                self.fiftyMove = int(parts[i])
            elif(i == 5):
                self.moveNumber = int(parts[i])
    def addStartingPosition(self):
        self.load_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

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
                        elif (event.key == pygame.K_k):
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

    def generateAllMoves(self, color):
        moves = defaultdict(list)
        for i in range(8):
            for j in range(8):
                if (self.game[i][j].piece != None and self.game[i][j].piece % 2 == color):
                    moves[(i, j)] += self.generateMove(i, j)
        return moves

    def makeMove(self, x, y, fx, fy):
        cur = self.game[x][y].piece
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

    def gameEnd(self):
        color = self.turn
        moves = self.generateAllMoves(color)
        if(self.fiftyMove >= 50):
            return 0
        for l in moves.values():
            if (len(l) > 0):
                return 2
        if (self.inCheck(color)):
            if (color == 0):
                return 1
            else:
                return -1
        else:
            return 0

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
