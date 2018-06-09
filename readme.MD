## Info
This is a project for WWW Applications course I attended in 2018 at the Department of Mathematics, Informatics and Mechanics of the University of Warsaw.

## Description
Soon.

## Important notes:
### 1. Installation:
	$ python3 -m venv /path/<env_name>
	$ source /path/<env_name>/bin/activate
	(<env_name>)$ git clone https://github.com/mbyra/airport
	(<env_name>)$ cd airport
	(<env_name>)$ pip install -r requirements.txt

### 2. Generating/restoring to initial state of database:
	(<env_name>)$ bash ./restore_and_generate_data.sh
	(this will create data as well make initial migrations and create superuser)
### 3. Testing:
	geckodriver is extracted in project, but you must point to it in system path: 
	(<env_name>)$ PATH=$PATH:/path/to/directory/containing/geckodriver
### 4. If something goes wrong:
	Then try this:
	(<env_name>)$ export PYTHONPATH=$PYTHONPATH:$PWD
	(<env_name>)$ export DJANGO_SETTINGS_MODULE=zadanie1.settings
