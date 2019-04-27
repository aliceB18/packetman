import logging
import subprocess
import threading
import json


#Read bash file and insert location in ping and traceroute commands
target = "google.com"
local = ""


#Read ping.sh and replace locations where appropriate
#Get local from traceroute.txt (first hop)

# Initialize holders for local/target ping latency data
localPings = []
targetPings = []


#Update the statistics for the ping sets
def UpdateStats() -> None:
    maxLocal: float = max(localPings)
    minLocal: float = min(localPings)
    avgLocal: float = sum(localPings)/len(localPings)

    maxTarget: float = max(targetPings)
    minTarget: float = min(targetPings)
    avgTarget: float = sum(targetPings)/len(targetPings)


#Get local address
def GetAddress () -> None:
    print("Getting address!")
    subprocess.run("./traceroute.sh", shell=True, check=True)
    #Get local
    #Set local
    local = "8.8.8.8"


def Substitute () -> None:
    # Read ping.sh and replace the local and target
    print("Substitute!")


    # Run data collection processes
def DataCollect () -> None:
    print("Pinging Website & Recording Data (This may take a bit)...")
    subprocess.run("./ping.sh", shell=True, check=True)

    # Create File objects as lists of lines
    localPingFile = open('localping.txt', 'r')
    targetPingFile = open('targetping.txt', 'r')

    # Retrieve first lines from localping.txt and targetping.txt
    print("Retreiving currentLocalLine")                    #DEBUG
    currentLocalLine = localPingFile.readline()
    print("Retreiving currentTargetLine")                   #DEBUG
    currentTargetLine = targetPingFile.readline()

    print("Entering While Loop")                            #DEBUG

    for i in range(100):
        # Retrieve next line from localping.txt and targetping.txt
        currentLocalLine = localPingFile.readline()
        # print("Current Local Line: " + currentLocalLine)  # DEBUG
        currentTargetLine = targetPingFile.readline()
        # print("Current Target Line: " + currentTargetLine)  # DEBUG

        # Split both current lines into lists
        # Example Line:
        # 64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=14.6 ms
        localLineData: [str] = currentLocalLine.split(" ")
        targetLineData: [str] = currentTargetLine.split(" ")

        if currentLocalLine == "\n":
            # LocalLineData being empty
            targetPings.append(float(targetLineData[6].strip("time=")))
            break
        else:
            # Add latency data to localPings/targetPings
            localPings.append(float(localLineData[6].strip("time=")))
            targetPings.append(float(targetLineData[6].strip("time=")))

    print("localPings: " + str(localPings))
    print("targetPings: " + str(targetPings))
    print("Data collected!")


def Clean () -> None:
    print("Cleaning...")


def GetKill () -> None:
    user_in = str(input("Enter 'K' to kill: "))

    while (user_in != 'K'):
        user_in = str (input ("Enter 'K' to kill: "))


#Main 
if __name__ == "__main__":
    GetAddress()
    Substitute()
    collectionThread = threading.Thread(target=DataCollect)
    collectionThread.start()
    collectionThread.join()

    cleanupThread = threading.Thread(target=Clean)
    cleanupThread.start()

    killThread = threading.Thread(target=GetKill)
    killThread.start()
    killThread.join()


#THREAD 1: Read localping.txt and targetping.txt, retreive minimum, maximum and average ping for each

#THREAD 2: Cleanup lines after they have been read

#THREAD 3: Process data and visualize it in matplotlib

#Implement a GUI (THREAD 3?)

#THREAD 4: wait for input to kill running processes
