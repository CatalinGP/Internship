class Signal:
    def __init__(self, name, byte, bit, size):
        self.name = name
        self.byte = byte
        self.bit = bit
        self.size = size


class Frame:
    def __init__(self, frame_hex, lsb_first=True):
        self.frame_bin = self.hex_to_bin(frame_hex, lsb_first)

    @staticmethod
    def hex_to_bin(hex_string, lsb_first):
        binary_string = ""
        hex_bytes = hex_string.split()
        for hex_byte in hex_bytes:
            bits = bin(int(hex_byte, 16))[2:].zfill(8)
            if not lsb_first:
                bits = bits[::-1]
            binary_string += bits
        return binary_string

    def extract_signal_value(self, signal):
        start_bit = (signal.byte * 8) + (7 - signal.bit if signal.bit is not None else 0)
        signal_bits = self.frame_bin[start_bit:start_bit + signal.size]
        return int(signal_bits, 2)


class Decoder:
    def __init__(self, signals, lsb_first=True):
        self.signals = [Signal(**sig) for sig in signals]
        self.lsb_first = lsb_first

    def decode_payloads(self, payloads):
        decoded_payloads = []
        for payload_hex in payloads:
            frame = Frame(payload_hex, self.lsb_first)
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

"""
    Info :
    Un sistem big-endian stochează octetul cel mai semnificativ al unui cuvânt la cea mai mică adresă de memorie și 
    octetul cel mai puțin semnificativ la cea mai mare. Un sistem little-endian, în schimb, 
    stochează octetul cel mai puțin semnificativ la cea mai mică adresă.
"""

# Seteaza lsb_first False daca bit 7 este LSB
decoder = Decoder(signals_info, lsb_first=True)
decoded_values = decoder.decode_payloads(payloads)
for d in decoded_values:
    print(d)
