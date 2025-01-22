def testDFAs(DFAList, InputWordsList):
    accuracy_list = []
    for i in range(len(DFAList)):
        dfa = DFAList[i]
        accepted = []
        words = InputWordsList[i].split(",")
        for word in words:
          word = word.strip()
          if word == "":
              words.remove(word)
          elif word == "ɛ": 
             if dfa.evalWordP([]):
                 accepted.append(word)
          else:
             if dfa.evalWordP(word):
                 accepted.append(word)
        accuracy = len(accepted) / len(words)
        accuracy_list.append(str(i) + ": " + str(int(accuracy*100)) + "%")
    return accuracy_list