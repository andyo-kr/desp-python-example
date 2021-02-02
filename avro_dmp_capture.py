import logging
import os
import string
import json
import avro.schema
from avro.io import DatumReader
from avro.datafile import DataFileReader
from DespKafka.AvroSerde import AvroSerde
from DespKafka.DespEnvironment import DespEnvironment, EnvironmentName
desp_environment: DespEnvironment = DespEnvironment(EnvironmentName.DIG_PROD_CDC)
avro_serde = AvroSerde(desp_environment)

path = 'PATH_TO_FILE'

reader = DataFileReader(open(path, 'rb'), DatumReader())
dict = {}
for reading in reader:
    data = reading["Body"]
    headers = reading["Properties"]
    print(data)
    parsed = avro_serde.decode_message(data)
    print(parsed)


    
    
