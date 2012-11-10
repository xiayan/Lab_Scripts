#!/bin/bash

echo Local Update
cd ~/rosetta_source
svn update &
./external/scons-local/scons.py -j8 mode=release bin &

echo R04 Update
ssh r04 'cd ~/rosetta/; svn update; external/scons-local/scons.py -j8 mode=release bin'

echo R05 Update
#ssh r05 'cd ~/rosetta; svn update &; ./external/scons-local/scons.py -j8 mode=release bin &'
ssh r05 'cd ~/rosetta_source/; svn update; external/scons-local/scons.py -j8 mode=release bin'

