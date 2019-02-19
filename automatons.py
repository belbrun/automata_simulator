
from abc import ABCMeta
from writer import Writer

"""
This file contains automaton definitions that can be simulated using
simulator.py.
"""


class Automaton(object):

    """
    Abstract class that implements common automaton features.
    """

    __metaclass_ = ABCMeta

    #@abstractmethod
    def simulate(self, input):
        pass


    def saveTransitions(self,transitions):
        """
        Adds a transition to the list of transitions
        """
        self.transitions = {}
        for transition in transitions:
            transition = transition.split("->")
            self.transitions[transition[0]] = transition[1].split(",")
        return

    #Base constructor
    def __init__(self, states, symbols, acceptableStates, q0, transitions):
        self.states = states
        self.symbols = symbols
        self.acceptableStates = acceptableStates
        self.q0 = q0
        self.saveTransitions(transitions)



class PushdownAutomaton(Automaton):

    def __init__(self, states, symbols, stacksymbols, acceptableStates, q0, z0, transitions):
        """
        Stores the automaton definition.

        states: States automaton can be in
        symbols: Input symbols that can be feed to the automaton entry
        stacksymbols: symbols that can be stored on the automatons stack
        acceptableStates: States in which the automaton should be when the
                        simulation ends if the automaton accepts the
                        char sequence fed to it
        q0: Start state
        z0: Start stack symbols
        tranistions: List of tranisitions the automaton can make
        """
        super(PushdownAutomaton, self).__init__(states, symbols, acceptableStates, q0, transitions)
        self.stacksymbols = stacksymbols
        self.z0 = z0
        self.stack = []
        self.simulationLog = ""
        self.writer = Writer(self)


    @staticmethod
    def parseAutomatonDefinition(definition):
        """
        Parses the automaton definition (if the definition  is correctly given)
        and returns a class instance.
        """
        if len(definition) < 8:
            return None

        pushdownAutomaton = \
        PushdownAutomaton(definition[1], definition[2], definition[3]\
        , definition[4], definition[5], definition[6], definition[7:])

        return pushdownAutomaton

    def simulate(self, input):
        """
        Simulates the behavior of the automaton for a given input.
        """
        #print and log the information about the start of simulation
        self.writer.writeSimulationIntro()

        #initialize the automaton according to the definition
        currentState = self.q0
        self.stack = []
        self.stack.extend(["$",self.z0])

        #print and log the state of the automaton on the start of simulation
        self.writer.writeCurrentState(currentState)

        currentState = self.makeEpsilonTransition(currentState)

        #simulate behaviour for every character in the given input
        for character in enumerate(input):

            currentState = self.makeTransition(currentState,character[1])
            if currentState is None:
                #end the simulation with an unsuccesful annotation
                self.writer.writeSimulationEnd(currentState, False)
                return self.simulationLog
            #don't make epsilon tranisions if the automaton is in an acceptable state
            #and has digested all the characters in the given sequence
            if character[0] == len(character) or currentState not in self.acceptableStates:
                currentState = self.makeEpsilonTransition(currentState)


        #if the automaton digests all characters without stopping end the
        #simulation with successfull annotation
        self.writer.writeSimulationEnd(currentState, True)
        return self.simulationLog

    def makeTransition(self, currentState, character, isEpsilon = False):
        """
        Makes a tranisition given a current state and an input character.
        Uses different behaviour if the transition is an epsilon tranisition.
        Returns the next state of the automaton (None if the transition can't
        be made).
        """


        nextState = None
        addToStack = None #character to be added to the stack
        poppedCharacter = "$"


        #get the character that is currently on top of stack
        try:
            poppedCharacter = self.stack.pop()
        except Exception as e:
            print("EXCEPTION:",currentState,character,isEpsilon)

        #concatinate the parameters to get a key in the tranitions dictionary
        currentConfiguration =  currentState + "," + character + "," + poppedCharacter
        #if the key is contained in the dictionary
        if currentConfiguration in self.transitions:
            #proccess the transition
            nextState = self.transitions.get(currentConfiguration)[0]
            addToStack = list(self.transitions.get(currentConfiguration)[1])
            #add the characters specified by the transition to the top of stack
            for i in xrange(len(addToStack)-1,-1,-1):
                if addToStack[i] == "$":
                    break
                self.stack.append(addToStack[i])
            #print and log the current state of the automaton
            self.writer.writeCurrentState(nextState, currentState, character)
        #if the transition is not possible and the tried transition was an
        #epsilon transition, return the popped character to the stack
        elif isEpsilon:
            self.stack.append(poppedCharacter)

        return nextState


    def makeEpsilonTransition(self, currentState):
            """
            Makes epsilon transition from a given current state until the
            epsilon tranistion can't be made or the state transitioned to
            is an acceptable state of the automaton.
            """
            nextState = self.makeTransition(currentState, "$", True)
            #if the epsilon transition cannot be made
            if nextState is None:
                #return the last state automaton was found in before the transition
                return currentState
            #return the current state if it is an acceptable state
            if nextState in self.acceptableStates:
                return nextState
            #otherwise try to make a new epsilon transition recursively
            return self.makeEpsilonTransition(nextState)

    def getStackString(self):
        """
            Returns a string representation of the stack
        """
        return "".join(self.stack[:0:-1])

    def __str__(self):
        return ('Automaton definition (pushdown automaton):\n'
                'States: {automaton.states}\n'
                'symboles: {automaton.symbols}\n'
                'Stack symboles: {automaton.stacksymbols}\n'
                'Acceptable states: {automaton.acceptableStates}\n'
                'Starting state: {automaton.q0}\n'
                'Starting stack: {automaton.z0}\n')\
                .format(automaton = self)


