import json
import logging
import traceback
from confluent_kafka.cimpl import KafkaError
from kafka.producer.future import RecordMetadata

from DespKafka.DespEnvironment import DespEnvironment, EnvironmentName
from DespKafka.AvroSerde import AvroSerde
from DespKafka.DespProducer import DespProducer
from argparse import ArgumentParser
import os.path

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

parser = ArgumentParser(description="JSON File Producer")
parser.add_argument("--topic", "-t", type=str, required=True, help='Topic to produce to')
parser.add_argument("--env", "-e", type=EnvironmentName, default='test', help='Environment')
parser.add_argument("-i", dest="filename", required=True,
                    help="input file of JSON Event", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

print(args.filename)
logging.basicConfig(level=logging.INFO)
desp_environment: DespEnvironment = DespEnvironment(args.env)
avro_serde = AvroSerde(desp_environment)

test_event = json.load(args.filename)

serialized_value = avro_serde.encode_message(test_event['data'], test_event['subject'])
producer = DespProducer(desp_environment)
future = producer.send(args.topic, value=serialized_value)
try:
    record_metadata: RecordMetadata = future.get(timeout=10)
    print(f"\n** Successfully Published Event. partition={record_metadata.partition} offet={record_metadata.offset} \n")
except KafkaError:
    # Decide what to do if produce request failed...
    logging.log.error(traceback.format_exc())
    result = 'Fail'
finally:
    producer.close()
