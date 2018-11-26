# UPE-coding-challenge-2018
answer to the maze solver coding challenge using API requests

coding_challenge_DFS is the implementation that correctly solves the mazes.
The algorithm implements DFS to recursively solve each maze. 

Speed is achieved by limiting post and get requests to the bare minimum. Instead of using get requests in the body of the algorithm, a 2D array is stored inside a class. The class also stores the size of the maze, the current position within the maze, and the list of all moves that have occured so far, in chronological order. The maze and the current position is updated each time a new move is made. Only post requests occur in the DFS algorithm, one for each direction at each level of recursion. a single get request is made at the start of each new maze.

In addition to limiting requests from the API, at each level of recursion, the algorithm only checks 3 possible moves. The idea is that  a move in the direction we just came from is superfluous. For example, if the last successful move was UP, there is no need to check to see if the next move can be DOWN, since that will always return false. The only exception to this is the first move. In this special case, all 4 possible directions must be considered.

coding_challenge_IDS was my attempt to implement the iterative deepening search algorithm. This algorithm attempts to take advantage of the best properties of both DFS and BFS. While a good idea in theory, the algorithm proved to take too many steps. Since the actual maze is hosted on a separate server, everytime we have exhausted all options of one iteration of IDS, we must return all the way to the beginning before increasing the max depth by 1 nd trying all over again. This lead to a significantly higher number of steps being made compared to regular DFS, and thus a significantly slower algorithm.
