from kafka import KafkaConsumer

from DespEnvironment import DespEnvironment


class DespConsumer(KafkaConsumer):

    def __init__(self, topic, username, password, desp_environment: DespEnvironment):
        KafkaConsumer.__init__(self, topic,
                               bootstrap_servers=desp_environment.current_environment.broker_list,
                               security_protocol="SASL_SSL",
                               ssl_check_hostname=False,
                               ssl_cafile='etc/ca.pem',
                               sasl_mechanism='PLAIN',
                               sasl_plain_username=username,
                               sasl_plain_password=password)
