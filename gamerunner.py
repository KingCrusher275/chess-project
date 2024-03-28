import sys
import pygame
import os
from game import Game
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
            if (cgame.game[x+dxx][y+dyy].piece == None):
                moves.append((x+dxx, y+dyy))
            elif (cgame.game[x+dxx][y+dyy].piece % 2 != cgame.turn):
                moves.append((x+dxx, y+dyy))
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
            if (cgame.game[x+i][y].piece == None):
                moves.append((x+i, y))
            elif (cgame.game[x+i][y].piece % 2 != cgame.turn):
                moves.append((x+i, y))
                break
            else:
                break
            mult += 1
        mult = 1
        while (y + i * mult >= 0 and y + i * mult < 8):
            if (cgame.game[x][y+i].piece == None):
                moves.append((x, y+i))
            elif (cgame.game[x][y+i].piece % 2 != cgame.turn):
                moves.append((x, y+i))
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
                    if (cgame.game[x+j][y+k].piece == None or cgame.game[x+j][y+k].piece % 2 != cgame.turn):
                        moves.append((x+j, y+k))

    return moves


def kingMove(x, y):
    moves = []
    dx = [-1, 0, 1]
    dy = [-1, 0, 1]
    for i in dx:
        for j in dy:
            if (x + i < 8 and x + i >= 0 and y + j >= 0 and y + j < 8):
                if (cgame.game[x+i][y+j].piece == None or cgame.game[x+i][y+j].piece % 2 != cgame.turn):
                    moves.append((x+i, y+j))
    rank = 0
    ix = 1
    if (cgame.turn == 1):
        rank = 7
        ix = 0
    if (not cgame.moved[ix][1]):
        if (not cgame.moved[ix][0]):
            if (cgame.game[rank][5].piece == None and cgame.game[rank][6].piece == None):
                moves.append((rank, 5))

        if (not cgame.moved[ix][2]):
            if (cgame.game[rank][1].piece == None and cgame.game[rank][2].piece == None and cgame.game[rank][3].piece == None):
                moves.append((rank, 2))
    else:
        pass
    return moves


def pawnMove(x, y):
    moves = []
    if (cgame.turn == 0):
        mult = 1
        rank = 1
    else:
        mult = -1
        rank = 6
    if (cgame.game[x+mult][y].piece == None):
        moves.append((x+mult, y))
        if (x == rank and cgame.game[x+2*mult][y].piece == None):
            moves.append((x+2*mult, y))
    if ((y < 7 and cgame.game[x+mult][y+1].piece != None and cgame.game[x+mult][y+1].piece % 2 != cgame.turn % 2)
        or (y < 7 and cgame.game[x][y+1].piece != None and cgame.game[x][y+1].piece % 2 != cgame.turn % 2 and
            (cgame.game[x][y+1].piece == 0 or cgame.game[x][y+1].piece == 1) and cgame.lastMove[1] == (x, y+1) and
            cgame.lastMove[1][1] - cgame.lastMove[0][1] == 2 * mult)):
        moves.append((x+mult, y+1))
    if ((y > 0 and cgame.game[x+mult][y-1].piece != None and cgame.game[x+mult][y-1].piece % 2 != cgame.turn % 2)
        or (y > 0 and cgame.game[x][y-1].piece != None and cgame.game[x][y-1].piece % 2 != cgame.turn % 2 and
            (cgame.game[x][y-1].piece == 0 or cgame.game[x][y-1].piece == 1) and
            cgame.lastMove[1] == (x, y-1) and cgame.lastMove[1][1] - cgame.lastMove[0][1] == 2 * mult)):
        moves.append((x+mult, y-1))

    return moves


def handleMove(event):
    y, x = event.dict['pos']
    relx, rely = x // cgame.SQUARE_SIZE, y // cgame.SQUARE_SIZE

    if (cgame.game[relx][rely].clicked):
        cgame.game[relx][rely].clicked = False
        cgame.clicked = False
    elif (not cgame.clicked and cgame.game[relx][rely].piece != None):
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
            cgame.clicked = False
            cgame.game[cgame.squareClicked[0]
                       ][cgame.squareClicked[1]].clicked = False
            cgame.turn = 1 - cgame.turn


def inCheck():
    moves = []
    px, py = -1, -1
    for i in range(8):
        for j in range(8):
            if (cgame.game[i][j].piece != None and cgame.game[i][j].piece % 2 != cgame.turn):
                if (cgame.game[i][j].piece == 0 or cgame.game[i][j].piece == 1):
                    moves += pawnMove(i, j)
                elif (cgame.game[i][j].piece == 2 or cgame.game[i][j].piece == 3):
                    moves += knightMove(i, j)
                elif (cgame.game[i][j].piece == 4 or cgame.game[i][j].piece == 5 or cgame.game[i][j].piece == 8 or cgame.game[i][j].piece == 9):
                    moves += bishopMove(i, j)
                elif (cgame.game[i][j].piece == 6 or cgame.game[i][j].piece == 7 or cgame.game[i][j].piece == 8 or cgame.game[i][j].piece == 9):
                    moves += rookMove(i, j)
            elif (cgame.game[i][j].piece == 10 or cgame.game[i][j].piece == 11 and cgame.game[i][j].piece % 2 == cgame.turn):
                px, py = i, j
    if ((px, py) in moves):
        return False
    else:
        return True


def validateMove(x, y, fx, fy):
    moves = []
    cur = cgame.game[x][y].piece
    if (cur == 0 or cur == 1):
        moves += pawnMove(x, y)
    elif (cur == 2 or cur == 3):
        moves += knightMove(x, y)
    elif (cur == 4 or cur == 5 or cur == 8 or cur == 9):
        moves += bishopMove(x, y)
    elif (cur == 6 or cur == 7 or cur == 8 or cur == 9):
        moves += rookMove(x, y)
    elif (cur == 10 or cur == 11):
        moves += kingMove(x, y)

    if (fx, fy) in moves:
        if ((cur == 0 or cur == 1) and (abs(fx - x) == 1 and abs(fy - y) == 1 and cgame.game[fx][fy].piece == None)):
            tmp = cgame.game[x][fy]
            cgame.game[fx][fy].piece = cgame.game[x][y].piece
            cgame.game[x][y].piece = None
            cgame.game[x][fy] = None
            if (not inCheck()):
                return True
            else:
                cgame.game[x][y].piece = cgame.game[fx][fy].piece
                cgame.game[fx][fy].piece = None
                cgame.game[x][fy] = tmp
                return False
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
                if (inCheck()):
                    cgame.game[4+i*mult].piece = None
                    cgame.game[rank][4].piece = 11
                    works = False
                    break
                cgame.game[rank][4+i*mult].piece = None
                cgame.game[rank][5+i*mult].piece = 11

            if (works):
                if (fy - y > 1):
                    cgame.game[rank][5].piece = cgame.game[rank][7].piece
                    cgame.game[rank][7].piece = None
                else:
                    cgame.game[rank][3].piece = cgame.game[rank][0].piece
                    cgame.game[rank][0].piece = None
                return True
        else:
            tmp = cgame.game[fx][fy].piece
            cgame.game[fx][fy].piece = cgame.game[x][y].piece
            cgame.game[x][y].piece = None
            if (inCheck()):
                cgame.game[x][y].piece = cgame.game[fx][fy].piece
                cgame.game[fx][fy].piece = None
                cgame.game[fx][fy].piece
            else:
                return True
    return False


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
