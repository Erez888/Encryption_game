
# encoding method one
def zigzagA (text):
    encoding1 = ""
    encoding2 = ""
    text = text.replace(" ", "")
    num = len(text)
    for i in range (num):
        if i % 2 == 0:
            encoding1 += text[i]
        else:
            encoding2 += text[i]
    fin_encoding = encoding1 + encoding2
    return cut4(fin_encoding)
# encoding method 2
def zigzagB(text):
    text = text.replace(" ","")
    encoding = text[::2] + text[1::2]
    return cut4(encoding)
# divide encrypted to words 4 letter each
def cut4(encoding):
    fin_encoding = ""
    num = len(encoding)
    for i in range (num):
        if i % 4 == 0:
            fin_encoding += (" " + encoding[i])
        else:
            fin_encoding += encoding[i]
    return (fin_encoding)
# decoding method one
def decoding (z_text):
    z_text = z_text.replace(" ", "")
    fin_encoding = ""
    if len(z_text)%2 == 0:
        index = int(len(z_text) / 2)
    else:
        index = int(len(z_text)/2 + 1)
    encoding1 = z_text [0:index]
    encoding2 = z_text [index:]
    for number in range (0 , index):
        fin_encoding += encoding1[number]
        fin_encoding += encoding2[number]
    return fin_encoding
# decoding method 2
def zigzagb_dec(text):
    text = text.replace(" ", "")
    if len(text)%2 == 1:
        text = text + " "
    size = (len(text))//2
    enc1 = text[:size]
    enc2 = text[size:]
    enc = ""
    for i in range (size):
        enc += enc1[i] + enc2[i]
    return enc

# encryption with variable depth:
def encrypt(text, depth):

    # if required depth is smaller than 1 ( minus value is invalid),returns the initial value without change

    if depth <= 1:
        return text

    ciphertext = ""
    direction = 1
    row = 0

    zigzag = [[] for _ in range(depth)]

    for char in text:
        zigzag[row].append(char)
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1

    for row in zigzag:
        ciphertext += "".join(row)

    return ciphertext

def decrypt(ciphertext, depth):

    # if required depth is smaller than 1 ( minus value is invalid),returns the initial value without change
    if depth <= 1:
        return ciphertext

    n = len(ciphertext)
    zigzag = [[] for _ in range(depth)]
    pattern = [0] * n

    row, direction = 0, 1
    for i in range(n):
        pattern[i] = row
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1

    index = 0
    for r in range(depth):
        for i in range(n):
            if pattern[i] == r:
                zigzag[r].append(ciphertext[index])
                index += 1

    plaintext = ""
    row, direction = 0, 1
    for i in range(n):
        plaintext += zigzag[row].pop(0)
        row += direction
        if row == 0 or row == depth - 1:
            direction *= -1

    return plaintext

if __name__ == "__main__":
    text = input("Enter text for encryption: ")
    depth = int(input("Enter depth of encryption: "))
    encrypted_text = encrypt(text, depth)
    decrypted_text = decrypt(encrypted_text, depth)
    print(f"Encrypted text: {encrypted_text}")
    print(f"Decrypted text: {decrypted_text}")


