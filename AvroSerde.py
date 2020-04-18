from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
from avro.io import DatumReader, BinaryDecoder
from DespEnvironment import DespEnvironment
import io
import struct


class AvroSerde:

    def __init__(self, desp_environment: DespEnvironment):
        self.schema_registry = CachedSchemaRegistryClient(desp_environment.current_environment.scheme_registry)
        self.reader_map: dict = dict()

    def get_reader(self, schema_id):
        if schema_id not in self.reader_map:
            schema = self.schema_registry.get_by_id(schema_id)
            self.reader_map[schema_id] = DatumReader(schema)
        return self.reader_map.get(schema_id)

    def decode_message(self, payload):
        raw_bytes = payload[5:] + bytes([0x00])
        magic, schema_id = struct.unpack('>bI', payload[0:5])
        message_bytes = io.BytesIO(raw_bytes)
        decoder = BinaryDecoder(message_bytes)
        reader = self.get_reader(schema_id)
        event_dict = reader.read(decoder)
        return event_dict

    # def encode_message(self, msg_dict):
    #     """Encode message using Avro Schema from schema_registry
    #     """
    #     bytes_writer = io.BytesIO()
    #     encoder = BinaryEncoder(bytes_writer)
    #     self.writer.write(msg_dict, encoder)
    #     return bytes_writer.getvalue()