# Foggy-Battleships-SAT-Reduction
A reduction to SAT of the Foggy Battleships puzzle

This project is an implementation of a SAT reduction in Microsoft's Z3 SAT solver for Python. The SAT reduction is an encoding of a simplified version of the Foggy Battleships puzzle (https://web.archive.org/web/20120408123228/http://acertijos-y-enigmas.com.ar/2006/07/batalla-naval-xiii.html), which is very similar to the single-player puzzle game Battleship based on the popular two-player board game of the same name. It was developed in the PyCharm IDE and can be executed once the Z3 package is installed in the Python terminal using the command: pip install "z3-solver". fbs.py contains the well-documented SAT reduction of Foggy Battleships and prints a solution of one instance of the puzzle. tests.py contains the same SAT reduction formatted for unit testing with the built-in Python unittest library.
