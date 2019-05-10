#!/bin/bash
 rm traceroute.txt
 sudo -S traceroute -I -n www.google.com > traceroute.txt