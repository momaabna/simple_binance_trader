#!/bin/bash
echo '1'>flag.txt
python3 online_stategy_mavg.py >output.log 2>&1 &
