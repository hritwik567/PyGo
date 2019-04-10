#! /bin/bash
./parser.py $1
ir=`basename $1 | cut -d'.' -f1`".ir"
csymt=`basename $1 | cut -d'.' -f1`".csymt"
python codegen/main.py $ir $csymt
