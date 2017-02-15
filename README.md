# Scale Take Home Project
## Juliet Liu
Objective: build a simple database-backed Task Queue class that will handle assigning and un-assigning tasks to different Scalers.
Stack: Heroku, Flask, and Postgres

# Installation
## Requirements:
1. Requirements for Heroku
* Set up a free Heroku account.
* Python version 2.7 installed locally 
* Pip installed locally
* Virtualenv installed locally (accomplish this by running `pip install virtualenv`)

# Database Architecture
'Tasks' table schema:
* id SERIAL PRIMARY KEY NOT NULL,
* created_at timestamp,
* complete_by timestamp,
* completed_at timestamp,
* status text,
* urgency varchar (50),
* assigned_to integer

'Queue' table schema:
* task_id integer PRIMARY KEY,
* complete_by timestamp
