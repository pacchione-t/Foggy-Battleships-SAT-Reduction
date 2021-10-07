from z3 import Int, And, Or, Not, Implies, Solver, sat
import unittest

board = [[Int("x_%i_%i" % (i, j)) for j in range(6)]
         for i in range(6)]

foggy_battleships = []

for i in range(6):
    for j in range(6):
        foggy_battleships += [And(board[i][j] >= 0,
                                  board[i][j] <= 6)]

for i in range(6):
    foggy_battleships += [board[i][5] != 3]
    foggy_battleships += [board[i][0] != 4]
    foggy_battleships += [board[5][i] != 5]
    foggy_battleships += [board[0][i] != 6]

foggy_battleships += [board[0][0] != 2]
foggy_battleships += [board[0][5] != 2]
foggy_battleships += [board[5][0] != 2]
foggy_battleships += [board[5][5] != 2]

for i in range(6):
    for j in range(5):
        foggy_battleships += [Implies(board[i][j] == 3,
                                      Or(board[i][j + 1] == 2,
                                         board[i][j + 1] == 4))]
        foggy_battleships += [Implies(board[i][j + 1] == 4,
                                      Or(board[i][j] == 2,
                                         board[i][j] == 3))]
        foggy_battleships += [Implies(board[j][i] == 5,
                                      Or(board[j + 1][i] == 2,
                                         board[j + 1][i] == 6))]
        foggy_battleships += [Implies(board[j + 1][i] == 6,
                                      Or(board[j][i] == 2,
                                         board[j][i] == 5))]

for i in range(4):
    foggy_battleships += [Implies(board[0][i + 1] == 2,
                                  And(board[0][i] == 3,
                                      board[0][i + 2] == 4))]
    foggy_battleships += [Implies(board[5][i + 1] == 2,
                                  And(board[5][i] == 3,
                                      board[5][i + 2] == 4))]
    foggy_battleships += [Implies(board[i + 1][0] == 2,
                                  And(board[i][0] == 5,
                                      board[i + 2][0] == 6))]
    foggy_battleships += [Implies(board[i + 1][5] == 2,
                                  And(board[i][5] == 5,
                                      board[i + 2][5] == 6))]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 2,
                                      Or(And(board[i + 1][j] == 3,
                                             board[i + 1][j + 2] == 4),
                                         And(board[i][j + 1] == 5,
                                             board[i + 2][j + 1] == 6)))]

foggy_battleships += [Implies(board[0][0] == 1,
                              And(board[0][1] == 0,
                                  board[1][0] == 0,
                                  board[1][1] == 0))]
foggy_battleships += [Implies(board[0][5] == 1,
                              And(board[0][4] == 0,
                                  board[1][5] == 0,
                                  board[1][4] == 0))]
foggy_battleships += [Implies(board[5][0] == 1,
                              And(board[5][1] == 0,
                                  board[4][0] == 0,
                                  board[4][1] == 0))]
foggy_battleships += [Implies(board[5][5] == 1,
                              And(board[5][4] == 0,
                                  board[4][5] == 0,
                                  board[4][4] == 0))]

for i in range(4):
    foggy_battleships += [Implies(board[0][i + 1] == 1,
                                  And(board[0][i] == 0,
                                      board[0][i + 2] == 0,
                                      board[1][i] == 0,
                                      board[1][i + 1] == 0,
                                      board[1][i + 2] == 0))]
    foggy_battleships += [Implies(board[i + 1][0] == 1,
                                  And(board[i][0] == 0,
                                      board[i + 2][0] == 0,
                                      board[i][1] == 0,
                                      board[i + 1][1] == 0,
                                      board[i + 2][1] == 0))]
    foggy_battleships += [Implies(board[5][i + 1] == 1,
                                  And(board[5][i] == 0,
                                      board[5][i + 2] == 0,
                                      board[4][i] == 0,
                                      board[4][i + 1] == 0,
                                      board[4][i + 2] == 0))]
    foggy_battleships += [Implies(board[i + 1][5] == 1,
                                  And(board[i][5] == 0,
                                      board[i + 2][5] == 0,
                                      board[i][4] == 0,
                                      board[i + 1][4] == 0,
                                      board[i + 2][4] == 0))]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 1,
                                      And(board[i][j] == 0,
                                          board[i][j + 1] == 0,
                                          board[i][j + 2] == 0,
                                          board[i + 1][j] == 0,
                                          board[i + 1][j + 2] == 0,
                                          board[i + 2][j] == 0,
                                          board[i + 2][j + 1] == 0,
                                          board[i + 2][j + 2] == 0))]

