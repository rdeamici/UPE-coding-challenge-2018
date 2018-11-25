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

def go_back(moves):
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
'''
def start_over(maze,moves):
    while len(moves) > 0:
        move = append.moves
        go_back(moves)'''

def mazeSolverIDS (maze,moves,result, L):
    mazeState = requests.get(mazeURL, params=accessToken).json()
    curX = mazeState['current_location'][0]
    curY = mazeState['current_location'][1]    
    #print ('L = ', L)
    #    for y in range(len(maze)):
    #       print (maze[y])
    if result == 'END':
        return True
    if result == 'WALL' or result == 'OUT_OF_BOUNDS':
        return False
    if L < 1:
        go_back(moves)
        return False
    if result == 'SUCCESS':
        if mazeSolverIDS(maze, moves, moveDirection(maze,moves,UP), L-1):
            return True
        elif mazeSolverIDS(maze, moves, moveDirection(maze,moves,RIGHT), L-1):
            return True
        elif mazeSolverIDS(maze, moves, moveDirection(maze,moves,DOWN), L-1):
            return True
        elif mazeSolverIDS(maze, moves, moveDirection(maze,moves,LEFT), L-1):
            return True
        elif len(moves) > 0:
            go_back(moves)
            return False
        else:
            return False

def new_maze(mazeState):
    cols = mazeState['maze_size'][0]
    rows = mazeState['maze_size'][1]
    maze = [[' ' for x in range(cols)] for y in range(rows)]
    curX = mazeState['current_location'][0]
    curY = mazeState['current_location'][1]
    maze[curY][curX] = '*'
    return maze

while not finished:
    mazeState = requests.get(mazeURL, params=accessToken).json()
    curLevel = mazeState['levels_completed']
    
    #initialize maze
    maze = new_maze(mazeState)
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
        L = 20
        while not mazeSolverIDS(maze,moves,'SUCCESS', L):
            print('increasing L to', L)
            L = L + 5
            moves = []
            maze = new_maze(mazeState)