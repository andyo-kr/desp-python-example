## Simple Python based DESP Consumer and Producer
* Handles DESP specific configurations (SSL + SASL)
* Integrates DESP Schema Registry to Deserialize avro serialized messages
* Uses the [kafka-python](https://kafka-python.readthedocs.io/en/master/) package
* Uses the [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python) primarily for schema registry integration
* Simple consumer in 15-lines of python code!

### Setting up your local environment for this project
Getting the environment set up for this is a bit tricky.  We recommend
following [this guide](https://github.com/krogertechnology/desp-developer-onboarding-kit#setting-up-your-python-development-environment-in-desp)
installing python, virtual environments, and project packages.  IMPORTANT NOTE: For step 6, as you set up your
virtual environment, make sure you select python version 3.8, since 
some packages in this project depend on it.  

One the environment is set up, run any commands from the terminal lauched
from the IDE as it will have the virtual environment automatically activated.

### Steps to running your consumer
* rename 'secrets/rename_me.json' to 'secrets.json', and update with your secrets
* use you topic, user, password in simple-consumer.py
* run the program
```shell script
> python3 simple-consumer.py
```

## Using the py-desp docker image
If you don't want to install the pydesp environment, you
can run your python scripts in a dockerized python environment.
The docker run command is wrapped up in a shell script.
An example call looks like this:
```shell script
> ./py-desp.sh produce_from_json.py -t sandbox -i test-data/INT390.json  
```
