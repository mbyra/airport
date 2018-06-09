$ Important notes:
$$ 1. INSTALATION:
	```shell
	$ python3 -m venv /path/<env_name>
	$ source /path/<env_name>/bin/activate
	(<env_name>)$ git clone https://github.com/mbyra/airport
	(<env_name>)$ cd airport
	(<env_name>)$ pip install -r requirements.txt
    ```

$$ 2. GENERATING/RESTORING TO INITIAL STATE OF DATABASE:
	```shell
	(<env_name>)$ bash ./restore_and_generate_data.sh
	(this will create data as well make initial migrations and create superuser)
    ```
$$ 3. TESTING:
	geckodriver is extracted in project, but you must point to it in system path: 
	```shell
	(<env_name>)$ PATH=$PATH:/path/to/directory/containing/geckodriver
    ```
$$ 4. IF SOMETHING DOESN'T WORK:
	Then try this:
	```shell
	(<env_name>)$ export PYTHONPATH=$PYTHONPATH:$PWD
	(<env_name>)$ export DJANGO_SETTINGS_MODULE=zadanie1.settings
	```