# Week 1 — App Containerization

**1st] DOCKER CONTAINERS, General video Review, & Notes Taken**

I reviewed all the videos for Week 1; then I went back to the Container Video and typed out notes as I followed along, attempting to peice together what needed to be done to get the solution; I am not providing all my notes that I took, seeing how there were alot, however here's the summary:

After having followed along with Andrew, James, & Edith I have come to a refined list of steps; much of it was cleaver ways to teach the studnets more about how GITPOD, BASH, or DOCKER worked; here are All of the ACTUAL Steps that need to be completed:

*A:  /workspace/aws-bootcamp-cruddur-2023/backend-flask*

Create "dockerfile" and input this code:
```
FROM python:3.10-slim-buster

WORKDIR /backend-flask 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]	
```

*B:	/workspace/aws-bootcamp-cruddur-2023/frontend-react-js $ npm i*

installing NPM
further into my notes below, you'll see this step is important later on; fail to do this now and it messes up the Compose Up later

*C: /workspace/aws-bootcamp-cruddur-2023/frontend-react-js*
Create "dockerfile" and input this code:
```
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD {"npm", "start"}
```

*D: /workspace/aws-bootcamp-cruddur-2023*

 Create "docker-compose.yml" and input this code:

I removed ```version: "3.8"``` because I noticed a message in the logs "...version is obselete..."; turns out that Docker-Compose files no longer require specifying the version; in fact if you do, it'll tell you if it's obselete, then ignore the version you listed, and reference the latest updated version instead.

```

services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST_ID}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST_ID}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST_ID}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

networks:
  internal-network:
    driver: bridge
    name: cruddur
```
 NOTE: I had some typos I had to fix

*E: /workspace/aws-bootcamp-cruddur-2023 $ docker compose up *
It'll take some time to download all the files needed from the registry 

*F:	Make sure the Ports are open & Servered*

If you see any Ports saying "Not Servered", you likely failed to install NPM in /Frontend-react-js prior to Compose Up

*G: Open a Ports; click the link (or past the URL into a browser tab) for the Front-End; then troubleshoot if it doesn't work; once the ports were fixed, it worked fine*

----------------------------------------
What I actually did...

1. Setup an account on Docker Hub
2. Installed Docker, NPM, & Python Extensions for my Gitpod Workspace
3. Completed Steps A; had some typos that I found along the way, and had to fix those
4. Completed Steps B - D just fine
5. Completed Steps E & F....well I went to open the Ports and noticed that Port 3000 was not listed at all
6. I found the cause; I did ```docker compose up``` but from the Frontend-React-Js folder
7. Corrected my mistake; ran it from " Workspace/aws-bootcamp-cruddur-2023 " this time Port 3000 was built but "not Servered"
8. Troubleshooted, and found out that I needed to install NPM in /frontend-react-js before Compose Up; so I Compose Down the Containers
   I also realized that the Frontend Container will build without the NPM install but when it goes to run it's Dockerfile it'll failed at ```CMD ["npm","start"]```; it'll fail to see the Start command since NPM is not installed, so the Container will be left in a Stop or Exit state, hence why Port 3000 was built but "Not Servered"

![Screenshot 2025-04-21 100143](https://github.com/user-attachments/assets/e399d0db-ee5e-4cbc-a0ad-8db8c8f892b8)


   
10. Then ```npm i``` while in frontend-react-js
11. Then Compose Up
12. Ports were built & "Open"
14. Link for the Frontend worked, I was able to get into the basic CRUDDUR application
----------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------

**2nd] Add code in the API for the Notifications acitivity for the CRUDDUR application**

![Screenshot 2025-04-21 113327](https://github.com/user-attachments/assets/d04b1a92-3684-48cc-bbd8-fae74d87124a)

----------------------------------------------------------------------------------------------------------------------------------------------------------------

**3rd] Add code & built the DyanmoDB (local) & Postgres for the CRUDDUR application**

*A: He's got you adding code to:  docker-compose.yml file, at the end of the "services"*

```
dynamodb-local:
	# https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
	# We needed to add user:root to get this working.
	user: root
	command: "-jar DynamoDBLocal.jar -sharedDB -dbPath ./data"
	image: "amazon/dynamodb-local:latest"
	container_name: dynamodb-latest
	ports:
		- "8000:8000"
	volumes:
		- "./docker/dynamodb:/home/dynamodblocal/data"
	working_dir: /home/dynamodblocal
```

