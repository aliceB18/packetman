import subprocess
import threading


#Read bash file and insert location in ping and traceroute commands
target = "google.com"
local = ""


#Read ping.sh and replace locations where appropriate
#Get local from traceroute.txt (first hop)


localPings = {}
targetPings = {}


#Update the statistics for the ping sets
def UpdateStats() -> None:
    maxLocal: int = max(localPings)
    minLocal: int = min(localPings)
    avgLocal: int = sum(localPings)/len(localPings)

    maxTarget: int = max(targetPings)
    minTarget: int = min(targetPings)
    avgTarget: int = sum(targetPings)/len(targetPings)


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
    subprocess.run("./ping.sh", shell=True, check=True)
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
