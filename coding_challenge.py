import requests

# initialize constants
sessionURL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
mazeURL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game"

UID = {"uid":"204772456"}
UP = {"action": "UP"}
DOWN = {"action": "DOWN"}
RIGHT = {"action": "RIGHT"}
LEFT = {"action": "LEFT"}
finished = False

# get token
token = requests.post(sessionURL,UID).json()["token"]
#make a dictionary to change the value of ACCESS_TOKEN in mazeURL
accessToken = {"token": token}
# find total levels
mazeState = requests.get(mazeURL,params=accessToken).json()
totalLevels = mazeState['total_levels']
'''#define a maze object
class Maze(object):
    def __init__(self):
        self.cols = 0
        self.rows = 0
        self.maze= []
        self.moves = []
'''
def go_back(maze, moves):
    move = moves.pop()
    if move == UP:
        requests.post(mazeURL, DOWN, params = accessToken)
    elif move == DOWN:
        requests.post(mazeURL, UP, params = accessToken)
    elif move == RIGHT:
        requests.post(mazeURL, LEFT, params = accessToken)
    elif move == LEFT:
        requests.post(mazeURL, RIGHT, params = accessToken)

def checkMove(ans, moves, maze, newY, newX, dir):
    if ans == 'WALL':
        maze[newY][newX] = 'W'
    elif ans == 'SUCCESS':
        moves.append(dir)
        maze[newY][newX] = '*'

def moveDirection (maze, moves, dir):
    mazeState = requests.get(mazeURL, params=accessToken).json()
    maxX = mazeState['maze_size'][0]-1
    maxY = mazeState['maze_size'][1]-1
    curX = mazeState['current_location'][0]
    curY = mazeState['current_location'][1]
    
    if dir == UP:
        if curY-1 < 0:
            return 'WALL'
        elif maze[curY-1][curX] != ' ':
            return 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans, moves, maze, curY-1, curX, dir)
            
    elif dir == RIGHT:
        if curX+1 > maxX:
            return 'WALL'
        elif maze[curY][curX+1] != ' ':
            return 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans,moves,maze,curY,curX+1, dir)

    elif dir == DOWN:
        if curY+1 > maxY:
            return 'WALL'
        elif maze[curY+1][curX] != ' ':
            return 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans,moves,maze,curY+1,curX, dir)

    elif dir == LEFT:
        if curX-1 < 0:
            return 'WALL'
        elif maze[curY][curX-1] != ' ':
            return 'WALL'
        else:
            ans =  requests.post(mazeURL, dir, params=accessToken).json()['result']
            checkMove(ans,moves,maze,curY,curX-1, dir)
    return ans


def mazeSolver (maze,moves,result):
    mazeState = requests.get(mazeURL, params=accessToken).json()
    curX = mazeState['current_location'][0]
    curY = mazeState['current_location'][1]    
    if len(moves) > 0:
            for y in range(len(maze)):
                print(maze[y])
    print('result of last attempted move = ',result)
    if result == 'END':
        return True
    if result == 'WALL' or result == 'OUT_OF_BOUNDS':
        return False
    if result == 'SUCCESS':
        if mazeSolver(maze, moves, moveDirection(maze,moves,UP)):
            return True
        elif mazeSolver(maze, moves, moveDirection(maze,moves,RIGHT)):
            return True
        elif mazeSolver(maze, moves, moveDirection(maze,moves,DOWN)):
            return True
        elif mazeSolver(maze, moves, moveDirection(maze,moves,LEFT)):
            return True
        elif len(moves) > 0:
            go_back(maze, moves)
            return False
        else:
            return False

'''    
    #try move UP
    #make sure UP is still on board
    if curY-1 >= 0:
        #ensure UP is to a new position
        if maze[curY-1][curX] == '-':
            move = moveDirection(curX, curY, maze, UP)
            if move == 'END':
                return True
            elif move == 'SUCCESS':
                move.append(UP)
                maze[curY-1][curX] = '*'
                ans = mazeSolver(mazeState, maze)
    #try move RIGHT
    if curX+1 <= mazeX:
        if maze[curY][curX+1] == '-':
            move = moveDirection(curX, curY, maze, RIGHT)
            if move == 'END':
                return True
            elif move == 'SUCCESS':
                move.append(UP)
                maze[curY-1][curX] = '*'
                mazeSolver(mazeState, maze)

    #check result of attempted move via post call
        if moveDirection(mazeState, maze, curX, curY-1, UP) == 'END':
            return True
        elif moveDirection(mazeState, maze) == 'SUCCESS':
    return False
'''

while not finished:
    mazeState = requests.get(mazeURL, params=accessToken).json()
    curLevel = mazeState['levels_completed']
    
    #make empty maze
    cols = mazeState['maze_size'][0]
    rows = mazeState['maze_size'][1]
    maze = [[' ' for x in range(cols)] for y in range(rows)]
    
    #set current position in maze
    curX = mazeState['current_location'][0]
    curY = mazeState['current_location'][1]
    maze[curY][curX] = '*'

    print ('curLevel = ',curLevel)

    #check to see if all mazes have been solved
    if curLevel == totalLevels:
        print('curLevel == ',curLevel)
        print('totalLevels == ',totalLevels)
        print('you finally did it!')
        finished = True
    else:
        #solve the current maze, moves holds all moves made so far
        moves = []
        if not mazeSolver(maze,moves,'SUCCESS'):
            print('wtf!?!?')
