#!/bin/bash
for h in {00..23}; do
  HOUR=$(printf "%02d" $h)
  mkdir $HOUR
  echo "$HOUR"
  mv 201?????_${HOUR}* ${HOUR}/ 
done
