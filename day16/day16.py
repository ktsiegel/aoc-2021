from copy import deepcopy
from math import prod

hex_to_binary_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}
def hex_to_binary(hex_code):
    binary_code = ''
    for c in hex_code:
        binary_code += hex_to_binary_map[c]
    return binary_code

# a literal value packet starts with 3 digits for the packet version, followed
# by 3 digits for the type (4), followed by the digits of the number.
# returns the decoded value, the length of the packet, and the version summed
# value
def decode_literal_value_packet(packet):
    packet_version = int(packet[0:3], 2)
    print('processing literal value with version {}: {}'.format(packet_version, packet))
    packet_type_id = int(packet[3:6], 2)
    assert packet_type_id == 4

    packet_index = 6
    decoded_binary_value = ''
    while True:
        last_packet_digit = packet[packet_index:packet_index+1]
        next_digit = packet[packet_index+1:packet_index+5]
        decoded_binary_value += next_digit
        packet_index += 5
        if last_packet_digit == '0':
            break
    return int(decoded_binary_value, 2), packet_index, packet_version

# performs the operation (by packet type id) on the values provided
# packet_type_id is an int, as are the values provided
def perform_operation_on_values(packet_type_id, values):
    assert packet_type_id != 4 and packet_type_id >= 0 and packet_type_id <= 7
    if packet_type_id == 0:
        return sum(values)
    elif packet_type_id == 1:
        return prod(values)
    elif packet_type_id == 2:
        return min(values)
    elif packet_type_id == 3:
        return max(values)
    elif packet_type_id == 5:
        if values[0] > values[1]:
            return 1
        return 0
    elif packet_type_id == 6:
        if values[0] < values[1]:
            return 1
        return 0
    else:
        if values[0] == values[1]:
            return 1
        return 0

# returns calculated value, packet length, version summed value
def decode_operator_packet(packet):
    packet_version = int(packet[0:3], 2)
    print('decode operator packet with version {}:{}'.format(packet_version, packet))
    packet_type_id = int(packet[3:6], 2)
    assert packet_type_id != 4
    length_type_id = packet[6:7]
    assert length_type_id == '0' or length_type_id == '1'
    num_bits_in_sub_packet_count = 15
    if length_type_id == '1':
        num_bits_in_sub_packet_count = 11
    sub_packet_start = 7 + num_bits_in_sub_packet_count
    sub_packets_length = int(packet[7:sub_packet_start], 2)
    print('sub packet count {} -> {}'.format(packet[7:sub_packet_start],sub_packets_length))

    packet_index = sub_packet_start
    total_version_value = packet_version
    sub_packet_values = []
    packet_count = 0
    while (length_type_id == '0' and packet_index - sub_packet_start < \
    sub_packets_length) or (length_type_id == '1' and packet_count < \
    sub_packets_length):
        print('processing packet: {}'.format(packet[packet_index:]))
        (sub_packet_value, sub_packet_length, sub_packet_version_value) = decode_packet(packet[packet_index:])
        packet_index += sub_packet_length
        total_version_value += sub_packet_version_value
        sub_packet_values.append(sub_packet_value)
        packet_count += 1
    return perform_operation_on_values(packet_type_id, sub_packet_values), packet_index, total_version_value

# returns calculated value, packet length, version summed value
def decode_packet(packet):
    packet_version = packet[0:3]
    packet_type_id = int(packet[3:6], 2)
    total_version_value = 0
    total_packet_length = 0
    if packet_type_id == 4:
        # literal value packet
        return decode_literal_value_packet(packet)
    else:
        # operator packet
        return decode_operator_packet(packet)

def decode_hex(hex_packet):
    return decode_packet(hex_to_binary(hex_packet))[0]

problem_input = 'E0525D9802FA00B80021B13E2D4260004321DC648D729DD67B2412009966D76C0159ED274F6921402E9FD4AC1B0F652CD339D7B82240083C9A54E819802B369DC0082CF90CF9280081727DAF41E6A5C1B9B8E41A4F31A4EF67E2009834015986F9ABE41E7D6080213931CB004270DE5DD4C010E00D50401B8A708E3F80021F0BE0A43D9E460007E62ACEE7F9FB4491BC2260090A573A876B1BC4D679BA7A642401434937C911CD984910490CCFC27CC7EE686009CFC57EC0149CEFE4D135A0C200C0F401298BCF265377F79C279F540279ACCE5A820CB044B62299291C0198025401AA00021D1822BC5C100763A4698FB350E6184C00A9820200FAF00244998F67D59998F67D5A93ECB0D6E0164D709A47F5AEB6612D1B1AC788846008780252555097F51F263A1CA00C4D0946B92669EE47315060081206C96208B0B2610E7B389737F3E2006D66C1A1D4ABEC3E1003A3B0805D337C2F4FA5CD83CE7DA67A304E9BEEF32DCEF08A400020B1967FC2660084BC77BAC3F847B004E6CA26CA140095003900BAA3002140087003D40080022E8C00870039400E1002D400F10038C00D100218038F400B6100229500226699FEB9F9B098021A00800021507627C321006E24C5784B160C014A0054A64E64BB5459DE821803324093AEB3254600B4BF75C50D0046562F72B1793004667B6E78EFC0139FD534733409232D7742E402850803F1FA3143D00042226C4A8B800084C528FD1527E98D5EB45C6003FE7F7FCBA000A1E600FC5A8311F08010983F0BA0890021F1B61CC4620140EC010100762DC4C8720008641E89F0866259AF460C015D00564F71ED2935993A539C0F9AA6B0786008D80233514594F43CDD31F585005A25C3430047401194EA649E87E0CA801D320D2971C95CAA380393AF131F94F9E0499A775460'

def main():
    assert decode_literal_value_packet(hex_to_binary('D2FE28')) == (2021, 21, 6)
    assert decode_hex('C200B40A82') == 3
    assert decode_hex('04005AC33890') == 54
    assert decode_hex('880086C3E88112') == 7
    assert decode_hex('CE00C43D881120') == 9
    assert decode_hex('D8005AC2A8F0') == 1
    assert decode_hex('F600BC2D8F') == 0
    assert decode_hex('9C005AC2F8F0') == 0
    assert decode_hex('9C0141080250320F1802104A08') == 1
    print(decode_hex(problem_input))

if __name__ == "__main__":
	main()
