#!/bin/bash
for PY in $(ls */*py)
do
  python2 $PY -m local
done
