# MetaOpenData API

* see API docs here: https://bmvimetadaten.mundialis.de/api/latest/api/swagger.json
* see templates here: actinia_gdi/templates/geonetwork/template_metadaten.xml


## Requirements
```
sudo apt install \
    python-virtualenv\
    python3.5\
    python3-dev\
    # uwsgitop\
```
* a running GeoNetwork instance
* a running PostgreSQL instance


## DEV - Installation
It is preferred to run actinia-GDI in a virtual python environment.


Clone repository, create virtual environment and activate it:
```
git clone git@github.com:mundialis/metaopendata.git
cd metaopendata/actinia-gdi
virtualenv -p python3 venv
. venv/bin/activate
```

Change configuration in ```config/mount```

Install required Python packages into the virtual environment:

```
pip install -r requirements.txt
python setup.py install
```
Run tests:
```
python setup.py test
```

Run the server for development:
```
python -m actinia_gdi.main
```

Or for production use actinia_gdi.wsgi as WSGI callable:
```
gunicorn -b :5000 actinia_gdi.wsgi
```

If all done, leave environment
```
deactivate
```

## INT - Installation


```
git clone git@github.com:mundialis/metaopendata.git
cd metaopendata/actinia-gdi
docker build s2i-actinia-gdi-builder -t s2i-actinia-gdi-builder
s2i build . s2i-actinia-gdi-builder actinia-gdi

docker run -v /mnt/data/metaopendata:/tmp/metaopendata:Z -p 5000:8080 actinia-gdi

# or if you have a docker-compose setup, include the content of the
# docker-compose.yaml into yours and run

docker-compose -f ~/docker-example/docker-compose.yml up -d actinia-gdi
```


## INT - Update

```
cd metaopendata/actinia-gdi
s2i build . s2i-actinia-gdi-builder actinia-gdi

docker-compose -f ~/docker-example/docker-compose.yml up -d actinia-gdi
```



## DEV notes:


#### Logging:
in any module, import `from actinia_gdi.resources.logging import log` and call logger with `log.info("my info i want to log")`
