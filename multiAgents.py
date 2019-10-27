import random

import util
from game import Agent, Directions
from util import manhattanDistance


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
      

        "*** YOUR CODE HERE ***"

        if successorGameState.isWin():
              return 50000
        newfoodpositions = newFood.asList()
        oldfoodpositions=prevFood.asList()
        food_dist = 0
        for pos in newfoodpositions:
              food_dist = food_dist + manhattanDistance(newPos,pos)
         

        avg_food_dist = float(food_dist/len(newfoodpositions))


        ghost_dist=0
        for pos in successorGameState.getGhostPositions():
              ghost_dist= ghost_dist + manhattanDistance(newPos,pos)

        avg_ghost_dist=float(ghost_dist/len(successorGameState.getGhostPositions()))   
  

        result=successorGameState.getScore()
         

        if successorGameState.isWin():
              return 50000

        if(len(newfoodpositions)>len(oldfoodpositions)):
              result+=500
        
        if (avg_ghost_dist==1):
               result-=5000
        
        if avg_ghost_dist!=0 and avg_food_dist!=0:
              return result + (1/avg_food_dist)-(1/avg_ghost_dist)
        elif avg_food_dist==0:
              return result +(1/avg_ghost_dist)
        elif avg_ghost_dist==0:
              return result - (1/avg_food_dist)
        else:
              return result
              


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        if  gameState.isWin() or gameState.isLose() or self.depth == 0:
              return self.evaluationFunction(gameState)
        v = -1000
        legalActions = gameState.getLegalActions(0)
        if len(legalActions)==0:
              return Directions.STOP
        else:
              for nextaction in legalActions:
                    state = gameState.generateSuccessor(0, nextaction)
                    x = self.findmin(state, self.depth, 1)
                    if x > v:
                          v,action = x,nextaction
              return action
        util.raiseNotDefined()

    def findmin(self, gameState, depth, agentIndex):
          if  gameState.isWin() or gameState.isLose() or depth == 0:
              return self.evaluationFunction(gameState)
          v = 1000
          legalActions = gameState.getLegalActions(agentIndex)
          for nextaction in legalActions:     
              succ=gameState.generateSuccessor(agentIndex,nextaction)
              if agentIndex+1 == gameState.getNumAgents():
                  if v > self.findmax(succ, depth-1):
                        v=self.findmax(succ, depth-1)      
              else:
                  if v > self.findmin(succ, depth, agentIndex+1):
                        v=self.findmin(succ, depth, agentIndex+1)
          return v                                               

    def findmax(self, gameState, depth):
          if  gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
          v = -1000
          legalActions = gameState.getLegalActions(0)
          for nextaction in legalActions:
            succ=gameState.generateSuccessor(0,nextaction)
            if v < self.findmin(succ, depth, 1):
              v=self.findmin(succ, depth, 1)
          return v
        
class AlphaBetaAgent(MultiAgentSearchAgent):  

  def getAction(self, gameState):
    if  gameState.isWin() or gameState.isLose() or self.depth == 0:
      return self.evaluationFunction(gameState)
    v = -100000
    alfa=-100000
    beta=100000
    legalActions = gameState.getLegalActions(0)
    if len(legalActions)==0:
      return Directions.STOP
    else:
      for nextaction in legalActions:
        state = gameState.generateSuccessor(0, nextaction)
        x = self.findmin(state, self.depth, 1, alfa, beta)
        if x > beta:
          return nextaction
        if x > alfa:
          alfa=x
        if x > v:
          v, action = x, nextaction
      return action
      util.raiseNotDefined()

  def findmin(self, gameState, depth, agentIndex,alfa,beta):
    if  gameState.isWin() or gameState.isLose() or depth == 0:
      return self.evaluationFunction(gameState)
    v = 100000
    legalActions = gameState.getLegalActions(agentIndex)
    if len(legalActions) == 0: return self.evaluationFunction(gameState)
    for nextaction in legalActions:
      succ=gameState.generateSuccessor(agentIndex,nextaction)
      if (agentIndex+1 == gameState.getNumAgents()):
          v = min(v ,self.findmax(succ,0, depth-1,alfa,beta))    
          if v < alfa:
            return v
          beta=min(beta,v)                    
      else:
        v= min(v ,self.findmin(succ, depth, agentIndex+1,alfa,beta))
        if v < alfa:
          return v
        beta=min(beta,v)
    return v                                               

  def findmax(self, gameState, agentIndex, depth,alfa,beta):
    if  gameState.isWin() or gameState.isLose() or depth == 0:
      return self.evaluationFunction(gameState)
    v = -100000
    legalActions = gameState.getLegalActions(0)
    if len(legalActions) == 0: return self.evaluationFunction(gameState)
    for nextaction in legalActions:
      succ = gameState.generateSuccessor(agentIndex,nextaction)
      v=max(v , self.findmin(succ, depth, 1,alfa,beta))
      if v > beta:
        return v
      alfa=max(alfa,v)
    return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
            if gameState.isWin() or gameState.isLose() or self.depth == 0:
              return self.evaluationFunction(gameState)
            v = -1000
            legalActions = gameState.getLegalActions(0)
            if len(legalActions)==0:
              return Directions.STOP
            for nextaction in legalActions:
              state = gameState.generateSuccessor(0, nextaction)
              x = self.expected(state, 0, 1)
              if x > v:
                 v = x
                 action = nextaction
            return action
            
    def findmax(self, gameState, depth, agentIndex):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
              return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(agentIndex)
            if len(legalActions) != 0:# we have some actions to chose from
              val = float('-inf')
            else:
              val = self.evaluationFunction(gameState)
            for action in gameState.getLegalActions(agentIndex):
              a = self.expected(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
              if a > val:
                val = a

            return val # return max value


    def expected(self, gameState, depth, agentIndex):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
              return self.evaluationFunction(gameState)       
            value = 0;
            legalActions = gameState.getLegalActions(agentIndex)
            for action in legalActions:
              if agentIndex+1 == gameState.getNumAgents() :
                value = value+ self.findmax( gameState.generateSuccessor(agentIndex, action),depth+1, 0)
              else:
                value = value + self.expected(gameState.generateSuccessor(agentIndex, action),depth, agentIndex + 1)
            length=len(legalActions)
            if length== 0:
              value = self.evaluationFunction(gameState)    
            else:
              value =  value / length
            return value

def betterEvaluationFunction(currentGameState):
      
    if currentGameState.isWin():
      result = 50000
    result,ghscore=0,0
    pos = currentGameState.getPacmanPosition()
    ghoststates = currentGameState.getGhostStates()
    Scared = [ghstate.scaredTimer for ghstate in ghoststates]
    food = currentGameState.getFood()
    if Scared[0] > 0:
      ghscore = ghscore + 75
    list_food = food.asList()
    tot_food = sum(manhattanDistance(fo, pos) for fo in list_food)
    for state in ghoststates:
      dist = manhattanDistance(pos, state.getPosition())
      if dist > state.scaredTimer:
        ghscore = float(ghscore+ 1/ (dist))
      if  dist < 4 and state.scaredTimer == 0:
        ghscore = float(ghscore - 1 / (4- dist));

    return result + float( 1 / (1 + tot_food) + ghscore + 1/ (1 + len(list_food))+ currentGameState.getScore())

# Abbreviation
better=betterEvaluationFunction

