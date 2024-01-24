class Signal:
    def __init__(self, name, byte, bit, size, new_value=None):
        self.name = name
        self.byte = byte
        self.bit = bit
        self.size = size
        self.new_value = new_value


class Frame:
    def __init__(self, frame_hex):
        self.frame_hex = frame_hex
        self.frame_bin = self.hex_to_bin(frame_hex)

    @staticmethod
    def hex_to_bin(hex_string):
        binary_string = ""
        hex_bytes = hex_string.split()
        for hex_byte in hex_bytes:
            binary_string += bin(int(hex_byte, 16))[2:].zfill(8)[::-1]
        return binary_string

    @staticmethod
    def bin_to_hex(bin_string):
        return ' '.join(f"{int(bin_string[i:i +8][::-1], 2):02X}" for i in range(0, len(bin_string), 8))

    def extract_signal_value(self, signal):
        start_bit = (signal.byte * 8) + signal.bit
        signal_bits = self.frame_bin[start_bit:start_bit + signal.size]
        return int(signal_bits, 2)

    def modify_signal_value(self, signal, new_value):
        start_bit = (signal.byte * 8) + signal.bit
        end_bit = start_bit + signal.size
        new_value_bin = f"{new_value:0{signal.size}b}"
        self.frame_bin = self.frame_bin[:start_bit] + new_value_bin + self.frame_bin[end_bit:]


class Decoder:
    def __init__(self, signals):
        self.signals = {sig['name']: Signal(**sig) for sig in signals}

    def decode_and_modify_frame(self, frame_hex, modifications):
        frame = Frame(frame_hex)
        original_values = {signal.name: frame.extract_signal_value(signal) for signal in self.signals.values() }
        for mod in modifications:
            signal = self.signals.get(mod['name'])
            if signal:
                frame.modify_signal_value(signal, mod['new_value'])
        modified_frame_hex = frame.bin_to_hex(frame.frame_bin)
        return original_values, modified_frame_hex


# Frame 1 & 4 for LDW_AlertStatus CPO
hex_frame1 = "80 00 00 00 00 00 00 00"
hex_frame4 = "40 00 00 10 00 00 00 00"

# Frame 2 & 5 for DW_FollowUpTimeDisplay CPO
hex_frame2 = "FF 60 00 00 02 00 00 00"
hex_frame5 = "21 20 00 00 02 00 00 00"

# Frame 3 & 6 for LCA_OverrideDisplay CPO
hex_frame3 = "80 00 00 00 00 00 00 00"
hex_frame6 = "80 00 00 00 00 00 00 00"

signals_info = [
    {'name': 'LDW_AlertStatus', 'byte': 2, 'bit': 5, 'size': 2},
    {'name': 'LCA_OverrideDisplay', 'byte': 5, 'bit': 2, 'size': 1},
    {'name': 'DW_FollowUpTimeDisplay', 'byte': 4, 'bit': 7, 'size': 6}
]

decoder = Decoder(signals_info)

modifications = {
    'LDW_AlertStatus': 2,
    'LCA_OverrideDisplay': 1,
    'DW_FollowUpTimeDisplay': 45
}

frame = [hex_frame1, hex_frame2, hex_frame3, hex_frame4, hex_frame5, hex_frame6]

for frame in frame:
    frame_modifications = [{'name': key, 'new_value': value} for key, value in modifications.items()]
    original_value, modified_frame = decoder.decode_and_modify_frame(frame, frame_modifications)

    print(f"Original Frame: {frame}")
    print(f"Original Values: {original_value}")
    print(f"Modified Frame: {modified_frame}\n")