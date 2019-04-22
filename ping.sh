#!/bin/bash
ping -i .200 -c 100 8.8.8.8 > localping.txt
ping -i .200 -c 100 8.8.8.8 > targetping.txt
