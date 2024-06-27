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

### Backoffice
```
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

### Frontoffice
```
uvicorn api:app --host 0.0.0.0 --port 5000 --workers 5 --proxy-headers --reload
```


## Available Scripts in frontend directory
In the project directory, you can run:


### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.
