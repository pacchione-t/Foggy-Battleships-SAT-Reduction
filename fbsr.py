# Import the relevant attributes of Z3Py
from z3 import Int, And, Or, Not, Implies, Solver, sat, print_matrix


# The width and height of the game board
size = 6


# Variables:

# The board: a 6x6 matrix of integers representing the various cell states
board = [[Int("x_%i_%i" % (i, j)) for j in range(size)]
         for i in range(size)]

# Cell states:
# 0: Water
# 1: Submarine
# 2: Middle ship piece
# 3: Left ship piece
# 4: Right ship piece
# 5: Top ship piece
# 6: Bottom ship piece


# The SAT solver instance
solver = Solver()


# Constraints:

# Each cell must either be a water cell or a ship cell
for i in range(size):
    for j in range(size):
        solver.add(And(board[i][j] >= 0,
                       board[i][j] <= 6))


# Restrictions on ship pieces on the borders of the board

# Left, right, top, and bottom ship pieces cannot be on the corresponding opposite border
for i in range(size):
    # Left ship pieces cannot be on the right border
    solver.add(board[i][size - 1] != 3)

    # Right ship pieces cannot be on the left border
    solver.add(board[i][0] != 4)

    # Top ship pieces cannot be on the bottom border
    solver.add(board[size - 1][i] != 5)

    # Bottom ship pieces cannot be on the top border
    solver.add(board[0][i] != 6)

# Middle ship pieces cannot be in the corners

# Top-left corner
solver.add(board[0][0] != 2)

# Top-right corner
solver.add(board[0][size - 1] != 2)

# Bottom-left corner
solver.add(board[size - 1][0] != 2)

# Bottom-right corner
solver.add(board[size - 1][size - 1] != 2)


# Ship pieces must be part of a ship

# Left, right, top, and bottom ship pieces must be part of a ship
for i in range(size):
    for j in range(size - 1):
        # Left ship pieces
        solver.add(Implies(board[i][j] == 3,
                           Or(board[i][j + 1] == 2,
                              board[i][j + 1] == 4)))

        # Right ship pieces
        solver.add(Implies(board[i][j + 1] == 4,
                           Or(board[i][j] == 2,
                              board[i][j] == 3)))

        # Top ship pieces
        solver.add(Implies(board[j][i] == 5,
                           Or(board[j + 1][i] == 2,
                              board[j + 1][i] == 6)))

        # Bottom ship pieces
        solver.add(Implies(board[j + 1][i] == 6,
                           Or(board[j][i] == 2,
                              board[j][i] == 5)))

# Middle ship pieces must be part of a ship

# Middle ship pieces on the borders
for i in range(size - 2):
    # Top border
    solver.add(Implies(board[0][i + 1] == 2,
                       And(board[0][i] == 3,
                           board[0][i + 2] == 4)))

    # Bottom border
    solver.add(Implies(board[size - 1][i + 1] == 2,
                       And(board[size - 1][i] == 3,
                           board[size - 1][i + 2] == 4)))

    # Left border
    solver.add(Implies(board[i + 1][0] == 2,
                       And(board[i][0] == 5,
                           board[i + 2][0] == 6)))

    # Right border
    solver.add(Implies(board[i + 1][size - 1] == 2,
                       And(board[i][size - 1] == 5,
                           board[i + 2][size - 1] == 6)))

# Middle ship pieces in the inner 4x4 square
for i in range(size - 2):
    for j in range(size - 2):
        solver.add(Implies(board[i + 1][j + 1] == 2,
                           Or(And(board[i + 1][j] == 3,
                                  board[i + 1][j + 2] == 4),
                              And(board[i][j + 1] == 5,
                                  board[i + 2][j + 1] == 6))))


# Submarines must be surrounded by water

# Submarines in the corners

# Top-left corner
solver.add(Implies(board[0][0] == 1,
                   And(board[0][1] == 0,
                       board[1][0] == 0,
                       board[1][1] == 0)))

# Top-right corner
solver.add(Implies(board[0][size - 1] == 1,
                   And(board[0][size - 2] == 0,
                       board[1][size - 1] == 0,
                       board[1][size - 2] == 0)))

# Bottom-left corner
solver.add(Implies(board[size - 1][0] == 1,
                   And(board[size - 1][1] == 0,
                       board[size - 2][0] == 0,
                       board[size - 2][1] == 0)))

# Bottom-right corner
solver.add(Implies(board[size - 1][size - 1] == 1,
                   And(board[size - 1][size - 2] == 0,
                       board[size - 2][size - 1] == 0,
                       board[size - 2][size - 2] == 0)))

