# SAT-sudoku

Encode Sudoku game in CNF (Dimacs Format)

Generate 9 x 9 board using the following command:

python sudoku.py -n 9 -i sudoku9.txt

or if you have python3 then run the following instead

python3 sudoku.py -n 9 -i sudoku9.txt

It is possible to generate an N x N board by replacing 'N' for:

python sudoku.py -n 'N'

Check solution on a Linux machine via:

./MiniSat_v1.14_linux sudoku9.txt9.cnf