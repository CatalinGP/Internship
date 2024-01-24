class Signal:
    def __init__(self, name, byte, bit, size, new_value=None):
        self.name = name
        self.byte = byte
        self.bit = bit
        self.size = size
        self.new_value = new_value


class Frame:
    def __init__(self, frame_hex, lsb_first=True):
        self.frame_hex = frame_hex
        self.lsb_first = lsb_first
        self.frame_bin = self.hex_to_bin(frame_hex, lsb_first)

    def hex_to_bin(self, hex_string, lsb_first):
        binary_string = ""
        hex_bytes = hex_string.split()
        for hex_byte in hex_bytes:
            bits = bin(int(hex_byte, 16))[2:].zfill(8)
            if not lsb_first:
                bits = bits[::-1]
            binary_string += bits
        return binary_string

    def bin_to_hex(self):
        hex_payload = ""
        for i in range(0, len(self.frame_bin), 8):
            byte = self.frame_bin[i:i+8]
            if not self.lsb_first:
                byte = byte[::-1]
            hex_payload += f"{int(byte, 2):02X} "
        return hex_payload.strip()

    def extract_signal_value(self, signal):
        start_bit = signal.byte * 8 + signal.bit
        signal_bits = self.frame_bin[start_bit:start_bit + signal.size]
        return int(signal_bits[::-1] if self.lsb_first else signal_bits, 2)

    def modify_signal_value(self, signal):
        start_bit = signal.byte * 8 + signal.bit
        end_bit = start_bit + signal.size
        new_value_bin = bin(signal.new_value)[2:].zfill(signal.size)
        new_value_bin = new_value_bin[::-1] if self.lsb_first else new_value_bin
        self.frame_bin = self.frame_bin[:start_bit] + new_value_bin + self.frame_bin[end_bit:]


class Decoder:
    def __init__(self, signals, lsb_first=True):
        self.signals = {sig['name']: Signal(**sig) for sig in signals}
        self.lsb_first = lsb_first

    def decode_and_modify_frame(self, frame_hex):
        frame = Frame(frame_hex, self.lsb_first)
        original_values = {}
        for name, signal in self.signals.items():
            original_values[name] = frame.extract_signal_value(signal)
            if signal.new_value is not None:
                frame.modify_signal_value(signal)
        modified_frame_hex = frame.bin_to_hex()
        return original_values, modified_frame_hex


signals_info = [
    {'name': 'LDW_AlertStatus', 'byte': 2, 'bit': 5, 'size': 2, 'new_value': 2},
    {'name': 'LCA_OverrideDisplay', 'byte': 5, 'bit': 2, 'size': 1, 'new_value': 1},
    {'name': 'DW_FollowUpTimeDisplay', 'byte': 4, 'bit': 7, 'size': 6, 'new_value': 45}
]

frames = [
    "80 00 00 00 00 00 00 00",
    "40 00 00 10 00 00 00 00",
    "FF 60 00 00 02 00 00 00",
    "21 20 00 00 02 00 00 00",
    "80 00 00 00 00 00 00 00",
    "80 00 00 00 00 00 00 00"
]

"""
    Info :
    Un sistem big-endian stochează octetul cel mai semnificativ al unui cuvânt la cea mai mică adresă de memorie și 
    octetul cel mai puțin semnificativ la cea mai mare. Un sistem little-endian, în schimb, 
    stochează octetul cel mai puțin semnificativ la cea mai mică adresă.
"""

# Seteaza lsb_first False daca bit 7 este LSB
decoder = Decoder(signals_info, lsb_first=True)

for frame_hex in frames:
    original_value, modified_frame = decoder.decode_and_modify_frame(frame_hex)

    print(f"Original Values: {original_value}")
    print(f"Modified Frame: {modified_frame}\n")