*B: added code again into Services right below our 1st modification 
this code is modified with my changes; read further to find out what I altered*

```
db:
	image: postgres:13-alpine
	restart: always
	environment:
		-POSTGRES_USER=postgres
		-POSTGRES_PASSWORD=password
	ports:
		- "5432:5432"
	volumes:
		- db:/var/lib/postgresql/data
```

*C: added code again at the bottom of our YML file, below the Networks we had already defined:*

```
volumes:
	db:
		driver: local
		
```

------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------

**4th] Setting up for Postgres**

*A: Attempted to Create a Table*

input
```
aws dynamodb create-table \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --table-class STANDARD
```
result lines were generated by AWS CLI in GITPOD terminal:
```
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Artist",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SongTitle",
:...skipping...
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Artist",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SongTitle",
                "AttributeType": "S"
            }
        ],
        "TableName": "Music",
        "KeySchema": [
            {
                "AttributeName": "Artist",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SongTitle",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": "2025-04-22T01:43:38.681000+00:00",
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": "1970-01-01T00:00:00+00:00",
            "LastDecreaseDateTime": "1970-01-01T00:00:00+00:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 1,
:...skipping...
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Artist",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SongTitle",
                "AttributeType": "S"
            }
        ],
        "TableName": "Music",
        "KeySchema": [
            {
                "AttributeName": "Artist",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SongTitle",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": "2025-04-22T01:43:38.681000+00:00",
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": "1970-01-01T00:00:00+00:00",
            "LastDecreaseDateTime": "1970-01-01T00:00:00+00:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
:
```
then exited with Q

*B: Attempted to Create an Item*

input
```
aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}}' \
    --return-consumed-capacity TOTAL
```
result
```
{
    "ConsumedCapacity": {
        "TableName": "Music",
        "CapacityUnits": 1.0
    }
}
```

*C: list tables*

input
```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```
result
```
{
    "TableNames": [
        "Music"
    ]
}
```

*D: Get Records*

input
```
aws dynamodb scan --table-name Music  --query "Items" --endpoint-url http://localhost:8000
```
result
```
[
    {
        "Artist": {
            "S": "No One You Know"
        },
        "SongTitle": {
            "S": "Call Me Today"
        },
        "AlbumTitle": {
            "S": "Somewhat Famous"
        }
    }
]
```

*E: ProgreSQL directory*

added to my gipod.yml file:
```
	- name: postgres
		init: |
			curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
			echo "deb http://apt.postgresql.org/pub/repos/apt/ 	`lsb_release -cs` -pgdg main" |sudo tee /etc/apt/sources.list.d/pgdg.list
			sudo apt-get update
			sudo apt install -y postgresql-client-13 libpq-dev 
		
```
Got an error message
"
E: Unable to locate package postgresql-client-13
E: Unable to locate package libpg-dev
"
Fix:
1.typo, I had ```sudo apt updated``` when it should have been ```sudo apt update```; fixed it and the error went away
2. typo, I had ```sudo tee /etc/apt/sources.list.d/pgdp.list``` when it was supposed to be sudo tee /etc/apt/sources.list.d/pgdg.list```

All the lines of code for this are now correct, yet I am still seeing these errors:
"
Err:3 http://apt.postgresql.org/pub/repos/apt jammy Release                                                                                    
  404  Not Found
 "
 and
 "
 E: Unable to locate package postgresql-client-13
 "
 
 **The Problem:** Something has changed syntaically and/or PostgreSQL has changed in how you interact with their directory
 
 **The Solution:**
 I just went to PostgreSQL sit to look up how to download the Directory into an Ubuntu Linux server
 https://www.postgresql.org/download/linux/ubuntu/#apt
 
So I changed the code to this:

```
sudo apt install curl ca-certificates
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc
. /etc/os-release
sudo sh -c "echo 'deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $VERSION_CODENAME-pgdg main' > /etc/apt/sources.list.d/pgdg.list"
sudo apt update
sudo apt -y install postgresql
```

Download was successful

*F: Setup the Connection via the PostgreSQL Extension; setup a connection to the Local Postgress Container*


*G: then I accessed PostgreSQL Successfully*
```
psql --host localhost -U postgres
```
and then manually typed in the password
and PostreSQL was accessible

*H: Add my PostgreSQL Explorer to my gitpod YML file*
```
- ric-v.postgres-explorer
```
