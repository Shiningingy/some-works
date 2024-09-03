import time, heapq as pq
from copy import deepcopy

class pathfinding:
    def __init__(self, filename_a="pathfinding_a.txt", filename_b="pathfinding_b.txt"):
        self.filename_a = filename_a
        self.filename_b = filename_b
        self.filename_a_out = "pathfinding_a_out.txt"
        self.filename_b_out = "pathfinding_b_out.txt"
        self.remove_empty = lambda input_list: [x for x in input_list if x] # Remove empty elements and zeros
        self.grids_a = self.read_file(self.filename_a) # Grid for executing part a
        self.grids_b = self.read_file(self.filename_b) # Grid for executing part b
        self.movement_without_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Legal movement offsets
        self.movement_with_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def read_file(self, filename): # Read file to generate maps
        input_list = [] # All grids
        line = True
        with open(filename, "r") as f:
            tmp = [] # One m x n input grid
            while line != "":
                line = f.readline()
                if len(line) > 1:
                    tmp.append(list(line[:-1]) if line[-1]=="\n" else list(line))
                else:
                    input_list.append(tmp)
                    tmp = []
        return self.remove_empty(input_list)

    def write_file(self, filename, path, algo_type): # Write results to file
        with open(filename, "a+") as f:
            f.write(algo_type+"\n")
            for p in path:
                f.write("".join(p))
                f.write("\n")
            if algo_type == "A*":
                f.write("\n")
        return None

    def draw(self, path, grid): # Format output to be map
        for x, y in path:
            if grid[x][y] == "G":
                continue
            grid[x][y] = "P"
        return grid

    def find_start_goal(self, grid): # Find start point and goal point
        start_goal = [None, None]
        rows = len(grid)
        cols = len(grid[0])
        for row in range(0,rows):
            for col in range(0,cols):
                if grid[row][col] == "S":
                    start_goal[0] = (row, col)
                elif grid[row][col] == "G":
                    start_goal[1] = (row, col)
        print("Start point is at:", start_goal[0], "\nEnd point is at:", start_goal[1], "\n")
        start_goal = self.remove_empty(start_goal)
        return start_goal if len(start_goal)==2 else None

    def heuristics(self, a, b, t): # Find corresponding heuristic algorithm to use
        return self.chebyshev(a, b) if not t else self.manhattan(a, b)

    def manhattan(self, x, y): # Manhattan distance on a grid
        return sum([abs(a - b) for a, b in zip(x, y)])

    def chebyshev(self, x, y): # Chebyshev distance on a grid
        return max([abs(a - b) for a, b in zip(x, y)])

    def A_star(self, grid, start, goal, movement, diag): # A* algorithm based on pseudo code given
        frontier = [] # Priority queue
        cost_so_far = {start: 0}
        priority = {start: 0}
        pq.heappush(frontier, (priority[start], start))
##        visited = set()
        came_from = {start:None} # Start comes from none
        while frontier:
            current = pq.heappop(frontier)[1] # Get coordinates
            # If goal found
            if current == goal: # If its goal its done, and print the path
                path = []
                while current in came_from and current != start:
                    path.append(current)
                    current = came_from[current] # Back trace to origin
                path = list(reversed(path)) # Reverse the path to real goal
                print("A*")
                print(len(came_from))
                return path
##            visited.add(current)
            for i, j in movement:
                neighbor = current[0] + i, current[1] + j # Check for neighbors
                new_cost = cost_so_far[current] + self.heuristics(current, neighbor, diag) # - self.heuristics(current, goal, diag))
                if 0 <= neighbor[0] < len(grid):
                    if 0 <= neighbor[1] < len(grid[0]):
                        if grid[neighbor[0]][neighbor[1]] == "X":
                            continue
                    else:
                        # Grid bound y walls
                        continue
                else:
                    # Grid bound x walls
                    continue
                if neighbor in cost_so_far and new_cost >= cost_so_far.get(neighbor, cost_so_far[current]) : #neighbor in visited and
                    continue
                else: # Updates    #new_cost < cost_so_far.get(neighbor, 0) or neighbor not in came_from
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    priority[neighbor] = new_cost + self.heuristics(neighbor, goal, diag)
                    pq.heappush(frontier, (priority[neighbor], neighbor))
        return None

    def greedy(self, grid, start, goal, movement, diag): # Greedy algorithm based on pesuedo code given
        frontier = [] # Priority queue
        priority = {start: 0}
        pq.heappush(frontier, (priority[start], start))
