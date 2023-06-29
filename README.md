# NCEO ARD STAC API

Feng Yin

feng.yin.15@ucl.ac.uk

Department of Geography, University College London


This is a STAC API implementation for the NCEO ARD data. It is based on the [stac-stac-fastapi-pgstac](https://github.com/stac-utils/stac-fastapi-pgstac/tree/main).

## Usage

### Syncing data

The [sync_stac_items.py](sync_stac_items.py) script can be used to sync the NCEO ARD data to [STAC directory](STAC). This script requires the [requests](https://docs.python-requests.org/en/master/) and [retry](https://pypi.org/project/retry/) packages to be installed.

Install the packages with pip.

```bash
pip install requests retry
```

You can then run the script to sync the data.

```bash
python sync_stac_items.py
``` 


### Docker

The easiest way to run this is with Docker. You can use the [docker-compose.yml](docker-compose.yml) file to run the API and a Postgres database with the NCEO ARD data loaded.

```bash
docker-compose up
```

This will start the API on port 8080. You can then access the API at http://localhost:8080.
