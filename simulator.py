from automatons import PushdownAutomaton, EpsilonNFA
import sys,argparse

"""
    Module used to simulate automatons in the automatons.py module.
    Handles console line input arguments to specify the simulation parameters and
    console line output to give an overall view of the simulation results.
"""


def readCommand(argv):
    """
        Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description = 'Simple automaton simulator')

    parser.add_argument('-test_num', type = int, help = 'Number of a test case\
                        you want to run (there are 25 of them numbered from 1 - 25)')

    parser.add_argument('--all', action='store_true',
                    help='Optional argument that runs all the test cases')

    parser.add_argument('-dpda', action='store_true',
                        help='Argument for running tests on a pushdown automaton')

    parser.add_argument('-enfa', action='store_true',
                        help='Argument for running tests on an epsilon \
                        non-deterministic finite automaton')

    return parser.parse_args()

def getInput(testNum, automatonType):
    """
        Returns the input for the test case under the given number
    """
    return readTestFile(testNum, automatonType)

def getOutput(testNum, automatonType):
    """
        Returns the output for the test case under the given number
    """
    return readTestFile(testNum, automatonType, 'out')

def readTestFile(testNum,  automatonType, extension = 'in'):
    """
        Reads a test file under the given number.
        Input extension is given by default but the output extension can be
        specified in the method call.
    """
    if automatonType == 'enfa':
        extension += '.txt'
    path = 'tests\\{automaton}\\test{testNum}\\test.{extension}'\
            .format(testNum = testNum, extension = extension, automaton = automatonType)
    return open(path, "r").read().splitlines()


def runTestCase(testNum, automatonType):

    """
        Runs a simulation of one test case, compares the simulation log with
        a correct one and returns true if the simulation finished as projected,
        false otherwise.
    """

    input = getInput(testNum, automatonType)
    characters = []
    automaton = None

    for sequence in input[0].split("|"):
        characters.append(sequence.split(","))

    if automatonType == 'dpda':
        automaton = PushdownAutomaton.parseAutomatonDefinition(input)
    elif automatonType == 'enfa':
        automaton = EpsilonNFA.parseAutomatonDefinition(input)

    correctOutput = getOutput(testNum, automatonType)

    print('Test case No{num}'.format(num = testNum))
    for sequence in enumerate(characters):
        log = automaton.simulate(sequence[1])
        correctLog = correctOutput[sequence[0]]
        if log:
            if len(log) > len(correctLog):
                print('Part of the log cut off: ' + log[len(correctLog):])
                log = log[:len(correctLog)]
            print ('Simulation log:\n{simulated}\n'
                    'Correct log:\n{correct}'\
                    .format(simulated = log, correct = correctLog))
            if log == correctLog :
                print('\nLogs match\nTEST SUCCEDED')
                print('\n' + 15*'-' + '\n')
                return True
            else :
                print('\nLogs do not match\nTEST FAILED')
                print('\n' + 15*'-' + '\n')
                return False

#main method
def main():
    args = readCommand(sys.argv)

    testsAttempted = 0
    testsSucceded = 0
    testsFailed = []
    testMax = -1
    automatonType = ""


    if not args.dpda and not args.enfa:
        print('One type of automaton must be chosen in the arguments (use -help for\
        explanation)')
    elif args.dpda:
        automatonType = "dpda"
        testMax = 25
    elif args.enfa:
        automatonType = "enfa"
        testMax = 24

    if args.all :
        for i in range(1,testMax):
            success = runTestCase(i, automatonType)
            testsAttempted += 1
            testsSucceded += 1 if success else 0
            if not success:
                testsFailed.append(i)

    elif 1 <= args.test_num <=testMax :
        success = runTestCase(args.test_num, automatonType)
        testsAttempted += 1
        testsSucceded += 1 if success else 0

    else :
        print('Test case number is not valid, must be between 1 and 25.')
        return

    print('Tests succeded\n {succeses}/{attempts}'\
    .format(succeses = testsSucceded, attempts = testsAttempted))

    print('Test cases that resulted in a failure:\n{cases}'\
        .format(cases = ','.join(map(str, testsFailed))))


if __name__ == '__main__':
    main()
