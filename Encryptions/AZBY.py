def AZBY(p_text):
    #p_text = input("Text for encryption: ")
    #p_text = p_text.replace(" ", "")
    p_text = p_text.lower()
    start = "abcdefghijklmnopqrstuvwxyz"
    end =   "zyxwvutsrqponmlkjihgfedcba"
    text = ""
    for item in p_text:
        if item in start:
            num = start.find(item)
            ot = end[num]
            text = text + ot
        else:
            text = text + item
    return text
AZBY("Text")
