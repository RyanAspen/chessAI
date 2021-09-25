from graphics import *
from chess import chessBoard
from chessAgent import basicPointAgent, minimaxPointAgent, randomChessAgent
import math
import time


boxSize = 50
speed = 0.0

moveNotation = list()

def getClickPos(window: GraphWin):
    point = window.getMouse()
    c = math.floor(point.getX() / boxSize) + 1
    r = 8 - (math.floor(point.getY() / boxSize))
    cChar = chr(ord('a') + c - 1)
    return str(cChar)+ str(r)

def promptMoveAgent(board : chessBoard, window : GraphWin, agent, visual):
    allPossibleMoves = board.getAllMoves()
    chosenMove = agent.chooseMove(board, allPossibleMoves)
    _, notation = board.makeMove(chosenMove, isBot=True)
    if visual:
        board.drawBoard(window)
        time.sleep(speed)
    return notation

def promptMove(board : chessBoard, window : GraphWin):
    moveTaken = False
    while not moveTaken:
        board.resetHighlight()
        board.drawBoard(window)
        clickPosNotation = getClickPos(window)
        clickPos = board.getPosFromChessNotation(clickPosNotation)
        if not board.isWhitePos(clickPos) and board.isWhiteTurn:
            continue
        if not board.isBlackPos(clickPos) and not board.isWhiteTurn:
            continue
        
        allPossibleMoves = board.getAllMovesPos(clickPos)
        board.highlight(clickPos)
        for move in allPossibleMoves:
            pos = move.finalPos
            board.highlight(pos)
        moveConfirmed = False
        board.drawBoard(window)
        while not moveConfirmed:
            movePosNotation = getClickPos(window)
            movePos = board.getPosFromChessNotation(movePosNotation)
            if movePosNotation == clickPosNotation:
                moveConfirmed = True
                break
            for move in allPossibleMoves:
                pos = move.finalPos
                if pos == movePos:
                    isLegal, notation = board.makeMove(move)
                    moveNotation.append(notation)
                    moveTaken = True
                    moveConfirmed = True
                    break
    board.drawBoard(window)
    return notation

def completeGame(agent1 = None, agent2 = None, isAgent1Auto = True, isAgent2Auto = True, visual = False, printNotation=False, printResult=True):
    board = chessBoard()
    turn = 1
    if visual:
        win = GraphWin("Chess Board", boxSize * 8, boxSize * 8)
    else:
        win = None
    while True:
        if board.isWhiteTurn:
            if isAgent1Auto:
                notation = promptMoveAgent(board=board, window=win, agent=agent1, visual=visual)
            else:
                notation = promptMove(board=board, window=win)
            if printNotation:
                print(str(turn) + ". " + notation, end='')
                if notation[-1] != '#':
                    print(",", end='')
        else:
            if isAgent2Auto:
                notation = promptMoveAgent(board=board, window=win, agent=agent2, visual=visual)
            else:
                notation = promptMove(board=board, window=win)
            if printNotation:
                print(notation)
            turn += 1
        status, inCheck, details = board.getCheckmateStatus() 
        if status > 0:
            if printResult:
                if status == 1:
                    noLegalMoves, threefoldRepetition, insufficientMaterial, fiftyMoveRule = details
                    if noLegalMoves:
                        print("Draw by stalemate")
                    elif threefoldRepetition:
                        print("Draw by threefold repetition")
                    elif insufficientMaterial:
                        print("Draw by insufficient material")
                    elif fiftyMoveRule:
                        print("Draw by fifty move rule")
                    else:
                        print("Draw by unknown means. If this prints, there is a bug")
                elif status == 2:
                    print("White wins")
                elif status == 3:
                    print("Black wins")
            win.getMouse()
            win.close()
            return status
        board.updateCheckStatus(inCheck)

blackAgent = minimaxPointAgent(depth = 4)
whiteAgent = basicPointAgent()

completeGame(agent1=whiteAgent, agent2=blackAgent, visual=True)
#status = completeGame(agent1 = whiteAgent, agent2 = blackAgent, visual=True)
#print(status)

"""
win = GraphWin("Chess Board", boxSize * 8, boxSize * 8)
board = chessBoard()

while True:
    promptMove(board=board, window=win)
    status, inCheck, details = board.getCheckmateStatus() 
    if status != 0:
        if status == 1: 
            noLegalMoves, threefoldRepetition, insufficientMaterial, fiftyMoveRule = details
            if noLegalMoves:
                print("Draw by stalemate")
            elif threefoldRepetition:
                print("Draw by threefold repetition")
            elif insufficientMaterial:
                print("Draw by insufficient material")
            elif fiftyMoveRule:
                print("Draw by fifty move rule")
            else:
                print("Draw by unknown means. If this prints, there is a bug")
        elif status == 2:
            print("White wins")
        elif status == 3:
            print("Black wins")
        break
    board.updateCheckStatus(inCheck)
win.getMouse()
a = 2
for n in moveNotation:
    if a % 2 == 0:
        print(str(int(a / 2)) + ". " + n, end='')
        if n[-1] != '#':
            print(",", end='')
    else:
        print(n)
    a += 1
win.close()


"""