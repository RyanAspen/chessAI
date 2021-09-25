import numpy
import copy
import math
from graphics import *
import copy
import time

boxSize = 50

class imageBank:
    
    def __init__(self):
        self.gridImgs = list()
        for c in range(8):
            gridImgCol = list()
            for r in range(8):
                rect = Rectangle(Point(c * boxSize, (8 - r) * boxSize), Point((c + 1) * boxSize, (7 - r) * boxSize))
                if (c + r) % 2 == 0:
                    rect.setFill(color_rgb(153,84,51))
                else:
                    rect.setFill(color_rgb(220,185,145))
                gridImgCol.append(rect)
            self.gridImgs.append(gridImgCol)

        self.highlightGridImgs = list()
        for c in range(8):
            highlightGridImgCol = list()
            for r in range(8):
                rect = Rectangle(Point(c * boxSize, (8 - r) * boxSize), Point((c + 1) * boxSize, (7 - r) * boxSize))
                rect.setFill(color_rgb(255,165,0))
                highlightGridImgCol.append(rect)
            self.highlightGridImgs.append(highlightGridImgCol)

        self.pieceImgs = list()
        for c in range(8):
            pieceImgCol = list()
            for r in range(8):
                pieceImgRow = list()
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/Black_Pawn.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/Black_Knight.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/Black_Bishop.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/Black_Rook.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/Black_Queen.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/Black_King.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/White_Pawn.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/White_Knight.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/White_Bishop.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/White_Rook.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/White_Queen.png'))
                pieceImgRow.append(Image(Point((c + 0.5) * boxSize, (7.5 - r) * boxSize), 'chessPiecePictures/White_King.png'))
                pieceImgCol.append(pieceImgRow)
            self.pieceImgs.append(pieceImgCol)

    def getPieceImg(self, pieceId, r, c):
        return self.pieceImgs[c][r][pieceId - 1]

    def drawPieceImg(self, window : GraphWin, pieceId, r, c):
        if not self.pieceImgs[c][r][pieceId - 1].canvas:
            self.pieceImgs[c][r][pieceId - 1].draw(window)

    def undrawPieceImg(self, pieceId, r, c):
        self.pieceImgs[c][r][pieceId - 1].undraw()

    def updatePieceImg(self, window : GraphWin, pieceId, r, c):
        for id in range(1, 13):
            self.undrawPieceImg(id, r, c)
        if pieceId > 0:
            self.drawPieceImg(window, pieceId, r, c)

    def highlightSpace(self, window: GraphWin, r, c):
        self.gridImgs[c][r].undraw()
        if not self.highlightGridImgs[c][r].canvas:
            self.highlightGridImgs[c][r].draw(window)

    def unhighlightSpace(self, window : GraphWin, r, c):
        self.highlightGridImgs[c][r].undraw()
        if not self.gridImgs[c][r].canvas:
            self.gridImgs[c][r].draw(window)

    def drawBoardWithoutPieces(self, window: GraphWin):
        for c in range(8):
            for r in range(8):
                if not self.gridImgs[c][r].canvas:
                    self.gridImgs[c][r].draw(window)

    def drawBoard(self, window : GraphWin, board):
        for r in range(8):
            for c in range(8):
                if board.isHighlighted((r,c)):
                    self.highlightSpace(window, r, c)
                else:
                    self.unhighlightSpace(window, r, c)
                pieceId = board.board[c][r]
                self.updatePieceImg(window, pieceId, r, c)

class move:
    #Move -> (initialPos, finalPos, isWhiteKingCastle, isWhiteQueenCastle, isBlackKingCastle, isBlackQueenCastle, enPassantIndex)
    #Board (col increases from left to right, row increases from up to down)
    def __init__(self, initialPos = None, finalPos = None, isWhiteKingCastle = False, isWhiteQueenCastle = False, isBlackKingCastle = False, isBlackQueenCastle = False, enPassantIndex = -1, removeEnPassantPos = None, promotionPieceId = 0):
        self.initialPos = initialPos
        self.finalPos = finalPos
        self.isWhiteKingCastle = isWhiteKingCastle
        self.isWhiteQueenCastle = isWhiteQueenCastle
        self.isBlackKingCastle = isBlackKingCastle
        self.isBlackQueenCastle = isBlackQueenCastle
        self.enPassantIndex = enPassantIndex
        self.removeEnPassantPos = removeEnPassantPos
        self.promotionPieceId = promotionPieceId

imgBank = imageBank()

