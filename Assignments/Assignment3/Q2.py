def get_sbox_value(sbox, x):
    row = (x >> 5) * 2 + (x & 1)
    col = (x >> 1) & 0b1111
    return sbox[row][col]

S1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

x1 = 0b000000
x2 = 0b000001
x1_value = get_sbox_value(S1, x1)
x2_value = get_sbox_value(S1, x2)
x1x2_value = get_sbox_value(S1, x1 ^ x2)

print(f"S1(x1) = {x1_value}")
print(f"S1(x2) = {x2_value}")
print(f"S1(x1 ^ x2) = {x1x2_value}")
print(f"S1(x1) ^ S1(x2) = {x1_value ^ x2_value}")