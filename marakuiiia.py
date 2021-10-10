def text2code(fileI, fileO):
    with open(fileI, 'r') as file:
        text = file.read()
    result = ' '.join(map(bin, bytearray(text, 'utf8')))
    with open(fileO, 'w') as file2:
        file2.write(result)

def code2text(fileI, fileO):
    with open(fileI, 'r') as file:
        text = file.read()
    result = ''.join([chr(int(x, 2)) for x in text.split(sep=' ')])
    with open(fileO, 'w') as file2:
        file2.write(result)
