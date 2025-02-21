import os
import time

from DFABuilder_MakeDFA import makeDFA
from DFABuilder_OpenAI_Interface import makeRequest
from DFABuilder_Testing import *

# Makes requests to OpenAI API
# Reads from TestSuite?_Inputs.txt
# Outputs DFA definitions to TestSuite?_Outputs.txt
def buildOutputFiles(pathToFile, testSuiteNumber):
    requests = []
    responses = []
    inputFile = open(pathToFile + "TestSuite" + testSuiteNumber + "_Inputs.txt", "r")
    for line in inputFile:
        requests.append(line.strip())
    inputFile.close()
    for request in requests:
        responses.append(makeRequest(request, "gpt-4o-mini"))
    outputFile = open(pathToFile + "TestSuite" + testSuiteNumber + "_Outputs.txt", "w")
    for response in responses:
        outputFile.write(response + "\n")
        
# Reads from TestSuite?_Outputs.txt
# Returns a list of all the DFAs as FAdo DFA Objects
def DFAsFromOutputFile(pathToFile, testSuiteNumber):
    DFAList = []
    inputFile = open(pathToFile + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt", "r")
    for line in inputFile:
        DFAList.append(makeDFA(line.strip()))
    return DFAList

def constructDFAs(pathToTestFiles, testSuiteNumber):
    if not(os.path.isfile(pathToTestFiles + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt")):
        if os.path.isfile(pathToTestFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt"):
            start = time.perf_counter()
            print("Building DFAs from " + pathToTestFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt")
            buildOutputFiles(pathToTestFiles, str(testSuiteNumber))
            print("Built " + pathToTestFiles + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt\nin " + str(round(time.perf_counter() - start, 5)) + " seconds.")
            print("Elapsed time: " + str(round(time.perf_counter() - start, 5)) + " seconds.")
            return DFAsFromOutputFile(pathToTestFiles, str(testSuiteNumber))
        else:
            print("No file " + pathToTestFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt exists")
    else :
        return DFAsFromOutputFile(pathToTestFiles, str(testSuiteNumber))

def evaluateDFAs(DFAList, pathToTestFiles, testSuiteNumber):
    input_file = open(pathToTestFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt")
    input_list = []
    for line in input_file:
        input_list.append(line.strip())
  
    return evaluateDFAList(DFAList, input_list)

def userInterface(DFAList, accuracy_list):
    print("[1] Print full DFA evaluation")
    print("[2] Print specific DFA evaluation")
    print("[3] Display specific proposed DFA")
    print("[4] Display specific recall DFA")
    print("[5] Print specific DFA definition")
    user_choice = input()
    if user_choice == '1':
        print("--------------------")
        for item in accuracy_list:
            print(item[1])
    if user_choice == '2':
        print("Which DFA? (Index starts at 0)")
        user_choice = int(input())
        print("--------------------")
        print(accuracy_list[user_choice][1])
    if user_choice == '3':
        print("Which DFA? (Index starts at 0)")
        user_choice = int(input())
        print("--------------------")
        if accuracy_list[user_choice][0]:
            DFAList[user_choice].display()
            print("Displayed DFA Successfully")
        else:
            print("Invalid DFA, cannot display")
    if user_choice == '4':
        print("Which DFA? (Index starts at 0)")
        user_choice = int(input())
        print("--------------------")
        if accuracy_list[user_choice][0]:
            accuracy_list[user_choice][2].display()
            print("Displayed DFA Successfully")
        else:
            print("Invalid DFA, cannot display")
    if user_choice == '5':
        print("Which DFA? (Index starts at 0)")
        user_choice = int(input())
        print("--------------------")
        if accuracy_list[user_choice][0]:
            print(str(user_choice) + ": " + str(DFAList[user_choice]))
        else:
            print("Invalid DFA, cannot display")
        
    print("--------------------")
        
def main():
    pathToTestFiles = "TestSuiteFiles/"
    testSuiteNumber = 1
    
    DFAList = constructDFAs(pathToTestFiles, testSuiteNumber)
  
    accuracy_list = evaluateDFAs(DFAList, pathToTestFiles, testSuiteNumber)
    
    on = True
    while on:
        userInterface(DFAList, accuracy_list)

if __name__ == "__main__":
    main()
