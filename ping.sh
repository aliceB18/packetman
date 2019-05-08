#!/bin/bash
 ping -i .200 -c 20 8.8.8.8 > localping.txt
 ping -i .200 -c 20 google.com > targetping.txt