foggy_battleships += [Implies(board[0][0] == 3,
                              board[1][0] == 0)]
foggy_battleships += [Implies(board[5][0] == 3,
                              board[4][0] == 0)]

for i in range(4):
    foggy_battleships += [Implies(board[i + 1][0] == 3,
                                  And(board[i][0] == 0,
                                      board[i + 2][0] == 0))]
    foggy_battleships += [Implies(board[0][i + 1] == 3,
                                  And(board[0][i] == 0,
                                      board[1][i] == 0,
                                      board[1][i + 1] == 0))]
    foggy_battleships += [Implies(board[5][i + 1] == 3,
                                  And(board[5][i] == 0,
                                      board[4][i] == 0,
                                      board[4][i + 1] == 0))]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 3,
                                      And(board[i][j] == 0,
                                          board[i][j + 1] == 0,
                                          board[i + 1][j] == 0,
                                          board[i + 2][j] == 0,
                                          board[i + 2][j + 1] == 0))]

foggy_battleships += [Implies(board[0][5] == 4,
                              board[1][5] == 0)]
foggy_battleships += [Implies(board[5][5] == 4,
                              board[4][5] == 0)]

for i in range(4):
    foggy_battleships += [Implies(board[i + 1][5] == 4,
                                  And(board[i][5] == 0,
                                      board[i + 2][5] == 0))]
    foggy_battleships += [Implies(board[0][i + 1] == 4,
                                  And(board[0][i + 2] == 0,
                                      board[1][i + 1] == 0,
                                      board[1][i + 2] == 0))]
    foggy_battleships += [Implies(board[5][i + 1] == 4,
                                  And(board[5][i + 2] == 0,
                                      board[4][i + 1] == 0,
                                      board[4][i + 2] == 0))]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 4,
                                      And(board[i][j + 1] == 0,
                                          board[i][j + 2] == 0,
                                          board[i + 1][j + 2] == 0,
                                          board[i + 2][j + 1] == 0,
                                          board[i + 2][j + 2] == 0))]

foggy_battleships += [Implies(board[0][0] == 5,
                              board[0][1] == 0)]
foggy_battleships += [Implies(board[0][5] == 5,
                              board[0][4] == 0)]

for i in range(4):
    foggy_battleships += [Implies(board[0][i + 1] == 5,
                                  And(board[0][i] == 0,
                                      board[0][i + 2] == 0))]
    foggy_battleships += [Implies(board[i + 1][0] == 5,
                                  And(board[i][0] == 0,
                                      board[i][1] == 0,
                                      board[i + 1][1] == 0))]
    foggy_battleships += [Implies(board[i + 1][5] == 5,
                                  And(board[i][4] == 0,
                                      board[i][5] == 0,
                                      board[i + 1][4] == 0))]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 5,
                                      And(board[i][j] == 0,
                                          board[i][j + 1] == 0,
                                          board[i][j + 2] == 0,
                                          board[i + 1][j] == 0,
                                          board[i + 1][j + 2] == 0))]

foggy_battleships += [Implies(board[5][0] == 6,
                              board[5][1] == 0)]
foggy_battleships += [Implies(board[5][5] == 6,
                              board[5][4] == 0)]

for i in range(4):
    foggy_battleships += [Implies(board[5][i + 1] == 6,
                                  And(board[5][i] == 0,
                                      board[5][i + 2] == 0))]
    foggy_battleships += [Implies(board[i + 1][0] == 6,
                                  And(board[i + 1][1] == 0,
                                      board[i + 2][0] == 0,
                                      board[i + 2][1] == 0))]
    foggy_battleships += [Implies(board[i + 1][5] == 6,
                                  And(board[i + 1][4] == 0,
                                      board[i + 2][4] == 0,
                                      board[i + 2][5] == 0))]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 6,
                                      And(board[i + 1][j] == 0,
                                          board[i + 1][j + 2] == 0,
                                          board[i + 2][j] == 0,
                                          board[i + 2][j + 1] == 0,
                                          board[i + 2][j + 2] == 0))]

