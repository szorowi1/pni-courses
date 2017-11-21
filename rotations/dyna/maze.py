import numpy as np

def maze_1( ):
    '''No obstacles'''
    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = [1, 1]
    end   = [9, 1]
    return np.array(M), np.array(start), np.array(end)

def maze_2( ):
    '''Single divider'''
    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = [1, 1]
    end   = [9, 1]
    return np.array(M), np.array(start), np.array(end)

def maze_3( ):
    '''complexity = 0.1, density = 0.1'''
    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = [5, 1]
    end   = [5, 3]
    return np.array(M), np.array(start), np.array(end)

def maze_4( ):
    '''complexity = 0.2, density = 0.2'''
    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = [1, 1]
    end   = [7, 3]
    return np.array(M), np.array(start), np.array(end)

def maze_5( ):
    '''complexity = 0.2, density = 0.2'''
    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = [1, 9]
    end   = [7, 3]
    return np.array(M), np.array(start), np.array(end)

def maze_6( ):
    '''complexity = 0.2, density = 0.2'''
    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = [1, 9]
    end   = [9, 1]
    return np.array(M), np.array(start), np.array(end)
        

def random_maze(row=10, col=10, complexity=0.25, density=0.25):
    '''https://en.wikipedia.org/wiki/Maze_generation_algorithm'''
    
    ## Define shape (must be odd).
    shape = ((row // 2) * 2 + 1, (col // 2) * 2 + 1)
    
    ## Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    
    ## Preallocate space.
    Z = np.zeros(shape, dtype=bool)
    
    ## Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    
    ## Make aisles
    for i in np.arange(density):
        x = np.random.randint(0, shape[1] // 2) * 2
        y = np.random.randint(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[np.random.randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    
    ## Invert map (path = 1, wall = 0)
    Z = 1 - Z.astype(int)
    
    ## Select start/end randomly.
    indices = np.vstack(Z.nonzero()).T
    start, end = indices[np.random.choice(np.arange(Z.sum()), 2, replace=False)]
                    
    return Z, start, end

def MazeGenerator(maze='random', row=10, col=10, complexity=0.25, density=0.25):
    
    if maze == 1: 
        maze, start, end = maze_1() 
    elif maze == 2:
        maze, start, end = maze_2() 
    elif maze == 3:
        maze, start, end = maze_3() 
    elif maze == 4:
        maze, start, end = maze_4() 
    elif maze == 5:
        maze, start, end = maze_5() 
    elif maze == 6:
        maze, start, end = maze_6()
    else:
        maze, start, end = random_maze(row, col, complexity, density)
        
    return maze, start, end