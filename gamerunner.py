import sys
import pygame
import os
from game import Game
from collections import defaultdict
pygame.init()
size = width, height = 480, 480
screen = pygame.display.set_mode(size)
names = ['bpawn', 'wpawn', 'bknight', 'wknight', 'bbishop',
         'wbishop', 'brook', 'wrook', 'bqueen', 'wqueen', 'bking', 'wking']


def bishopMove(x, y):
    moves = []
    dx = [-1, 1, -1, 1]
    dy = [1, -1, -1, 1]
    for dxx, dyy in zip(dx, dy):
        mult = 1
        while (x + dxx * mult >= 0 and x + dxx * mult < 8 and y + dyy * mult >= 0 and y + dyy * mult < 8):
            if (cgame.game[x+dxx*mult][y+dyy*mult].piece == None):
                moves.append((x+dxx*mult, y+dyy*mult))
            elif (cgame.game[x+dxx*mult][y+dyy*mult].piece % 2 != cgame.game[x][y].piece % 2):
                moves.append((x+dxx*mult, y+dyy*mult))
                break
            else:
                break
            mult += 1

    return moves


def rookMove(x, y):
    moves = []
    d = [-1, 1]
    for i in d:
        mult = 1
        while (x + i * mult >= 0 and x + i * mult < 8):
            if (cgame.game[x+i*mult][y].piece == None):
                moves.append((x+i*mult, y))
            elif (cgame.game[x+i*mult][y].piece % 2 != cgame.game[x][y].piece % 2):
                moves.append((x+i*mult, y))
                break
            else:
                break
            mult += 1
        mult = 1
        while (y + i * mult >= 0 and y + i * mult < 8):
            if (cgame.game[x][y+i*mult].piece == None):
                moves.append((x, y+i*mult))
            elif (cgame.game[x][y+i*mult].piece % 2 != cgame.game[x][y].piece % 2):
                moves.append((x, y+i*mult))
                break
            else:
                break
            mult += 1

    return moves


def knightMove(x, y):
    moves = []
    dx = [2, 1]
    dy = [1, 2]
    for i in range(2):
        for j in (-dx[i], dx[i]):
            for k in (-dy[i], dy[i]):
                if (x + j < 8 and x + j >= 0 and y + k < 8 and y + k >= 0):
                    if (cgame.game[x+j][y+k].piece == None or cgame.game[x+j][y+k].piece % 2 != cgame.game[x][y].piece % 2):
                        moves.append((x+j, y+k))

    return moves


def kingMove(x, y):
    color = cgame.game[x][y].piece % 2
    moves = []
    dx = [-1, 0, 1]
    dy = [-1, 0, 1]
    for i in dx:
        for j in dy:
            if (x + i < 8 and x + i >= 0 and y + j >= 0 and y + j < 8):
                if (cgame.game[x+i][y+j].piece == None or cgame.game[x+i][y+j].piece % 2 != cgame.game[x][y].piece % 2):
                    moves.append((x+i, y+j))
    rank = 0
    ix = 0
    if (cgame.game[x][y].piece % 2 == 1):
        rank = 7
        ix = 1
    if (cgame.castle[ix] and not inCheck(color)):
        if (cgame.game[rank][5].piece == None and cgame.game[rank][6].piece == None):
            moves.append((rank, 6))
    if (cgame.castle[ix+2] and not inCheck(color)):
        if (cgame.game[rank][1].piece == None and cgame.game[rank][2].piece == None and cgame.game[rank][3].piece == None):
            moves.append((rank, 2))
    else:
        pass
    return moves


