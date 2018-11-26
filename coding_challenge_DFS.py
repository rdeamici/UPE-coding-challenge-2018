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
    def __init__(self, rows,cols, curX, curY):
        self.rows = rows - 1
        self.cols = cols - 1
        self.maze = [[' ' for x in range(cols)] for y in range(rows)]
        self.moves = []
        self.curX = curX
        self.curY = curY

# get token
token = requests.post(sessionURL,UID).json()["token"]
#make a dictionary to change the value of ACCESS_TOKEN in mazeURL
accessToken = {"token": token}
# find total levels
mazeState = requests.get(mazeURL,params=accessToken).json()
totalLevels = mazeState['total_levels']

# ensure the player is at the same spot on the API server as it is
# in the recursive algorithm
def go_back(maze):
    move = maze.moves.pop()
    if move == UP:
        requests.post(mazeURL, DOWN, params = accessToken)
        maze.curY = maze.curY+1
    elif move == DOWN:
        requests.post(mazeURL, UP, params = accessToken)
        maze.curY = maze.curY-1
    elif move == RIGHT:
        requests.post(mazeURL, LEFT, params = accessToken)
        maze.curX = maze.curX-1
    elif move == LEFT:
        requests.post(mazeURL, RIGHT, params = accessToken)
        maze.curX = maze.curX+1

def update_maze(ans, maze, newY, newX, dir):
    if ans == 'WALL':
        maze.maze[newY][newX] = 'W'
    elif ans == 'SUCCESS':
        maze.moves.append(dir)
        maze.maze[newY][newX] = '*'
        maze.curX = newX
        maze.curY = newY

#attempt to move in the direction indicated by dir
def moveDirection (maze,dir):
    curX = maze.curX
    curY = maze.curY
    if dir == UP:
        # check if UP will result in out of bounds
        if curY-1 < 0:
            ans = 'OUT_OF_BOUNDS'
        # check in UP is to a position we have already visited before
        elif maze.maze[curY-1][curX] != ' ':
            ans = 'WALL'
        else:
            # make move 
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            # update maze
            update_maze(ans, maze,curY-1,curX, dir)
    elif dir == RIGHT:
        if curX+1 > maze.cols:
            ans = 'OUT_OF_BOUNDS'
        elif maze.maze[curY][curX+1] != ' ':
            ans = 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            update_maze(ans,maze,curY,curX+1, dir)
    elif dir == DOWN:
        if curY+1 > maze.rows:
            ans = 'OUT_OF_BOUNDS'
        elif maze.maze[curY+1][curX] != ' ':
            ans = 'WALL'
        else:
            ans = requests.post(mazeURL, dir, params=accessToken).json()['result']
            update_maze(ans,maze,curY+1,curX, dir)
    elif dir == LEFT:
        if curX-1 < 0:
            ans = 'OUT_OF_BOUNDS'
        elif maze.maze[curY][curX-1] != ' ':
            ans = 'WALL'
        else:
            ans =  requests.post(mazeURL, dir, params=accessToken).json()['result']
            update_maze(ans,maze,curY,curX-1, dir)
    return ans

def opposite(dir):
    if dir == UP:
        return DOWN
    if dir == DOWN:
        return UP
    if dir == RIGHT:
        return LEFT
    if dir == LEFT:
        return RIGHT

def make_move(maze, moves_list):
    #loop thru each direction in moves_list looking for the END
    while len(moves_list) > 0:
        move = moves_list.pop()
        result = moveDirection(maze,move)
        if mazeSolverDFS(maze,result):
            return True
    if len(maze.moves) > 0:
            go_back(maze)
            return False
    else:
        return False

# maze is the struct containing the current maze
# result contains the result of the most recent attempted move
def mazeSolverDFS (maze,result):
    # we have reached the end of the maze
    if result == 'END':
        return True
    if result == 'WALL' or result == 'OUT_OF_BOUNDS':
        return False
    if result == 'SUCCESS':
        # if first time thru maze, need to check all 4 directions
        if len(maze.moves) == 0:
            return make_move(maze,[UP,RIGHT,DOWN,LEFT])
        else:
            # if we have made at least one move, no need to check the
            # directions we just came from
            last_move = maze.moves[-1]
            moves_list = []
            opp = opposite(last_move)
            for i in [UP,RIGHT,DOWN,LEFT]:
                # don't move in the direction you just came from
                # don't add the most recent successful move (will be added later)
                if last_move != i and  opp != i:
                    moves_list.append(i)
            # try the last successful direction first
            moves_list.append(last_move)
            #make_move contains the recursive call
            return make_move(maze,moves_list)

while not finished:
    mazeState = requests.get(mazeURL, params=accessToken).json()
    curLevel = mazeState['levels_completed']
    status = mazeState['status']
 
    # check to see if we are done
    if status == 'FINISHED':
        print('YOU DID IT!')
        finished = True
    else:
        #make empty maze
        cols = mazeState['maze_size'][0]
        rows = mazeState['maze_size'][1]
        curX = mazeState['current_location'][0]
        curY = mazeState['current_location'][1]
        maze = Maze(rows,cols, curX,curY)
        #set current position in maze
        maze.maze[curY][curX] = '*'

        #solve the current maze
        if not mazeSolverDFS(maze,'SUCCESS'):
            print('wtf!?!?')