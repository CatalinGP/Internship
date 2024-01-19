
def hex_payload_to_bin(payload_hex):
    binary_string = ""
    hex_bytes = payload_hex.split()
    for hex_byte in hex_bytes:
        decimal_value = int(hex_byte, 16)
        binary_string += bin(decimal_value)[2:].zfill(8)
    return binary_string


def extract_signal_value(payload_bin, byte_pos, bit_pos, size):
    start_bit = (byte_pos * 8) + bit_pos
    signal_bits = payload_bin[start_bit:start_bit + size]
    return int(signal_bits, 2)


def decode_payloads(payload, signals):
    decoded_payloads = []
    for payload_hex in payload:
        payload_bin = hex_payload_to_bin(payload_hex)
        signal_values = {}
        for signal, details in signals.items():
            signal_values[signal] = extract_signal_value(
                payload_bin, details['byte'], details['bit'], details['size']
            )
        decoded_payloads.append(signal_values)
    return decoded_payloads


signals_info = {
    'PassengerSeatMemoRequest': {'byte': 0, 'bit': 7, 'size': 1},
    'ClimFPrightBlowingRequest': {'byte': 5, 'bit': 5, 'size': 3},
    'TimeFormatDisplay': {'byte': 5, 'bit': 3, 'size': 2},
}

payloads = [
    "60 20 45 6C FE 3D 4B AA",
    "40 12 6C AF 05 78 4A 04"
]

decoded_values = decode_payloads(payloads, signals_info)
for d in decoded_values:
    print(d)
