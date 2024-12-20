alphabet = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'

rail_cipher = "هلفککاسیرهد"
rail_key = 3

def decrypt_rail_fence(cipher, key):
    rows = [''] * key
    for index, char in enumerate(cipher):
        row = index % key
        rows[row] += char
    decrypted = ''.join(rows)
    
    original = [''] * len(cipher)
    index = 0
    for row in range(key):
        for char in rows[row]:
            original[index] = char
            index += 1
    return ''.join(original)

plain_text_part = decrypt_rail_fence(rail_cipher, rail_key)
print("متن آشکار بخش اول:", plain_text_part)

vigenere_cipher = (
    'ککممهسثعوکفروالثتونگعذخژبعاسمخیششذقهزحکخترنچورتگخسشثژویچجیززثخگیفغذگطگکدخکجذتصیزلومکهمژگتفلملژگسذغگشمگذتذوقبسمماسسببهمگجوز'
)
known_plain = 'هکرکلاهسفید'
key_length = 9

cipher_indices = [alphabet.index(char) for char in vigenere_cipher]
plain_indices = [alphabet.index(char) for char in known_plain]

def extract_vigenere_key(cipher_idx, plain_idx, key_len):
    key = []
    for i in range(len(cipher_idx) - len(plain_idx) + 1):
        temp_key = []
        for j in range(len(plain_idx)):
            shift = (cipher_idx[i + j] - plain_idx[j]) % len(alphabet)
            temp_key.append(shift)
        key = temp_key[:key_len]
        break
    return key

vigenere_key = extract_vigenere_key(cipher_indices, plain_indices, key_length)
print("کلید استخراج‌شده:", vigenere_key)

# رمزگشایی ویژنر
def decrypt_vigenere(cipher_idx, key, key_len, alphabet):
    decoded_indices = []
    for i in range(len(cipher_idx)):
        shift = key[i % key_len]
        decoded_char = (cipher_idx[i] - shift) % len(alphabet)
        decoded_indices.append(decoded_char)
    return ''.join([alphabet[index] for index in decoded_indices])

decoded_text = decrypt_vigenere(cipher_indices, vigenere_key, key_length, alphabet)
print("متن رمزگشایی شده دوم:", decoded_text)