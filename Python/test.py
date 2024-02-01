
def hex_to_binary(hex_payload):
    binary_payload = bin(int(hex_payload.replace(" ", ""), 16))[2:]
    return binary_payload.zfill(8 * ((len(binary_payload) + 7) // 8))

def binary_to_hex(binary_payload):
    hex_payload = hex(int(binary_payload, 2))[2:]
    return ' '.join(hex_payload[i:i + 2] for i in range(0, len(hex_payload), 2)).upper()


# split frame into 12 bytes
def frame_to_bytes(frame):
    return frame.split()

def split_frame_into_pdus(frame, ignore_bytes=4):

    bytes_list = frame_to_bytes(frame)
    pdus = [' '.join(bytes_list[i:i+12]) for i in range(0, len(bytes_list), 12)]
    return [pdu.split(' ', ignore_bytes)[-1] for pdu in pdus]

def split_into_pdus(frame):
    bytes_list = frame_to_bytes(frame)
    pdus = [' '.join(bytes_list[i:i + 12]) for i in range(0, len(bytes_list), 12)]
    return pdus


frame_1 = "00 06 02 08 80 00 00 00 00 00 00 00 00 05 D0 08 FF 60 00 00 02 00 00 00 00 06 01 08 80 00 00 00 00 00 00 00 00 00 10 C7 77 8A 70 AB AF 88 2A 8C"
frame_2 = "00 06 02 08 40 00 00 10 00 00 00 00 00 05 D0 08 21 20 00 00 02 00 00 00 00 06 01 08 80 00 00 00 00 00 00 00 00 00 00 11 29 FB 84 33 1D E5 5E 9D"

# just split
frame_1_to_pdu = split_into_pdus(frame_1)
frame_2_to_pdu = split_into_pdus(frame_2)

# split with ignoring the first 4 bytes of each pdu
pdus_1 = split_frame_into_pdus(frame_1)
pdus_2 = split_frame_into_pdus(frame_2)


signal_info = [
    ["LDW_AlertStatus", 2, 5, 2],
    ["DW_FollowUpTimeDisplay", 4, 7, 6],
    ["LCA_OverrideDisplay", 5, 2, 1]
]

def modify_signal(pdu, signal_info, new_value):
    binary_frame = hex_to_binary(pdu)

    signal_name, group_number, reverse_start_position, size = signal_info
    start_position = 7 - reverse_start_position

    # Extract the relevant group of 8 bits
    group = binary_frame[group_number * 8: (group_number + 1) * 8]

    # Modify the signal value
    group = group[:start_position] + format(new_value, f'0{size}b') + group[start_position + size:]

    # Update the binary frame with the modified group
    binary_frame = binary_frame[:group_number * 8] + group + binary_frame[(group_number + 1) * 8:]

    # Convert the modified binary frame back to hex
    modified_pdu = binary_to_hex(binary_frame)

    return modified_pdu

# New values for signals
ldw_alert_status_new_value = 2
dw_follow_up_time_display_new_value = 45
lca_override_display_new_value = 1

# Modify signals in frame 1
modified_pdu1 = modify_signal(pdus_1[0], signal_info[0], ldw_alert_status_new_value)

modified_pdu2 = modify_signal(pdus_1[1], signal_info[1], dw_follow_up_time_display_new_value)

modified_pdu3 = modify_signal(pdus_1[2], signal_info[2], lca_override_display_new_value)

# Modify signals in frame 2
modified_pdu4 = modify_signal(pdus_2[0], signal_info[0], ldw_alert_status_new_value)

modified_pdu5 = modify_signal(pdus_2[1], signal_info[1], dw_follow_up_time_display_new_value)

modified_pdu6 = modify_signal(pdus_2[2], signal_info[2], lca_override_display_new_value)

first_byte = frame_1_to_pdu[0].split()[0]
last_bytes_frame_1 = frame_1_to_pdu[-1]
last_bytes_frame_2 = frame_2_to_pdu[-1]

# header frame 1
header_frame_1_pdu_1 = frame_1_to_pdu[0].split()[1:3]
header_frame_1_pdu_2 = frame_1_to_pdu[1].split()[1:3]
header_frame_1_pdu_3 = frame_1_to_pdu[2].split()[1:3]

# dlc frame 1
dlc_frame_1_pdu_1 = frame_1_to_pdu[0].split()[3:4]
dlc_frame_1_pdu_2 = frame_1_to_pdu[1].split()[3:4]
dlc_frame_1_pdu_3 = frame_1_to_pdu[2].split()[3:4]

# header frame 2
header_frame_2_pdu_1 = frame_2_to_pdu[0].split()[1:3]
header_frame_2_pdu_2 = frame_2_to_pdu[1].split()[1:3]
header_frame_2_pdu_3 = frame_2_to_pdu[2].split()[1:3]

# dlc frame 2
dlc_frame_2_pdu_1 = frame_2_to_pdu[0].split()[3:4]
dlc_frame_2_pdu_2 = frame_2_to_pdu[1].split()[3:4]
dlc_frame_2_pdu_3 = frame_2_to_pdu[2].split()[3:4]

modified_frame_1_parts = [
    first_byte,
    *header_frame_1_pdu_1, *dlc_frame_1_pdu_1, modified_pdu1,
    first_byte,
    *header_frame_1_pdu_2, *dlc_frame_1_pdu_2, modified_pdu2,
    first_byte,
    *header_frame_1_pdu_3, *dlc_frame_1_pdu_3, modified_pdu3,
    last_bytes_frame_1
]

modified_frame_2_parts = [
    first_byte,
    *header_frame_2_pdu_1, *dlc_frame_2_pdu_1, modified_pdu4,
    first_byte,
    *header_frame_2_pdu_2, *dlc_frame_2_pdu_2, modified_pdu5,
    first_byte,
    *header_frame_2_pdu_3, *dlc_frame_2_pdu_3, modified_pdu6,
    last_bytes_frame_2
]

modified_frame_1 = ' '.join(modified_frame_1_parts)
modified_frame_2 = ' '.join(modified_frame_2_parts)

print("Original frame 1:")
print(frame_1)
print("Modified Frame 1:")
print(modified_frame_1)
print("\n")

print("Original frame 2:")
print(frame_2)
print("Modified Frame 2:")
print(modified_frame_2)