# Submarines on the borders
for i in range(size - 2):
    # Top border
    solver.add(Implies(board[0][i + 1] == 1,
                       And(board[0][i] == 0,
                           board[0][i + 2] == 0,
                           board[1][i] == 0,
                           board[1][i + 1] == 0,
                           board[1][i + 2] == 0)))

    # Left border
    solver.add(Implies(board[i + 1][0] == 1,
                       And(board[i][0] == 0,
                           board[i + 2][0] == 0,
                           board[i][1] == 0,
                           board[i + 1][1] == 0,
                           board[i + 2][1] == 0)))

    # Bottom border
    solver.add(Implies(board[size - 1][i + 1] == 1,
                       And(board[size - 1][i] == 0,
                           board[size - 1][i + 2] == 0,
                           board[size - 2][i] == 0,
                           board[size - 2][i + 1] == 0,
                           board[size - 2][i + 2] == 0)))

    # Right border
    solver.add(Implies(board[i + 1][size - 1] == 1,
                       And(board[i][size - 1] == 0,
                           board[i + 2][size - 1] == 0,
                           board[i][size - 2] == 0,
                           board[i + 1][size - 2] == 0,
                           board[i + 2][size - 2] == 0)))

# Submarines in the middle 4x4 square
for i in range(size - 2):
    for j in range(size - 2):
        solver.add(Implies(board[i + 1][j + 1] == 1,
                           And(board[i][j] == 0,
                               board[i][j + 1] == 0,
                               board[i][j + 2] == 0,
                               board[i + 1][j] == 0,
                               board[i + 1][j + 2] == 0,
                               board[i + 2][j] == 0,
                               board[i + 2][j + 1] == 0,
                               board[i + 2][j + 2] == 0)))


# Ships must be surrounded by water

# Left ship pieces

# Top-left corner
solver.add(Implies(board[0][0] == 3,
                   board[1][0] == 0))

# Bottom-left corner
solver.add(Implies(board[size - 1][0] == 3,
                   board[size - 2][0] == 0))

# Borders
for i in range(size - 2):
    # Left border
    solver.add(Implies(board[i + 1][0] == 3,
                       And(board[i][0] == 0,
                           board[i + 2][0] == 0)))

    # Top border
    solver.add(Implies(board[0][i + 1] == 3,
                       And(board[0][i] == 0,
                           board[1][i] == 0,
                           board[1][i + 1] == 0)))

    # Bottom border
    solver.add(Implies(board[size - 1][i + 1] == 3,
                       And(board[size - 1][i] == 0,
                           board[size - 2][i] == 0,
                           board[size - 2][i + 1] == 0)))

# Inner 4x4 square
for i in range(size - 2):
    for j in range(size - 2):
        solver.add(Implies(board[i + 1][j + 1] == 3,
                           And(board[i][j] == 0,
                               board[i][j + 1] == 0,
                               board[i + 1][j] == 0,
                               board[i + 2][j] == 0,
                               board[i + 2][j + 1] == 0)))

# Right ship pieces

# Top-right corner
solver.add(Implies(board[0][size - 1] == 4,
                   board[1][size - 1] == 0))

# Bottom-right corner
solver.add(Implies(board[size - 1][size - 1] == 4,
                   board[size - 2][size - 1] == 0))

# Borders
for i in range(size - 2):
    # Right border
    solver.add(Implies(board[i + 1][size - 1] == 4,
                       And(board[i][size - 1] == 0,
                           board[i + 2][size - 1] == 0)))

    # Top border
    solver.add(Implies(board[0][i + 1] == 4,
                       And(board[0][i + 2] == 0,
                           board[1][i + 1] == 0,
                           board[1][i + 2] == 0)))

    # Bottom border
    solver.add(Implies(board[size - 1][i + 1] == 4,
                       And(board[size - 1][i + 2] == 0,
                           board[size - 2][i + 1] == 0,
                           board[size - 2][i + 2] == 0)))

# Inner 4x4 square
for i in range(size - 2):
    for j in range(size - 2):
        solver.add(Implies(board[i + 1][j + 1] == 4,
                           And(board[i][j + 1] == 0,
                               board[i][j + 2] == 0,
                               board[i + 1][j + 2] == 0,
                               board[i + 2][j + 1] == 0,
                               board[i + 2][j + 2] == 0)))

# Top ship pieces

# Top-left corner
solver.add(Implies(board[0][0] == 5,
                   board[0][1] == 0))

# Top-right corner
solver.add(Implies(board[0][size - 1] == 5,
                   board[0][size - 2] == 0))

