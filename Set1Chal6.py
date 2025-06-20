import base64
import requests
from functools import singledispatch


@singledispatch
def hammingDistance(a, b):
    print("Type issue")
@hammingDistance.register
def _(a: bytes, b: bytes):
    assert len(a)==len(b)
    return sum(bin(x^y).count('1') for x,y in zip(a,b))
@hammingDistance.register
def _(a: str, b: str):
    aBytes=a.encode()
    bBytes=b.encode()
    assert len(aBytes)==len(bBytes)
    return sum(bin(x^y).count('1') for x,y in zip(aBytes,bBytes)) #bin converts an integer to binary string starting with 0b


def getKeySize(data64):
    dataSample=base64.b64decode(data64)
    assert len(dataSample)>=100, "Need a bigger data sample preferably. Else make a new function as this is written for large datasets and checks for KEYSIZEs upto 50."
    hammingDistances=[]
    for KEYSIZE in range(1,51):
        startIndex=0
        sumHamming=0
        i=0
        while ((startIndex+2*KEYSIZE)<=len(dataSample)):
            chunk1=dataSample[startIndex:(startIndex+KEYSIZE)]
            startIndex+=KEYSIZE
            chunk2=dataSample[startIndex:(startIndex+KEYSIZE)]
            sumHamming+=hammingDistance(chunk1,chunk2)
            i+=1
        sumHamming/=i
        hammingDistances.append((sumHamming/KEYSIZE, KEYSIZE))
    hammingDistances.sort()
    return hammingDistances #returns a list of pairs of hamming distances and corresponding keysizes.


def getBlocks(dataSample, KEYSIZE):
    blocks=[]
    for pos in range(KEYSIZE):
        byteList=[]
        i=pos
        while (i<len(dataSample)):
            byteList.append(dataSample[i])
            i+=KEYSIZE
        blocks.append(bytes(byteList))
    return blocks


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
        else:
            score-=200
    return score


def decryptSingleKeyBinary(binstring):
    max_str=""
    key=0
    for i in range(256):
        str=""
        for b in binstring:
            str+=chr(b^i)
        if (i==0):
            max_str=str
            continue
        if (scoreText(str)>=scoreText(max_str)):
            max_str=str
            key=i
    return (max_str, key)


def joinBlocks(decodedBlocks):
    output = ""
    for tup in zip(*decodedBlocks):
        output += ''.join(tup)
    return output


def getKeynCode(data64, KEYSIZE):
    dataSample=base64.b64decode(data64)
    blocks=getBlocks(dataSample,KEYSIZE)
    key=""
    decodedBlocks=[]
    for i in range(KEYSIZE):
        output=decryptSingleKeyBinary(blocks[i])
        key+=(chr(output[1]))
        decodedBlocks.append(output[0])
    return (key, joinBlocks(decodedBlocks))


def decipher(originalData):
    hammingDistances=getKeySize(originalData)
    print("Likely KEYSIZEs:", hammingDistances[0][1], hammingDistances[1][1], hammingDistances[2][1], hammingDistances[3][1])
    print("Corresponding values to see how close they are:", hammingDistances[0][0], hammingDistances[1][0], hammingDistances[2][0], hammingDistances[3][0])
    output=[]
    for i in range(4):
        output.append(getKeynCode(originalData, hammingDistances[i][1]))
    print("Possible keys are:", output[0][0], output[1][0], output[2][0], output[3][0])
    maxx=0
    for i in range(4):
        if (scoreText(output[i][1])>=scoreText(output[maxx][1])):
            maxx=i
    print("Getting best possible score for KEYSIZE =", hammingDistances[maxx][1])
    return output[maxx][0]


url="https://cryptopals.com/static/challenge-data/6.txt"
response=requests.get(url)
originalData=response.text
key=decipher(originalData)
print("Key is:", key)