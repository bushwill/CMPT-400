from FAdo.fa import *

def evaluateDFAList(DFAList, InputWordsList):
    evaluation_list = []

    for i in range(len(DFAList)):
        try:
            # Check if the DFA is valid by trying to convert it to a string
            str(DFAList[i])
            is_valid = 1  # The DFA is valid
        except:
            evaluation_list.append([0, str(i) + ": Invalid DFA", None])
            continue  # Skip to the next DFA if invalid

        dfa = DFAList[i]
        words = InputWordsList[i].split(",")
        words_evaluated = len(words)
        accepted = []
        rejected_words = []

        # Evaluate each word
        for word in words:
            word = word.strip()

            # Handle empty word (ɛ)
            if word == "":
                words.remove(word)
                words_evaluated -= 1
            elif word == "ɛ":
                if dfa.evalWordP([]):
                    accepted.append(word)
                else:
                    rejected_words.append(word)
            else:
                if dfa.evalWordP(word):
                    accepted.append(word)
                else:
                    rejected_words.append(word)

        # Calculate acceptance rate
        accuracy = len(accepted) / words_evaluated if words_evaluated > 0 else 0
        acceptance_rate = str(i) + ": " + str(int(accuracy * 100)) + "% (" + str(words_evaluated) + ")"

        # Generate a DFA that accepts the incorrectly rejected words
        rejected_dfa = makeDFAForRejectedWords(rejected_words)

        # Append the evaluation [validity, acceptance rate, rejected DFA]
        evaluation_list.append([is_valid, acceptance_rate, rejected_dfa])

    return evaluation_list

def makeDFAForRejectedWords(words):
    dfa = DFA()
    state_index = {}  # Maps word and position to state index
    
    # Initial state
    initial_state = dfa.addState("q0")
    dfa.setInitial(initial_state)

    next_state_index = 1  # Tracks state indices
    final_states = []  # To keep track of final states

    # Construct transitions for each word
    for word in words:
        current_state = 0  # Start from the initial state
        
        for i, symbol in enumerate(word):
            # Check if a state for this position exists, if not, create it
            if (current_state, symbol) not in state_index:
                new_state = dfa.addState(f"q{next_state_index}")
                state_index[(current_state, symbol)] = new_state
                next_state_index += 1
            else:
                new_state = state_index[(current_state, symbol)]
            
            # Add the transition from current state to new state
            dfa.addTransition(current_state, symbol, new_state)
            current_state = new_state  # Move to the next state

        # Mark the final state for this word
        final_states.append(current_state)

    # Set final states
    dfa.setFinal(final_states)

    # Set the alphabet based on the characters in the rejected words
    dfa.setSigma(sorted(set("".join(words))))

    return dfa