# Borders
for i in range(size - 2):
    # Top border
    solver.add(Implies(board[0][i + 1] == 5,
                       And(board[0][i] == 0,
                           board[0][i + 2] == 0)))

    # Left border
    solver.add(Implies(board[i + 1][0] == 5,
                       And(board[i][0] == 0,
                           board[i][1] == 0,
                           board[i + 1][1] == 0)))

    # Right border
    solver.add(Implies(board[i + 1][size - 1] == 5,
                       And(board[i][size - 2] == 0,
                           board[i][size - 1] == 0,
                           board[i + 1][size - 2] == 0)))

# Inner 4x4 square
for i in range(size - 2):
    for j in range(size - 2):
        solver.add(Implies(board[i + 1][j + 1] == 5,
                           And(board[i][j] == 0,
                               board[i][j + 1] == 0,
                               board[i][j + 2] == 0,
                               board[i + 1][j] == 0,
                               board[i + 1][j + 2] == 0)))

# Bottom ship pieces

# Bottom-left corner
solver.add(Implies(board[size - 1][0] == 6,
                   board[size - 1][1] == 0))

# Bottom-right corner
solver.add(Implies(board[size - 1][size - 1] == 6,
                   board[size - 1][size - 2] == 0))

# Borders
for i in range(size - 2):
    # Bottom border
    solver.add(Implies(board[size - 1][i + 1] == 6,
                       And(board[size - 1][i] == 0,
                           board[size - 1][i + 2] == 0)))

    # Left border
    solver.add(Implies(board[i + 1][0] == 6,
                       And(board[i + 1][1] == 0,
                           board[i + 2][0] == 0,
                           board[i + 2][1] == 0)))

    # Right border
    solver.add(Implies(board[i + 1][size - 1] == 6,
                       And(board[i + 1][size - 2] == 0,
                           board[i + 2][size - 2] == 0,
                           board[i + 2][size - 1] == 0)))

# Inner 4x4 square
for i in range(size - 2):
    for j in range(size - 2):
        solver.add(Implies(board[i + 1][j + 1] == 6,
                           And(board[i + 1][j] == 0,
                               board[i + 1][j + 2] == 0,
                               board[i + 2][j] == 0,
                               board[i + 2][j + 1] == 0,
                               board[i + 2][j + 2] == 0)))

# Middle ship pieces

# Borders
for i in range(4):
    # Top border
    solver.add(Implies(board[0][i + 1] == 2,
                       board[1][i + 1] == 0))

    # Bottom border
    solver.add(Implies(board[size - 1][i + 1] == 2,
                       board[size - 2][i + 1] == 0))

    # Left border
    solver.add(Implies(board[i + 1][0] == 2,
                       board[i + 1][1] == 0))

    # Right border
    solver.add(Implies(board[i + 1][size - 1] == 2,
                       board[i + 1][size - 2] == 0))

# Inner 4x4 square
for i in range(4):
    for j in range(4):
        solver.add(Implies(board[i + 1][j + 1] == 2,
                           Or(And(board[i + 1][j] == 0,
                                  board[i + 1][j + 2] == 0),
                              And(board[i][j + 1] == 0,
                                  board[i + 2][j + 1] == 0))))


# There must be exactly 3 submarines on the board
a = []
b = []

# Finding each combination of three cells on the board
for i in range(size ** 2):  # The first cell in the combination
    for j in range(size ** 2):  # The second cell in the combination
        if i < j:
            for k in range(size ** 2):  # The third cell in the combination
                if j < k:
                    b += [board[int(i / size)][i % size] == 1]
                    b += [board[int(j / size)][j % size] == 1]
                    b += [board[int(k / size)][k % size] == 1]

                    for t in range(size ** 2):  # The rest of the cells on the board
                        if i != t and j != t and k != t:
                            b += [board[int(t / size)][t % size] != 1]

                    # Those three cells must have a submarine and the rest must not
                    a += [And(b)]
                    b = []

# One of the combinations of cells must be true
solver.add(Or(a))


# There must be exactly 2 destroyers on the board
a = []
b = []

