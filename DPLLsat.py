#!/usr/bin/python3

import sys, getopt

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
    print(instance)
    print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code


    # Search for x, as well as the negation 'NOT" {+/-x}
    unit_clauses = []
    pure_literal_counters = {}
    for n in instance.VARS:
      pure_literal_counters[n] = 0
      pure_literal_counters[-n] = 0


    for i in range(0, len(instance.clauses)):
      if (len(instance.clauses[i]) == 1):
        unit_clauses.append(instance.clauses[i][0])

    # Now we have a list of the unit clauses we can go
    # through the list and remove non-unit clauses containing + or -x

    clauses_to_remove = []
    
    # Store all non-unit clauses containing +/-x
    for i in range(0, len(instance.clauses)):
      for j in range(0, len(unit_clauses)):
        if (unit_clauses[j] in instance.clauses[i]):
          clauses_to_remove.append(instance.clauses[i])
          break

    # Remove all non-unit clauses containing +/-x
    instance.clauses = [ clause for clause in instance.clauses if clause not in clauses_to_remove]

    # Add the single unit clauses back
    for i in range(0, len(unit_clauses)):
      instance.clauses.append([unit_clauses[i]])

    print(instance.clauses)

    # Reset clauses_to_remove
    clauses_to_remove = []

    # Reset unit_clauses to add
    unit_clauses = []

    # Check to see if each literal is pure
    for i in range(0, len(instance.clauses)):
      for j in range(0, len(instance.clauses[i])):
        pure_literal_counters[instance.clauses[i][j]] += 1

    pure_literals = []

    for i in instance.VARS:
      if ((pure_literal_counters[i] > 0) and (pure_literal_counters[-i] == 0)):
        pure_literals.append(i)
      if ((pure_literal_counters[-i] > 0) and (pure_literal_counters[i] == 0)):
        pure_literals.append(-i)
    
    # Iterate through the clause list and remove all clauses containing
    # the pure_literals
    for i in range(0, len(instance.clauses)):
      for j in range(0, len(pure_literals)):
        # print("pure_literals[i] " + str(pure_literals[i]))
        # print("instance.clauses[i] " + str(instance.clauses[i]))
        if pure_literals[j] in instance.clauses[i]:
          clauses_to_remove.append(instance.clauses[i])

    # Remove all clauses containing pure literal +x or -x
    instance.clauses = [ clause for clause in instance.clauses if clause not in clauses_to_remove]

    for i in range(0, len(pure_literals)):
      unit_clauses.append(pure_literals[i])
    # Add the pure literals as unit clauses clauses back
    for i in range(0, len(unit_clauses)):
      instance.clauses.append([unit_clauses[i]])

    print(instance.clauses)
    # print(sys.maxsize)

    # print(instance.clauses)

    # End your code
    return True
    ###########################################


if __name__ == "__main__":
   main(sys.argv[1:])
