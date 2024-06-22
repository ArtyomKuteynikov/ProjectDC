# Running project

## Start DB and Redis
### Installing PostgreSQL
```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
sudo -i -u postgres psql
```
### Setting up DB
```
alter user postgres with encrypted password 'L0l!k1510';
create database <db_name>;
grant all privileges on database <db_name> to postgres;
```
### Installing and starting Redis
```
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis
sudo service redis-server start
redis-cli
```

## Installing Python3 and starting VENV
```
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
python3 -m venv myprojectenv
```

Activate venv
```
source myprojectenv/bin/activate
```

Deactivate venv
```
deactivate
```


## Install requirements

```
source venv/bin/activate

cd backoffice

pip install -r requirements.txt

pip install psycopg
```

## Don't forget to set .env from .env.examples

## Starting project
```
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```
