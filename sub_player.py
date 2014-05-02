""" parses srt file and display subtitles """
#!/usr/bin/env python

import pysrt
from time import sleep
from ast import literal_eval
import sys

def main():
    """parse srt files and display text according to time"""
    subs = pysrt.open(sys.argv[1])
    previous = literal_eval(sys.argv[2]) + 0.0

    for sub in subs:
        time_point = sub.start.hours * 3600.0
        time_point = time_point + sub.start.minutes * 60.0
        time_point = time_point + sub.start.seconds
        time_point = time_point + sub.start.milliseconds / 1000.0

        if time_point < previous:
            continue

        sleep(time_point - previous)

        print sub.text
        previous = time_point

main()
