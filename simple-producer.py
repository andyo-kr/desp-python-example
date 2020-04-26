import json
import logging
import traceback
from confluent_kafka.cimpl import KafkaError
from DespKafka.DespEnvironment import DespEnvironment
from DespKafka.AvroSerde import AvroSerde
from DespKafka.DespProducer import DespProducer
logging.basicConfig(level=logging.INFO)
desp_environment: DespEnvironment = DespEnvironment()
avro_serde = AvroSerde(desp_environment)

with open('data/heartbeat.json') as json_file:
    test_event = json.load(json_file)

serialized_value = avro_serde.encode_message(test_event['data'], test_event['subject'])
producer = DespProducer(desp_environment)
future = producer.send("sandbox", value=serialized_value)
try:
    record_metadata = future.get(timeout=10)
    print(record_metadata)
except KafkaError:
    # Decide what to do if produce request failed...
    logging.log.error(traceback.format_exc())
    result = 'Fail'
finally:
    producer.close()
