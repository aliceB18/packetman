#!/bin/bash
 cowsay 'Pinging Website and Recording data... this may take a while'
ping -i .200 -c 20 10.252.10.54 > localping.txt
 ping -i .200 -c 20 google.com > targetping.txt