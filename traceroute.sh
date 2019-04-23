#!/bin/bash
rm traceroute.txt
echo me | sudo -S traceroute -I -n 8.8.8.8 > traceroute.txt
