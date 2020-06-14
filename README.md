# TODO: add docker file
# PyToolManageServicesYAML
Date: 2020-03-09
Created By: Volodymyr Moskov

# Update from 2020-03-22:
    ##Before:
     The core deps_helper_dic {} which identify what service can be started/ stooped next based
    on composite key was used for start / stop flow

    ##After
     Services it self can manage this logic after adding as entering points for process
        self.start_root: List[str]
        self.stop_root: List[str]

      and was introduced next_to_check: List[str] array as list of services
      pending to check is it can be ready to start/stol after next service will be started

    TODO: It is only left to merge services_start.py and  services_stop.py in one script
          and execute stop/start as argument to define usage of deps and dependants fields
          of Service for building start/stop flow
    TODO: implement class based approach and get rid of 'too much' args in methods

    TODo: fix test as class based

## Python Developer doing devOps/automation tools

*Please see task details in file "task.txt"

# Some assumptions had been made here:

    1. the yaml has reasonable size (can be parsed and stored with basic amount of RAM )

    2. common sense

# Here is solution

### Please see solution for the Task ./src/tool/main.py
Simple python module which doing the job and can be use as stand alon script to
run it from command line ("support two command-line arguments: "start" and "stop"")


## From point of view MVP (Minimum Valuable Product)

1. For simplicity - very simple-basic logging has been added

2. For simplicity - very simple-basic unit tests and integration tests has been implemented


## Project setup steps (Windows only)

 1. download project source code into your local drive

 2. Install latest Python 3.7 if you do not have [https://realpython.com/installing-python/]
    and run cmd console

 3. Install pip  use command
   > python get-pip.py
   or follow step by step [https://www.liquidweb.com/kb/install-pip-windows/]

 4. Install Python virtualenv with command
   > pip install virtualenv

 5. set project folder as you current folder
    > cd   your_local_folder/PyToolManageServicesYAML

 6. Run next command in order to create virtualenv for project
   > virtualenv venv

 7. Activate virtual environment
   > your_local_folder/PyToolManageServicesYAML/venv/Scripts/activate

 8. install project dependencies

   > pip install -r ../../requirements.txt

    and use

    > pip freeze > ../../requirements.txt

    in order to update list of project libraries
    and use

    > pip install <package-name>

    in case you miss some

## How to use it
    from \PyToolManageServicesYAML\src\tool>

    To see help
  > python main.py -h

   Run script to see services starting order
  > python main.py start

    Run script to see services stopping order
   > python main.py start

