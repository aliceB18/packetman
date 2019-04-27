import logging
import subprocess
import threading
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#Read bash file and insert location in ping and traceroute commands
target = "google.com"
local = ""


#Read ping.sh and replace locations where appropriate
#Get local from traceroute.txt (first hop)

# Initialize holders for local/target ping latency data
localPings = {}
targetPings = {}

# set up visualization
style.use('fivethirtyeight')


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
    """ Not yet documented
    """
    print("Getting address!")
    subprocess.run("./traceroute.sh", shell=True, check=True)
    #Get local
    #Set local
    local = "8.8.8.8"


def Substitute () -> None:
    """Not yet documented
    """
    # Read ping.sh and replace the local and target
    print("Substitute!")


def StaticVis(infoType: str) -> None:
    """ (str) -> None

        Takes as an input the name of the info desired to be visualized, then plots a
        graph corresponding to said info and prints out related data. *called by DataCollect*

        Currently only supports following infoTypes:
            - "LOCAL_PING"  -> Statically Visualizes localping.txt latency
            - "TARGET_PING" -> Statically Visualizes targetping.txt latency
    """

    if(infoType == "LOCAL_PING"):

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
                localPings[localIndex]: float = float(localLineSplit[6].strip("time="))


        # Store localPings info for easier use
        localPingsX: list = [*localPings.keys()]        # List of Package sequence numbers
        localPingsY: list = [*localPings.values()]      # List of Latency of each package corresponding to sequence

        # Title plot and label axis
        plt.title("Local Ping Latency")
        plt.xlabel("Number of Packet sent")
        plt.ylabel("Latency (in ms)")

        # plot and Set axis dimensions
        plt.plot(localPingsX, localPingsY)
        plt.axis([1, max(localPingsX), 10, max(localPingsY) + 5])

    elif(infoType == "TARGET_PING"):

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
                targetIndex: float = float(targetLineSplit[4].strip("icmp_seq="))

                # Retrieve latency of package (in milliseconds)
                targetPings[targetIndex]: float = float(targetLineSplit[6].strip("time="))

        # Store targetPings info for easier use
        targetPingsX = [*targetPings.keys()]
        targetPingsY = [*targetPings.values()]

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
def DataCollect (visInfoTypes: list) -> None:
    print("Pinging Website & Recording Data (This may take a bit)...")
    subprocess.run("./ping.sh", shell=True, check=True)
    for i in range(len(visInfoTypes)):
        StaticVis(visInfoTypes[i])



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
    collectionThread = threading.Thread(target=DataCollect(["LOCAL_PING", "TARGET_PING"]))
    collectionThread.start()
    collectionThread.join()

    cleanupThread = threading.Thread(target=Clean)
    cleanupThread.start()

    #DataCollect(["LOCAL_PING", "TARGET_PING"])
    killThread = threading.Thread(target=GetKill)
    killThread.start()
    killThread.join()


#THREAD 1: Read localping.txt and targetping.txt, retreive minimum, maximum and average ping for each

#THREAD 2: Cleanup lines after they have been read

#THREAD 3: Process data and visualize it in matplotlib

#Implement a GUI (THREAD 3?)

#THREAD 4: wait for input to kill running processes
