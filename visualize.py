import packetman
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# Create File objects
localPing = open("localping.txt", "r")
targetPing = open("targetping.txt", "r")

# set up visualization
style.use('fivethirtyeight')

fig = plt.figure()
axl = fig


