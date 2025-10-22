#! /bin/bash

pip install --upgrade pip

# PostgreSQL ---------->
sudo apt install curl ca-certificates
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc
. /etc/os-release
sudo sh -c "echo 'deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $VERSION_CODENAME-pgdg main' > /etc/apt/sources.list.d/pgdg.list"
sudo apt update
sudo apt -y install postgresql libpq-dev
# <----------

# Backend-Flask ---------->
cd backend-flask
pip install -r requirements.txt
# <----------

# Frontend-React-JS ---------->
cd ..
cd frontend-react-js
npm i
# <----------