import subprocess
import threading

#Read bash file and insert location in ping and traceroute commands
target = "google.com"

#Read ping.sh and replace locations where appropriate
#Get local from traceroute.txt (first hop)

localPings = {}
targetPings = {}

#Update the statistics for the ping sets
def UpdateStates ():
    maxLocal = max(localPings)
    minLocal = min(localPings)
    avgLocal = sum(localPings)/len(localPings)

    maxTarget = max(targetPings)
    minTarget = min(targetPings)
    avgTarget = sum(targetPings)/len(targetPings)

#Run data collection processes
def DataCollect ():
    subprocess.run("./traceroute.sh", shell=True, check=True)
    #Get local
    #Set local
    local = "8.8.8.8"
    subprocess.run("./ping.sh", shell=True, check=True)
    print("Data collected!")

def Clean ():
    print ("Cleaning...")
    
def GetKill ():
    user_in = str (input ("Enter 'K' to kill: "))
    while (user_in != 'K'):
       user_in = str (input ("Enter 'K' to kill: "))

#Main 
if __name__ == "__main__":
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
