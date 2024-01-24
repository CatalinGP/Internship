class Signal:
    def __init__(self, name, byte, bit, size):
        self.name = name
        self.byte = byte
        self.bit = bit
        self.size = size


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

    def extract_signal_value(self, signal):
        start_bit = (signal.byte * 8) + signal.bit
        signal_bits = self.frame_bin[start_bit:start_bit + signal.size]
        return int(signal_bits, 2)


class Decoder:
    def __init__(self, signals):
        self.signals = [Signal(**sig) for sig in signals]

    def decode_payloads(self, payloads):
        decoded_payloads = []
        for payload_hex in payloads:
            frame = Frame(payload_hex)
            signal_values = {signal.name: frame.extract_signal_value(signal) for signal in self.signals}
            decoded_payloads.append(signal_values)
            return decoded_payloads


signals_info = [
    {'name': 'PassengerSeatMemoRequest', 'byte': 0, 'bit': 7, 'size': 3},
    {'name': 'ClimFPrightBlowingRequest', 'byte': 5, 'bit': 7, 'size': 4},
    {'name': 'TimeFormatDisplay', 'byte': 5, 'bit': 3, 'size': 1},

]

payloads = [
    "60 20 45 6C FE 3D 4B AA",
    "40 12 6C AF 05 78 4A 04"
]

decoder = Decoder(signals_info)
decoded_values = decoder.decode_payloads(payloads)
for d in decoded_values:
    print(d)
