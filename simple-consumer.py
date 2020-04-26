import logging
from collections import defaultdict
from datetime import datetime
from kafka.consumer.fetcher import ConsumerRecord
from DespKafka.DespConsumer import DespConsumer
from DespKafka.DespEnvironment import DespEnvironment
from DespKafka.AvroSerde import AvroSerde

logging.basicConfig(level=logging.INFO)
desp_environment: DespEnvironment = DespEnvironment()
avro_serde = AvroSerde(desp_environment)

cnt = 0
counts_dict = defaultdict(int)


def print_cnts():
    print()
    for key in sorted(counts_dict.keys()):
        print(key, counts_dict[key])


try:
    consumer = DespConsumer("sandbox", desp_environment, group_id='grp_1')
    consumer.poll()
    consumer.seek_to_beginning()
    msg: ConsumerRecord
    for msg in consumer:
        # print(msg.value)
        ts = int(msg.timestamp / 1000)
        key = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        counts_dict[key] = counts_dict[key] + 1
        cnt = cnt + 1
        if cnt % 10000 == 0:
            print_cnts()
        print(avro_serde.decode_message(msg.value))

except Exception as e:
    print(e)
