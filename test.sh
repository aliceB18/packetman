rm ping.txt
rm traceroute.txt
ping 8.8.8.8 > ping.txt
sudo traceroute -I -n 8.8.8.8 > traceroute.txt
