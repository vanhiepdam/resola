#!/bin/sh
python src/manage.py collectstatic
python src/manage.py migrate
python src/manage.py loaddata seeds/seed.json
python src/manage.py runserver 0.0.0.0:8000
