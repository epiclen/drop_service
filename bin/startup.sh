#!/bin/bash

n=0

i=1

l=20

m=2

c=5

while getopts "i:l:m:c:h" arg
do
  case $arg in
    i)
      i=$OPTARG
      ;;
    l)
      l=$OPTARG
      ;;
    m)
      m=$OPTARG
      ;;
    c)
      c=$OPTARG
      ;;
    h)
     echo OPTION
     echo -i interval
     echo -l load limit
     echo -m memory available
     echo -c stop process number
     exit 1
     ;;
  esac
done

echo $i
echo $l
echo $m
echo $c

python pt10.py -i $i  -l $l -m $m -c $c 
#>> ./down_service.log &
