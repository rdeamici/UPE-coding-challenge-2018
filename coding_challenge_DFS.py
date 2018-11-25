import requests
import pdb

# initialize constants
sessionURL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
mazeURL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game"

UID = {"uid":"204772456"}
UP = {"action": "UP"}
DOWN = {"action": "DOWN"}
RIGHT = {"action": "RIGHT"}
LEFT = {"action": "LEFT"}
finished = False

class Maze:
    def __init__(self, rows,cols):
        self.rows = rows - 1
        self.cols = cols - 1
        self.maze = [[' ' for x in range(cols)] for y in range(rows)]
        self.moves = []
        self.curX = 0
        self.curY = 0

# get token
token = requests.post(sessionURL,UID).json()["token"]
#make a dictionary to change the value of ACCESS_TOKEN in mazeURL
accessToken = {"token": token}
# find total levels
mazeState = requests.get(mazeURL,params=accessToken).json()
totalLevels = mazeState['total_levels']

def go_back(maze):
    move = maze.moves.pop()
    if move == UP:
        requests.post(mazeURL, DOWN, params = accessToken)
        maze.curY = maze.curY +1
    elif move == DOWN:
        requests.post(mazeURL, UP, params = accessToken)
        maze.curY = maze.curY+1
    elif move == RIGHT:
        requests.post(mazeURL, LEFT, params = accessToken)
        maze.curX = maze.curX-1
    elif move == LEFT:
        requests.post(mazeURL, RIGHT, params = accessToken)
        maze.curX = maze.curX+1

def checkMove(ans, maze, newY, newX, dir):
    if ans == 'WALL':
        maze.maze[newY][newX] = 'W'
    elif ans == 'SUCCESS':
        maze.moves.append(dir)
        maze.maze[newY][newX] = '*'
        maze.curX = newX
        maze.curY = newY

def moveDirection (maze,dir):
    curX = maze.curX
    curY = maze.curY
    if dir == UP:
        if curY-1 < 0:
            return 'OUT_OF_BOUNDS'
        elif maze.maze[curY-1][curX] != ' ':
            return 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans, maze,curY-1,curX, dir)
            
    elif dir == RIGHT:
        if curX+1 > maze.cols:
            return 'OUT_OF_BOUNDS'
        elif maze.maze[curY][curX+1] != ' ':
            return 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans,maze,curY,curX+1, dir)

    elif dir == DOWN:
        if curY+1 > maze.rows:
            return 'OUT_OF_BOUNDS'
        elif maze.maze[curY+1][curX] != ' ':
            return 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans,maze,curY+1,curX, dir)

    elif dir == LEFT:
        if curX-1 < 0:
            return 'OUT_OF_BOUNDS'
        elif maze.maze[curY][curX-1] != ' ':
            return 'WALL'
        else:
            ans =  requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans,maze,curY,curX-1, dir)
    return ans


def mazeSolverDFS (maze,result):  
    #if len(moves) > 0:
    #        for y in range(len(maze)):
    #            print(maze[y])
    #print('result of last attempted move = ',result)
    if result == 'END':
        return True
    if result == 'WALL' or result == 'OUT_OF_BOUNDS':
        return False
    if result == 'SUCCESS':
        result = moveDirection(maze,RIGHT)
        if mazeSolverDFS(maze,result):
            return True
        result = moveDirection(maze,DOWN)
        if mazeSolverDFS(maze, result):
            return True
        result = moveDirection(maze,LEFT)
        if mazeSolverDFS(maze, result):
            return True        
        result = moveDirection(maze,UP)
        if mazeSolverDFS(maze, result):
            return True
        if len(maze.moves) > 0:
            go_back(maze)
            return False
        else:
            return False

while not finished:
    mazeState = requests.get(mazeURL, params=accessToken).json()
    curLevel = mazeState['levels_completed']
    
    #make empty maze
    cols = mazeState['maze_size'][0]
    rows = mazeState['maze_size'][1]
    maze = Maze(rows,cols)
    
    #set current position in maze
    curX = mazeState['current_location'][0]
    curY = mazeState['current_location'][1]
    maze.maze[curY][curX] = '*'
    print ('curLevel = ',curLevel)

    #check to see if all mazes have been solved
    if curLevel == totalLevels:
        print('curLevel == ',curLevel)
        print('totalLevels == ',totalLevels)
        print('you finally did it!')
        finished = True
    else:
        #solve the current maze, moves holds all moves made so far
        if not mazeSolverDFS(maze,'SUCCESS'):
            print('wtf!?!?')