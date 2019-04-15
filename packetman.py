import subprocess

#Read bash file and insert location in ping and traceroute commands
target: str = "google.com"

subprocess.call("./traceroute.sh")

#Read ping.sh and replace locations where appropriate
#Get local from traceroute.txt (first hop)
local: str = "8.8.8.8"

subprocess.call("./ping.sh")

localPings = {}
targetPings = {}

maxLocal: int = max(localPings)
minLocal: int = min(localPings)
avgLocal: int = sum(localPings)/len(localPings)

maxTarget: int = max(targetPings)
minTarget: int = min(targetPings)
avgTarget: int = sum(targetPings)/len(targetPings)

#THREAD 1: Read localping.txt and targetping.txt, retreive minimum, maximum and average ping for each

#THREAD 2: Cleanup lines after they have been read

#THREAD 3: Process data and visualize it in matplotlib

#Implement a GUI (THREAD 3?)

#THREAD 4: wait for input to kill running processes
