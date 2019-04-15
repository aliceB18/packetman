import subprocess

#Read bash file and insert location in ping and traceroute commands
str target = "google.com"

subprocess.call("./tracert.sh", shell=True)

#Read ping.sh and replace locations where appropriate
#Get local from traceroute.txt (first hop)
str local = "8.8.8.8"

subprocess.call("./ping.sh", shell=True)

localPings = {}
targetPings = {}

int maxLocal = max(localpings)
int minLocal = min(localPings)
int avgLocal = sum(localPings)/len(localPings)

int maxTarget = max(targetPings)
int minTarget = min(targetPings)
int avgTarget = sum(targetPings)/len(targetPings)

#THREAD 1: Read localping.txt and targetping.txt, retreive minimum, maximum and average ping for each

#THREAD 2: Cleanup lines after they have been read

#THREAD 3: Process data and visualize it in matplotlib

#Implement a GUI
