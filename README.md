## Simple Python based DESP Consumer and Producer
* Handles DESP specific configurations (SSL + SASL)
* Integrates DESP Schema Registry to Deserialize avro serialized messages
* Uses the [kafka-python](https://kafka-python.readthedocs.io/en/master/) package
* Uses the [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python) primarily for schema registry integration
* Simple consumer in 15-lines of python code!

### Steps to running your consumer
* set up a python 3 environment
* install requirements
```shell script
> pip3 install -r requirements.txt
```
* rename 'secrets/rename_me.json' to 'secrets.json', and update with your secrets
* use you topic, user, password in simple-consumer.py
* run the program
```shell script
> python3 simple-consumer.py
```

