#https://medium.com/@SereneBiologist/the-anatomy-of-a-chess-ai-2087d0d565#:~:text=The%20minimax%20algorithm%20takes%20advantage,other%20tries%20to%20minimize%20it.

from abc import abstractmethod
from typing import Deque
from chess import chessBoard
from chess import move
import random
import numpy
import time
from queue import LifoQueue

class chessAgent:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def chooseMove(self, board: chessBoard, possibleMoves : list):
        pass

class randomChessAgent(chessAgent):

    def __init__(self):
        pass

    def chooseMove(self, board: chessBoard, possibleMoves: list):
        return random.choice(possibleMoves)

class basicPointAgent(chessAgent):

    def __init__(self):
        pass

    def chooseMove(self, board: chessBoard, possibleMoves: list):
        bestScoreDiff = -10000
        bestMoves = list()
        boardScore = self.getBoardScore(board)
        bestMoves.append(possibleMoves[0])
        for move in possibleMoves:
            successor = board.getSuccessor(move)
            status =  successor.getCheckmateStatus()[0] 
            if status == 2 and board.isWhiteTurn:
                return move
            if status == 3 and not board.isWhiteTurn:
                return move
            if status == 2 and not board.isWhiteTurn:
                continue
            if status == 3 and board.isWhiteTurn:
                continue
            if status == 1:
                continue
            scoreDiff =  self.getBoardScore(successor) - boardScore
            if not board.isWhiteTurn:
                scoreDiff *= -1
            if scoreDiff > bestScoreDiff:
                bestScoreDiff = scoreDiff
                bestMoves = [move]
            elif scoreDiff == bestScoreDiff:
                bestMoves.append(move)
        return random.choice(bestMoves)


    def getBoardScore(self, board: chessBoard):
        scoreDiff = 0
        whiteKingExists = False
        blackKingExists = False
        for a in board.board:
            for x in a:
                if x == 1:
                    scoreDiff -= 1
                elif x == 2:
                    scoreDiff -= 3
                elif x == 3:
                    scoreDiff -= 3
                elif x == 4:
                    scoreDiff -= 5
                elif x == 5:
                    scoreDiff -= 9
                elif x == 6:
                    blackKingExists = True
                elif x == 7:
                    scoreDiff += 1
                elif x == 8:
                    scoreDiff += 3
                elif x == 9:
                    scoreDiff += 3
                elif x == 10:
                    scoreDiff += 5
                elif x == 11:
                    scoreDiff += 9
                elif x == 12:
                    whiteKingExists = True
        if not whiteKingExists:
            return -99999
        if not blackKingExists:
            return 99999
        return scoreDiff

class minimaxTree:
    def __init__(self, board : chessBoard, parent = None, move = None):
        self.parent = parent
        self.children = list()
        self.board = board
        self.move = move
        self.score = None

    def addChild(self, board : chessBoard, move = None):
        child = minimaxTree(board, parent=self, move = move)
        self.children.append(child)
        return child

    def isTerminalNode(self):
        return len(self.children) == 0

    def setScore(self, score):
        self.score = score

def printTree(origin, depth, justOrigin = True):
    if justOrigin:
        print(origin.score)
        return
    lastLayer = LifoQueue()
    lastLayer.put((origin, 0))
    currentLevel = -1
    while not lastLayer.empty():
        node, level = lastLayer.get()
        if level != currentLevel:
            currentLevel = level
            print()
            print(level, ": ", end='')
        print(node.score, ", ", end='')
        if level < depth:
            for child in node.children:
                lastLayer.put((child, level + 1))

def printBoard(board):
    print("------------------")
    for a in board.board:
        for x in a:
            print(x, ", ", end='')
        print()

def isMoveCapture(move : move, board : chessBoard):
    if not move.removeEnPassantPos is None:
        return True
    r, c = move.finalPos
    if board.board[c][r] > 0:
        return True
    return False

