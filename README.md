# La mia prima data pipeline

## setup api

```
cd api
go build
```

## setup pipeline

```
python3 -m venv venv
. ./venv/bin/activate 
pip install wheel
cd pipeline
python setup.py install
cd -
```

## setup superset

https://github.com/airbnb/superset/blob/master/docs/installation.rst#making-your-own-build

## quickstart

Start the api on a terminal:

```
./api/api
```

On another one we create the db and execute the pipeline for today:

```
. ./venv/bin/activate

python3 createdb.py

luigi.sh $(date +%Y-%m-%d)
```
