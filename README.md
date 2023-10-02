# IOT APP

## Prerequisites

<ol>
  <li>Python 3.10</li>
  <li>Pipenv</li>
  <li>Posgresql</li>
  <li>Redis Server</li>
  <li>NPM</li>
  <li>Node 16</li>
</ol> 

## Installing


Pipenv

```
pipenv shell
pipenv install
```

install backend
```
./release.sh
```

Build frontend
```
cd client
npm ci
npm run build
```


## Run server
run celery server
```
python manage.py start celery
```

run flask server
```
python manage.py start flask-gunicorn
```

or

run flask without gunicorn
```
python manage.py start flask
```


### Scheduled Job
run on server
```
python scheduler.py
```
or using cronjob
```
python daily_reset.py
```