##        visited = set()
        came_from = {start:None} # Start  comes from none
        while frontier:
            current = pq.heappop(frontier)[1] # Get coordinates
            if current == goal: # If its goal is found
                path = []
                while current in came_from and current != start:
                    path.append(current)
                    current = came_from[current] # Back trace to origin
                path = list(reversed(path)) # Reverse the path to real goal
                print("greedy")
                print(len(came_from))
                return path
##            visited.add(current) # Add current into visited list, prevent visit again
            for i, j in movement:
                neighbor = current[0] + i, current[1] + j # Neighbor's coordinate calculated with the move list
                if 0 <= neighbor[0] < len(grid): # If its inside left and right wall
                    if 0 <= neighbor[1] < len(grid[0]): # If itz inside up and bottom wall
                        if grid[neighbor[0]][neighbor[1]] == "X": # If its a internal wall
                            continue # Skip this move
                    else:
                        # Grid bound y walls
                        continue
                else:
                    # Grid bound x walls
                    continue
##                if neighbor in visited:
##                    continue
                if neighbor not in came_from:
                    priority[neighbor] = self.heuristics(neighbor, goal, diag)
                    pq.heappush(frontier, (priority[neighbor], neighbor))
                    came_from[neighbor] = current
##                else:
##                    print(neighbor)
##                    print(came_from)
        return None

    def execute(self, is_diagonal): # Execute two algorithms to get results
        if is_diagonal: # If allow diagonal movements
            if len(self.grids_b) <= 0: # Illegal grids
                print("The input is empty\n")
                return None
            for grid in self.grids_b: # Run algorithms and record time
                start_goal = self.find_start_goal(grid)
                if start_goal:
                    start = time.perf_counter()
                    greedy_path = self.greedy(grid, start_goal[0], start_goal[-1], self.movement_with_diagonal, is_diagonal)
                    end = time.perf_counter()
                    print("Time elapsed: %fs" % (end-start))
                    if greedy_path is None: # Check results
                        print("No solution found by greedy algorithm\n")
                    else:
                        print("Solution found by greedy algorithm\n")
                        self.write_file(self.filename_b_out, self.draw(greedy_path, deepcopy(grid)), "Greedy")
                    start = time.perf_counter()
                    A_star_path = self.A_star(grid, start_goal[0], start_goal[-1], self.movement_with_diagonal, is_diagonal)
                    end = time.perf_counter()
                    print("Time elapsed: %fs" % (end-start))
                    if A_star_path is None: # Check results
                        print("No solution found by A* algorithm\n")
                    else:
                        print("Solution found by A* algorithm\n")
                        self.write_file(self.filename_b_out, self.draw(A_star_path, deepcopy(grid)), "A*")
                else:
                    print("No start or goal point found\n")
        else: # If do not allow diagonal movements
            if len(self.grids_a) <= 0:
                print("The input is empty\n")
                return None
            for grid in self.grids_a: # Run algorithms and record time
                start_goal = self.find_start_goal(grid)
                if start_goal:
                    start = time.perf_counter()
                    greedy_path = self.greedy(grid, start_goal[0], start_goal[-1], self.movement_without_diagonal, is_diagonal)
                    end = time.perf_counter()
                    print("Time elapsed: %fs" % (end-start))
                    if greedy_path is None: # Check results
                        print("No solution found by greedy algorithm\n")
                    else:
                        print("Solution found by greedy algorithm\n")
                        self.write_file(self.filename_a_out, self.draw(greedy_path, deepcopy(grid)), "Greedy")
                    start = time.perf_counter()
                    A_star_path = self.A_star(grid, start_goal[0], start_goal[-1], self.movement_without_diagonal, is_diagonal)
                    end = time.perf_counter()
                    print("Time elapsed: %fs" % (end-start))
                    if A_star_path is None: # Check results
                        print("No solution found by A* algorithm\n")
                    else:
                        print("Solution found by A* algorithm\n")
                        self.write_file(self.filename_a_out, self.draw(A_star_path, deepcopy(grid)), "A*")
                else:
                    print("No start or goal point found\n")
        print("Execute Finished\n")
        return None

if __name__ == "__main__":
    pf = pathfinding()
    pf.execute(False) # Without diagonal movement
    pf.execute(True) # With diagonal movement
