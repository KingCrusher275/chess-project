import sys
import pygame
import os
from game import Game
from collections import defaultdict
pygame.init()
size = width, height = 650, 480
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
from display import Display
from sidebar import Sidebar
names = ['bpawn', 'wpawn', 'bknight', 'wknight', 'bbishop',
         'wbishop', 'brook', 'wrook', 'bqueen', 'wqueen', 'bking', 'wking']
colors = {"WHITE":(255, 255, 255), "BLACK":(100, 100, 100), "BLUE": (0, 0, 255), 
                       "GRAY":(180, 180, 180)        , "GREEN": (0, 255, 0), "BROWN": (150, 75, 0)}
done = False

def handleMove(event):
    y, x = event.dict['pos']
    relx, rely = x // displayBoard.SQUARE_SIZE, y // displayBoard.SQUARE_SIZE
    print(relx, rely)
    if(relx < 0 or relx > 7 or rely < 0 or rely > 7):
        pass
    elif (cgame.game[relx][rely].clicked):
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


def handleQuit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def handleKey(event):
    global done
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_r):
            done = False
            cgame = Game()
            cgame.addStartingPosition()

def handleResize(event):
    global screen
    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

def handleDown(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        handleMove(event)
        res = cgame.gameEnd()
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

if __name__ == "__main__":

    clock = pygame.time.Clock()
    cgame = Game()
    sidebar = Sidebar(colors)
    displayBoard = Display(cgame, sidebar, colors)
    cgame.addStartingPosition()
    print(cgame.export_fen())
    while True:
        for event in pygame.event.get():
            for button in displayBoard.sidebar.buttons:
                button.handle_event(event)
            handleQuit(event)
            handleKey(event)
            handleDown(event)
        displayBoard.drawBoard(screen)
        displayBoard.drawSidebar(screen)
        pygame.display.flip()
        clock.tick(10)
