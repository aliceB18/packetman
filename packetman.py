import logging
import subprocess
import threading

# Visuals
from threading import Thread

from matplotlib import style
import matplotlib.pyplot as plt

# File management
from shutil import move
from os import remove
import matplotlib.animation as animation

# Read ping.sh and replace locations where appropriate
# Get local from traceroute.txt (first hop)

# Track number of tests
tests: int = 0

# Initialize holders for local/target ping latency data
# Stores all ping test results
localPings = {}
targetPings = {}

# Stores last ping test results
lastLocal = {}
lastTarget = {}

# Store test stats
maxLocal = 0.0
minLocal = 0.0
avgLocal = 0.0

maxTarget = 0.0
minTarget = 0.0
avgTarget = 0.0

# Global Vars
global STOP_THREADS

# set up visualization
style.use('fivethirtyeight')


# Update the statistics for the ping sets
def UpdateStats() -> None:
    global maxLocal, minLocal, avgLocal, maxTarget, minTarget, avgTarget
    print("Updating Stats...")
    # Update Local
    maxLocal = max(localPings.values())
    minLocal = min(localPings.values())
    avgLocal = sum(localPings.values()) / len(localPings)
    # Update Target
    maxTarget = max(targetPings.values())
    minTarget = min(targetPings.values())
    avgTarget = sum(targetPings.values()) / len(targetPings)
    # Print stats
    PrintStats()


def PrintStats() -> None:
    global maxLocal, minLocal, avgLocal, maxTarget, minTarget, avgTarget, tests
    print("TEST STATISTICS:")
    print("LOCAL")
    print("MIN: " + str(minLocal))
    print("MAX: " + str(maxLocal))
    print("AVG: " + str(avgLocal))
    print("PACKETS: " + str(len(localPings)))
    print("PACKET LOSS " + str((tests-len(localPings))/tests))

    print("TARGET")
    print("MIN: " + str(minTarget))
    print("MAX: " + str(maxTarget))
    print("AVG: " + str(avgTarget))
    print("PACKETS: " + str(len(targetPings)))
    print("PACKET LOSS: " + str((tests-len(targetPings))/tests))


def InitScripts() -> None:
    """ Create scripts with a default format so the variables can be found easily
    """
    f = open("ping.sh", "w+")
    f.write("#!/bin/bash\n ping -i .200 -c 20 LOCAL > localping.txt\n ping -i .200 -c 20 TARGET > targetping.txt")
    f.close()

    f = open("traceroute.sh", "w+")
    f.write("#!/bin/bash\n rm traceroute.txt\n sudo -S traceroute -I -n TARGET > traceroute.txt")
    f.close()

    subprocess.run("./perms.sh", shell=True, check=True)


def GetTarget() -> None:
    """ None -> None

        Get target location from user and update scripts
    """
    # Credit for input: https://www.w3schools.com/python/ref_func_input.asp
    print("Please enter a location to test: ")
    target = input()
    GetLocal(target)  # Get local address from traceroute.sh and replace it in the ping script


# Get local address
def GetLocal(target) -> None:
    """ Str -> None

        Get local address from traceroute.sh and replace it in the ping script
    """
    print("Getting address!")
    SubstutituteTrace(target)
    subprocess.run("./traceroute.sh", shell=True, check=True)
    # Get local
    f = open("traceroute.txt", "r")
    line = f.readlines()[2]
    local = line.split(" ")[3]
    print("LOCAL: " + local + " TARGET: " + target)
    Substitute(local, target)


def SubstutituteTrace(target) -> None:
    """ Str -> None

        Replace the TARGET locaiton in the traceroute script
    """
    f = open("traceroute.sh", "r")
    newF = open("traceroute2.sh", "w+")
    lines = f.readlines()
    for line in lines:
        line = line.replace("TARGET", target)
        newF.write(line)

    f.close()
    newF.close()

    # Remove original file
    remove("./traceroute.sh")
    # Move new file
    move("./traceroute2.sh", "./traceroute.sh")
    subprocess.run("./perms.sh", shell=True, check=True)


def Substitute(local, target) -> None:
    """ Str, Str -> None

        Substitute the local and target variables in the bash scripts
    """
    print("Substituting locations")
    # Credit for file handling: https://www.guru99.com/reading-and-writing-files-in-python.html
    # Read ping.sh and replace the local and target
    f = open("ping.sh", "r")
    newF = open("ping2.sh", "w+")
    lines = f.readlines()
    for line in lines:
        line = line.replace("TARGET", target)
        line = line.replace("LOCAL", local)
        newF.write(line)

    f.close()
    newF.close()

    # Credit for remove and move method:
    # https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
    # Remove original file
    remove("./ping.sh")
    # Move new file
    move("./ping2.sh", "./ping.sh")
    subprocess.run("./perms.sh", shell=True, check=True)


