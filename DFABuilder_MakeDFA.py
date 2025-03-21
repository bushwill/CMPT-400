from FAdo.fa import *

def makeDFA(stringDFA):
    stringDFA = stringDFA.split('=')[1].strip(". ")[1:-1]
    
    listStringDFA = recStringParse(stringDFA, '{', '}')
    
    states = [state.strip() for state in listStringDFA[0].split(',')]
    alphabet = [symbol.strip() for symbol in listStringDFA[1].split(',')]
    transitions = recStringParse(listStringDFA[2], '(', ')')
    starting_state = stringDFA.split("},")[3].split(",")[0].strip()
    final_states = [int(final_state.strip()) for final_state in listStringDFA[3].split(',')]
    
    for i in range(len(transitions)):
        transitions[i] = [item.strip() for item in transitions[i].split(',')]

    return initDFA(states, alphabet, transitions, starting_state, final_states)

def recStringParse(str, leftItem, rightItem):
    l = str.find(leftItem)
    if l == -1:
        return []
    r = str.find(rightItem)
    if r == -1:
        return []
    return [str[l+1:r]] + recStringParse(str[r+1:], leftItem, rightItem)
        
def initDFA(Q, Sigma, Delta, starting_state, F):
    dfa = NFA()
    for state in Q:
        dfa.addState(state)
    dfa.setSigma(Sigma)
    for transition in Delta:
        dfa.addTransition(int(transition[0]), str(transition[1]), int(transition[2]))
    dfa.setInitial([Q.index(starting_state)])
    dfa.setFinal(F)
    dfa = dfa.toDFA()
    return dfa

def main():
    testString = "DFA = {{q0, q1, q2}, {a, b}, {(0, a, 1), (1, a, 2)}, q0, {2}}."
    dfa = makeDFA(testString)
    print(dfa)

if __name__ == "__main__":
    main()