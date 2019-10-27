"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state


        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):



    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push(problem.getStartState())
    path = []
    explored = []
    node=frontier.pop()
    if problem.isGoalState(node):
        return []
    else:
        explored.append(node)
        for succ in problem.getSuccessors(node):
            frontier.push(succ)
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-3]):
            for i in range(1,len(node),3):
                path.append(node[i])
            return path
        if node[-3] not in explored:
            explored.append(node[-3])
            for succ in problem.getSuccessors(node[-3]):
                frontier.push(node+succ)

    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push(problem.getStartState())
    path = []
    explored = []
    node=frontier.pop()
    if problem.isGoalState(node):
        return []
    else:
        explored.append(node)
        for succ in problem.getSuccessors(node):
            frontier.push(succ)
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-3]):
            for i in range(1,len(node),3):
                path.append(node[i])
            return path
        if node[-3] not in explored:
            explored.append(node[-3])
            for succ in problem.getSuccessors(node[-3]):
                frontier.push(node+succ)
    return []

    util.raiseNotDefined()


def uniformCostSearch(problem):

    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    path = []
    explored = []
    node=problem.getStartState()
    if problem.isGoalState(node):
        return []
    else:
        explored.append(node)
        for succ in problem.getSuccessors(node):
            frontier.push(succ,succ[2])
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-3]):
            for i in range(1,len(node),3):
                path.append(node[i])
            return path
        if node[-3] not in explored:
            explored.append(node[-3])
            for succ in problem.getSuccessors(node[-3]):
                npath=[]
                for i in range(1,len(node),3):
                    npath.append(node[i])
                frontier.push(node+succ,problem.getCostOfActions(npath)+succ[2])

    return []
    util.raiseNotDefined()
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    path = []
    explored = []
    node=problem.getStartState()
    if problem.isGoalState(node):
        return []
    else:
        explored.append(node)
        for succ in problem.getSuccessors(node):
            frontier.push(succ,succ[2]+heuristic(succ[0],problem))
    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.isGoalState(node[-3]):
            for i in range(1,len(node),3):
                path.append(node[i])
            return path
        if node[-3] not in explored:
            explored.append(node[-3])
            for succ in problem.getSuccessors(node[-3]):
                npath=[]
                for i in range(1,len(node),3):
                    npath.append(node[i])
                frontier.push(node+succ,problem.getCostOfActions(npath)+succ[2]+heuristic(succ[0],problem))

    return []


    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
