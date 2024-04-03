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


def handleMove(event):
    y, x = event.dict['pos']
    relx, rely = x // cgame.SQUARE_SIZE, y // cgame.SQUARE_SIZE
    if (cgame.game[relx][rely].clicked):
        cgame.game[relx][rely].clicked = False
        cgame.clicked = False
        cgame.togglePossibleMoves(relx, rely)
    elif (not cgame.clicked and cgame.game[relx][rely].piece != None and cgame.game[relx][rely].piece % 2 == cgame.turn):
        cgame.game[relx][rely].clicked = True
        cgame.clicked = True
        cgame.squareClicked = (relx, rely)
        cgame.togglePossibleMoves(relx, rely)
    elif (cgame.clicked):
        if (cgame.game[relx][rely].piece != None and cgame.game[relx][rely].piece % 2 == cgame.game[cgame.squareClicked[0]][cgame.squareClicked[1]].piece % 2):
            cgame.game[relx][rely].clicked = True
            cgame.togglePossibleMoves(
                cgame.squareClicked[0], cgame.squareClicked[1])
            cgame.game[cgame.squareClicked[0]
                       ][cgame.squareClicked[1]].clicked = False
            cgame.togglePossibleMoves(relx, rely)
            cgame.squareClicked = (relx, rely)
        elif (cgame.validateMove(cgame.squareClicked[0], cgame.squareClicked[1], relx, rely)):
            cgame.togglePossibleMoves(
                cgame.squareClicked[0], cgame.squareClicked[1])
            cgame.makeMove(cgame.squareClicked[0],
                           cgame.squareClicked[1], relx, rely)
            cgame.clicked = False
            cgame.game[cgame.squareClicked[0]
                       ][cgame.squareClicked[1]].clicked = False
            cgame.turn = 1 - cgame.turn


if __name__ == "__main__":

    clock = pygame.time.Clock()
    cgame = Game()
    cgame.addStartingPosition()
    done = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif (done):
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_r):
                        done = False
                        cgame = Game()
                        cgame.addStartingPosition()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handleMove(event)
                res = cgame.gameEnd()
                print(res)
                if (res == 2):
                    pass
                else:
                    if (res == 0):
                        print('Draw!')
                    elif (res == 1):
                        print('White Wins!')
                    else:
                        print('Black Wins!')
                    done = True
        cgame.drawBoard(screen)
        pygame.display.flip()
        clock.tick(60)
