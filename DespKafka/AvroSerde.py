from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
from avro.io import DatumReader, BinaryDecoder, BinaryEncoder, DatumWriter
from DespKafka.DespEnvironment import DespEnvironment
import io
import struct


class AvroSerde:

    def __init__(self, desp_environment: DespEnvironment):
        self.schema_registry = CachedSchemaRegistryClient(desp_environment.current_environment.scheme_registry)
        self.reader_map: dict = dict()
        self.writer_map: dict = dict()

    def get_writer(self, subject):
        if subject not in self.reader_map:
            # schema = self.schema_registry.get_by_id(schema_id)
            (schema_id, schema, version) = self.schema_registry.get_latest_schema(subject)
            self.writer_map[subject] = (DatumWriter(schema), schema_id)
        return self.writer_map.get(subject)

    def get_reader(self, schema_id):
        if schema_id not in self.reader_map:
            schema = self.schema_registry.get_by_id(schema_id)
            if schema is None:
                return None
            self.reader_map[schema_id] = DatumReader(schema)
        return self.reader_map.get(schema_id)

    def get_schema_id(self, payload):
        raw_bytes = payload[5:] + bytes([0x00])
        magic, schema_id = struct.unpack('>bI', payload[0:5])
        return schema_id

    def decode_message(self, payload):
        raw_bytes = payload[5:] + bytes([0x00])
        magic, schema_id = struct.unpack('>bI', payload[0:5])
        message_bytes = io.BytesIO(raw_bytes)
        decoder = BinaryDecoder(message_bytes)
        reader = self.get_reader(schema_id)
        if reader is None:
            return payload
        event_dict = reader.read(decoder)
        return event_dict

    def encode_message(self, msg_dict, subject):
        """ Encode message using Avro Schema from schema_registry
        """
        # b'\x00\x00\x00\x00\x01Hb0a15896-3352-4cec-a11a-2fc893c26b7f\xe4\xbc\xe1\xae\xaf\\\x18health-check\x1chealth-checker\x16cdc-dig-pcf\x10cdc-test\x02\x08v2.1'
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        (writer, schema_id) = self.get_writer(subject)
        print(schema_id)
        writer.write(msg_dict, encoder)
        payload = bytes_writer.getvalue()
        wrapped_message = struct.pack('>bI', 0, schema_id) + payload
        return wrapped_message
