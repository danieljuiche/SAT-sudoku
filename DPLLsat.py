#!/usr/bin/python3

import sys, getopt, copy, random, operator

class SatInstance:
    def __init__(self):
        pass
    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if not (maxvar == self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
      # Variables are numbered from 1 to p
        for i in range(1,self.p+1):
            self.VARS.add(i)
    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s



def main(argv):
   inputfile = ''
   verbosity=False
   inputflag=False
   try:
      opts, args = getopt.getopt(argv,"hi:v",["ifile="])
   except getopt.GetoptError:
      print ('DPLLsat.py -i <inputCNFfile> [-v] ')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('DPLLsat.py -i <inputCNFfile> [-v]')
           sys.exit()
    ##-v sets the verbosity of informational output
    ## (set to true for output veriable assignments, defaults to false)
       elif opt == '-v':
           verbosity = True
       elif opt in ("-i", "--ifile"):
           inputfile = arg
           inputflag = True
   if inputflag:
       instance = SatInstance()
       instance.from_file(inputfile)
       solve_dpll(instance, verbosity)
   else:
       print("You must have an input file!")
       print ('DPLLsat.py -i <inputCNFfile> [-v]')


""" Question 2 """
# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#    list of false literals (if verbosity == True)
#
#  You will need to define your own
#  solve(VARS, F), pure-elim(F), propagate-units(F), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
    # print(instance)
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    test_F = [
      [1],
      [1, 99],
      [-1, 4, 5],
      [-2],
      [2, 3, 5],
      [-2, 100, 101],
      [999, 9],
      [-1]
    ]

    test_F2 = [
      [1, 2],
      [-1, 3],
      [-2, -3],
      [-4, 4],
      [5],
      [6, 7],
      [5, 6, 7],
      [5, -1, 2],
      [6, -2, -3]

    ]

    test_empty_clause = [
      [-1],
      [1],
      [1, 2],
      [1, -1]
    ]

    # print(instance.clauses)

    # print(propagate_units(test_empty_clause))
    # propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = pure_elim(instance.clauses)
    # instance.clauses = propagate_units(instance.clauses)
    # instance.clauses = pure_elim(instance.clauses)

    # print(instance.clauses)


    # print(propagate_units(instance.clauses))

    # test_F = propagate_units(test_F)

    # print(propagate_units(test_F))

    # print(pure_elim(test_F2))


    VAR_LIST = instance.VARS
    clauses = copy.deepcopy(instance.clauses)


    clauses = solve(VAR_LIST, clauses, [])

    print("Finished")
    
    # print(clauses)
    # print(instance.clauses)
    # print(sys.maxsize)

    # print(instance.clauses)

    # End your code
    return True
    ###########################################


def solve(VARS, F, explored):
  explored_variables = copy.deepcopy(explored)
  # print("PRINTING!")
  # print(F)

  F = propagate_units(F)
  print("Printing after propagate and elimination: ")
  print(F)

  if (len(F) == 0):
    print("EMPTY UNSAT FROM PROPAGATE")
    return []

  F = pure_elim(F)
  print("Printing after propagate and elimination: ")
  print(F)

  if (len(F) == 0):
    print("EMPTY UNSAT FROM ELIMINATION")
    return []

  for i in F:
    if (i == []):
      print("EMPTY CLAUSE FOUND IN F")
      return []

  num = 0
  # print("VARS: " + str(VARS))
  for i in VARS:
    # print("F: " + str(F))
    if [i] in F:
      num += 1
    elif [-i] in F:
      num += 1
    else:
      num += 0

  if (num == len(VARS)):
    print("NUM == LEN VARS")
    return F

  x = pick_a_variable(VARS, explored_variables)
  print("PICKED VARIABLE " + str(x))

  explored_variables.append(x)

  F_X = copy.deepcopy(F)
  F_X.append([x])

  result = solve(VARS, F_X, explored_variables)

  if ( result != []):
    return result
  else:
    F_not_X = copy.deepcopy(F)
    F_not_X.append([-x])
    return solve(VARS, F_not_X, explored_variables)

"""
propagate-units(F):
    for each unit clause {+/-x} in F
        remove all non-unit clauses containing +/-x
        remove all instances of -/+x in every clause // flipped sign!
"""

def propagate_units(F):

  while (True):

    if ([] in F):
      print("EMPTY CLAUSE FOUND")
      break

    # Define variables to use
    unit_clauses = []
    add_empty_clause_flag = False

    # Find out the unit clauses in F
    for clause in F:
      if (len(clause) == 1):
        unit_clauses.append(clause)

    initial_F_length = len(F)
    initial_unit_clauses_length = len(unit_clauses)

    # Debugging
    # print("UNIT CLAUSES: " + str(unit_clauses))

    # Identify which non-unit clauses containing +/-x to remove
    clauses_to_remove = []

    for clause in F:
      # print("CLAUSE: " + str(clause))
      for unit_clause in unit_clauses:
        # print("UNIT_LITERAL: " + str(unit_literal[0]))
        if (unit_clause[0] in clause) and (len(clause) != 1):
          clauses_to_remove.append(clause)

    # Debugging
    # print("CLAUSES TO REMOVE: " + str(clauses_to_remove))

    # Remove the non-unit clauses that have +/-x
    F = [x for x in F if x not in clauses_to_remove]

    # Debugging
    # print("CLAUSES: " + str(F))

    clauses_to_remove = []
    clauses_to_add = []

    # Remove all instances of -/+x in every clause
    for unit_clause in unit_clauses:
      unit_clause_value = -unit_clause[0]
      for clause in F:
        # print("CLAUSE: " + str(clause))
        if (unit_clause_value in clause):
          # print("BEFORE " + str(clause))
          clauses_to_remove.append(clause)
          added_clause = [x for x in clause if -x not in unit_clause]
          # if (added_clause == []):
          #   add_empty_clause_flag = True
          # else:
          clauses_to_add.append(added_clause)

          #   print("EMPTY CLAUSE")
          # print("AFTER " + str(added_clause))
          # print("CLAUSES TO ADD: " + str(clauses_to_add))

    # Remove the non-unit clauses that have -/+x
    F = [x for x in F if x not in clauses_to_remove]

    # Add back
    for clause in clauses_to_add:
      if clause not in F:
        F.append(clause)

    unit_clauses_check = []
    for clause in F:
      if (len(clause) == 1):
        unit_clauses_check.append(clause)

    final_F_length = len(F)
    final_unit_clauses_length = len(unit_clauses_check)


    if (initial_F_length == final_F_length):
      print("NO CHANGE")
      if (initial_unit_clauses_length == final_unit_clauses_length):
        print("NO CHANGE IN UNIT CLAUSES")
        break

  return F

"""
pure-elim(F):   
    for each variable x
        if +/-x is pure in F
            remove all clauses containing +/-x
            add a unit clause {+/-x}
"""
def pure_elim(F):
  clauses = copy.deepcopy(F)
  pure_literal_counters = {}

  # Reset clauses_to_remove
  clauses_to_remove = []

  # Reset unit_clauses to add
  unit_clauses = []

  # Check to see if each literal is pure
  for i in range(0, len(clauses)):
    for j in range(0, len(clauses[i])):
      if (clauses[i][j] not in pure_literal_counters):
        pure_literal_counters[clauses[i][j]] = 1
      else:
        pure_literal_counters[clauses[i][j]] += 1

  pure_literals = []

  for i in pure_literal_counters:
    if (pure_literal_counters[i] >= 1) and (-i not in pure_literal_counters):
      pure_literals.append(i)
  
  # Iterate through the clause list and remove all clauses containing
  # the pure_literals
  for i in range(0, len(clauses)):
    for j in range(0, len(pure_literals)):
      # print("pure_literals[i] " + str(pure_literals[i]))
      # print("clauses[i] " + str(clauses[i]))
      if pure_literals[j] in clauses[i]:
        clauses_to_remove.append(clauses[i])

  # Remove all clauses containing pure literal +x or -x
  clauses = [ clause for clause in clauses if clause not in clauses_to_remove]

  for i in range(0, len(pure_literals)):
    unit_clauses.append(pure_literals[i])

  # Add the pure literals as unit clauses clauses back
  for i in range(0, len(unit_clauses)):
    clauses.append([unit_clauses[i]])

  return clauses

def pick_a_variable(VARS, explored):
  explored_set = set(explored)
  difference_set = VARS - explored_set

  choice = random.choice(tuple(difference_set))
  # literal_counters = {}

  # for i in range(0, len(clauses)):
  #   for j in range(0, len(clauses[i])):
  #     if (clauses[i][j] not in literal_counters):
  #       literal_counters[clauses[i][j]] = 0
  #     else:
  #       literal_counters[clauses[i][j]] += 1
  # # maximum = max(literal_counters.items(), key=operator.itemgetter(1))[0]
  # random_key = random.choice(list(literal_counters))
  # choice = literal_counters[random_key]

  return choice

if __name__ == "__main__":
   main(sys.argv[1:])