def StaticVis(infoType: str) -> None:
    """ (str) -> None

        Takes as an input the name of the info desired to be visualized, then plots a
        graph corresponding to said info and prints out related data. *called by DataCollect*

        Currently only supports following infoTypes:
            - "LOCAL_PING"  -> Statically Visualizes localping.txt latency
            - "TARGET_PING" -> Statically Visualizes targetping.txt latency
    """

    if infoType == "LOCAL_PING":

        # Format file object as list of lines
        localPingFileData = open('localping.txt', 'r').read()
        localPingLines: list = localPingFileData.split("\n")

        # Iterate through each line in total set of lines
        for localLine in localPingLines:

            # Skip first line of file as well as every other line which doesn't list immediate ping info
            if str(localLine).__contains__("PING") or not str(localLine).__contains__("icmp_seq="):
                continue

            else:
                # Split valid lines
                localLineSplit = localLine.split(" ")
                # print(localLineSplit)                                                     #DEBUG

                # Retrieve package sequence (Ie: number of package being sent)
                localIndex: float = float(localLineSplit[4].strip("icmp_seq="))

                # Retrieve latency of package (in milliseconds)
                localPings[len(localPings)+1]: float = float(localLineSplit[6].strip("time="))
                lastLocal[localIndex]: float = float(localLineSplit[6].strip("time="))

        #print(localPings)
        # Store localPings info for easier use
        localPingsX: list = [*lastLocal.keys()]  # List of Package sequence numbers
        localPingsY: list = [*lastLocal.values()]  # List of Latency of each package corresponding to sequence

        # Title plot and label axis
        plt.title("Local Ping Latency")
        plt.xlabel("Number of Packet sent")
        plt.ylabel("Latency (in ms)")

        # plot and Set axis dimensions
        plt.plot(localPingsX, localPingsY)
        plt.axis([1, max(localPingsX), 10, max(localPingsY) + 5])

    elif infoType == "TARGET_PING":

        # Format file object as list of lines
        targetPingFileData = open('targetping.txt', 'r').read()
        targetPingLines: list = targetPingFileData.split("\n")

        # Iterate through each line in total set of lines
        for targetLine in targetPingLines:

            # Skip first line of file as well as every other line which doesn't list immediate ping info
            if str(targetLine).__contains__("PING") or not str(targetLine).__contains__("icmp_seq="):
                continue
            else:
                # Split valid lines
                targetLineSplit = targetLine.split(" ")
                # print(targetLineSplit)                                                     #DEBUG
                # Retrieve package sequence (Ie: number of package being sent)
                try:
                    targetIndex = float(targetLineSplit[4].strip("icmp_seq="))
                except ValueError:
                    targetIndex = float(targetLineSplit[5].strip("icmp_seq="))

                # Retrieve latency of package (in milliseconds)
                try:
                    targetPings[len(targetPings)+1]: float = float(targetLineSplit[6].strip("time="))
                    lastTarget[targetIndex]: float = float(targetLineSplit[6].strip("time="))
                except ValueError:
                    targetPings[len(targetPings) + 1]: float = float(targetLineSplit[7].strip("time="))
                    lastTarget[targetIndex]: float = float(targetLineSplit[7].strip("time="))

        #print(targetPings)
        # Store targetPings info for easier use
        targetPingsX = [*lastTarget.keys()]
        targetPingsY = [*lastTarget.values()]

        # Title Plot and label axis
        plt.title("Target Ping Latency")
        plt.xlabel("Number of Packet sent")
        plt.ylabel("Latency (in ms)")

        # Plot and set axis dimensions
        plt.plot(targetPingsX, targetPingsY)
        plt.axis([1, max(targetPingsX), 10, max(targetPingsY) + 5])

    # Show whichever plot was constructed by function call
    plt.show()


# Run data collection processes
def DataCollect() -> None:
    # Call ping script
    print("Pinging Website & Recording Data (This may take a bit)...")
    subprocess.run("./ping.sh", shell=True, check=True)


def Visualize(visInfoTypes: list) -> None:
    print("Preparing visualization...")
    # calls visualize for each ping type
    for i in range(len(visInfoTypes)):
        StaticVis(visInfoTypes[i])


def Clean() -> None:
    print("Cleaning...")
    subprocess.run("./rm.sh", shell=True, check=True)


# Main
if __name__ == "__main__":
    STOP_THREADS = False
    # Have user input target

    # User traceroute to get local
    InitScripts()
    targetThread = threading.Thread(target=GetTarget())
    targetThread.start()
    targetThread.join()

    while True:
        try:
            # Data collection
            collectionThread: Thread = threading.Thread(target=DataCollect())
            collectionThread.start()
            collectionThread.join()

            tests += 20

            # Visualization
            visThread = threading.Thread(target=Visualize(["LOCAL_PING", "TARGET_PING"]))
            visThread.start()
            visThread.join()

            # Print Stats
            statThread = threading.Thread(target=UpdateStats())
            statThread.start()
            statThread.join()

            # Cleanup
            cleanupThread = threading.Thread(target=Clean)
            cleanupThread.start()
            cleanupThread.join()

        except KeyboardInterrupt:
            break

    # Reset bash scripts to the default 8.8.8.8 target (will be easier to modify again)
    # Somehow have the user trigger a graceful exit
