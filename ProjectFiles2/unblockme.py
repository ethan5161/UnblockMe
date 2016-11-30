### Name: Blake Buthod, Ethan Brizendine, Thomas Goodman, & George Wood
### Date: 12-9-2016
### File unblockme.py
### Implements the unblock me style puzzle for state space search

from informedSearchUnblock import *
from block import *
from display import *

class UnblockState(InformedProblemState):
    """
    The unblock me style puzzle: Given a 6x6 grid filled with blocks
    and having one exit, the goal is to get a particular block to the exit.
    Blocks are either 2 or 3 tiles long, and only move in the direction
    that they are oriented. In other words, vertical blocks can only move
    vertically, and horizontal blocks can only move horizontally.
    The target block is always 2 tiles long, horizontal and designated
    with the number 1h, with the exit located at (2,6).
    """
    # List index of target block, static
    targetInd = None
    def __init__(self, blockList):
        self.blockList = blockList
        self.boardSize = 6
    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
    def illegal(self):
        """
        Checks if this current state is illegal in the context of the puzzle
        """

        
        # A list that holds coordinates that have been encountered
        occupiedSpaces = []

        # The maximum number of blocks that can fit in a 6x6 square is 18.
        # So, if the number of blocks is greater than 18, the state is illegal.
        if len(self.blockList) > 18:
            return 1

        # For each block, checks if a block collision has occurred.
        # and adds the coordinates it occupies to the list.
        # Then checks if it is has out of bounds.
        for block in self.blockList:
            if block.collidedPieces == 1:
                return 1
            coordList = block.getCoords()
            for coords in coordList:
                if coords in occupiedSpaces:
                    return 1

                x = coords[0]
                y = coords[1]
        
            # The 0 space must be out of bounds in the horizontal plane
            # to be off the board, so it is not taken into consideration
            # when checking for horizontal bounds.
            
                size = block.getSize()
                if block.getNum() != 0:
                    if size == 3:
                        if x > 5 or x < 0 or y > 5 or y < 0:
                            return 1
                    elif size == 2:
                        if x > 5 or x < 0 or y > 5 or y < 0:
                            return 1
                else:
                    if y != 2:
                        return 1
            occupiedSpaces.append(coordList)
        return false
                    
    def equals(self, state):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        comparedBlockList = state.blockList
        for n in (len(self.blockList)):
            # Gets corresponding blocks from the list of the current state
            # and the list of the state being compared to.
            # Compares based on the number designation of the block.
            # These do not change after they are set, so two pieces with
            # the same number will always be equal.
            block1 = blockList[n]
            block2 = comparedBlockList[n]

            if (block1.getNum() != block2.getNum()):
                return false
        return true

        
    ## A* dist search    
    def heuristic(self):
        """
        Estimates the cost of getting from the current state to the goal
        state. This heuristic checks how many blocks are in between the
        target block and the exit.
        """
        interferingBlocks = 0
        targetX,targetY = self.blockList[0].getCoords()
        for block in self.blockList:
            x,y = block.getCoords()
            if block.getNum != 0:
                if (y == 2) and (x > (targetX + 1)):
                    interferingBlocks += 1
        return interferingBlocks

    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of possible successors to the current
        state, some of which may be illegal.  
        """
        possibleStates = []
        
        for block in blockList:
            for n in range(-boardSize, boardSize, 1):
                tempBlockList = blockList
                block.possibleMove(n, tempBlockList)
                possibleStates.append(tempBlockList)

        return possibleStates

# Gets problem state from input text file.
with open("unblockState.txt") as textFile:
    probState = [line.split() for line in textFile]

blockCount = 0
blockList = []
foundBlocks = []
probSize = len(probState)

"""
Uncomment for input test
for n in range(probSize):
    print("[", end=" ")
    for m in range(probSize):
        print(probState[n][m], end=" ")
    print("]")
"""

# Takes the input problem state and creates a list of block objects from it
for row in range(probSize):
    for column in range(probSize):
        size = 2 #Smallest size is 2, if larger is found we'll update that value
        #Get the current number at the space being checked
        checkBlock = int(probState[row][column])
        #Make sure the space is a block that isn't already found
        if checkBlock != 0 and checkBlock not in foundBlocks:
             #Check for horizontal
            if column + 1 < probSize and int(probState[row][column + 1]) == checkBlock:
                #Check if the block is 3 long
                if column + 2 < probSize and int(probState[row][column + 2]) == checkBlock:
                    size = 3
                blockList.append(Block(checkBlock,row,column,size,"h"))
                foundBlocks.append(checkBlock)
            #The block is not horizontal, so check for vertical
            elif row + 1 < probSize and int(probState[row + 1][column]) == checkBlock:
                if row + 2 < probSize and int(probState[row + 2][column]) == checkBlock:
                    size = 3
                blockList.append(Block(checkBlock,row,column,size,"v"))
                foundBlocks.append(checkBlock)   
            else:
                print("Something went wrong.")
                
            #Check for the red block
            if checkBlock == 1:
                UnblockState.targetInd = len(blockList) - 1

display = Display(blockList)
display.drawBlocks()
                    
# Initiates the informed search towards the goal state
#InformedSearchUnblock(UnblockState(blockList))
