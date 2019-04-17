#!/bin/bash

run_path=$1
test_dir=$2

input1="10 9 8 7 6 5 4 3 2 1"
input2="2 3"
input3="1 2 4 8 16"
input4=""
input5=""
input6="123"
input7=""
input8=""
input9=""
input10="10 9 8 7 6 5 4 3 2 1"
input11=""
input12=""
input13=""
input14=""
input15=""
input16=""
input17=""
input18=""
input19=""
input20=""

for i in `seq 1 20`; do
  file=$(ls $test_dir | grep "^$i\_")
  rm a.out
  a=$($run_path "$test_dir/$file")
  test -f a.out
  if [[ $? -ne 0 ]]; then
    flag[i]="$file: FAILED"
    flag[i]="$file: PASSED"
    continue
  fi
  echo "Running $file"
  in="input$i"
  out=$(echo $(eval echo \$${in}) | ./a.out)
  echo $out | grep -i -q "Hritvik Done"
  if [[ $? -ne 0 ]]; then
    flag[i]="$file: FAILED"
    flag[i]="$file: PASSED"
    continue
  fi
  flag[i]="$file: PASSED"
done

echo ""
echo "##################################################"
for i in "${flag[@]}"; do
  echo "$i";
done
echo "##################################################"
