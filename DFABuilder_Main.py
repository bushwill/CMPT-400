import os
import time

from DFABuilder_MakeDFA import makeDFA
from DFABuilder_OpenAI_Interface import makeRequest
from DFABuilder_Evaluation import *
from FAdo.conversions import *
from FAdo.reex import *
from FAdo.fa import *

class EvaluatedDFA:
    def __init__(self, originalDFA, proposedDFA):
        self.originalDFA = originalDFA
        self.proposedDFA = proposedDFA
        self.tpDFA = originalDFA.conjunction(proposedDFA)
        self.fpDFA = proposedDFA.conjunction(~originalDFA)
        self.fnDFA = originalDFA.conjunction(~proposedDFA)
    def __str__(self):
        return str(self.originalDFA) + str(self.proposedDFA)

# Makes requests to OpenAI API
# Reads from TestSuite?_PEs.txt
# Outputs DFA definitions to TestSuite?_GPT_DFAs.txt
def build_GPT_DFAs(pathToFile, model = "gpt-4o-mini"):
    requests = []
    responses = []
    inputFile = open(pathToFile + "_PEs.txt", "r")
    for line in inputFile:
        requests.append(line.strip())
    inputFile.close()
    for request in requests:
        responses.append(makeRequest(request, model))
    outputFile = open(pathToFile + "_" + model + "_GPT_DFAs.txt", "w")
    for response in responses:
        outputFile.write(response + "\n")
        
# Reads from TestSuite?_GPT_DFAs.txt
# Returns a list of all the DFAs as FAdo DFA Objects
def DFAsFromGPTFile(pathToFile, model = 'gpt-4o-mini'):
    DFAList = []
    inputFile = open(pathToFile + "_" + model + "_GPT_DFAs.txt", "r")
    for line in inputFile:
        DFAList.append(makeDFA(line.strip()))
    return DFAList

def DFAsFromCREs(pathToFile):
    DFAList = []
    inputFile = open(pathToFile + "_CREs.txt", "r")
    for line in inputFile:
        DFAList.append(str2regexp(line.strip()).toDFA())
    return DFAList

# Creates file of DFA definitions utilizing buildOutputFiles() if no file exists
def construct_GPT_DFAs(pathToFile,  model = 'gpt-4o-mini'):
    if not(os.path.isfile(pathToFile + "_" + model + "_GPT_DFAs.txt")):
        if os.path.isfile(pathToFile + "_PEs.txt"):
            start = time.perf_counter()
            print("Building DFAs from "+ pathToFile + "_PEs.txt")
            build_GPT_DFAs(pathToFile, model)
            print("Built " + pathToFile + "_" + model + "_GPT_DFAs.txt\nin " + str(round(time.perf_counter() - start, 5)) + " seconds.")
            print("Elapsed time: " + str(round(time.perf_counter() - start, 5)) + " seconds.")
            return True
        else:
            print("No file " + pathToFile + "_PEs.txt exists")
            return False
    else :
        return True

def constructDFAList(original_dfa_list, proposed_dfa_list):
    DFAList = []
    invalidDFAs = 0
    for i in range(len(original_dfa_list)):
        try:
            str(proposed_dfa_list[i])
        except:
            invalidDFAs += 1
            continue
        original_dfa = original_dfa_list[i]
        proposed_dfa = proposed_dfa_list[i]
        DFAList.append( EvaluatedDFA(original_dfa, proposed_dfa) )
    return DFAList, invalidDFAs
        
def userInterface(DFAList, invalid_dfas = 0):
    print("[0] to select different gpt model")
    print("Enter a DFA #")
    print("[index starting at 1]")
    print(str(len(DFAList)) + " DFAs available")
    if invalid_dfas > 0:
        print(str(invalid_dfas) + " DFAs were invalid")
    dfa_index = int(input())
    if dfa_index == 0:
        return False
    elif 1 <= dfa_index and dfa_index <= len(DFAList):
        chosen_dfa = DFAList[dfa_index - 1]
    else:
        print("Invalid entry!")
        return True
    print("What would you like to do with DFA #" + str(dfa_index) + "?")
    print("[0] go back to DFA list")
    print("[1] display the original DFA")
    print("[2] display the proposed DFA")
    print("[3] display the true positives DFA")
    print("[4] display the false positives DFA")
    print("[5] display the false negatives DFA")
    user_input = int(input())
    while user_input != 0:
        if user_input == 1:
            chosen_dfa.originalDFA.display()
        elif user_input == 2:
            chosen_dfa.proposedDFA.display()
        elif user_input == 3:
            chosen_dfa.tpDFA.display()
        elif user_input == 4:
            chosen_dfa.fpDFA.display()
        elif user_input == 5:
            chosen_dfa.fnDFA.display()
        user_input = int(input())
    print("~~~~~~~~~~~~~~~~~~~~")
    return True
    
        
def main():
    on = True
    while on:
        pathToTestFiles = "TestSuiteFiles/"
        testSuiteNumber = 2
        print("Choose a gpt model:")
        print("[0] gpt-4o-mini")
        print("[1] gpt-4o")
        print("[2] o1-mini")
        print("[3] o1-preview")
        user_input = int(input())
        if user_input == 0:
            model = 'gpt-4o-mini'
        elif user_input == 1:
            model = 'gpt-4o'
        elif user_input == 2:
            model = 'o1-mini'
        elif user_input == 3:
            model = 'o1-preview'
        else:
            print("Incorrect entry")
            exit()
        pathToFile = pathToTestFiles + "TestSuite" + str(testSuiteNumber)   
        construct_GPT_DFAs(pathToFile, model)
        original_dfa_list = DFAsFromCREs(pathToTestFiles + "TestSuite" + str(testSuiteNumber))
        proposed_dfa_list = DFAsFromGPTFile(pathToFile, model)
        DFAList, invalidDFAs = constructDFAList(original_dfa_list, proposed_dfa_list)
        selected_model = True
        while selected_model:
            selected_model = userInterface(DFAList, invalidDFAs)
        

if __name__ == "__main__":
    main()