class chessBoard:
    #Board (row increases from left to right, column increases from up to down)


    #Move -> (initialPos, finalPos, isWhiteKingCastle, isWhiteQueenCastle, isBlackKingCastle, isBlackQueenCastle, enPassantIndex)
    def __init__(self, boardProvided = False, board = None):
        self.turn = 1
        self.initializedVisual = False
        self.highlightBoard = numpy.full((8,8), False, dtype=bool)
        if not boardProvided:
            self.board = numpy.array([
            [10,7,0,0,0,0,1,4],
            [8,7,0,0,0,0,1,2],
            [9,7,0,0,0,0,1,3],
            [11,7,0,0,0,0,1,5],
            [12,7,0,0,0,0,1,6],
            [9,7,0,0,0,0,1,3],
            [8,7,0,0,0,0,1,2],
            [10,7,0,0,0,0,1,4]], dtype=numpy.int8)
        else:
            self.board = copy.deepcopy(board)

        self.isWhiteTurn = True
        self.whiteCanCastleKingSide = True
        self.whiteCanCastleQueenSide = True
        self.blackCanCastleKingSide = True
        self.blackCanCastleQueenSide = True
        self.movedForwardTwoSpaces = -1 #Keep track of en passant
        self.boardHistory = dict()
        hashableBoard = self.hashBoard()
        self.boardHistory[hashableBoard] = 1
        self.movesSinceCaptureOrPawnMove = 0
        self.lastMove = None
        self.inCheck = False
        
    def getNotation(self, move):
        if move.isWhiteKingCastle or move.isBlackKingCastle:
            return "0-0"
        if move.isWhiteQueenCastle or move.isBlackQueenCastle:
            return "0-0-0"
        notation = ""
        if not move.removeEnPassantPos is None:
            notation += "e.p. "

        initialR, initialC = move.initialPos
        pieceId = self.board[initialC][initialR]
        if pieceId == 1 or pieceId == 7:
            moveChar = ""
        elif pieceId == 2 or pieceId == 8:
            moveChar = "N"
        elif pieceId == 3 or pieceId == 9:
            moveChar = "B"
        elif pieceId == 4 or pieceId == 10:
            moveChar = "R"
        elif pieceId == 5 or pieceId == 11:
            moveChar = "Q"
        else:
            moveChar = "K"
        notation += moveChar
        finalR, finalC = move.finalPos
        takenPieceId = self.board[finalC][finalR]
        if takenPieceId > 0:
            notation += "x"
        newPosNotation = self.getChessNotationFromPos(move.finalPos)
        notation += newPosNotation
        return notation

    def updateCheckStatus(self, status):
        self.inCheck = status

    def getSuccessor(self, move):
        copyBoard = copy.deepcopy(self) 
        copyBoard.makeMove(move, isReal=True, isBot=True)
        return copyBoard

    def hashBoard(self):
        if self.isWhiteTurn:
            hashed = "1"
        else:
            hashed = "0"
        if self.whiteCanCastleKingSide:
            hashed += "1"
        else:
            hashed += "0"
        if self.whiteCanCastleQueenSide:
            hashed += "1"
        else:
            hashed += "0"
        if self.blackCanCastleKingSide:
            hashed += "1"
        else:
            hashed += "0"
        if self.blackCanCastleQueenSide:
            hashed += "1"
        else:
            hashed += "0"
        if self.movedForwardTwoSpaces == -1:
            hashed += "-"
        else:
            hashed += str(self.movedForwardTwoSpaces)
        for c in range(8):
            for r in range(8):
                hashed += str(self.board[c][r])
        return hashed

    def isPosOnBoard(self, pos):
        r,c = pos
        return (c < 8) and (r < 8) and (c > -1) and (r > -1)

    def getPosFromChessNotation(self, notation):
        letter = notation[0]
        number = notation[1]
        row = int(number) - 1
        col = ord(letter) - ord('a')
        return row, col

    def getChessNotationFromPos(self, pos):
        r,c = pos
        row = str(r + 1)
        col = chr(ord('a') + c)
        return col + row

    def isHighlighted(self, pos):
        r,c = pos
        return self.highlightBoard[c][r]

    def highlight(self, pos):
        r,c = pos
        self.highlightBoard[c][r] = True

    def resetHighlight(self):
        self.highlightBoard = numpy.full((8,8), False, dtype=bool)

    def containsPiece(self, pos):
        r,c = pos
        return self.board[c][r] != 0

    def isWhite(self, pieceId):
        return (pieceId >= 7) and (not pieceId == 0)

    def isBlack(self, pieceId):
        return (pieceId <= 6) and (not pieceId == 0)

    def isWhitePos(self, pos):
        r,c = pos
        pieceId = self.board[c][r]
        return self.isWhite(pieceId)

    def isBlackPos(self, pos):
        r,c = pos
        pieceId = self.board[c][r]
        return self.isBlack(pieceId)

    def getAllMovesPos(self, pos, legalCheck = True, castleCheck = False): 
        r,c = pos
        pieceId = self.board[c][r]
        possibleMoves = list()
        if pieceId == 0:
            return []
        elif pieceId == 1: #black pawn
            """
            Options are
            - move forward one space
            - move forward two spaces if it is the piece's first move
            - move forward in a diagonal one space if that space has an enemy to be taken or that space is behind an enemy pawn which just moved forward two spaces
            """
            if self.isPosOnBoard((r - 1, c)):
                if not self.containsPiece((r - 1, c)):
                    if r - 1 == 0:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c), promotionPieceId=2))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c), promotionPieceId=3))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c), promotionPieceId=4))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c), promotionPieceId=5))
                    else:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c)))
            if self.isPosOnBoard((r - 2, c)) and self.isPosOnBoard((r - 1, c)):
                if r == 6 and not self.containsPiece((r - 2, c)) and not self.containsPiece((r - 1, c)):
                    possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 2, c), enPassantIndex = c))
            if self.isPosOnBoard((r - 1, c + 1)):
                if self.isWhitePos((r - 1, c + 1)):
                    if r - 1 == 0:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c + 1), promotionPieceId=2))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c + 1), promotionPieceId=3))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c + 1), promotionPieceId=4))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c + 1), promotionPieceId=5))
                    else:
                       possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c + 1)))
                if self.movedForwardTwoSpaces == (c + 1) and r == 3:
                    possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c + 1), removeEnPassantPos = (r,c+1)))
            if self.isPosOnBoard((r - 1, c - 1)):
                if self.isWhitePos((r - 1, c - 1)):
                    if r - 1 == 0:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c - 1), promotionPieceId=2))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c - 1), promotionPieceId=3))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c - 1), promotionPieceId=4))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c - 1), promotionPieceId=5))
                    else:
                       possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c - 1)))
                if self.movedForwardTwoSpaces == (c - 1) and r == 3:
                    possibleMoves.append(move(initialPos = (r,c), finalPos = (r - 1, c - 1), removeEnPassantPos = (r,c-1)))

        elif pieceId == 2: #black knight
            """
            Move two spaces in one direction and one space in another
            No check for movement between pieces
            """
            rawPositions = list()
            rawPositions.append((r - 2, c - 1))
            rawPositions.append((r - 2, c + 1))
            rawPositions.append((r - 1, c - 2))
            rawPositions.append((r - 1, c + 2))
            rawPositions.append((r + 2, c - 1))
            rawPositions.append((r + 2, c + 1))
            rawPositions.append((r + 1, c - 2))
            rawPositions.append((r + 1, c + 2))
            for tempPos in rawPositions:
                if self.isPosOnBoard(tempPos):
                    if not self.isBlackPos(tempPos):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))

        elif pieceId == 3: #black bishop
            """
            Move any amount in a diagonal, which stops either at
            - the edge of the board
            - the space before an allied piece
            - the space of an enemy piece
            """
            
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

        elif pieceId == 4: #black rook
            """
            Move any amount in a vertical or horizontal, which stops either at
            - the edge of the board
            - the space before an allied piece
            - the space of an enemy piece
            """
            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c) 
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)


        elif pieceId == 5: #black queen
            """
            Combined options of bishop and rook
            """
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)
            
            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isWhitePos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)

        elif pieceId == 6: #black king
            """
            Move one space in any direction OR
            Castle: Move king two spaces in the direction of an unmoved rook if this is the king's first move. The rook then moves to the opposite side of the king
            """
            rawPositions = list()
            rawPositions.append((r - 1, c - 1))
            rawPositions.append((r - 1, c))
            rawPositions.append((r - 1, c + 1))
            rawPositions.append((r, c - 1))
            rawPositions.append((r, c + 1))
            rawPositions.append((r + 1, c - 1))
            rawPositions.append((r + 1, c))
            rawPositions.append((r + 1, c + 1))
            for tempPos in rawPositions:
                if self.isPosOnBoard(tempPos):
                    if not self.isBlackPos(tempPos):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
            if self.blackCanCastleKingSide and not self.inCheck and not castleCheck:
                if (not self.containsPiece((r, c + 1))) and (not self.containsPiece((r, c + 2))): 
                    if not self.isBoardInCheckPos((r, c + 1), True) and not self.isBoardInCheckPos((r, c + 2), True):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r, c + 2), isBlackKingCastle = True))
            if self.blackCanCastleQueenSide and not self.inCheck and not castleCheck:
                if (not self.containsPiece((r, c - 1))) and (not self.containsPiece((r, c - 2))) and (not self.containsPiece((r, c - 3))): 
                    if not self.isBoardInCheckPos((r, c - 1), True) and not self.isBoardInCheckPos((r, c - 2), True) and not self.isBoardInCheckPos((r, c - 3), True):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r, c - 2), isBlackQueenCastle = True))

        elif pieceId == 7: #white pawn
            """
            Options are
            - move forward one space
            - move forward two spaces if it is the piece's first move
            - move forward in a diagonal one space if that space has an enemy to be taken or that space is behind an enemy pawn which just moved forward two spaces
            """

            if self.isPosOnBoard((r + 1, c)):
                if not self.containsPiece((r + 1, c)):
                    if r + 1 == 7:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c), promotionPieceId=8))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c), promotionPieceId=9))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c), promotionPieceId=10))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c), promotionPieceId=11))
                    else:
                       possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c)))
            if self.isPosOnBoard((r + 2, c)) and self.isPosOnBoard((r + 1, c)):
                if r == 1 and not self.containsPiece((r + 2, c)) and not self.containsPiece((r + 1, c)):
                    possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 2, c), enPassantIndex = c))
            if self.isPosOnBoard((r + 1, c + 1)):
                if self.isBlackPos((r + 1, c + 1)):
                    if r + 1 == 7:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c + 1), promotionPieceId=8))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c + 1), promotionPieceId=9))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c + 1), promotionPieceId=10))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c + 1), promotionPieceId=11))
                    else:
                       possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c + 1)))
                if self.movedForwardTwoSpaces == (c + 1) and r == 4:
                    possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c + 1), removeEnPassantPos = (r,c+1)))
            if self.isPosOnBoard((r + 1, c - 1)):
                if self.isBlackPos((r + 1, c - 1)):
                    if r + 1 == 7:
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c - 1), promotionPieceId=8))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c - 1), promotionPieceId=9))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c - 1), promotionPieceId=10))
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c - 1), promotionPieceId=11))
                    else:
                       possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c - 1)))
                if self.movedForwardTwoSpaces == (c - 1) and r == 4:
                    possibleMoves.append(move(initialPos = (r,c), finalPos = (r + 1, c - 1), removeEnPassantPos = (r,c-1)))

        elif pieceId == 8: #white knight
            """
            Move two spaces in one direction and one space in another
            No check for movement between pieces
            """
            rawPositions = list()
            rawPositions.append((r - 2, c - 1))
            rawPositions.append((r - 2, c + 1))
            rawPositions.append((r - 1, c - 2))
            rawPositions.append((r - 1, c + 2))
            rawPositions.append((r + 2, c - 1))
            rawPositions.append((r + 2, c + 1))
            rawPositions.append((r + 1, c - 2))
            rawPositions.append((r + 1, c + 2))
            for tempPos in rawPositions:
                if self.isPosOnBoard(tempPos):
                    if not self.isWhitePos(tempPos):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))

        elif pieceId == 9: #white bishop
            """
            Move any amount in a diagonal, which stops either at
            - the edge of the board
            - the space before an allied piece
            - the space of an enemy piece
            """
            
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

        elif pieceId == 10: #white rook
            """
            Move any amount in a vertical or horizontal, which stops either at
            - the edge of the board
            - the space before an allied piece
            - the space of an enemy piece
            """
            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)


        elif pieceId == 11: #white queen
            """
            Combined options of bishop and rook
            """
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1
                tempPos = (tempPosR, tempPosC)

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1
                tempPos = (tempPosR, tempPosC)

            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
                if self.isBlackPos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)


        elif pieceId == 12: #white king
            """
            Move one space in any direction OR
            Castle: Move king two spaces in the direction of an unmoved rook if this is the king's first move. The rook then moves to the opposite side of the king
            """
            rawPositions = list()
            rawPositions.append((r - 1, c - 1))
            rawPositions.append((r - 1, c))
            rawPositions.append((r - 1, c + 1))
            rawPositions.append((r, c - 1))
            rawPositions.append((r, c + 1))
            rawPositions.append((r + 1, c - 1))
            rawPositions.append((r + 1, c))
            rawPositions.append((r + 1, c + 1))
            for tempPos in rawPositions:
                if self.isPosOnBoard(tempPos):
                    if not self.isWhitePos(tempPos):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = tempPos))
            if self.whiteCanCastleKingSide and not self.inCheck and not castleCheck:
                if (not self.containsPiece((r, c + 1))) and (not self.containsPiece((r, c + 2))): 
                    if not self.isBoardInCheckPos((r, c + 1), True) and not self.isBoardInCheckPos((r, c + 2), True): 
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r, c+2), isWhiteKingCastle = True))
            if self.whiteCanCastleQueenSide and not self.inCheck and not castleCheck:
                if (not self.containsPiece((r, c - 1))) and (not self.containsPiece((r, c - 2))) and (not self.containsPiece((r, c - 3))): 
                    if not self.isBoardInCheckPos((r, c - 1), True) and not self.isBoardInCheckPos((r, c - 2), True) and not self.isBoardInCheckPos((r, c - 3), True):
                        possibleMoves.append(move(initialPos = (r,c), finalPos = (r, c - 2), isWhiteQueenCastle = True))
        if not legalCheck:
            return possibleMoves
        legalMoves = list()
        for potentialMove in possibleMoves:
            isLegal, _ = self.makeMove(move = potentialMove, isReal=False)
            if isLegal:
                legalMoves.append(potentialMove)
        return legalMoves

    #copy.makeMove(move, isReal=True, isBot=True)
    def makeMove(self, move: move, isReal: bool = True, isBot : bool = False, notationOn = False): 
        if isReal and notationOn:
            notation = self.getNotation(move)
        else:
            notation = None
        isCaptureOrPawnMove = False
        if not isReal:
            prevBoard = copy.deepcopy(self.board)
            prevWhiteKingCastle = self.whiteCanCastleKingSide
            prevWhiteQueenCastle = self.whiteCanCastleQueenSide
            prevBlackKingCastle = self.blackCanCastleKingSide
            prevBlackQueenCastle = self.blackCanCastleQueenSide
            prevMovedForwardTwoSpaces = self.movedForwardTwoSpaces
            prevIsWhiteTurn = self.isWhiteTurn
            prevHighlightGrid = copy.deepcopy(self.highlightBoard)

        if move.isWhiteKingCastle:
            self.board[4][0] = 0
            self.board[5][0] = 10
            self.board[6][0] = 12
            self.board[7][0] = 0
            self.whiteCanCastleKingSide = False
            self.whiteCanCastleQueenSide = False
        elif move.isWhiteQueenCastle:
            self.board[0][0] = 0
            self.board[1][0] = 0
            self.board[2][0] = 12
            self.board[3][0] = 10
            self.board[4][0] = 0
            self.whiteCanCastleKingSide = False
            self.whiteCanCastleQueenSide = False
        elif move.isBlackKingCastle:
            self.board[4][7] = 0
            self.board[5][7] = 4
            self.board[6][7] = 6
            self.board[7][7] = 0
            self.blackCanCastleKingSide = False
            self.blackCanCastleQueenSide = False
        elif move.isBlackQueenCastle:
            self.board[0][7] = 0
            self.board[1][7] = 0
            self.board[2][7] = 6
            self.board[3][7] = 4
            self.board[4][7] = 0
            self.blackCanCastleKingSide = False
            self.blackCanCastleQueenSide = False
        else:
            initialR, initialC = move.initialPos
            finalR, finalC = move.finalPos
            pieceId = self.board[initialC][initialR]
            if self.board[finalC][finalR] > 0 or pieceId == 1 or pieceId == 7:
                isCaptureOrPawnMove = True
            self.board[initialC][initialR] = 0
            if not move.removeEnPassantPos is None:
                enPassantR, enPassantC = move.removeEnPassantPos
                self.board[enPassantC][enPassantR] = 0
            self.movedForwardTwoSpaces = move.enPassantIndex
            if (pieceId == 1) and (finalR == 0) and isReal:
                # Black Pawn Promotion
                if isBot:
                    newPieceId = move.promotionPieceId
                else:
                    newPieceId = self.promotionPrompt()
                self.board[finalC][finalR] = newPieceId
            elif (pieceId == 7) and (finalR == 7) and isReal:
                # White Pawn Promotion
                if isBot:
                    newPieceId = move.promotionPieceId
                else:
                    newPieceId = self.promotionPrompt()
                self.board[finalC][finalR] = newPieceId
            else:
                self.board[finalC][finalR] = pieceId
            if pieceId == 4 or pieceId == 6:
                self.blackCanCastleKingSide = False
                self.blackCanCastleQueenSide = False
            elif pieceId == 10 or pieceId == 12:
                self.whiteCanCastleKingSide = False
                self.whiteCanCastleQueenSide = False
        if not isReal:
            if self.isBoardInCheck():
                safe = False
            else:
                safe = True
            time2 = time.perf_counter()
        else:
            safe = True
            self.resetHighlight()
            self.isWhiteTurn = not self.isWhiteTurn
            if self.isWhiteTurn:
                self.turn += 1
            if notationOn:
                checkmateStatus, _, _ = self.getCheckmateStatus()
                if checkmateStatus == 1:
                    notation += " 1/2-1/2"
                elif checkmateStatus > 1:
                    notation += "#"
                elif self.isBoardInCheck():
                    notation += "+"
            hashableTable = self.hashBoard()
            if hashableTable in self.boardHistory:
                self.boardHistory[hashableTable] += 1
            else:
                self.boardHistory[hashableTable] = 1
            if isCaptureOrPawnMove:
                self.movesSinceCaptureOrPawnMove = 0
            else:
                self.movesSinceCaptureOrPawnMove += 1
        if not isReal:
            self.board = prevBoard
            self.whiteCanCastleKingSide = prevWhiteKingCastle
            self.whiteCanCastleQueenSide = prevWhiteQueenCastle
            self.blackCanCastleKingSide = prevBlackKingCastle
            self.blackCanCastleQueenSide = prevBlackQueenCastle
            self.movedForwardTwoSpaces = prevMovedForwardTwoSpaces
            self.isWhiteTurn = prevIsWhiteTurn
            self.highlightBoard = prevHighlightGrid
            notation = None     
        self.lastMove = move
        return safe, notation

    def promotionPrompt(self):
        isBlack = not self.isWhiteTurn
        win = GraphWin("Promotion Box", boxSize * 4, boxSize)
        for c in range(4):
            rect = Rectangle(Point(c * boxSize, 0), Point((c + 1) * boxSize, boxSize))
            rect.setFill(color_rgb(220,185,145))
            rect.setOutline('black')
            rect.draw(win)
        if isBlack:
            img = Image(Point(0.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/Black_Knight.png')
            img.draw(win)
            img = Image(Point(1.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/Black_Bishop.png')
            img.draw(win)
            img = Image(Point(2.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/Black_Rook.png')
            img.draw(win)
            img = Image(Point(3.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/Black_Queen.png')
            img.draw(win)
        else:
            img = Image(Point(0.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/White_Knight.png')
            img.draw(win)
            img = Image(Point(1.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/White_Bishop.png')
            img.draw(win)
            img = Image(Point(2.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/White_Rook.png')
            img.draw(win)
            img = Image(Point(3.5 * boxSize, 0.5 * boxSize), 'chessPiecePictures/White_Queen.png')
            img.draw(win)  

        point = win.getMouse()
        x = math.floor(point.getX() / boxSize)
        if x == 0 and isBlack:
            pieceId = 2
        elif x == 1 and isBlack:
            pieceId = 3
        elif x == 2 and isBlack:
            pieceId = 4
        elif x == 3 and isBlack:
            pieceId = 5
        elif x == 0 and not isBlack:
            pieceId = 8
        elif x == 1 and not isBlack:
            pieceId = 9
        elif x == 2 and not isBlack:
            pieceId = 10
        elif x == 3 and not isBlack:
            pieceId = 11
        win.close()
        return pieceId

    def getAllMoves(self):
        moves = list()
        if self.isWhiteTurn:
            for r in range(8):
                for c in range(8):
                    pos = r,c
                    if self.isWhitePos(pos):
                        moves.extend(self.getAllMovesPos(pos))
        else:
            for r in range(8):
                for c in range(8):
                    pos = r,c
                    if self.isBlackPos(pos):
                        moves.extend(self.getAllMovesPos(pos))
        return moves

    def getKingPos(self, isWhiteKing):
        if isWhiteKing:
            for r in range(8):
                for c in range(8):
                    if self.board[c][r] == 12:
                        return (r,c)
        else:
            for r in range(8):
                for c in range(8):
                    if self.board[c][r] == 6:
                        return (r,c)
        return None

    def checkIfPosInCheck(self, pos):
        isBlack = not self.isWhiteTurn
        r,c = pos
        
        if isBlack:
            #Check nearby white pawn
            rawPositions = []
            rawPositions.append((r + 1, c - 1))
            rawPositions.append((r + 1, c + 1))
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 7:
                        return True

            #Check nearby white knight
            rawPositions = []
            rawPositions.append((r - 2, c - 1))
            rawPositions.append((r - 2, c + 1))
            rawPositions.append((r - 1, c - 2))
            rawPositions.append((r - 1, c + 2))
            rawPositions.append((r + 2, c - 1))
            rawPositions.append((r + 2, c + 1))
            rawPositions.append((r + 1, c - 2))
            rawPositions.append((r + 1, c + 2))
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 8:
                        return True

            #Check nearby white bishop
            rawPositions = []
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1

            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 9:
                        return True

            #Check nearby white rook
            rawPositions = []
            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)

            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 10:
                        return True

            #Check nearby white queen
            rawPositions = []
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1

            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isBlackPos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isBlackPos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isBlackPos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)

            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 11:
                        return True

            #Check nearby white king
            rawPositions = []
            rawPositions.append((r - 1, c - 1))
            rawPositions.append((r - 1, c))
            rawPositions.append((r - 1, c + 1))
            rawPositions.append((r, c - 1))
            rawPositions.append((r, c + 1))
            rawPositions.append((r + 1, c - 1))
            rawPositions.append((r + 1, c))
            rawPositions.append((r + 1, c + 1))
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 12:
                        return True

        else:
            #Check nearby black pawn
            rawPositions = []
            rawPositions.append((r - 1, c - 1))
            rawPositions.append((r - 1, c + 1))
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 1:
                        return True

            #Check nearby black knight
            rawPositions = []
            rawPositions.append((r - 2, c - 1))
            rawPositions.append((r - 2, c + 1))
            rawPositions.append((r - 1, c - 2))
            rawPositions.append((r - 1, c + 2))
            rawPositions.append((r + 2, c - 1))
            rawPositions.append((r + 2, c + 1))
            rawPositions.append((r + 1, c - 2))
            rawPositions.append((r + 1, c + 2))
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 2:
                        return True

            #Check nearby black bishop
            rawPositions = []
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1

            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 3:
                        return True

            #Check nearby black rook
            rawPositions = []
            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)

            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 4:
                        return True

            #Check nearby black queen
            rawPositions = []
            # diagonal down-right
            tempPosR = r + 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = r - 1
            tempPosC = c + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = r + 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = r - 1
            tempPosC = c - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPosC -= 1

            # down
            tempPosR = r + 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isWhitePos(tempPos):
                    break
                tempPosR += 1
                tempPos = (tempPosR, c)

            # diagonal up
            tempPosR = r - 1
            tempPos = (tempPosR, c)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((tempPosR, c))
                if self.isWhitePos(tempPos):
                    break
                tempPosR -= 1
                tempPos = (tempPosR, c)

            # left
            tempPosC = c - 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosC -= 1
                tempPos = (r, tempPosC)

            # right
            tempPosC = c + 1
            tempPos = (r, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                rawPositions.append((r, tempPosC))
                if self.isWhitePos(tempPos):
                    break
                tempPosC += 1
                tempPos = (r, tempPosC)
                
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 5:
                        return True

            #Check nearby black king
            rawPositions = []
            rawPositions.append((r - 1, c - 1))
            rawPositions.append((r - 1, c))
            rawPositions.append((r - 1, c + 1))
            rawPositions.append((r, c - 1))
            rawPositions.append((r, c + 1))
            rawPositions.append((r + 1, c - 1))
            rawPositions.append((r + 1, c))
            rawPositions.append((r + 1, c + 1))
            for position in rawPositions:
                r, c = position
                if self.isPosOnBoard(position):
                    if self.board[c][r] == 6:
                        return True

        return False

    def isBoardInCheckPos(self, checkPos, castleCheck = False):
        if self.isWhiteTurn:
            for r in range(8):
                for c in range(8):
                    pos = r,c
                    if self.isBlackPos(pos):
                        for move in self.getAllMovesPos(pos, legalCheck=False, castleCheck = castleCheck):
                            if checkPos == move.finalPos:
                                return True
        else:
            for r in range(8):
                for c in range(8):
                    pos = r,c
                    if self.isWhitePos(pos):
                        for move in self.getAllMovesPos(pos, legalCheck=False, castleCheck = castleCheck):
                            if checkPos == move.finalPos:
                                return True
        return False

    #Checks to see if prevMove would cause the opponent to be in check
    """
    def isBoardInCheck(self, prevMove):
        if prevMove == None:
            return False
        originR, originC = prevMove.initialPos
        targetR, targetC = prevMove.finalPos
        pieceId = self.board[originC][originR]
        kingR, kingC = self.getKingPos(self.isWhiteTurn)

        #Target square check black pawn
        if pieceId == 1:
            if (targetR + 1, targetC - 1) == (kingR, kingC) or (targetR + 1, targetC + 1) == (kingR, kingC):
                return True

        #Target square check black knight
        if pieceId == 2:
            if (targetR - 2, targetC - 1) == (kingR, kingC) or (targetR - 2, targetC + 1) == (kingR, kingC) \
                    or (targetR - 1, targetC - 2) == (kingR, kingC) or (targetR - 1, targetC + 2) == (kingR, kingC) \
                    or (targetR + 2, targetC + 1) == (kingR, kingC) or (targetR + 2, targetC - 1) == (kingR, kingC) \
                    or (targetR + 1, targetC + 2) == (kingR, kingC) or (targetR + 1, targetC - 2) == (kingR, kingC):
                return True

        #Target square check black bishop
        if pieceId == 3:

            # diagonal down-right
            tempPosR = targetR + 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = targetR - 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = targetR + 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = targetR - 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC -= 1

        #Target square check black rook
        if pieceId == 4:

            # down
            tempPosR = targetR + 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPos = (tempPosR, targetC)

            # diagonal up
            tempPosR = targetR - 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPos = (tempPosR, targetC)

            # left
            tempPosC = targetC - 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC -= 1
                tempPos = (targetR, tempPosC)

            # right
            tempPosC = targetC + 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC += 1
                tempPos = (targetR, tempPosC)

        #Target square check black queen
        if pieceId == 5:

            # diagonal down-right
            tempPosR = targetR + 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = targetR - 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = targetR + 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = targetR - 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC -= 1

            # down
            tempPosR = targetR + 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPos = (tempPosR, targetC)

            # up
            tempPosR = targetR - 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPos = (tempPosR, targetC)

            # left
            tempPosC = targetC - 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC -= 1
                tempPos = (targetR, tempPosC)

            # right
            tempPosC = targetC + 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                if self.isWhitePos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC += 1
                tempPos = (targetR, tempPosC)

        #Target square check black king
        if pieceId == 6:

            if (targetR - 1, targetC - 1) == (kingR, kingC) or (targetR - 1, targetC) == (kingR, kingC) \
                    or (targetR - 1, targetC + 1) == (kingR, kingC) or (targetR, targetC - 1) == (kingR, kingC) \
                    or (targetR, targetC + 1) == (kingR, kingC) or (targetR + 1, targetC - 1) == (kingR, kingC) \
                    or (targetR + 1, targetC) == (kingR, kingC) or (targetR + 1, targetC + 1) == (kingR, kingC):
                return True

        #Target square check white pawn
        if pieceId == 7:
            if (targetR - 1, targetC - 1) == (kingR, kingC) or (targetR - 1, targetC + 1) == (kingR, kingC):
                return True

        #Target square check white knight
        if pieceId == 8:
            if (targetR - 2, targetC - 1) == (kingR, kingC) or (targetR - 2, targetC + 1) == (kingR, kingC) \
                    or (targetR - 1, targetC - 2) == (kingR, kingC) or (targetR - 1, targetC + 2) == (kingR, kingC) \
                    or (targetR + 2, targetC + 1) == (kingR, kingC) or (targetR + 2, targetC - 1) == (kingR, kingC) \
                    or (targetR + 1, targetC + 2) == (kingR, kingC) or (targetR + 1, targetC - 2) == (kingR, kingC):
                return True

        #Target square check white bishop
        if pieceId == 9:

            # diagonal down-right
            tempPosR = targetR + 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = targetR - 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = targetR + 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = targetR - 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC -= 1

        #Target square check white rook
        if pieceId == 10:

            # down
            tempPosR = targetR + 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPos = (tempPosR, targetC)

            # up
            tempPosR = targetR - 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPos = (tempPosR, targetC)

            # left
            tempPosC = targetC - 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC -= 1
                tempPos = (targetR, tempPosC)

            # right
            tempPosC = targetC + 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC += 1
                tempPos = (targetR, tempPosC)

        #Target square check white queen
        if pieceId == 11:

            # diagonal down-right
            tempPosR = targetR + 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC += 1

            # diagonal up-right
            tempPosR = targetR - 1
            tempPosC = targetC + 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC += 1

            # diagonal down-left
            tempPosR = targetR + 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPosC -= 1

            # diagonal up-left
            tempPosR = targetR - 1
            tempPosC = targetC - 1
            tempPos = (tempPosR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPosC -= 1

            # down
            tempPosR = targetR + 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR += 1
                tempPos = (tempPosR, targetC)

            # up
            tempPosR = targetR - 1
            tempPos = (tempPosR, targetC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosR -= 1
                tempPos = (tempPosR, targetC)

            # left
            tempPosC = targetC - 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC -= 1
                tempPos = (targetR, tempPosC)

            # right
            tempPosC = targetC + 1
            tempPos = (targetR, tempPosC)
            while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                if self.isBlackPos(tempPos):
                    if tempPos == (kingR, kingC):
                        return True
                    break
                tempPosC += 1
                tempPos = (targetR, tempPosC)

        #Target square check white king
        if pieceId == 12:

            if (targetR - 1, targetC - 1) == (kingR, kingC) or (targetR - 1, targetC) == (kingR, kingC) \
                    or (targetR - 1, targetC + 1) == (kingR, kingC) or (targetR, targetC - 1) == (kingR, kingC) \
                    or (targetR, targetC + 1) == (kingR, kingC) or (targetR + 1, targetC - 1) == (kingR, kingC) \
                    or (targetR + 1, targetC) == (kingR, kingC) or (targetR + 1, targetC + 1) == (kingR, kingC):
                return True

        #Origin square check

        #Check from the left 
        if (originR == kingR) and (originC < kingC):
            tempPosC = originC - 1
            tempPos = (originR, tempPosC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[tempPosC][originR] == 4 or self.board[tempPosC][originR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosC = originC - 1
                    tempPos = (originR, tempPosC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[tempPosC][originR] == 10 or self.board[tempPosC][originR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosC = originC - 1
                    tempPos = (originR, tempPosC)

        #Check from the right 
        if (originR == kingR) and (originC > kingC):
            tempPosC = originC + 1
            tempPos = (originR, tempPosC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[tempPosC][originR] == 4 or self.board[tempPosC][originR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosC = originC + 1
                    tempPos = (originR, tempPosC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[tempPosC][originR] == 10 or self.board[tempPosC][originR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosC = originC + 1
                    tempPos = (originR, tempPosC)

        #Check from the top 
        if (originC == kingC) and (originR < kingR):
            tempPosR = originR - 1
            tempPos = (tempPosR, originC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[tempPosC][originR] == 4 or self.board[tempPosC][originR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosR = originR - 1
                    tempPos = (tempPosR, originC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[tempPosC][originR] == 10 or self.board[tempPosC][originR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosR = originR - 1
                    tempPos = (tempPosR, originC)

        #Check from the bottom
        if (originC == kingC) and (originR > kingR):
            tempPosR = originR + 1
            tempPos = (tempPosR, originC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[originC][tempPosR] == 4 or self.board[originC][tempPosR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosR = originR + 1
                    tempPos = (tempPosR, originC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[originC][tempPosR] == 10 or self.board[originC][tempPosR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosR = originR + 1
                    tempPos = (tempPosR, originC)

        #Check from the top-left
        if (originC - originR == kingC - kingR) and (originR < kingR):
            tempPosR = originR - 1
            tempPosC = originC - 1
            tempPos = (tempPosR, originC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[originC][tempPosR] == 4 or self.board[originC][tempPosR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosR = originR - 1
                    tempPosC = originC - 1
                    tempPos = (tempPosR, originC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[originC][tempPosR] == 10 or self.board[originC][tempPosR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosR = originR - 1
                    tempPosC = originC - 1
                    tempPos = (tempPosR, originC)

        #Check from the bottom-right
        if (originC - originR == kingC - kingR) and (originR > kingR):
            tempPosR = originR + 1
            tempPosC = originC + 1
            tempPos = (tempPosR, originC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[tempPosC][originR] == 3 or self.board[tempPosC][originR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosR = originR + 1
                    tempPosC = originC + 1
                    tempPos = (tempPosR, originC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[tempPosC][originR] == 9 or self.board[tempPosC][originR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosR = originR + 1
                    tempPosC = originC + 1
                    tempPos = (tempPosR, originC)

        #Check from the top-right
        if (originC + originR == kingC + kingR) and (originR < kingR):
            tempPosR = originR - 1
            tempPosC = originC + 1
            tempPos = (tempPosR, originC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[tempPosC][originR] == 3 or self.board[tempPosC][originR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosR = originR - 1
                    tempPosC = originC + 1
                    tempPos = (tempPosR, originC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[tempPosC][originR] == 9 or self.board[tempPosC][originR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosR = originR - 1
                    tempPosC = originC + 1
                    tempPos = (tempPosR, originC)

        #Check from the bottom-left
        if (originC + originR == kingC + kingR) and (originR > kingR):
            tempPosR = originR + 1
            tempPosC = originC - 1
            tempPos = (tempPosR, originC)
            if self.isWhiteTurn:
                while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                    if self.board[tempPosC][originR] == 3 or self.board[tempPosC][originR] == 5:
                        return True
                    elif self.isBlackPos(tempPos):
                        break
                    tempPosR = originR + 1
                    tempPosC = originC - 1
                    tempPos = (tempPosR, originC)
            else:
                while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                    if self.board[tempPosC][originR] == 9 or self.board[tempPosC][originR] == 11:
                        return True
                    elif self.isWhitePos(tempPos):
                        break
                    tempPosR = originR + 1
                    tempPosC = originC - 1
                    tempPos = (tempPosR, originC)

        # Have to check en-passant discovered checks (extra pawn removed)
        if not prevMove.enPassantIndex is None:
            if self.isWhiteTurn:
                origin2C = prevMove.enPassantIndex
                origin2R = 3

            else:
                origin2C = prevMove.enPassantIndex
                origin2R = 4

            #Check from the top-left
            if (origin2C - origin2R == kingC - kingR) and (origin2R < kingR):
                tempPosR = origin2R - 1
                tempPosC = origin2C - 1
                tempPos = (tempPosR, origin2C)
                if self.isWhiteTurn:
                    while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                        if self.board[tempPosC][origin2R] == 3 or self.board[tempPosC][origin2R] == 5:
                            return True
                        elif self.isBlackPos(tempPos):
                            break
                        tempPosR = origin2R - 1
                        tempPosC = origin2C - 1
                        tempPos = (tempPosR, origin2C)
                else:
                    while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                        if self.board[tempPosC][origin2R] == 9 or self.board[tempPosC][origin2R] == 11:
                            return True
                        elif self.isWhitePos(tempPos):
                            break
                        tempPosR = origin2R - 1
                        tempPosC = origin2C - 1
                        tempPos = (tempPosR, origin2C)

            #Check from the bottom-right
            if (origin2C - origin2R == kingC - kingR) and (origin2R > kingR):
                tempPosR = originR + 1
                tempPosC = originC + 1
                tempPos = (tempPosR, origin2C)
                if self.isWhiteTurn:
                    while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                        if self.board[tempPosC][origin2R] == 3 or self.board[tempPosC][origin2R] == 5:
                            return True
                        elif self.isBlackPos(tempPos):
                            break
                        tempPosR = origin2R + 1
                        tempPosC = origin2C + 1
                        tempPos = (tempPosR, origin2C)
                else:
                    while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                        if self.board[tempPosC][origin2R] == 9 or self.board[tempPosC][origin2R] == 11:
                            return True
                        elif self.isWhitePos(tempPos):
                            break
                        tempPosR = origin2R + 1
                        tempPosC = origin2C + 1
                        tempPos = (tempPosR, origin2C)

            #Check from the top-right
            if (origin2C + origin2R == kingC + kingR) and (origin2R < kingR):
                tempPosR = origin2R - 1
                tempPosC = origin2C + 1
                tempPos = (tempPosR, origin2C)
                if self.isWhiteTurn:
                    while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                        if self.board[tempPosC][origin2R] == 3 or self.board[tempPosC][origin2R] == 5:
                            return True
                        elif self.isBlackPos(tempPos):
                            break
                        tempPosR = origin2R - 1
                        tempPosC = origin2C + 1
                        tempPos = (tempPosR, origin2C)
                else:
                    while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                        if self.board[tempPosC][origin2R] == 9 or self.board[tempPosC][origin2R] == 11:
                            return True
                        elif self.isWhitePos(tempPos):
                            break
                        tempPosR = origin2R - 1
                        tempPosC = origin2C + 1
                        tempPos = (tempPosR, origin2C)

            #Check from the bottom-left
            if (origin2C + origin2R == kingC + kingR) and (origin2R > kingR):
                tempPosR = origin2R + 1
                tempPosC = origin2C - 1
                tempPos = (tempPosR, origin2C)
                if self.isWhiteTurn:
                    while self.isPosOnBoard(tempPos) and not self.isWhitePos(tempPos):
                        if self.board[tempPosC][origin2R] == 3 or self.board[tempPosC][origin2R] == 5:
                            return True
                        elif self.isBlackPos(tempPos):
                            break
                        tempPosR = origin2R + 1
                        tempPosC = origin2C - 1
                        tempPos = (tempPosR, origin2C)
                else:
                    while self.isPosOnBoard(tempPos) and not self.isBlackPos(tempPos):
                        if self.board[tempPosC][origin2R] == 9 or self.board[tempPosC][origin2R] == 11:
                            return True
                        elif self.isWhitePos(tempPos):
                            break
                        tempPosR = origin2R + 1
                        tempPosC = origin2C - 1
                        tempPos = (tempPosR, origin2C)

        return False
    """
    
    def isBoardInCheck(self): #Takes too long
        if self.isWhiteTurn:
            kingPos = self.getKingPos(True)
            for r in range(8):
                for c in range(8):
                    pos = r,c
                    if self.isBlackPos(pos):
                        for move in self.getAllMovesPos(pos, legalCheck=False):
                            if kingPos == move.finalPos:
                                return True
        else:
            kingPos = self.getKingPos(False)
            for r in range(8):
                for c in range(8):
                    pos = r,c
                    if self.isWhitePos(pos):
                        for move in self.getAllMovesPos(pos, legalCheck=False):
                            if kingPos == move.finalPos:
                                return True
        return False
    
    def drawBoard(self, window : GraphWin):
        if not self.initializedVisual:
            self.initializedVisual = True
            imgBank.drawBoardWithoutPieces(window)
        imgBank.drawBoard(window, self)

    def isThreefoldRepetition(self):
        for val in self.boardHistory.values():
            if val >= 3:
                return True
        return False

    def isSufficientMaterial(self):
        """ 
        You can check with
        - A rook
        - A queen
        - A bishop and knight
        - Two bishops
        - Three Knights
        - A pawn
        """
        numberOfWhiteBishops = 0
        numberOfBlackBishops = 0
        numberOfWhiteKnights = 0
        numberOfBlackKnights = 0
        for c in range(8):
            for r in range(8):
                pieceId = self.board[c][r]
                if pieceId == 1 or pieceId == 4 or pieceId == 5 or pieceId == 7 or pieceId == 10 or pieceId == 11:
                    return True
                elif pieceId == 2:
                    numberOfBlackKnights += 1
                    if numberOfBlackKnights >= 3:
                        return True
                    elif numberOfBlackKnights >= 1 and numberOfBlackBishops >= 1:
                        return True
                elif pieceId == 3:
                    numberOfBlackBishops += 1
                    if numberOfBlackBishops >= 2:
                        return True
                    elif numberOfBlackKnights >= 1 and numberOfBlackBishops >= 1:
                        return True
                elif pieceId == 8:
                    numberOfWhiteKnights += 1
                    if numberOfWhiteKnights >= 3:
                        return True
                    elif numberOfWhiteKnights >= 1 and numberOfWhiteBishops >= 1:
                        return True
                elif pieceId == 9:
                    numberOfWhiteBishops += 1
                    if numberOfWhiteBishops >= 2:
                        return True
                    elif numberOfWhiteKnights >= 1 and numberOfWhiteBishops >= 1:
                        return True
        return False

    def isFiftyMoveRule(self):
        return self.movesSinceCaptureOrPawnMove >= 50

    # 0 = nothing, 1 = stalemate, 2 = white wins, 3 = black wins
    def getCheckmateStatus(self, noKnownMoves = False):
        if noKnownMoves:
            noLegalMoves = True
        else:
            noLegalMoves = len(self.getAllMoves()) == 0
        threefoldRepetition = self.isThreefoldRepetition()
        sufficientMaterial = self.isSufficientMaterial()
        fiftyMoveRule = self.isFiftyMoveRule()
        inCheck = self.isBoardInCheck()
        if (not noLegalMoves) and (threefoldRepetition or (not sufficientMaterial) or fiftyMoveRule):
            return 1, inCheck, (False, threefoldRepetition, (not sufficientMaterial), fiftyMoveRule)
        elif noLegalMoves:
            if inCheck:
                if self.isWhiteTurn:
                    return 3, inCheck, (True, False, False, False)
                else:
                    return 2, inCheck, (True, False, False, False)
            else:
                return 1, inCheck, (True, False, False, False)
        return 0, inCheck, (False, False, False, False)



