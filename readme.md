usage
=====

`docker build docker -t bmvi-metadaten-wfs-getfeature-gml-download-parser`

`docker run --net dockerexample_default -it --rm -v /mnt/data/gml:/download -v /home/ubuntu/bmvi-metadaten-wfs-getfeature-gml-download-parser/src:/src --name running-bmvi-metadaten-wfs-getfeature-gml-download-parser bmvi-metadaten-wfs-getfeature-gml-download-parser /src/parser.py



`docker run --link db -it --rm -v /dir/of/py-files/src:/src --name running-bmvi-metadaten-wfs-getfeature-gml-download-parser bmvi-metadaten-wfs-getfeature-gml-download-parser /src/parser.py`
