#!/bin/bash
kill `ps -ax | grep $1 | grep -v grep | awk '{print $1}'`