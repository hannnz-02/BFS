import time
import tracemalloc
from collections import deque
import copy

class PuzzleSolver:
    def __init__(self, board, walls=None):
        self.n = len(board)
        self.board = board
        self.walls = walls if walls else []
        self.dx = [-1, 1, 0, 0]
        self.dy = [0, 0, -1, 1]
    
    def board_to_tuple(self, b):
        return tuple(tuple(row) for row in b)

    def get_neighbors(self, b):
        neighbors = []
        for i in range(self.n):
            for j in range(self.n):
                for d in range(4):
                    ni, nj = i + self.dx[d], j + self.dy[d]
                    if 0 <= ni < self.n and 0 <= nj < self.n:
                        # Cek dinding
                        if ((i,j),(ni,nj)) in self.walls or ((ni,nj),(i,j)) in self.walls:
                            continue
                        # Swap hanya jika salah satu posisi kosong
                        if b[i][j]==0 or b[ni][nj]==0:
                            new_board = copy.deepcopy(b)
                            new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                            neighbors.append(new_board)
        return neighbors

    def solve(self, goal):
        start = self.board_to_tuple(self.board)
        goal_t = self.board_to_tuple(goal)

        queue = deque([(self.board, [])])
        visited = set()
        visited.add(start)

        while queue:
            current, path = queue.popleft()
            if self.board_to_tuple(current) == goal_t:
                return path

            for neighbor in self.get_neighbors(current):
                t_neighbor = self.board_to_tuple(neighbor)
                if t_neighbor not in visited:
                    visited.add(t_neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

def print_board(b):
    for row in b:
        print(' '.join(f"{v:2}" for v in row))
    print()

def run_solver(board, goal, walls=None):
    print("Initial state:")
    print_board(board)
    print("Goal state:")
    print_board(goal)

    solver = PuzzleSolver(board, walls)
    tracemalloc.start()
    start_time = time.time()
    solution = solver.solve(goal)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"banyak langkah: {len(solution) if solution else 'No solution'}")
    print(f"waktu yang dibutuhkan: {end_time - start_time:.6f} seconds")
    print(f"memory yang digunakan={current/1024:.2f} KB")
    print("="*50)

board_3x3_easy = [
    [2,5,6],
    [1,3,8],
    [7,4,0]
]
goal_3x3_easy = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
print("3x3 puzzle:")
run_solver(board_3x3_easy, goal_3x3_easy)

board_4x4_medium = [
    [2,3,8,6],
    [1,10,5,4],
    [0,9,7,12],
    [13,14,11,15]
]
goal_4x4_medium = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,0]
]
print("4x4 puzzle:")
run_solver(board_4x4_medium, goal_4x4_medium)

board_4x4_hard = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,0,14,0]
]

goal_4x4_hard = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,0,0]
]
walls = [((0,0),(0,1))]  

print("4x4 puzzle with 2 empty tiles and wall:")
run_solver(board_4x4_hard, goal_4x4_hard, walls)