# Finding each combination of 2 cells on the board
for i in range(size ** 2):  # The first cell in the combination
    for j in range(size ** 2):  # The second cell in the combination
        if i < j:
            if int(i / size) != (size - 1) and (i % size) != (size - 1):
                b += [Or(And(board[int(i / size)][i % size] == 3,
                             board[int(i / size)][(i % size) + 1] == 4),
                         And(board[int(i / size)][i % size] == 5,
                             board[int(i / size) + 1][i % size] == 6))]
            if int(i / size) == (size - 1) and (i % size) != (size - 1):
                b += [And(board[int(i / size)][i % size] == 3,
                          board[int(i / size)][(i % size) + 1] == 4)]
            if int(i / size) != (size - 1) and (i % size) == (size - 1):
                b += [And(board[int(i / size)][i % size] == 5,
                          board[int(i / size) + 1][i % size] == 6)]

            if int(j / size) != (size - 1) and (j % size) != (size - 1):
                b += [Or(And(board[int(j / size)][j % size] == 3,
                             board[int(j / size)][(j % size) + 1] == 4),
                         And(board[int(j / size)][j % size] == 5,
                             board[int(j / size) + 1][j % size] == 6))]
            if int(j / size) == (size - 1) and (j % size) != (size - 1):
                b += [And(board[int(j / size)][j % size] == 3,
                          board[int(j / size)][(j % size) + 1] == 4)]
            if int(j / size) != (size - 1) and (j % size) == (size - 1):
                b += [And(board[int(j / size)][j % size] == (size - 1),
                          board[int(j / size) + 1][j % size] == 6)]

            for t in range(size ** 2):  # The rest of the cells on the board
                if i != t and j != t:
                    if int(t / size) != (size - 1) and (t % size) != (size - 1):
                        b += [Not(Or(And(board[int(t / size)][t % size] == 3,
                                         board[int(t / size)][(t % size) + 1] == 4),
                                     And(board[int(t / size)][t % size] == 5,
                                         board[int(t / size) + 1][t % size] == 6)))]
                    if int(t / size) == (size - 1) and (t % size) != (size - 1):
                        b += [Not(And(board[int(t / size)][t % size] == 3,
                                      board[int(t / size)][(t % size) + 1] == 4))]
                    if int(t / size) != (size - 1) and (t % size) == (size - 1):
                        b += [Not(And(board[int(t / size)][t % size] == 5,
                                      board[int(t / size) + 1][t % size] == 6))]

            # Those two cells must have a destroyer and the others must not
            a += [And(b)]
            b = []

# One of the combinations of cells must be true
solver.add(Or(a))


# There must be exactly 1 cruiser on the board
a = []
b = []

# Finding each cell on the board
for i in range(size ** 2):  # The cell
    if int(i / size) < (size - 2) and (i % size) < (size - 2):
        b += [Or(And(board[int(i / size)][i % size] == 3,
                     board[int(i / size)][(i % size) + 1] == 2,
                     board[int(i / size)][(i % size) + 2] == 4),
                 And(board[int(i / size)][i % size] == 5,
                     board[int(i / size) + 1][i % size] == 2,
                     board[int(i / size) + 2][i % size] == 6))]
    if int(i / size) >= (size - 2) > (i % size):
        b += [And(board[int(i / size)][i % size] == 3,
                  board[int(i / size)][(i % size) + 1] == 2,
                  board[int(i / size)][(i % size) + 2] == 4)]
    if int(i / size) < (size - 2) <= (i % size):
        b += [And(board[int(i / size)][i % size] == 5,
                  board[int(i / size) + 1][i % size] == 2,
                  board[int(i / size) + 2][i % size] == 6)]

    for t in range(size ** 2):  # The rest of the cells on the board
        if i != t:
            if int(t / size) < (size - 2) and (t % size) < (size - 2):
                b += [Not(Or(And(board[int(t / size)][t % size] == 3,
                                 board[int(t / size)][(t % size) + 1] == 2,
                                 board[int(t / size)][(t % size) + 2] == 4),
                             And(board[int(t / size)][t % size] == 5,
                                 board[int(t / size) + 1][t % size] == 2,
                                 board[int(t / size) + 2][t % size] == 6)))]
            if int(t / size) >= (size - 2) > (t % size):
                b += [Not(And(board[int(t / size)][t % size] == 3,
                              board[int(t / size)][(t % size) + 1] == 2,
                              board[int(t / size)][(t % size) + 2] == 4))]
            if int(t / size) < (size - 2) <= (t % size):
                b += [Not(And(board[int(t / size)][t % size] == 5,
                              board[int(t / size) + 1][t % size] == 2,
                              board[int(t / size) + 2][t % size] == 6))]

    # That cell must have a cruiser and the others must not
    a += [And(b)]
    b = []

# One of the cells must be true
solver.add(Or(a))


# Instance of a foggy battleship puzzle
solver.add(board[0][1] != 0,
           board[0][5] == 4,
           board[2][1] == 3,
           board[2][4] != 0,
           board[4][2] != 0,
           board[4][4] == 6,
           board[5][0] != 0)


# Check for a solution and print one if it exists
if solver.check() == sat:
    print("Solvable:")
    model = solver.model()
    matrix = [[model.evaluate(board[i][j]) for j in range(size)]
              for i in range(size)]
    print_matrix(matrix)
    # print(solver.statistics())
else:
    print("Unsolvable.")
    # print(solver.statistics())