class EpsilonNFA(Automaton):

    def __init__(self, states, symbols, acceptableStates, q0, transitions):
        super(EpsilonNFA, self).__init__(states, symbols, acceptableStates, q0, transitions)
        self.simulationLog = ""
        self.writer = Writer(self)


    @staticmethod
    def parseAutomatonDefinition(definition):
        """
        Parses the automaton definition (if the definition  is correctly given)
        and returns a class instance.
        """
        if len(definition) < 6:
            return None

        epsilonNFA = \
        EpsilonNFA(definition[1], definition[2], definition[3]\
        , definition[4], definition[5:])

        return epsilonNFA

    def simulate(self, input):
        """
            Simulates the behavior of the automaton for a given
            character sequence (input).
        """
        self.writer.writeSimulationIntro()
        currentStates = set(self.q0)
        self.writer.writeCurrentStates(currentStates)
        currentStates = epsilonTransition(currentStates)
        self.writer.writeCurrentStates(currentStates)

        for index, character in input.enumerate():
            nextStates = self.makeTransition(currentStates, character)
            nextStates = self.makeEpsilonTransition(nextStates)
            currentStates.clear()
            currentStates |= nextStates
            if '#' in currentStates:
                self.writer.writeSimulationEnd(currentStates, success = False)

        self.writer.writeSimulationEnd(currentStates, success = True)
        return self.simulationLog

    def makeTransition(self, currentStates, character, isEpsilon = False):
        """
            Makes a tranisition given a current state and an input character.
            Uses different behavior if the transition is an epsilon tranisition.
            Returns the next states of the automaton (None if the transition can't
            be made).
        """

        nextStates = set()
        for state in currentStates:
            currentConfiguration = state + "," + character
            if currentConfiguration in self.transitions:
                newStates = self.transitions.get(currentConfiguration)
                nextStates |= newStates
                self.writer.writeTransition(state, character, newStates, isEpsilon)
        nextStates.intersection_update(self.states)

        if not nextStates and not isEpsilon:
            nextState.add("#") # hashtag simbolizes end of simulation

        return nextStates

    def makeEpsilonTransition(self, currentStates):
        """
            Makes a transition with an epsilon transition character recursively
            until the transition cannot be made anymore.
            Original call af the function will return all new states gathered
            in upper described recursive search.
        """
        nextStates = self.makeTransition(currentStates, '$', True)
        if not nextStates:
            return nextStates
        else:
            return nextStates.union(self.makeEpsilonTransition(nextStates))

    def __str__(self):
        return ('Automaton definition '
                '(non-finite automaton with epsilon transitions automaton):\n'
                'States: {automaton.states}\n'
                'symboles: {automaton.symbols}\n'
                'Acceptable states: {automaton.acceptableStates}\n'
                'Starting state: {automaton.q0}\n')\
                .format(automaton = self)
