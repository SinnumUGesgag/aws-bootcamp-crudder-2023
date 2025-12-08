# Week 4 — Postgres and RDS
# Week 5 — DynamoDB and Serverless Caching

I had to work through a lot of problems especially with Dyanmo DB, Lambda , & Cognito Tokens to get everything to work; While working through the project my notes were in a file that somehow corrupted and I lost a lot of my notes, so I'll be summarizing a lot of what I did; I had to read through a lot of posts and the AWS Documentation to get a better understanding of either why I did not understand how the Service was meant to be interacted with, or how a supporting service had changed (i.e. Psycopg), etc. I learned a lot.

In short, I followed along with Andrew through out all the Videos for Weeks 4 & 5, however I did encounter some problems and found my own solutions for the following issues:

Week 4
1. Problems with Lambda Layer
There are Public Repos that are being utilized in Andrew's tutorial for Lamda support for creating Lambda Layers to support Psycopg for Lambda; the Repo they relied on literally stopped providing support within less than a year after his video was posted, so I just had to take the time to figure out setup my own Lambda Layer; additionally, Psycopg has gone through some changes and the Python 3.9 support in Lambda was ending; I elected to go with setting up commpletely a Psycopg setup instead of just the older Psycogp 2, for Python 3.13 (which required some updates but not much)

For Building My own Lambda Layer for Psycopg for Python 3.13, I largely followed the instruciton I found outline in 2 sources:
A Solutions using MAC Terminal: https://towardsaws.com/how-to-fix-psycopg2-modulenotfounderror-using-aws-lambda-layer-f94fadb26d22
Python Instructions for "Install packages in a virtual environment using pip and venv" :
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/


2. Probelms with Cognito Tokens
I found an article the lays out exactly what Andrew was attempting to do in his tutorials on Cognito JWT Tokens:
https://binli.hashnode.dev/verify-cognito-jwt-in-a-flask-application
I found that my Frontend was not pulling the JWT out of Local Storage and using it in the Authorization header for my outgoing HTTP messages
Thus, my responses where not showing any Authorization Headers when the Backend goes to pull the the Authorization Header for Verifying if a Live Token is valid or not

I updated all "res" contants for all Pages to the following:
'''
const res = await fetch(backend_url, {
			headers: {
				Authorization: `Bearer ${localStorage.getItem("access_token")}`
			},
        method: "GET"
      });
'''


Week 5
1. Creating New Message Groups & Updating Exsisting Message Groups Kept Failing

I followed along and noticed that either when I created a New Message the Message Group wouldn't be updated with the correct message for it's lastest message, or that when creating a new Message Group to another User I could not see the Message Groups actually create; I eventually realized that Andrew has the Frontend providing the Backend with either the Receiver's Handle (when messaging a User for the 1st time, so no pre-exsisting Message Groups) or the Message Group UUID; this create problems where:

Aside from having to queiry your SQL Db for some informaiton, If you are messaging a User where you have an Exsisting Message Group you'll have all your information and information about the Group YET you'll never have the Receiver's informaiton; yet, if you are messaging a User you do not have an exsisting Message Group with, you technically will have all the information you need.

To remedy this I simply made a few changes to the Frontend & how Messages are created:
a. I now have it so that either you'll get BOTH the Message Group UUID & the Receiver's Handle, or you'll only get the Receiver's Handle; since you already have access to your information, then gaurnette's that you'll never need to do additional queries on the DyanmoDB to get anything on the Receiver, you'll always be able to pull what you need from the SQL DB to Create Messages & Create/Update Message Groups

b. I updated a Message Record to also carry the "other_user_handle" so a message always is pointing to You via "user_uuid", to the Reciever via "other_user_handle", and to the Group via "pk"; and since Groups already have the Message UUID, Other User UUID, & Your User UUID backed into them, this insures that any Message or Message Group points to all necessary information needed to further pull additional Messages, Groups, Users Info, etc, without the need to do addiitonal Reads on the DyanmoDB (which furthers one of the original pillars for this project: Build it CHEAP)

2. Gitpod was replaced with ONA, which I did not care for so I switch to Codespaces and had to make some changes but nothing major to the Cruddur Application itself

3. Additionally, since in the tutorials we originally build a DynamoDB locally then switch to the AWS Cloud, I created a DyDb Setup script for local and for setting up the cloud DB with the Schema & Seed Data
