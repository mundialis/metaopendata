#!/bin/bash

################################################################################
# This script will read all downloaded data files by name, parse the UUID and
# write the according metadata to filesystem with the same name.


# TODO confirm filename is parsed correctly
# (split by '-', remove first and last item, UUID should be left)
# from parser.py:
# wfsName = wfsUrl.text.split('?')[0].split('/')[-1]
# fileName = wfsName + "-" + identifier.text + "-" + featureType.text.split(':')[-1] + "-" + version.text + ".gml"

################################################################################

DATA_DIR=/download
META_DIR=/metadata

GNOS_URL="https://bmvimetadaten.mundialis.de/geonetwork/srv/eng/csw"
GNOS_REQUEST="request=GetRecordById&service=CSW&version=2.0.2&elementSetName=full&outputSchema=http:%2F%2Fwww.isotc211.org%2F2005%2Fgmd"

user=mundialis
password=thecaiXishahsu3n


for data in $DATA_DIR/*
do
    echo -ne "\n\n"
    filename=$(basename ${data%.*})
    echo "Parsing filename $DATA_DIR/$filename ..."

    IFS='-';
    read -ra part_of_name <<< "$filename"
    total=${#part_of_name[*]}
    uuid_spaces="${part_of_name[@]:1:${#part_of_name[@]}-3}"
    uuid="${uuid_spaces// /-}"
    unset IFS
    echo "    Found UUID: $uuid"

    echo "    Get metadata: ${GNOS_URL}?${GNOS_REQUEST}&id=$uuid"
    curl -u $user:$password -X GET "${GNOS_URL}?${GNOS_REQUEST}&id=$uuid" \
        > $META_DIR/${filename}.xml

    echo "    Wrote metadata to $META_DIR/${filename}.xml ."

done
