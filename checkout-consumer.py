import logging
from collections import defaultdict
from datetime import datetime
from kafka.consumer.fetcher import ConsumerRecord
from DespKafka.DespConsumer import DespConsumer
from DespKafka.DespEnvironment import DespEnvironment, EnvironmentName
from DespKafka.AvroSerde import AvroSerde

logging.basicConfig(level=logging.INFO)
desp_environment: DespEnvironment = DespEnvironment(EnvironmentName.DIG_PROD_CDC)
avro_serde = AvroSerde(desp_environment)

cnt = 0
counts_dict = defaultdict(int)


def print_cnts():
    print()
    for key in sorted(counts_dict.keys()):
        print(key, counts_dict[key])


try:
    consumer = DespConsumer("kcp_checkout", desp_environment, group_id='my-kcp', secret_name='prod')
    consumer.poll()
    consumer.seek_to_beginning()
    msg: ConsumerRecord
    for msg in consumer:
        ts = int(msg.timestamp / 1000)
        cnt = cnt + 1
        if cnt % 100 == 0:
            print_cnts()
        print(avro_serde.decode_message(msg.value))

except Exception as e:
    print(e)
