#!/bin/bash
echo Cleaning python code in \'`pwd`\' and subdirectories
for file in `find * | egrep '(\.py$)|(\.rst$)|(^scripts/tr-*)'`; do
  echo $file
  sed -i -e $'s/\t/    /' ${file}
  sed -i -e $'s/[ \t]\+$//' ${file}
  sed -i -e $'s/^# --$/#--/' ${file}
  ./updateheaders.py ${file}
done
exit 0
