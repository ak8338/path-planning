from math import sqrt
from queue import PriorityQueue

class Node:
    # Represents a node in the search graph
    def __init__(self, position, parent=None, action=None, g=0, h=0):
        self.position = position  # Node position
        self.parent = parent  # Parent node
        self.action = action  # Action taken to reach this node
        self.g = g  # Cost from start to current node
        self.h = h  # Heuristic cost from current node to goal
        self.f = g + h  # Total cost

    def __lt__(self, other):
        # Comparison method for priority queue
        return self.f < other.f

def heuristic(a, b):
    # Heuristic function using Euclidean distance
    return sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

def a_star_search(start, goal, grid):
    # A* search algorithm
    open_set = PriorityQueue()
    open_set.put((0, Node(start, None, None, 0, heuristic(start, goal))))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    closed_set = set()
    moves_dict = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    moves_mapping = {moves_dict[i]: i for i in range(len(moves_dict))}
    
    while not open_set.empty():
        _, current = open_set.get()
        if current.position == goal:
            return reconstruct_path(current), len(closed_set) + 1
        
        closed_set.add(current.position)
        
        for dx, dy in moves_dict:
            neighbor_pos = (current.position[0] + dx, current.position[1] + dy)
            
            if (0 <= neighbor_pos[0] < len(grid)) and (0 <= neighbor_pos[1] < len(grid[0])):
                if grid[neighbor_pos[0]][neighbor_pos[1]] != 1:
                    tentative_g_score = g_score[current.position] + (sqrt(2) if dx != 0 and dy != 0 else 1)
                
                if neighbor_pos not in g_score or tentative_g_score < g_score[neighbor_pos]:
                    came_from[neighbor_pos] = current
                    g_score[neighbor_pos] = tentative_g_score
                    f_score[neighbor_pos] = tentative_g_score + heuristic(neighbor_pos, goal)
                    if neighbor_pos not in closed_set:
                        open_set.put((f_score[neighbor_pos], Node(neighbor_pos, current, moves_mapping[(dx, dy)], tentative_g_score, f_score[neighbor_pos])))
    
    return [], 0

def reconstruct_path(current):
    # Reconstructs the path from start to goal
    path = []
    moves = []
    f_values = []
    while current.parent is not None:
        path.append(current.position)
        moves.append(current.action)
        f_values.append(current.f)
        current = current.parent
    path.reverse()
    moves.reverse()
    f_values.reverse()
    return path, moves, f_values

def read_input_file(file_path):
    # Reads the input file and returns start, goal, and the grid
    with open(file_path, 'r') as file:
        lines = file.readlines()
        start_goal = list(map(int, lines[0].split()))
        start = (start_goal[0], start_goal[1])
        goal = (start_goal[2], start_goal[3])
        grid = [[int(cell) for cell in line.split()] for line in lines[1:]]
        
        # Optionally find '2' and '5' in the grid
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 2:
                    start = (i, j)
                elif cell == 5:
                    goal = (i, j)

    return start, goal, grid

def write_output_file(output_path, start, goal, path, moves, f_values, grid, node_count):
    # Writes the output to a file
    with open(output_path, 'w') as file:
        file.write(f"{len(path)}\n")
        file.write(f"{node_count}\n")
        file.write(" ".join(str(move) for move in moves) + "\n")
        file.write(" ".join(f"{f:.2f}" for f in f_values) + "\n")
        
        # Mark the path in the grid
        for position in path[1:-1]:  # Exclude start and goal
            grid[position[0]][position[1]] = 4

        # Ensure start and goal are correctly marked
        grid[start[0]][start[1]] = 2
        grid[goal[0]][goal[1]] = 5
        
        for row in grid:
            file.write(" ".join(str(cell) for cell in row) + "\n")

def main(input_file_path, output_file_path):
    # Main function to run A* search
    start, goal, grid = read_input_file(input_file_path)
    result, node_count = a_star_search(start, goal, grid)
    if result:
        path, moves, f_values = result
        write_output_file(output_file_path, start, goal, path, moves, f_values, grid, node_count)
    else:
        print("No path found.")

if __name__ == "__main__":
    main("Input3.txt", "output.txt")
