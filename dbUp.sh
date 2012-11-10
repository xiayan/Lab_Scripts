#!/bin/bash

echo Local Update
cd ~/rosetta_database
svn update &

echo R04 Update
ssh r04 'cd ~/rosetta_database; svn update &'

echo R05 Update
ssh r05 'cd ~/rosetta_database; svn update &'
