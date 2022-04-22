import pygame, sys, random
from pygame.locals import *

BOARDWIDTH = 3 # columns
BOARDHEIGHT =3# rows
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BLACK =         (  0,   0,   0)#rgb value
WHITE =         (255, 191, 0)
BRIGHTBLUE =    (  121,  121, 0)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  2, 15,   168)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('n Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # buttons
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 420)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 350)
    SOLVE_SURF, SOLVE_RECT = makeText('Apply AI',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 300)

    mainBoard, solutionSeq = generateNewPuzzle(5)  
    SOLVEDBOARD = getStartingBoard() #solved board at the start
    allMoves = [] 

    while True: # main game loop
        slideTo = None 
        msg = 'Click the cell to apply action.' 
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit() #########################################################################################
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(5) # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        a_Star(mainBoard)
#                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on AI button
                        allMoves = []
                else:

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) 
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): 
        terminate() 
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event)


def getStartingBoard():#returns the solved board structure [1 2 3 4; 5 6 7 8]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

#count displacement
def displacement(c_board):
    count = 0
    for i in range(BOARDHEIGHT):
        for j in range(BOARDWIDTH):
            #print(i,j,c_board[i][j])
            if c_board[i][j] == BLANK:
                continue
            if c_board[i][j] != j*BOARDWIDTH+i+1:
                count = count+1
    return (count)
    
#count displacement

#coment start
def a_Star(board):
    
    #print(board)
    
    g_of_n = 0
    
    
    #g_of_n = g_of_n + 1
    
    
    moooov = 0 # 1 = left, 2 = right, 3 = up, 4 = down
    loop = 0
    last = None
    
    while True:
        f_of_n = 500
        #print(board)
        #break
        loop = loop+1
        print('loop',loop)
        g_of_n = g_of_n + 1
        #print(g_of_n)
        h_of_n = displacement(board)
        #print(h_of_n)
        if h_of_n == 0:
            break
        blank_col,blank_row = getBlankPosition(board)
        #print(blank_col,blank_row)
        req = blank_row*BOARDWIDTH + blank_col +1 #blank col req
        #print(req)
        if blank_col > 0:#left element
            #print(blank_col)
            #break
            
            #print(board[blank_col-1][blank_row])
            #break
            if req == board[blank_col-1][blank_row] and last != RIGHT:
                #print('yes')
                #break
                dis = h_of_n - 1
                temp = g_of_n + dis
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 1
                    #last = LEFT
            elif board[blank_col-1][blank_row] == blank_row*BOARDWIDTH+blank_col and last != RIGHT:
                dis = h_of_n + 1
                temp =g_of_n + dis
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 1
                    #last = LEFT
                    #print('yes')
            elif board[blank_col-1][blank_row] != blank_row*BOARDWIDTH+blank_col and last != RIGHT:
                temp =g_of_n + h_of_n
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 1
                    #last = LEFT

        if blank_col < BOARDWIDTH-1: #RIGHT ELEMENT
            if req == board[blank_col+1][blank_row] and last != LEFT:
                dis = h_of_n -1
                temp = g_of_n + dis
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 2
                    #last = RIGHT
            elif board[blank_col+1][blank_row] == blank_row*BOARDWIDTH+blank_col+2 and last != LEFT:
                dis = h_of_n + 1
                temp = g_of_n + dis
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 2
                    #last = RIGHT
                    #print('yes',f_of_n)
            elif board[blank_col+1][blank_row] != blank_row*BOARDWIDTH+blank_col and last != LEFT:
                temp = g_of_n+h_of_n
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 2
                    #last = RIGHT
                    
        if blank_row > 0: #up element
            if req == board[blank_col][blank_row-1] and last != DOWN:
                dis = h_of_n - 1
                temp = g_of_n + dis
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 3
                   # last = UP
            elif board[blank_col][blank_row-1] == (blank_row-1)*BOARDWIDTH+blank_col+1  and last != DOWN:
                dis = h_of_n + 1
                temp = g_of_n + dis
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 3
                    #last = UP
                    #print('yes', f_of_n)
            elif board[blank_col][blank_row-1] != (blank_row-1)*BOARDWIDTH+blank_col+1  and last != DOWN:
                temp = g_of_n + h_of_n
                if temp <= f_of_n:
                    f_of_n = temp
                    moooov = 3
                    #last = UP
        #f_of_n = 500
        if blank_row < BOARDHEIGHT-1: #DOWN element
           if req == board[blank_col][blank_row+1]  and last != UP:
               dis = h_of_n -1
               temp = g_of_n + dis
               if temp <= f_of_n:
                   f_of_n = temp
                   moooov = 4
                   #last = DOWN
                   #print('yes',f_of_n)
           elif board[blank_col][blank_row+1] == (blank_row+1)*BOARDWIDTH+blank_col+1 and last != UP:
               dis = h_of_n + 1
               temp = g_of_n + dis
               if temp <= f_of_n:
                   f_of_n = temp
                   moooov = 4
                   #last = DOWN
           elif board[blank_col][blank_row+1] != (blank_row+1)*BOARDWIDTH+blank_col+1 and last != UP:
               dis = g_of_n + h_of_n
               if temp <= f_of_n:
                   f_of_n = temp
                   moooov = 4
                   #last = DOWN
        if moooov == 1:
            operate = RIGHT
            last = LEFT
        elif moooov == 2:
            operate = LEFT
            last = RIGHT
        elif moooov == 3:
            operate = DOWN
            last = UP
            #print('yes',moooov)
        elif moooov == 4:
            operate = UP
            ast = DOWN
        print(moooov, operate)
        slideAnimation(board, operate, '', animationSpeed=int(TILESIZE / 30))
        makeMove(board, operate)
            
    
    

    
#coment end

def resetAnimation(board, allMoves):#------------backtrack-----------------------------------------------------------------
    
    revAllMoves = allMoves[:] 
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 30))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()
