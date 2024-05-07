import sys, string, math

alphabet = string.ascii_uppercase
english_freqs = {
        'A': 8.4966, 'B': 2.0720, 'C': 4.5388, 'D': 3.3844,
        'E': 11.1607, 'F': 1.8121, 'G': 2.4705, 'H': 3.0034,
        'I': 7.5448, 'J': 0.1965, 'K': 1.1016, 'L': 5.4893,
        'M': 3.0129, 'N': 6.6544, 'O': 7.1635, 'P': 3.1671,
        'Q': 0.1962, 'R': 7.5809, 'S': 5.7351, 'T': 6.9509,
        'U': 3.6308, 'V': 1.0074, 'W': 1.2899, 'X': 0.2902,
        'Y': 1.7779, 'Z': 0.2722
    }
eng_freq_list = list(english_freqs.values()) 

def get_freqs(text: str):
    freqs = [0]*26
    for c in text:
        if c.isalpha():
            freqs[alphabet.index(c.upper())]+=1
    for i in range(26):
        freqs[i] = freqs[i] / len(text)
    return freqs

def get_ioc(text) -> float:
    counts = [0]*26
    for c in text:
        counts[alphabet.index(c)]+=1
    numerator = 0
    total = 0
    for i in range(26):
        numerator += counts[i]*(counts[i]-1)
        total += counts[i]
    IoC_text = (numerator * 26) / (total * (total - 1))
    return IoC_text

def vig_attack_driver(text, key_len):
    # make the splits
    splits = ['']*key_len
    for i in range(len(text)):
        splits[i%key_len]+=text[i]
    # get the freqs of every split
    freqs = []
    # for i in range(key_len):
    for split in splits:
        freqs.append(get_freqs(split))
    # make a dummy key
    key = ['A']*key_len
    for key_index in range(key_len):
        for letter in range(26):
            # shifts the frequency dist by the letter, then compares it with english
            temp = freqs[key_index][letter:]+freqs[key_index][:letter]
            # if it looks like its close enough, %75 match, uses that letter as the letter in the key
            if cosine_similarity(eng_freq_list, temp) > 0.75:
                key[key_index]=alphabet[letter]
    return vig_decrypt(text, key)

def dot_product(list1, list2):
    return sum(x * y for x, y in zip(list1, list2))

def magnitude(list):
    return math.sqrt(sum(x ** 2 for x in list))

def cosine_similarity(list1, list2):
    dot_prod = dot_product(list1, list2)
    mag_list1 = magnitude(list1)
    mag_list2 = magnitude(list2)
    similarity = dot_prod / (mag_list1 * mag_list2)
    return similarity

def vig_decrypt(ciphertext, key):
    plaintext=''
    for char in range(len(ciphertext)):
        if ciphertext[char].isalpha():
            cipher_letter = alphabet.index(ciphertext[char].upper())
            key_letter = alphabet.index(key[char%len(key)])
            letter = (cipher_letter - key_letter)%26
            plaintext+=alphabet[letter]
    return plaintext

def viginere_attack(filename: str):
    with open(filename) as raw_data:
        ciphertext = ''.join([line.strip('\n') for line in raw_data.readlines()])
        ciphertext = ''.join([c for c in ciphertext if c.isalpha()])
        # key_len = vig_key_len(ciphertext)
        key_lens = [5, 9, 13]
        possible_decrypts = []
        for key_len in key_lens:
            possible_decrypts.append(vig_attack_driver(ciphertext, key_len))
        return possible_decrypts

def main(args):
    # if len(args) != 2:
    #     print("Usage: python3 vigereneCrack.py <ciphertext_file>")
    #     sys.exit(1)
    viginere_attack("encrypted/vigerne_medium_encrypt.txt")

if __name__=="__main__":
    main(sys.argv)