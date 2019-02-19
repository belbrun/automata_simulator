

class Writer():

    """
        Class that is initialized in an automaton object to handle the
        command line printout and managing the simulation log.
    """

    def __init__(self, automaton):
        self.automaton = automaton

    def writeSimulationIntro(self):
        """
            Prints an introduction message for the simulation and
            some general information about the automaton
        """
        print 'Starting simulation of :'
        print str(self.automaton)
        print '-Start of simulation-\n'
        return

    def writeCurrentState(self, currentState, previousState = None, character = None):
        """
            Prints out the current state of the automaton in simulation.
            If the previous state is not specified presumes it's
            the start of the simulation and prints out the starting state of the
            automaton.
        """
        if not previousState :
            print 'Simulation begins in the starting state: {state}'\
            .format(state = currentState)
        else :
            if character != '$':
                self.writeTransition(previousState, character, [currentState], False)
            else :
                self.writeTransition(previousState, character, [currentState], True)

        print 'Current stack:'
        if len(self.automaton.stack) == 1:
            self.automaton.simulationLog += currentState + "#" + "$"
            print 'Empty'
        else:
            self.automaton.simulationLog += currentState + "#" + self.automaton.getStackString()
            print self.automaton.getStackString()
        self.automaton.simulationLog += "|"
        print '-'*15
        return

    def writeTransition(self, previousState, character, currentState, isEpsilon):
        """
            Wraps data about an automaton transition and prints out the result.
            warrning: currentState argument is supposed to be a data structure
        """
        if not isEpsilon:
            print 'Character {char} triggered a transition :'\
            .format(char = character)
        else :
            print 'Epsilon transition occured :'
        print '{previous} ---> {current}'\
        .format(previous = previousState, current = ','.join(currentState)

    def writeCurrentStates(self, currentStates):
        """
            Prints given current states joined with a comma
        """
        print 'Current states of the automaton: {states}'\
        .format(states = ','.join(currentStates))


    def writeSimulationEnd(self, currentState, success):
        """
            Prints out a message specifying the way that the simulation ended
        """
        if not success:
            self.automaton.simulationLog += "fail|"
            print 'Automaton failed in digesting character sequence'
        if isInAcceptableState(currentState):
            self.automaton.simulationLog += "1"
            print 'Simulation ended in an acceptable state'
        else:
            self.automaton.simulationLog += "0"
            print 'Simulation ended in an unacceptable state'
        print '-End of simulation-\n'
        return

    def isInAcceptableState(currentState):
        """
            Checks if the automaton in a given current state is in an acceptable
            state. Method is class specific (depending on which automaton was
            used to initialize the writer).
        """

        if isinstance(self.automaton, PushdownAutomaton):
            return currentState is not None and \
            currentState in self.automaton.acceptableStates

        if isinstance(self.automaton, EpsilonNFA):
            return not currentState.isdisjoin(self.automaton.acceptableStates)

        return False
