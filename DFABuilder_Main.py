import os
import time

from DFABuilder_Library import makeDFA
from DFABuilder_OpenAI_Interface import makeRequest
from FAdo.fa import DFA

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
    start = time.perf_counter()
    if not(os.path.isfile(pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt")):
        buildOutputFiles(pathToInputFiles, str(testSuiteNumber))
        print("Built " + pathToInputFiles + "TestSuite" + str(testSuiteNumber) + "_Outputs.txt\nin " + str(round(time.perf_counter() - start, 5)) + " seconds.")
    DFAList = DFAsFromInputFile(pathToInputFiles, str(testSuiteNumber))
    print("Elapsed time: " + str(round(time.perf_counter() - start, 5)) + " seconds.")

if __name__ == "__main__":
    main()