#!/usr/bin/python3

import sys, getopt
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
# num_hours_i_spent_on_this_assignment = 0

# 4.5 hours understanding
# 3.5 hours on sudoku
# 20 hours on DPLLsat

#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
"""

"""
#####################################################
#####################################################

def main(argv):
   inputfile = ''
   N=0
   try:
      opts, args = getopt.getopt(argv,"hn:i:",["N=","ifile="])
   except getopt.GetoptError:
      print ('sudoku.py -n <size of Sodoku> -i <inputputfile>')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
           sys.exit()
       elif opt in ("-n", "--N"):
           N = int(arg)
       elif opt in ("-i", "--ifile"):
           inputfile = arg
   instance = readInstance(N, inputfile)
   toCNF(N,instance,inputfile+str(N)+".cnf")




def readInstance (N, inputfile):
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance =[]
        for line in input_file:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [int(n) for n in number_strings] # Convert to integers
            if len(numbers) == N:
                instance.append(numbers) # Add the "row" to your list.
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
        return instance # a 2d list: [[1, 3, 4], [5, 5, 6]]


""" Question 1 """
def toCNF (N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"
    number_of_variables = N*N*N
    number_of_clauses = 0

    clauses = []

    # Constraint 1
    for x in range(1, N+1):
      for y in range(1, N+1):
        new_clause = ""
        for k in range(1, N+1):
          new_clause += str(convertIndex(x,y,k,N)) + " "

        new_clause += "0\n"
        clauses.append(new_clause)
        number_of_clauses += 1

    # Constraint 2
    for x in range(1, N+1):
      for y in range(1, N+1):
        for k in range(1, N+1):
          for l in range(k+1, N+1):
            new_clause = ""
            new_clause += str(-convertIndex(x,y,k,N)) + " "
            new_clause += str(-convertIndex(x,y,l,N)) + " "
            new_clause += "0\n"
            clauses.append(new_clause)
            number_of_clauses += 1

    # Constraint 3
    for x in range(1, N+1):
      for k in range(1, N+1):
        for j1 in range(1, N+1):
          for j2 in range(j1+1, N+1):
            new_clause = ""
            new_clause += str(-convertIndex(x,j1,k,N)) + " "
            new_clause += str(-convertIndex(x,j2,k,N)) + " "
            new_clause += "0\n"
            clauses.append(new_clause)
            number_of_clauses += 1

    # Constraint 4
    for j in range(1, N+1):
      for k in range(1, N+1):
        for i1 in range(1, N+1):
          for i2 in range(i1+1, N+1):
            new_clause = ""
            new_clause += str(-convertIndex(i1,j,k,N)) + " "
            new_clause += str(-convertIndex(i2,j,k,N)) + " "
            new_clause += "0\n"
            clauses.append(new_clause)
            number_of_clauses += 1

    # Constraint 5
    for y in range(0, len(instance)):
      for x in range(0, len(instance[y])):
        fixedValue = instance[y][x]
        if (fixedValue != 0):
          # print("x: " + str(x+1) + " y: " + str(y+1) + " =  " + str(instance[y][x]))

          # Add clauses
          clauses.append(str(convertIndex(x+1,y+1,fixedValue,N)) + " 0\n")
          number_of_clauses += 1


    output_file.write("c " + str(outputfile) +"\n")
    output_file.write("p cnf " + str(number_of_variables) + " " + str(number_of_clauses) + "\n")

    for i in range(0, len(clauses)-1):
      output_file.write(clauses[i])

    final_line = clauses[len(clauses)-1].strip('\n')
    output_file.write(final_line)


    "*** YOUR CODE ENDS HERE ***"
    output_file.close()


# Accepts grid coordinates from (1,1) to (N,N)
# i is the x-coordinate
# j is the y-coordinate
# k is the value at that coordinate
# N is the puzzle size
def convertIndex(i, j, k, N):
  return (i - 1)*(N*N) + (j - 1)*(N) + k


if __name__ == "__main__":
   main(sys.argv[1:])