def pawnMove(x, y):
    moves = []
    if (cgame.game[x][y].piece % 2 == 0):
        mult = 1
        rank = 1
    else:
        mult = -1
        rank = 6
    if (cgame.game[x+mult][y].piece == None):
        moves.append((x+mult, y))
        if (x == rank and cgame.game[x+2*mult][y].piece == None):
            moves.append((x+2*mult, y))

    if ((y < 7 and cgame.game[x+mult][y+1].piece != None and cgame.game[x+mult][y+1].piece % 2 != cgame.game[x][y].piece % 2)
        or (y < 7 and cgame.game[x][y+1].piece != None and cgame.game[x][y+1].piece % 2 != cgame.game[x][y].piece % 2 and
            (cgame.game[x][y+1].piece == 0 or cgame.game[x][y+1].piece == 1) and cgame.lastMove[1] == (x, y+1) and
            cgame.lastMove[1][0] - cgame.lastMove[0][0] == -2 * mult)):
        moves.append((x+mult, y+1))
    if ((y > 0 and cgame.game[x+mult][y-1].piece != None and cgame.game[x+mult][y-1].piece % 2 != cgame.game[x][y].piece % 2)
        or (y > 0 and cgame.game[x][y-1].piece != None and cgame.game[x][y-1].piece % 2 != cgame.game[x][y].piece % 2 and
            (cgame.game[x][y-1].piece == 0 or cgame.game[x][y-1].piece == 1) and
            cgame.lastMove[1] == (x, y-1) and cgame.lastMove[1][0] - cgame.lastMove[0][0] == -2 * mult)):
        moves.append((x+mult, y-1))

    return moves


def handleMove(event):
    y, x = event.dict['pos']
    relx, rely = x // cgame.SQUARE_SIZE, y // cgame.SQUARE_SIZE
    if (cgame.game[relx][rely].clicked):
        cgame.game[relx][rely].clicked = False
        cgame.clicked = False
    elif (not cgame.clicked and cgame.game[relx][rely].piece != None and cgame.game[relx][rely].piece % 2 == cgame.turn):
        cgame.game[relx][rely].clicked = True
        cgame.clicked = True
        cgame.squareClicked = (relx, rely)
    elif (cgame.clicked):
        if (cgame.game[relx][rely].piece != None and cgame.game[relx][rely].piece % 2 == cgame.game[cgame.squareClicked[0]][cgame.squareClicked[1]].piece % 2):
            cgame.game[relx][rely].clicked = True
            cgame.game[cgame.squareClicked[0]
                       ][cgame.squareClicked[1]].clicked = False
            cgame.squareClicked = (relx, rely)
        elif (validateMove(cgame.squareClicked[0], cgame.squareClicked[1], relx, rely)):
            makeMove(cgame.squareClicked[0],
                     cgame.squareClicked[1], relx, rely)
            cgame.clicked = False
            cgame.game[cgame.squareClicked[0]
                       ][cgame.squareClicked[1]].clicked = False
            cgame.turn = 1 - cgame.turn


def inCheck(color):
    moves = defaultdict(list)
    px, py = -1, -1
    for i in range(8):
        for j in range(8):
            if (cgame.game[i][j].piece != None and cgame.game[i][j].piece % 2 != color):
                if (cgame.game[i][j].piece == 0 or cgame.game[i][j].piece == 1):
                    moves[(i, j)] += pawnMove(i, j)
                if (cgame.game[i][j].piece == 2 or cgame.game[i][j].piece == 3):
                    moves[(i, j)] += knightMove(i, j)
                if (cgame.game[i][j].piece == 4 or cgame.game[i][j].piece == 5 or cgame.game[i][j].piece == 8 or cgame.game[i][j].piece == 9):
                    moves[(i, j)] += bishopMove(i, j)
                if (cgame.game[i][j].piece == 6 or cgame.game[i][j].piece == 7 or cgame.game[i][j].piece == 8 or cgame.game[i][j].piece == 9):
                    moves[(i, j)] += rookMove(i, j)
            elif (cgame.game[i][j].piece == 10 or cgame.game[i][j].piece == 11 and cgame.game[i][j].piece % 2 == color):
                px, py = i, j

    for mov in moves.values():
        if ((px, py) in mov):
            return True
    return False


