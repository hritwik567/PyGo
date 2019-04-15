#! /bin/bash
./parser.py $1
if [[ $? -eq 0 ]]; then
  ir=`basename $1 | cut -d'.' -f1`".ir"
  csymt=`basename $1 | cut -d'.' -f1`".csymt"
  s=`basename $1 | cut -d'.' -f1`".s"
  python codegen/main.py $ir $csymt
  if [[ $? -eq 0 ]]; then
    gcc -m32 $s
  fi
fi
