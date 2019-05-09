#!/bin/bash
 ping -i .200 -c 20 10.108.0.2 > localping.txt
 ping -i .200 -c 20 8.8.8.8 > targetping.txt