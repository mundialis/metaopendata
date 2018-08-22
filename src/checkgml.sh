#!/bin/bash

GML_DIR=$1

# echo "GML_DIR: ${GML_DIR}"

#### check if gml-file is valid
for filepath in ${GML_DIR}/*.gml; do
  filename=$(basename ${filepath})
  # echo "filename: ${filename}"
  docker run -v ${GML_DIR}:/data geodata/gdal ogrinfo /data/${filename} > /dev/null
  if [ $? -ne 0 ]; then
    echo -e "\e[31mFAIL\e[0m ${filename}"
    mkdir -p ${GML_DIR}/invalid
    mv ${GML_DIR}/${filename} ${GML_DIR}/invalid
  else
    echo -e "\e[32mOK\e[0m ${filename}"
  fi
done
