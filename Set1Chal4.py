def scoreText(text):
    score_table = {
        'a': 9, 'b': 2, 'c': 4, 'd': 5, 'e': 14, 'f': 3, 'g': 3,
        'h': 7, 'i': 8, 'j': 1, 'k': 2, 'l': 5, 'm': 3, 'n': 8,
        'o': 9, 'p': 3, 'q': 1, 'r': 7, 's': 7, 't': 10, 'u': 4,
        'v': 2, 'w': 3, 'x': 1, 'y': 3, 'z': 1, ' ': 10
    }
    score=0
    for c in text:
        if c.isalpha() or c==' ':
            score+=score_table.get(c.lower(), 0)
        elif c in ',.\'":;!?-':
            score += 2
        elif c in '`@#$%^*()/+[]|"':
            score+=1
        else:           #punishes the unusual characters
            score-=200
    return score
#this scoreText function has been written considering the use case in mind. Since we will be doing XOR with another byte, other than the correct deciphered text, most will have 
#lots of unusual characters leading to a lower score. The score_table does relate to frequency but that is not the main reason my scoreText function is working in this scenario
#in case of a general scoreText function a better written score_table with more accurate frequencies and vector dot product analysis can be used to get accurate predictions but
#here this simple scoreText function based on a simple idea should fulfill our purpose so I will be using this only.

def decryptHex(encr_hex):
    by=bytes.fromhex(encr_hex)
    max_str=""
    key=-1
    for i in range(256):
        str=""
        for b in by:
            str+=chr(b^i)
        if i==0:
            max_str=str
            key=0
            continue
        if (scoreText(str)>=scoreText(max_str)):
            max_str=str
            key=i
    return (max_str, key)

encr_hex="1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
print("Answer is:", decryptHex(encr_hex)[0])
