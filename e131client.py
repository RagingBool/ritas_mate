import base64
import struct
import uuid
import socket
import time


DEFAULT_BASE_IP = "239.255.0.0"
DEFAULT_PORT = 5568


class E1_31DmxMultiverse(object):
    def __init__(self, universe_ids, component_identifier, source_name, base_ip=DEFAULT_BASE_IP, port=DEFAULT_PORT):
        self._universes = dict()

        for universe_id in universe_ids:
            self._universes[universe_id] = E1_31DmxUniverse(universe_id, component_identifier, source_name)

    def __getitem__(self, universe_id):
        return self._universes[universe_id]


class E1_31DmxUniverse(object):
    def __init__(self, universe_id, component_identifier, source_name, base_ip=DEFAULT_BASE_IP, port=DEFAULT_PORT):
        self._universe_id = universe_id;
        self._component_identifier = component_identifier;
        self._source_name = source_name;

        self._connection = E1_31MulticastConncetion(universe_id, base_ip, port);

    def send_frame(self, values):
        packet = construct_packet(self._component_identifier, self._source_name, self._universe_id, values)
        self._connection.send(packet)


class E1_31MulticastConncetion(object):
    def __init__(self, universe_id, base_ip=DEFAULT_BASE_IP, port=DEFAULT_PORT):
        self._dest = (self._generate_ip(base_ip, universe_id), port)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def _generate_ip(self, base_ip, universe_id):
        parts = list(base_ip.split("."))

        parts[2] = "%d" % ((universe_id >> 8) & 0xFF)
        parts[3] = "%d" % (universe_id & 0xFF)

        return ".".join(parts)

    def send(self, data):
        self._socket.sendto(data, self._dest)


test_packet = "ABAAAEFTQy1FMS4xNwAAAHBzAAAABB+gbZO9mp1NgMcCr4XIIqhwXQAAAAJ0ZXN0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZAAAAAAAA3AQAqEAAAABAAYAChQeKDI="

def to_bin(data):
    return "".join([chr(int(x)) for x in data])

DEFAULT_PRIORITY = 100

PROPERTY_VALUE_LENGTH_OVERHEAD = 1
DMP_LAYER_LENGTH_OVERHEAD = PROPERTY_VALUE_LENGTH_OVERHEAD + 10
E1_31_FRAMING_LAYER_LENGTH_OVERHEAD = DMP_LAYER_LENGTH_OVERHEAD + 77
ROOT_LAYER_LENGTH_OVERHEAD = E1_31_FRAMING_LAYER_LENGTH_OVERHEAD + 22

ROOT_LAYER_PREFIX = to_bin([
    0x00, 0x10, # Preamble Size
    0x00, 0x00, # Post-amble Size
    0x41, 0x53, 0x43, 0x2D, 0x45, 0x31, 0x2E, 0x31, 0x37, 0x00, 0x00, 0x00, # ACN Packet Identifier
])

ROOT_LAYER_VECTOR = to_bin([0x00, 0x00, 0x00, 0x04])

E1_31_FRAMING_LAYER_VECTOR = to_bin([0x00, 0x00, 0x00, 0x02])

DMP_LAYER_FIELDS = to_bin([
    0x02,       # Vector
    0xA1,       # Address Type & Data Type
    0x00, 0x00, # First Property Address
    0x00, 0x01  # Address Increment
])


def construct_packet(component_identifier, source_name, universe_id, propeties):
    parts = []

    properties_length = len(propeties)
    write_root_layer_header(parts, properties_length, component_identifier)
    write_e1_31_framing_layer_header(parts, properties_length, source_name, universe_id)
    write_dmp_layer_header(parts, properties_length)
    write_properties(parts, propeties)

    return "".join(parts)


def write_root_layer_header(parts, propeties_length, component_identifier):
    parts.append(ROOT_LAYER_PREFIX)

    # Flags and Length
    write_flags_and_length(parts, propeties_length + ROOT_LAYER_LENGTH_OVERHEAD)

    # Vector
    parts.append(ROOT_LAYER_VECTOR)

    # CID (Component Identifier)
    parts.append(component_identifier.bytes)


def write_e1_31_framing_layer_header(parts, properties_length, source_name, universe_id):
    # Flags and Length
    write_flags_and_length(parts, properties_length + E1_31_FRAMING_LAYER_LENGTH_OVERHEAD)

    # Vector
    parts.append(E1_31_FRAMING_LAYER_VECTOR)

    # Source Name
    parts.append(source_name.ljust(64, '\x00'))

    # Priority
    parts.append(chr(DEFAULT_PRIORITY))

    # Reserved
    parts.append("\x00\x00")

    # Sequence Number
    parts.append("\x00") # TODO: Understand this better

    # Options
    parts.append("\x00") # Preview_Data = FALSE; Stream_Terminated = FALSE

    # Universe
    parts.append(struct.pack(">H", universe_id))


def write_dmp_layer_header(parts, properties_length):
    # Flags and Length
    write_flags_and_length(parts, properties_length + DMP_LAYER_LENGTH_OVERHEAD)

    # Vector; Address Type & Data Type; First Property Address; Address Increment
    parts.append(DMP_LAYER_FIELDS)

    # Property value count
    parts.append(struct.pack(">H", properties_length + PROPERTY_VALUE_LENGTH_OVERHEAD))


def write_properties(parts, properties):
    # DMX512-A START Code
    parts.append("\x00") # TODO: Understand this better

    # Data
    parts.append(to_bin(properties))


def write_flags_and_length(parts, length):
    parts.append(struct.pack(">H", 0x7000 | length))


def main():
    universe_id = 3
    component_identifier = uuid.UUID("936DA01F-9ABD-4d9d-80C7-02AF85C822A8")
    source_name = "test"

    dmx = E1_31DmxMultiverse([universe_id], component_identifier, source_name)

    fr = 31
    to = fr + 6
    for i in xrange(10000):
        frame = [0] * 512
        frame[fr + (i % (to - fr))] = 255

        dmx[universe_id].send_frame(frame)
        print frame

        time.sleep(0.5)


    #packet = construct_packet(component_identifier, source_name, universe_id, [10, 20, 30, 40, 50])
    #expected = base64.b64decode(test_packet)

    #print repr(packet[38+64:])
    #print repr(expected[38+64:])


main()