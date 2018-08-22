#!/bin/bash

usage="checkgml.sh [-n] -d GML_DIR "

DRY_RUN=0

while getopts nd:h options; do
  case "${options}" in
    d) GML_DIR=$OPTARG;;
    n) DRY_RUN=1;;
    h) echo $usage
    \? ) echo $usage
      exit 1;;
    * ) echo $usage
      exit 1;;
  esac
done

if [ "x" == "x$GML_DIR" ]; then
  echo "-d [option] is required"
  exit 1
fi

if [ $DRY_RUN -eq 0 ]; then
  mkdir -p ${GML_DIR}/invalid
else
  echo "## doing dry run ##"
fi

for filepath in ${GML_DIR}/*.gml; do
  filename=$(basename ${filepath})
  docker run -v ${GML_DIR}:/data geodata/gdal ogrinfo /data/${filename} > /dev/null
  if [ $? -ne 0 ]; then
    echo -e "\e[31mFAIL\e[0m ${filename}"
    if [ $DRY_RUN -eq 0 ]; then
      mv ${GML_DIR}/${filename} ${GML_DIR}/invalid
    fi
  else
    echo -e "\e[32mOK\e[0m ${filename}"
  fi
done
