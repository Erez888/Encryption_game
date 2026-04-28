def encrypt(message, key):
    message = message.lower()
    key = key.lower()
    new_message = ""
    for pair in enumerate(message):
        index = pair[0]
        char = pair[1]
        index %= len(key)
        new_char = ((ord(char) -97) + (ord(key[index])-97)) % 26
        new_char += 97
        new_char = chr(new_char)
        new_message+= new_char
    return  new_message

def decrypt(message, key):
    new_message = ""
    message = message.lower()
    key = key.lower()
    for pair in enumerate(message):
        index = pair[0]
        char = pair[1]
        index %= len(key)
        new_char = ((ord(char) -97) - (ord(key[index])-97)) % 26
        new_char += 97
        new_char = chr(new_char)
        new_message+= new_char
    return  new_message

if __name__ == "__main__":
    original_text = "hello"
    key = "banana"
    encrypted_text = encrypt(original_text, key)
    decrypted_text = decrypt(encrypted_text, key)
    print(f"original text:{original_text}")
    print(f"encrypted text:{encrypted_text}")
    print(f"decrypted text:{decrypted_text}")





