import os
import time

from DFABuilder_MakeDFA import makeDFA
from DFABuilder_OpenAI_Interface import makeRequest
from DFABuilder_Testing import testDFAs

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
        responses.append(makeRequest(request))
    outputFile = open(pathToFile + "TestSuite" + testSuiteNumber + "_Outputs.txt", "w")
    for response in responses:
        outputFile.write(response + "\n")
        
# Reads from TestSuite?_Outputs.txt
# Returns a list of all the DFAs as FAdo DFA Objects
def DFAsFromInputFile(pathToFile, testSuiteNumber):
    DFAList = []
    inputFile = open(pathToFile + "TestSuite" + testSuiteNumber + "_Outputs.txt", "r")
    for line in inputFile:
        DFAList.append(makeDFA(line.strip()))
    return DFAList

def main():
    pathToInputFiles = "TestSuiteFiles/"
    testSuiteNumber = 1
    if not(os.path.isfile(pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt")):
        if os.path.isfile(pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt"):
            start = time.perf_counter()
            print("Building DFAs from " + pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt")
            buildOutputFiles(pathToInputFiles, str(testSuiteNumber))
            print("Built " + pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt\nin " + str(round(time.perf_counter() - start, 5)) + " seconds.")
            DFAList = DFAsFromInputFile(pathToInputFiles, str(testSuiteNumber))
            print("Elapsed time: " + str(round(time.perf_counter() - start, 5)) + " seconds.")
        else:
            print("No file " + pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt exists")
    else :
        DFAList = DFAsFromInputFile(pathToInputFiles, str(testSuiteNumber))
    
    input_file = open(pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Inputs.txt")
    input_list = []
    for line in input_file:
        input_list.append(line.strip())
  
    accuracy_list = testDFAs(DFAList, input_list)
    
    for item in accuracy_list:
        print(item)

if __name__ == "__main__":
    main()
