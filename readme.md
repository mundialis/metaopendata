usage
=====

`cd bmvi-metadaten-wfs-getfeature-gml-download-parser`

`docker build docker -t bmvi-metadaten-wfs-getfeature-gml-download-parser`

`docker run --net dockerexample_default -it --rm -v /mnt/data/gml:/download -v /home/ubuntu/bmvi-metadaten-wfs-getfeature-gml-download-parser/src:/src --name running-bmvi-metadaten-wfs-getfeature-gml-download-parser bmvi-metadaten-wfs-getfeature-gml-download-parser /src/parser.py --cleanup --no-dryrun --debug | tee parse.log`


to overwrite python as entrypoint, run

`docker run --net dockerexample_default -it --rm -v /mnt/data/gml:/download -v /mnt/data/metadata:/metadata -v /home/ubuntu/bmvi-metadaten-wfs-getfeature-gml-download-parser/src:/src --name running-bmvi-metadaten-wfs-getfeature-gml-download-parser --entrypoint /bin/bash bmvi-metadaten-wfs-getfeature-gml-download-parser /src/get_metadata_from_data.sh --cleanup --no-dryrun --debug | tee parse.log`
