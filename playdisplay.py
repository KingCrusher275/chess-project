import pygame
import os
import sys

names = ['bpawn', 'wpawn', 'bknight', 'wknight', 'bbishop',
         'wbishop', 'brook', 'wrook', 'bqueen', 'wqueen', 'bking', 'wking']


class PlayDisplay:
    def __init__(self, context, SQUARE_SIZE=60):
        self.firstPress = False
        self.relcur = None
        self.dragging = False
        self.flipboard = False
        self.context = context
        self.SQUARE_SIZE = SQUARE_SIZE
    def drawBoard(self, screen, sidebar):
        screen.fill(self.context.colors[self.context.game_settings["bcolor"]])
        # screen_size = (width, height)
        screen_size = screen.get_size()
        self.SQUARE_SIZE = min(screen_size[1], screen_size[0] - sidebar.minWidth) // 8

        for row in range(self.context.game.ROWS):
            for col in range(self.context.game.COLS):
                square = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                square_rect = square.get_rect()
                if (self.context.game.game[row][col].clicked):
                    square.fill(self.context.colors["BLUE"])
                elif (self.context.game.game[row][col].possibleMove):
                    square.fill(self.context.colors["GREEN"])
                else:
                    square.fill(self.context.colors[self.context.game.game[row][col].color])
                if (self.context.game.game[row][col].piece != None and not (self.relcur != None and self.relcur == (row, col))):
                    
                    img = pygame.image.load(
                        os.path.join(
                            'public', f'{names[self.context.game.game[row][col].piece]}.png')
                    )
                    img = pygame.transform.scale(
                        img, (self.SQUARE_SIZE, self.SQUARE_SIZE))

                    piece_rect = img.get_rect()


                    piece_rect.center = square_rect.center
                    square.blit(img, piece_rect.topleft)
                
                if(self.flipboard):
                    screen.blit(square, ((7-col) * self.SQUARE_SIZE,
                            (7-row) * self.SQUARE_SIZE))
                else:
                    screen.blit(square, (col * self.SQUARE_SIZE,
                            row * self.SQUARE_SIZE))
        if(self.relcur != None):
            img = pygame.image.load(
                        os.path.join(
                            'public', f'{names[self.context.game.game[self.relcur[0]][self.relcur[1]].piece]}.png')
                    )
            img = pygame.transform.scale(
                img, (self.SQUARE_SIZE, self.SQUARE_SIZE))

            piece_rect = img.get_rect()


            piece_rect.center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) 

            screen.blit(img, piece_rect.topleft)

    def drawSidebar(self, screen, sidebar):
        # screen_size = (width, height)
    

        screen_size = screen.get_size()
        center_ypos = min(screen_size[1], screen_size[0] - sidebar.minWidth) + (screen_size[0] - self.SQUARE_SIZE * 8)//2
        center_xpos = 0.1 * screen_size[1]

        button_width = (screen_size[0] - self.SQUARE_SIZE * 8) * sidebar.widthPercent
        button_height = screen_size[1] * sidebar.heightPercent
        xpos = center_xpos - (button_height // 2)
        ypos = center_ypos - (button_width // 2) 
        
        for i in range(sidebar.numButton):
            sidebar.buttons[i].tlx = xpos + i * (button_height + sidebar.padding)
            sidebar.buttons[i].tly = ypos
            sidebar.buttons[i].width = button_width
            sidebar.buttons[i].height = button_height
            sidebar.buttons[i].draw_button(screen)

    def setFlipBoard(self):
        self.flipboard = not self.flipboard
    def setSettings(self):
        print("settings!")
    def setNewGame(self):
        print("new game!")
         
    def handleMove(self, relx, rely):
        self.firstPress = False

        if(relx < 0 or relx > 7 or rely < 0 or rely > 7):
            return
        if (self.context.game.game[relx][rely].clicked):
            self.context.game.game[relx][rely].clicked = False
            self.context.game.clicked = False
            self.context.game.togglePossibleMoves(relx, rely)
        elif (not self.context.game.clicked and self.context.game.game[relx][rely].piece != None and self.context.game.game[relx][rely].piece % 2 == self.context.game.turn):
            self.context.game.game[relx][rely].clicked = True
            self.context.game.clicked = True
            self.context.game.squareClicked = (relx, rely)
            self.context.game.togglePossibleMoves(relx, rely)
        elif (self.context.game.clicked):
            if (self.context.game.game[relx][rely].piece != None and self.context.game.game[relx][rely].piece % 2 == self.context.game.game[self.context.game.squareClicked[0]][self.context.game.squareClicked[1]].piece % 2):

                if(not self.dragging):
                    self.context.game.game[relx][rely].clicked = True
                    self.context.game.togglePossibleMoves(
                        self.context.game.squareClicked[0], self.context.game.squareClicked[1])
                    self.context.game.game[self.context.game.squareClicked[0]
                               ][self.context.game.squareClicked[1]].clicked = False
                    self.context.game.togglePossibleMoves(relx, rely)
                    self.context.game.squareClicked = (relx, rely)
            elif (self.context.game.validateMove(self.context.game.squareClicked[0], self.context.game.squareClicked[1], relx, rely)):
                self.context.game.togglePossibleMoves(
                    self.context.game.squareClicked[0], self.context.game.squareClicked[1])
                self.context.game.makeMove(self.context.game.squareClicked[0],
                               self.context.game.squareClicked[1], relx, rely)
                self.context.game.clicked = False
                self.context.game.game[self.context.game.squareClicked[0]
                           ][self.context.game.squareClicked[1]].clicked = False
                self.context.game.turn = 1 - self.context.game.turn




    def handleQuit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def handleKey(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_r):
                self.context.game.__init__()

    def getRelPosition(self, x, y):
        relx, rely = x // self.SQUARE_SIZE, y // self.SQUARE_SIZE
        if(self.flipboard):
            relx = 7 - relx
            rely = 7 - rely
        return relx, rely

    def handleDown(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            y, x = event.dict['pos']
            relx, rely = self.getRelPosition(x,y)
            if(relx >= 0 and relx < 8 and rely >= 0 and rely < 8): 
                if(self.context.game.game[relx][rely].piece != None and self.context.game.game[relx][rely].piece % 2 == self.context.game.turn):
                    self.relcur = (relx, rely)
                    if(not (self.context.game.clicked and (relx, rely) == self.context.game.squareClicked)):
                        self.handleMove(relx, rely)
                    self.dragging = True
                elif(not (self.context.game.clicked and (relx, rely) == self.context.game.squareClicked)):
                    self.handleMove(relx, rely)
            res = self.context.game.gameEnd()
            if (res == 2):
                pass
            else:
                if (res == 0):
                    print('Draw!')
                elif (res == 1):
                    print('White Wins!')
                else:
                    print('Black Wins!')


    def handleUp(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if(self.relcur != None):
                y, x = event.dict['pos']
                relx, rely = self.getRelPosition(x, y)
                if((relx, rely) != self.relcur or self.firstPress):
                    self.handleMove(relx, rely)
                    if((relx, rely) == self.relcur or self.context.game.squareClicked == None):
                        self.firstPress = False
                else:
                    self.firstPress = True
                self.relcur = None
                self.dragging = False

            
    def handleEvent(self, event):
        self.handleQuit(event)
        self.handleKey(event)
        self.handleDown(event)
        self.handleUp(event)