def makeMove(x, y, fx, fy):
    cur = cgame.game[x][y].piece
    # print(cur)
    cgame.lastMove = ((x, y), (fx, fy))
    if ((cur == 0 or cur == 1) and (abs(fx - x) == 1 and abs(fy - y) == 1 and cgame.game[fx][fy].piece == None)):
        cgame.game[fx][fy].piece = cgame.game[x][y].piece
        cgame.game[x][y].piece = None
        cgame.game[x][fy].piece = None
    elif ((cur == 10 or cur == 11) and (abs(fy-y) > 1)):
        if (fy - y > 1):
            mult = 1
        else:
            mult = -1
        if (cur == 10):
            rank = 0
        else:
            rank = 7
        cgame.game[rank][4+2*mult].piece = cgame.game[rank][4].piece
        cgame.game[rank][4].piece = None
        if (fy - y > 1):
            cgame.game[rank][5].piece = cgame.game[rank][7].piece
            cgame.game[rank][7].piece = None
        else:
            cgame.game[rank][3].piece = cgame.game[rank][0].piece
            cgame.game[rank][0].piece = None
    else:
        cgame.game[fx][fy].piece = cgame.game[x][y].piece
        cgame.game[x][y].piece = None

    if (cur == 10 or cur == 11):
        cgame.castle[cur % 2] = False
        cgame.castle[2 + cur % 2] = False
    elif (x == 0 and y == 0):
        cgame.castle[0] = False
    elif (x == 0 and y == 7):
        cgame.castle[2] = False
    elif (x == 7 and y == 0):
        cgame.castle[1] = False
    elif (x == 7 and y == 7):
        cgame.castle[3] = False


def validateMove(x, y, fx, fy):
    moves = generateMove(x, y)
    if ((fx, fy) in moves):
        return True
    else:
        return False


def generateMove(x, y):
    moves = []
    cur = cgame.game[x][y].piece
    if (cur == 0 or cur == 1):
        moves += pawnMove(x, y)
    if (cur == 2 or cur == 3):
        moves += knightMove(x, y)
    if (cur == 4 or cur == 5 or cur == 8 or cur == 9):
        moves += bishopMove(x, y)
    if (cur == 6 or cur == 7 or cur == 8 or cur == 9):
        moves += rookMove(x, y)
    if (cur == 10 or cur == 11):
        moves += kingMove(x, y)

    validmoves = []
    for (fx, fy) in moves:
        if ((cur == 0 or cur == 1) and (abs(fx - x) == 1 and abs(fy - y) == 1 and cgame.game[fx][fy].piece == None)):
            tmp = cgame.game[x][fy].piece
            cgame.game[fx][fy].piece = cgame.game[x][y].piece
            cgame.game[x][y].piece = None
            cgame.game[x][fy].piece = None

            if (not inCheck(cur % 2)):
                validmoves.append((fx, fy))

            cgame.game[x][y].piece = cgame.game[fx][fy].piece
            cgame.game[fx][fy].piece = None
            cgame.game[x][fy].piece = tmp
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
                if (inCheck(cur % 2)):
                    cgame.game[rank][4].piece = cgame.game[rank][4+i*mult].piece
                    cgame.game[rank][4+i*mult].piece = None
                    works = False
                    break
                if (i == 2):
                    cgame.game[rank][4].piece = cgame.game[rank][4+i*mult].piece
                    cgame.game[rank][4+i*mult].piece = None
                    break
                cgame.game[rank][4+(i+1) *
                                 mult].piece = cgame.game[rank][4+i*mult].piece
                cgame.game[rank][4+i*mult].piece = None
            if (works):
                validmoves.append((fx, fy))
        else:
            tmp = cgame.game[fx][fy].piece
            cgame.game[fx][fy].piece = cgame.game[x][y].piece
            cgame.game[x][y].piece = None
            if (not inCheck(cur % 2)):
                validmoves.append((fx, fy))

            cgame.game[x][y].piece = cgame.game[fx][fy].piece
            cgame.game[fx][fy].piece = tmp
    return validmoves


if __name__ == "__main__":

    clock = pygame.time.Clock()
    cgame = Game()
    cgame.addStartingPosition()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handleMove(event)
        cgame.drawBoard(screen)
        pygame.display.flip()
        clock.tick(60)