# Basic move ordering that has captures first
def orderMoves(moves : list(), board : chessBoard):
    sorted = []
    notCaptures = []
    for move in moves:
        if isMoveCapture(move, board):
            sorted.append(move)
        else:
            notCaptures.append(move)
    sorted.extend(notCaptures)
    return sorted


class minimaxPointAgent(chessAgent):

    def __init__(self, depth):
        self.depth = depth
        self.w = 0

    def chooseMove(self, board: chessBoard, possibleMoves: list):
        self.w = 0
        #Create tree
        origin = minimaxTree(board = board)
        time0 = time.perf_counter()
        self.minimax(origin, -9999999, 9999999, self.depth, board.isWhiteTurn)
        time1 = time.perf_counter()
        print("Mimimax Calls: ", self.w, "Time taken: ", time1-time0)     
        bestMoves = list()
        for child in origin.children:
            if origin.score == child.score and not child.score is None:
                bestMoves.append(child.move)
        if origin.score != self.getBoardScore(board):
            printTree(origin, depth = 2, justOrigin=False)
            print("Best score diff = ", self.getBoardScore(board) - origin.score)
            print("Best moves: ")
            for move in bestMoves:
                print(move.initialPos, " to ", move.finalPos)
            test = 0
        return random.choice(bestMoves)

    
    def minimax(self, node : minimaxTree, alpha, beta, depth, maximizingPlayer): #Using alpha-beta pruning -> Something is wrong, as suboptimal moves are done
        self.w += 1
        if depth == 0:# or node.isTerminalNode():
            score = self.getBoardScore(board = node.board) # 0.0007-0.0014 seconds
            node.setScore(score)
            return score
        
        pMoves = node.board.getAllMoves() #Takes about 0.03-0.04 seconds. This is a bit long
        if len(pMoves) == 0: #Game end
            checkmateStatus, _, _ = node.board.getCheckmateStatus(noKnownMoves=True)
            # 0 = nothing, 1 = stalemate, 2 = white wins, 3 = black wins
            if checkmateStatus == 1: #Try to avoid stalemate
                if maximizingPlayer:
                    node.setScore(-9999)
                    return -9999
                else:
                    node.setScore(9999)
                    return 9999
            elif checkmateStatus == 2:
                node.setScore(99999)
                return 99999
            else:
                node.setScore(-99999)
                return -99999

        pMoves = orderMoves(pMoves, node.board)

        if maximizingPlayer:
            value = -9999999
            for move in pMoves:
                child = node.addChild(board=node.board.getSuccessor(move), move=move)
                m = self.minimax(child, alpha, beta, depth - 1, False)
                value = max((value, m))
                if value >= beta:
                    break
                alpha = max((alpha, value))
            node.setScore(value)
            return value
        else:
            value = 9999999
            for move in pMoves:
                child = node.addChild(board=node.board.getSuccessor(move), move=move)
                m = self.minimax(child, alpha, beta, depth - 1, True)
                value = min((value, m))
                if value <= alpha:
                    break
                beta = min((beta, value))
            node.setScore(value)
            return value
    

    def getBoardScore(self, board: chessBoard):
        scoreDiff = 0
        whiteKingExists = False
        blackKingExists = False
        for a in board.board:
            for x in a:
                if x == 1:
                    scoreDiff -= 1
                elif x == 2:
                    scoreDiff -= 3
                elif x == 3:
                    scoreDiff -= 3
                elif x == 4:
                    scoreDiff -= 5
                elif x == 5:
                    scoreDiff -= 9
                elif x == 6:
                    blackKingExists = True
                elif x == 7:
                    scoreDiff += 1
                elif x == 8:
                    scoreDiff += 3
                elif x == 9:
                    scoreDiff += 3
                elif x == 10:
                    scoreDiff += 5
                elif x == 11:
                    scoreDiff += 9
                elif x == 12:
                    whiteKingExists = True
        if not whiteKingExists:
            return -99999
        if not blackKingExists:
            return 99999
        return scoreDiff