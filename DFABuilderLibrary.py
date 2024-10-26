import pandas as pd
from FAdo.fa import *
from FAdo.conversions import *
from FAdo.common import *
from FAdo.fio import *
from OpenAI_Interface import *

# response = makeRequest("A DFA that accepts 'aaa' and 'bbb'")
def stringToDfa(input):
    # gets rid of the 'DFA ='
    input = input.split('=')[1].strip(".  ")[0:]
    print(input)
    states = input[input.find("{")+1:input.find("}")].split(",")
    input = input[input.find("}")+1:]

    symbols = input[input.find("{")+1:input.find("}")].split(",")
    input = input[input.find("}")+1:]

    transition_string = input[input.find("{")+1:input.find("}")]
    input = input[input.find("}")+1:]

    transitions = []
    while transition_string.find('(') != -1:   
        transition = transition_string[transition_string.find('(')+1:transition_string.find(')')].strip().split(',')
        transition[0] = int(transition[0])
        transition[2] = int(transition[2])
        transitions.append(transition)
        transition_string = transition_string[transition_string.find(')')+1:]
        
    input = input.strip().split(',')
    starting_state = input[1].strip()
    final_states = [int(s.strip('{ }')) for s in input[2:]]
    
    dfa = initDFA(states, symbols, transitions, starting_state, final_states)
    
    return dfa



def initDFA(Q, Sigma, Delta, starting_state, F):
    dfa = DFA()
    for state in Q:
        dfa.addState(state)
    dfa.setSigma(Sigma)
    for transition in Delta:
        dfa.addTransition(transition[0], transition[1], transition[2])
    dfa.setInitial(Q.index(starting_state))
    dfa.setFinal(F)
    return dfa

def main():
    testString = "DFA = {{q0, q1, q2}, {a}, {(0, a, 1), (1, a, 2)}, q0, {2, 3, 4}}."
    dfa = stringToDfa(testString)
    # dfa.display()

if __name__ == "__main__":
    main()