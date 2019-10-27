#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean result 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters
        """
        self.fingerprint = []
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

    def check_status(self,board):

        for i in board:
            for j in i:
                if j==True:
                    return False
        
        return True

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}

    def getAction(self, gameState, gameRules):

        if  gameState.boards[0][4]!=True and gameRules.check_status(gameState.boards):
            gameRules.preAction = "A4"
            gameRules.fingerprint.append(gameState.generateSuccessor("A4"))
            return gameRules.preAction

        states = [] 
        i=0
        while i < 3:
            if gameRules.deadTest(gameState.boards[i]) == False:states.append(chr(i + 65) + "4")
            i=i+1
    
        preGameState = gameRules.fingerprint.pop()
        previous_opp_loc= [chr(i + 65)+str(j) for i, x in enumerate(gameState.boards) for j, y in enumerate(x) if y != preGameState.boards[i][j]][0]


        actions = gameState.getLegalActions(gameRules)
        no_action=len(actions)
        no_states=len(states)
        if no_action <13:self.findmax(gameState,gameRules,None,0)
        count=0
        if no_states == 3:
            for action in actions:
                for i in range(3):
                    if self.findmin(gameState.generateSuccessor(action), gameRules, states[i], 7) == -99:
                        self.winAction = action
                        count=1
                if count==1:break
                if previous_opp_loc[0] != gameRules.preAction[0]:
                    x=0
                    while x<9:
                        if gameState.boards[2][x] != False:break
                        x=x+1
                    else:
                        gameRules.fingerprint.append(gameState.generateSuccessor("C4"))
                        gameRules.preAction = "C4"
                        return gameRules.preAction

                if previous_opp_loc[0] == "C":
                    x=0
                    while x<9:
                        if gameState.boards[1][x] != False:break
                        x=x+1
                    else:
                        gameRules.fingerprint.append(gameState.generateSuccessor("B4"))
                        gameRules.preAction = "B4"
                        return gameRules.preAction

                lis = []
                for i,x in enumerate(gameState.boards[ord(previous_opp_loc[0])-65]):
                    if x == True:
                        lis.append(i)
                if len(lis)>1:
                    for j in range(9):
                        if j % 3 != lis[1] % 3 and j//3 !=lis[1]//3 and j//3 !=lis[0]//3 and j % 3 != lis[0] % 3 :
                            self.winAction = previous_opp_loc[0]+str(j)
                            break
                else:
                    self.findmax(gameState, gameRules, previous_opp_loc, 0)                            

        elif len(states) == 1:self.findmax(gameState, gameRules, states[0], 0)
        
        if len(states)==2:
             for x in range(3):
                 for y in range(9):
                     if gameState.boards[x][y]!=False:break
                 else:
                    self.winAction = chr(x + 65) + "4"
                    break
             else:

                    value = self.findmax(gameState, gameRules, states[0], 0)  
                    nvalue = self.findmax(gameState, gameRules, states[1], 0)
                    if  nvalue==198 and value==-198:
                        for i in range(no_action):
                           if self.findmin(gameState.generateSuccessor(actions[i]), gameRules, states[1], 7)==-198:
                               self.winAction = actions[i]
                               break
                        else:
                            lis = []
                            for i, x in enumerate(gameState.boards[ord(states[1][0]) - 65]):
                                if x== True:lis.append(i)
                            if len(lis)>1:
                                j=0
                                while j < 9:    
                                    if j % 3 != lis[1] % 3 and j//3 !=lis[1]//3 and j//3 !=lis[0]//3 and j % 3 != lis[0] % 3 :
                                        self.winAction = previous_opp_loc[0]+str(j)
                                        break
                                    j+=1
                    if value ==198 and nvalue == -198:
                        for i in range(no_action):
                            if self.findmin(gameState.generateSuccessor(actions[i]), gameRules, states[0], 7) == -198:
                               self.winAction = actions[i]
                               break
                        else:
                            lis = []
                            for i, x in enumerate(gameState.boards[ord(states[0][0]) - 65]):
                                if x == True:lis.append(i)
                            if len(lis)>1:
                                j=0
                                while j<9:
                                    if j % 3 != lis[1] % 3 and j//3 !=lis[1]//3 and j//3 !=lis[0]//3 and j % 3 != lis[0] % 3 :
                                        self.winAction = previous_opp_loc[0]+str(j)
                                        break
                                    j+=1
                    if value == -198 and nvalue == -198:
                        for i in range(no_action):
                           if self.findmin(gameState.generateSuccessor(actions[i]), gameRules, states[0], 7) == -198:
                               self.winAction = actions[i]
                               break
                           elif self.findmin(gameState.generateSuccessor(actions[i]), gameRules, states[1], 7) == -198:
                               self.winAction = actions[i]
                               break
                        else:
                            lis = []
                            for i, x in enumerate(gameState.boards[ord(states[1][0]) - 65]):
                                if x== True: lis.append(i)
                            if len(lis)>1:
                                j=0
                                while j<9:
                                    if j % 3 != lis[1] % 3 and j//3 !=lis[1]//3 and j//3 !=lis[0]//3 and j % 3 != lis[0] % 3 :
                                        self.winAction = previous_opp_loc[0]+str(j)
                                        break
                                    j+=1
                                            
                    if value==198 and nvalue==198: self.findmax(gameState, gameRules, previous_opp_loc, 0)

        gameRules.preAction = self.winAction
        gameRules.fingerprint.append(gameState.generateSuccessor(self.winAction))
        return gameRules.preAction


    def findmin(self, gameState, gameRules, previous_opp_loc,depth): 
        actions = gameState.getLegalActions(gameRules)
        no_actions=len(actions)
        if no_actions==0:return -(self.getevauluation(gameState, gameRules))
        if previous_opp_loc ==None:
            if gameRules.isGameOver(gameState.boards) or depth == 8:return -(self.getevauluation(gameState, gameRules))
            result = 100000
            i=0
            while i<no_actions:
                successor = gameState.generateSuccessor(actions[i])
                value = self.findmax(successor, gameRules,previous_opp_loc,depth + 1)
                if value<result and depth ==0: self.winAction = actions[i]
                result=min(value,result)
                i=i+1
            return result
        else:
            if gameRules.deadTest(gameState.boards[ord(previous_opp_loc[0]) - 65]) or depth == 8:
                return -self.getevauluation(gameState, gameRules)
            result = 100000
            i=0
            while i<no_actions:
                if actions[i][0] == previous_opp_loc[0]:
                    successor = gameState.generateSuccessor(actions[i])
                    value = self.findmax(successor, gameRules,previous_opp_loc,depth + 1)
                    if value<result and depth ==0: self.winAction = actions[i]
                    result=min(value,result)
                i=i+1
            return result


    def findmax(self, gameState, gameRules, previous_opp_loc,depth):
        actions = gameState.getLegalActions(gameRules)
        no_actions=len(actions)
        if no_actions==0: return self.getevauluation(gameState, gameRules)
        if previous_opp_loc==None:
            if gameRules.isGameOver(gameState.boards) or depth == 8:
                return self.getevauluation(gameState, gameRules)
            result = -10000
            i=0
            while i<no_actions:
                successor = gameState.generateSuccessor(actions[i])
                value = self.findmin(successor, gameRules, previous_opp_loc, depth + 1)
                if value>result and depth ==0: self.winAction = actions[i]
                result=max(value,result)
                i=i+1
            return result
        else:
            if gameRules.deadTest(gameState.boards[ord(previous_opp_loc[0]) - 65]) or depth == 8: return self.getevauluation(gameState,gameRules)
            result = -10000
            i=0
            while i<no_actions:
                if actions[i][0] == previous_opp_loc[0]:
                    successor = gameState.generateSuccessor(actions[i])
                    value = self.findmin(successor, gameRules,previous_opp_loc,depth+1)
                    if value>result and depth ==0: self.winAction = actions[i]
                    result=max(value,result)
                i=i+1
            return result


    def getevauluation(self, gameState, gameRules):
        if gameRules.isGameOver(gameState.boards):
            return 999
        else:
            result = 0
            i=0
            while i < 3:
                if gameRules.deadTest(gameState.boards[i])!=False:
                    result = result + 99
                i=i+1
            return result
        
class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
