#!/bin/sh

clean() {
  for file in $1/*
  do
    if [ -d $file ]
    then
      clean $file
    else
      echo $file
      temp=$(tail -100 $file)
      echo "$temp" > $file
    fi
  done
}
 
dir=/code/logs
clean $dir
