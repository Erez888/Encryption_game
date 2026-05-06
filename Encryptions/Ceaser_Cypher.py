def CeaserCyhper(p_text, key):
    p_text = p_text.lower()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypted_text = ""
    for char in p_text:
        if char in alphabet:
            index = alphabet.find(char)
            new_index = (index + key) % 26
            new_char = alphabet[new_index]
            encrypted_text +=new_char
        else:
            encrypted_text += char
    return encrypted_text

