#!/bin/bash
for h in {06..17}; do
  HOUR=$(printf "%02d" $h)
  echo "$HOUR"
  mv ${HOUR}/* .
done