for i in range(4):
    foggy_battleships += [Implies(board[0][i + 1] == 2,
                                  board[1][i + 1] == 0)]
    foggy_battleships += [Implies(board[5][i + 1] == 2,
                                  board[4][i + 1] == 0)]
    foggy_battleships += [Implies(board[i + 1][0] == 2,
                                  board[i + 1][1] == 0)]
    foggy_battleships += [Implies(board[i + 1][5] == 2,
                                  board[i + 1][4] == 0)]

for i in range(4):
    for j in range(4):
        foggy_battleships += [Implies(board[i + 1][j + 1] == 2,
                                      Or(And(board[i + 1][j] == 0,
                                             board[i + 1][j + 2] == 0),
                                         And(board[i][j + 1] == 0,
                                             board[i + 2][j + 1] == 0)))]

a = []
b = []
for i in range(6 ** 2):
    for j in range(6 ** 2):
        if i < j:
            for k in range(6 ** 2):
                if j < k:
                    b += [board[int(i / 6)][i % 6] == 1]
                    b += [board[int(j / 6)][j % 6] == 1]
                    b += [board[int(k / 6)][k % 6] == 1]
                    for t in range(6 ** 2):
                        if i != t and j != t and k != t:
                            b += [board[int(t / 6)][t % 6] != 1]
                    a += [And(b)]
                    b = []
foggy_battleships += [Or(a)]

a = []
b = []
for i in range(6 ** 2):
    for j in range(6 ** 2):
        if i < j:
            if int(i / 6) != 5 and (i % 6) != 5:
                b += [Or(And(board[int(i / 6)][i % 6] == 3,
                             board[int(i / 6)][(i % 6) + 1] == 4),
                         And(board[int(i / 6)][i % 6] == 5,
                             board[int(i / 6) + 1][i % 6] == 6))]
            if int(i / 6) == 5 and (i % 6) != 5:
                b += [And(board[int(i / 6)][i % 6] == 3,
                          board[int(i / 6)][(i % 6) + 1] == 4)]
            if int(i / 6) != 5 and (i % 6) == 5:
                b += [And(board[int(i / 6)][i % 6] == 5,
                          board[int(i / 6) + 1][i % 6] == 6)]
            if int(j / 6) != 5 and (j % 6) != 5:
                b += [Or(And(board[int(j / 6)][j % 6] == 3,
                             board[int(j / 6)][(j % 6) + 1] == 4),
                         And(board[int(j / 6)][j % 6] == 5,
                             board[int(j / 6) + 1][j % 6] == 6))]
            if int(j / 6) == 5 and (j % 6) != 5:
                b += [And(board[int(j / 6)][j % 6] == 3,
                          board[int(j / 6)][(j % 6) + 1] == 4)]
            if int(j / 6) != 5 and (j % 6) == 5:
                b += [And(board[int(j / 6)][j % 6] == 5,
                          board[int(j / 6) + 1][j % 6] == 6)]
            for t in range(6 ** 2):
                if i != t and j != t:
                    if int(t / 6) != 5 and (t % 6) != 5:
                        b += [Not(Or(And(board[int(t / 6)][t % 6] == 3,
                                         board[int(t / 6)][(t % 6) + 1] == 4),
                                     And(board[int(t / 6)][t % 6] == 5,
                                         board[int(t / 6) + 1][t % 6] == 6)))]
                    if int(t / 6) == 5 and (t % 6) != 5:
                        b += [Not(And(board[int(t / 6)][t % 6] == 3,
                                      board[int(t / 6)][(t % 6) + 1] == 4))]
                    if int(t / 6) != 5 and (t % 6) == 5:
                        b += [Not(And(board[int(t / 6)][t % 6] == 5,
                                      board[int(t / 6) + 1][t % 6] == 6))]
            a += [And(b)]
            b = []
foggy_battleships += [Or(a)]

