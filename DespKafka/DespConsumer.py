from kafka import KafkaConsumer

from DespKafka.DespEnvironment import DespEnvironment
from DespKafka.DespSecrets import DespSecrets, Secret

secrets: DespSecrets = DespSecrets()


class DespConsumer(KafkaConsumer):

    def __init__(self, topic, desp_environment: DespEnvironment,
                 secret_name='default', **kw):
        secret: Secret = secrets.get_secret(secret_name)
        super().__init__(topic,
                         bootstrap_servers=desp_environment.current_environment.broker_list,
                         security_protocol="SASL_SSL",
                         ssl_check_hostname=False,
                         ssl_cafile='etc/ca.pem',
                         sasl_mechanism='PLAIN',
                         sasl_plain_username=secret.user,
                         sasl_plain_password=secret.password,
                         **kw)
