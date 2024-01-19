def hex_payload_to_bin(payload_hex):
    return ''.join(f"{int(byte, 16):08b}" for byte in payload_hex.split())


def bin_payload_to_hex(payload_bin):
    return ' '.join(f"{int(payload_bin[i:i + 8], 2):02X}" for i in range(0, len(payload_bin), 8))


def modify_signal_value(payload_bin, byte_pos, bit_pos, size, new_value):
    start_bit = (byte_pos * 8) + bit_pos
    end_bit = start_bit + size
    new_value_bin = f"{new_value:0{size}b}"
    return payload_bin[:start_bit] + new_value_bin + payload_bin[end_bit:]


def decode_and_modify_frame(frame_hex, signal_info):
    frame_bin = hex_payload_to_bin(frame_hex)
    original_values = {}
    for signal, details in signal_info.items():
        byte_pos = details['byte']
        bit_pos = details['bit']
        size = details['size']
        start_bit = (byte_pos * 8) + bit_pos
        original_value_bin = frame_bin[start_bit:start_bit + size]
        original_values[signal] = int(original_value_bin, 2)

    modified_frame_bin = frame_bin
    for signal, details in signal_info.items():
        new_value = details['new_value']
        byte_pos = details['byte']
        bit_pos = details['bit']
        size = details['size']
        modified_frame_bin = modify_signal_value(modified_frame_bin, byte_pos, bit_pos, size, new_value)

    modified_frame_hex = bin_payload_to_hex(modified_frame_bin)
    return original_values, modified_frame_hex


hex_frame = ("00 06 02 08 80 00 00 00 00 00 00 00 00 05 D0 08 FF 60 00 00 02 00 00 00 "
             "00 06 01 08 80 00 00 00 00 00 00 00 00 00 10 C7 77 8A 70 AB AF 88 2A 8C")

signals_info = {
    'LDW_AlertStatus': {'byte': 2, 'bit': 0, 'size': 2, 'new_value': 2},
    'DW_FollowUpTimeDisplay': {'byte': 18, 'bit': 0, 'size': 16, 'new_value': 45},
    'LCA_OverrideDisplay': {'byte': 36, 'bit': 0, 'size': 3, 'new_value': 1},
}

original_value, modified_frame = decode_and_modify_frame(hex_frame, signals_info)

print(f"Original Values: {original_value}")
print(f"Original Frame: {hex_frame}")
print(f"Modified Frame: {modified_frame}")