a = []
b = []
for i in range(6 ** 2):
    if int(i / 6) < 4 and (i % 6) < 4:
        b += [Or(And(board[int(i / 6)][i % 6] == 3,
                     board[int(i / 6)][(i % 6) + 1] == 2,
                     board[int(i / 6)][(i % 6) + 2] == 4),
                 And(board[int(i / 6)][i % 6] == 5,
                     board[int(i / 6) + 1][i % 6] == 2,
                     board[int(i / 6) + 2][i % 6] == 6))]
    if int(i / 6) >= 4 > (i % 6):
        b += [And(board[int(i / 6)][i % 6] == 3,
                  board[int(i / 6)][(i % 6) + 1] == 2,
                  board[int(i / 6)][(i % 6) + 2] == 4)]
    if int(i / 6) < 4 <= (i % 6):
        b += [And(board[int(i / 6)][i % 6] == 5,
                  board[int(i / 6) + 1][i % 6] == 2,
                  board[int(i / 6) + 2][i % 6] == 6)]
    for t in range(6 ** 2):
        if i != t:
            if int(t / 6) < 4 and (t % 6) < 4:
                b += [Not(Or(And(board[int(t / 6)][t % 6] == 3,
                                 board[int(t / 6)][(t % 6) + 1] == 2,
                                 board[int(t / 6)][(t % 6) + 2] == 4),
                             And(board[int(t / 6)][t % 6] == 5,
                                 board[int(t / 6) + 1][t % 6] == 2,
                                 board[int(t / 6) + 2][t % 6] == 6)))]
            if int(t / 6) >= 4 > (t % 6):
                b += [Not(And(board[int(t / 6)][t % 6] == 3,
                              board[int(t / 6)][(t % 6) + 1] == 2,
                              board[int(t / 6)][(t % 6) + 2] == 4))]
            if int(t / 6) < 4 <= (t % 6):
                b += [Not(And(board[int(t / 6)][t % 6] == 5,
                              board[int(t / 6) + 1][t % 6] == 2,
                              board[int(t / 6) + 2][t % 6] == 6))]
    a += [And(b)]
    b = []
foggy_battleships += [Or(a)]


# Checks whether the given instance of a foggy battleship puzzle can be solved
# Returns a list representing the solution board if it can be solved
# and returns an empty list if it cannot be solved
def check_instance(instance):
    solver = Solver()

    solver.add(And(foggy_battleships), And(instance))

    if solver.check() == sat:
        model = solver.model()
        matrix = [[model.evaluate(board[i][j]) for j in range(6)]
                  for i in range(6)]
        return matrix
    else:
        return []


