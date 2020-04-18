import logging
from AvroSerde import AvroSerde
from DespConsumer import DespConsumer
from DespEnvironment import DespEnvironment
logging.basicConfig(level=logging.INFO)
desp_environment: DespEnvironment = DespEnvironment()
avro_serde = AvroSerde(desp_environment)

try:
    consumer = DespConsumer("healthcheck", "user", "password", desp_environment)
    for msg in consumer:
        print(avro_serde.decode_message(msg.value))

except Exception as e:
    print(e)
