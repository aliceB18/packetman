#!/bin/bash
rm traceroute.txt
sudo -S traceroute -I -n 8.8.8.8 > traceroute.txt