# Tester class for the Foggy Battleships SAT solver
# Each unsolved puzzle instance to be tested must have at most one solution
# because the solver could reasonably produce any solution to a puzzle
class TestFoggyBattleships(unittest.TestCase):
    def test_check_instance(self):
        # Testing solvable boards
        # A "normal" puzzle instance
        sat1 = [board[0][1] != 0,
                board[0][5] == 4,
                board[2][1] == 3,
                board[2][4] != 0,
                board[4][2] != 0,
                board[4][4] == 6,
                board[5][0] != 0]
        self.assertEqual(check_instance(sat1),
                         [[0, 1, 0, 0, 3, 4],
                          [0, 0, 0, 0, 0, 0],
                          [0, 3, 4, 0, 5, 0],
                          [0, 0, 0, 0, 2, 0],
                          [0, 0, 1, 0, 6, 0],
                          [1, 0, 0, 0, 0, 0]])

        # Putting all the pieces as close together as possible
        sat2 = [board[0][0] != 0,
                board[0][3] == 4,
                board[2][1] == 2,
                board[2][4] == 5,
                board[4][0] != 0,
                board[4][2] != 0]
        self.assertEqual(check_instance(sat2),
                         [[1, 0, 3, 4, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [3, 2, 4, 0, 5, 0],
                          [0, 0, 0, 0, 6, 0],
                          [1, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0]])

        # Putting the end of every ship on the right or bottom border of the board
        sat3 = [board[0][2] != 0,
                board[0][5] != 0,
                board[2][0] != 0,
                board[2][5] == 4,
                board[3][2] != 0,
                board[4][4] == 5,
                board[5][2] != 0]
        self.assertEqual(check_instance(sat3),
                         [[0, 0, 1, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0],
                          [1, 0, 0, 0, 3, 4],
                          [0, 0, 5, 0, 0, 0],
                          [0, 0, 2, 0, 5, 0],
                          [0, 0, 6, 0, 6, 0]])

        # Putting every ship on the right or bottom border of the board
        sat4 = [board[1][1] != 0,
                board[1][5] == 5,
                board[2][3] != 0,
                board[3][1] != 0,
                board[3][5] == 0,
                board[5][0] == 3,
                board[5][3] == 3]
        self.assertEqual(check_instance(sat4),
                         [[0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 5],
                          [0, 0, 0, 1, 0, 6],
                          [0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [3, 4, 0, 3, 2, 4]])

        # Giving all the hints as unspecified ship pieces
        sat5 = [board[0][1] != 0,
                board[0][3] != 0,
                board[1][5] != 0,
                board[2][0] != 0,
                board[2][2] != 0,
                board[3][0] != 0,
                board[4][3] != 0,
                board[4][4] != 0,
                board[5][1] != 0]
        self.assertEqual(check_instance(sat5),
                         [[0, 3, 2, 4, 0, 0],
                          [0, 0, 0, 0, 0, 1],
                          [5, 0, 1, 0, 0, 0],
                          [6, 0, 0, 0, 0, 0],
                          [0, 0, 0, 3, 4, 0],
                          [0, 1, 0, 0, 0, 0]])

        # Giving all the hints as either unspecified ship pieces or water cells
        sat6 = [board[0][1] == 0,
                board[1][5] != 0,
                board[2][0] == 0,
                board[2][1] != 0,
                board[3][4] != 0,
                board[3][5] == 0,
                board[4][0] == 0,
                board[4][2] != 0,
                board[4][4] == 0,
                board[5][0] != 0,
                board[5][4] != 0,
                board[5][5] == 0]
        self.assertEqual(check_instance(sat6),
                         [[0, 0, 0, 0, 0, 0],
                          [0, 5, 0, 3, 2, 4],
                          [0, 6, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0],
                          [0, 0, 5, 0, 0, 0],
                          [1, 0, 6, 0, 1, 0]])

        # Another "normal" puzzle
        sat7 = [board[0][1] == 1,
                board[1][4] == 4,
                board[3][0] == 5,
                board[3][4] != 0,
                board[3][5] == 0,
                board[4][2] != 0,
                board[5][5] != 0]
        self.assertEqual(check_instance(sat7),
                         [[0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 3, 4, 0],
                          [0, 0, 0, 0, 0, 0],
                          [5, 0, 0, 0, 1, 0],
                          [2, 0, 1, 0, 0, 0],
                          [6, 0, 0, 0, 3, 4]])

        # Testing unsolvable boards
        # None of the cells can have a value less than 0 or greater than 6
        unsat1 = [board[0][0] == -1]
        self.assertEqual(check_instance(unsat1), [])

        unsat2 = [board[0][0] == 7]
        self.assertEqual(check_instance(unsat2), [])

        # Ship pieces cannot be on some borders
        unsat3 = [board[2][5] == 3]
        self.assertEqual(check_instance(unsat3), [])

        unsat4 = [board[0][2] == 6]
        self.assertEqual(check_instance(unsat4), [])

        unsat5 = [board[5][0] == 2]
        self.assertEqual(check_instance(unsat5), [])

        # Ship pieces must be part of a larger ship
        unsat6 = [board[2][2] == 3,
                  board[2][3] == 0]
        self.assertEqual(check_instance(unsat6), [])

        unsat7 = [board[3][3] == 6,
                  board[2][3] == 0]
        self.assertEqual(check_instance(unsat7), [])

        unsat8 = [board[2][2] == 2,
                  board[2][3] == 0,
                  board[3][2] == 0]
        self.assertEqual(check_instance(unsat8), [])

        # Pieces of separate ships cannot be adjacent
        unsat9 = [board[2][2] != 0,
                  board[3][3] != 0]
        self.assertEqual(check_instance(unsat9), [])

        unsat10 = [board[2][2] == 1,
                   board[3][2] != 0]
        self.assertEqual(check_instance(unsat10), [])

        unsat11 = [board[2][2] == 3,
                   board[3][2] != 0]
        self.assertEqual(check_instance(unsat11), [])

        unsat12 = [board[2][2] == 2,
                   board[2][3] != 0,
                   board[3][2] != 0]
        self.assertEqual(check_instance(unsat12), [])

        # There must be exactly 3 submarines, 2 destroyers and 1 cruiser on the board
        unsat13 = [board[0][0] == 1,
                   board[0][2] == 1,
                   board[0][4] == 1,
                   board[2][0] == 1]
        self.assertEqual(check_instance(unsat13), [])

        unsat14 = [board[0][0] == 3,
                   board[2][0] == 3,
                   board[4][0] == 3,
                   board[0][3] == 5]
        self.assertEqual(check_instance(unsat14), [])

        unsat15 = [board[0][1] != 0,
                   board[1][3] != 0,
                   board[2][0] != 0,
                   board[2][5] != 0,
                   board[3][2] != 0,
                   board[4][4] != 0,
                   board[5][1] != 0]
        self.assertEqual(check_instance(unsat15), [])


if __name__ == '__main__':
    unittest.main()
