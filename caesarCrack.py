import sys, string

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
        freqs[i] = (freqs[i] / len(text)) * 100
    return freqs

def caesar(ciphertext: str) -> list:
    plaintexts = []
    for shift in range(26):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                if char.isupper():
                    plaintext += chr((ord(char) - shift - 65) % 26 + 65)
                else:
                    plaintext += chr((ord(char) - shift - 97) % 26 + 97)
            else:
                plaintext += char
        plaintexts.append(plaintext)
    return plaintexts

def get_likely_decrypt(decrypts: list) -> str:
    freqs = [get_freqs(decrypt) for decrypt in decrypts]
    scores = []
    for freq in freqs:
        score = 0
        for i in range(26):
            score += abs(freq[i] - eng_freq_list[i])
        scores.append(score)
    return decrypts[scores.index(min(scores))]

def main(args):
    with open(args[1], "r") as ciphertext_file:
        ciphertext = ciphertext_file.read()
        decrypts = caesar(ciphertext)
        print(get_likely_decrypt(decrypts))

#Example usage
if __name__=="__main__":
    main(sys.argv)
