#!/bin/bash

cd picture && rm -rf *
pwd
cd ..
cp ../../default.jpg ./picture/
mongo infos
