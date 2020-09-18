import sys
from cpu import *

cpu = CPU()

#if no program ask for program
if len(sys.argv) < 2:
    print('\nWelcome to LS8.')
    print("\nPlease provide an LS8 argument path.")
    print("Example: \"python ls8.py examples/print8.ls8\"")
    sys.exit()
#if program itterate lines
with open(sys.argv[1]) as a:
    # for each line return first 8 chars if first char is 1 or 0... else discard
    myArg = [int(line[:8], 2) for line in a if line[0] == '0' or line[0] == '1']
    print('\nArguments:')
    print(myArg)
    print()
    print('Executing:')
    #sys.exit()

cpu.load(myArg)
cpu.run()