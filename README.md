# Scale Take Home Project
## Juliet Liu
Objective: build a simple database-backed Task Queue class that will handle assigning and un-assigning tasks to different Scalers.

Stack: Heroku, Flask, and Postgres

# Installation
1. Requirements for Heroku
  1. Set up a free Heroku account.
  2. Python version 2.7 installed locally 
  3. Pip installed locally
  4. Virtualenv installed locally (accomplish this by running `pip install virtualenv`)
  5. Follow the setup [instructions here](https://devcenter.heroku.com/articles/getting-started-with-python#set-up), don't follow through with the subsequent steps on that page.
2. Git clone this repo (`git clone git@github.com:liujuliet/scale_take_home.git`)
3. Test that heroku commands work by running `heroku info`
  * I've added *alex@scaleapi.com* as a collaborator on the heroku app, let me know if your heroku login email is different.
  
# Running the tests
Type this into the command line, where you've checked out this repo: `heroku run python MainTestCase.py`

## Notes
### Additional field
I've added an attribute for tasks called `complete_by` to order the tasks in the queue. `complete_by` for an 'immediate' task is 1 hour after the task was created, etc. 

### Other test cases I would've implemented:
* checking that `create_task` created a task with the expected complete_by date given it's urgency
* check that `receive_tasks` retrieves highest priority tasks

# Helpful to know
## Database Architecture
`tasks` table schema:
* id SERIAL PRIMARY KEY NOT NULL,
* created_at timestamp,
* complete_by timestamp,
* completed_at timestamp,
* status text,
* urgency text,
* assigned_to integer

`queue` table schema:
* task_id integer PRIMARY KEY,
* complete_by timestamp
