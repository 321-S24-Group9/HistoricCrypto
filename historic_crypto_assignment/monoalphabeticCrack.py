import sys,string, random

alphabet = string.ascii_uppercase
expected_digraph_distribution = {'th': 0.033, 'he': 0.0302, 'in': 0.0179, 'er': 0.0169,
                                     'an': 0.0181, 're': 0.0133, 'nd': 0.0146, 'at': 0.0104,
                                     'on': 0.0106, 'nt': 0.0106, 'ha': 0.0114, 'es': 0.0115,
                                     'st': 0.0109, 'en': 0.0111, 'ed': 0.0126, 'to': 0.0115,
                                     'it': 0.0093, 'ou': 0.0115, 'ea': 0.0110, 'hi': 0.0097,
                                     'is': 0.0086, 'or': 0.0084, 'ti': 0.0076, 'as': 0.0095,
                                     'te': 0.0075, 'et': 0.0083, 'ng': 0.0092, 'of': 0.0080,
                                     'al': 0.0057, 'de': 0.0057, 'se': 0.0074, 'le': 0.0064,
                                     'sa': 0.0067, 've': 0.0065,
                                     'ra': 0.04, 'ar': 0.0075, 
                                     'me':0.0068, 'ne':0.0066, 'wa': 0.0066, 'no':0.0060,
                                     'ta': 0.0059, 'ot': 0.0057, 'so': 0.0057, 'dt':0.0056,
                                      'll': 0.0056,'tt':0.0056, 'el':0.0055, 'ro':0.0055,
                                    'ad':0.0052, 'di':0.0050, 'ew':0.0050, 'ra':0.0050, 
                                    'ri':0.0050,'sh':0.0050 }

def get_freqs(text: str):
    freq_list = {letter: 0 for letter in alphabet}
    for c in text:
        if c.isalpha():
            freq_list[c.upper()]+=1
    # for i in range(26):
    #     freqs[i] = (freqs[i] / len(text)) * 100
    return freq_list

def single_analysis(message, sorted_freq):
    key = "ETAOINSRHDLUCMFYWGPBVKXQJZ"
    map = {letter: letter for letter in alphabet}
    #print(sorted_freq)
    for i,l in enumerate(sorted_freq):
        map[l[0]] = key[i]
    print(map)
    res = ""
    for letter in message:
        if letter.isalpha():
            res += map[letter]
        else:
            res += letter
    return [res,map]


def double_analysis(message, sorted_freq, single_map):
    ordered_double_freq = sorted(expected_digraph_distribution.items(), key=lambda item: [item[1],item[0]], reverse=True)
    # print(ordered_double_freq)
    # print(sorted_freq)
    map = {}
    free_alpha = [x for x in alphabet]
    for i,l in enumerate(ordered_double_freq):
        if sorted_freq[i][0][0] not in map.keys() and l[0][0].upper() in free_alpha:
            map[sorted_freq[i][0][0]] = l[0][0].upper()
            free_alpha.remove(l[0][0].upper())
        if sorted_freq[i][0][1] not in map.keys() and l[0][1].upper() in free_alpha:
            map[sorted_freq[i][0][1]] = l[0][1].upper()
            free_alpha.remove(l[0][1].upper())
    for letter in alphabet:
        if letter not in map.keys():
            if single_map[letter] in free_alpha:
                map[letter] = single_map[letter]
                free_alpha.remove(single_map[letter])
            else:
                rand_letter = random.choice(free_alpha)
                map[letter] = rand_letter
                free_alpha.remove(rand_letter)
    map = {k: v for k, v in sorted(map.items(), key=lambda item: item[0])}
    print(map)
    res = ""
    for letter in message:
        if letter.isalpha():
            res += map[letter]
        else:
            res += letter
    return res

def manual_transl(message,map):
    res = ""
    for letter in message:
        if letter.isalpha():
            res += map[letter]
        else:
            res += letter
    return res    


def get_double_freq(input):
    dict = {}
    ignore_count = 0
    for i in range(0,len(input)-1,2):
        if(input[i].isalpha() and input[i+1].isalpha()):
            if input[i:i+2] in dict.keys():
                dict[input[i:i+2]] += 1
            else:
                dict[input[i:i+2]] = 1 
        else:
            ignore_count+=2
    
    for i in range(1,len(input)-1,2):
        if(input[i].isalpha() and input[i+1].isalpha()):
            if input[i:i+2] in dict.keys():
                dict[input[i:i+2]] += 1
            else:
                dict[input[i:i+2]] = 1 
        else:
            ignore_count+=2

    for val in dict.keys():
        dict[val] = round(dict[val]/((2*len(input)-ignore_count)/2),3)
    sorted_dict = sorted(dict.items(), key=lambda item: [item[1],item[0]], reverse=True)
    return sorted_dict

def main():
    with open("./encrypted/mono_medium_encrypt.txt") as raw_data:
        orig = raw_data.readlines()
        ciphertext = ''.join([line.strip('\n') for line in orig])
    input = ciphertext
    freq_list = get_freqs(input)
    sorted_dict = sorted(freq_list.items(), key=lambda item: item[1], reverse=True)
    s_analysis = single_analysis(input, sorted_dict)
    # print(s_analysis[0])
    s_list = s_analysis[1]
    double_freq_list = get_double_freq(input)
    #print(double_freq_list)
    print(double_analysis(input,double_freq_list,s_list))

    ## mono-easy
    # Manually saw these words and change key from there
    # FEET, IN, THEIR, THOUGH, ANOTHER, STATES, WAS, PROBABLY, JEFFERSON
    # print()
    #  map = { 'A': 'W',
    #         'B': 'E',
    #         'C': 'V',
    #         'D': 'Y',
    #         'E': 'Z',
    #         'F': 'S',
    #         'G': 'R',
    #         'H': 'X',
    #         'I': 'N',
    #         'J': 'L', 
    #         'K': 'T', 
    #         'L': 'I',
    #         'M': 'K',
    #         'N': 'G', 
    #         'O': 'C', 
    #         'P': 'J', 
    #         'Q': 'P', 
    #         'R': 'D',
    #         'S': 'O', 
    #         'T': 'M', 
    #         'U': 'F', 
    #         'V': 'Q', 
    #         'W': 'U',
    #         'X': 'H', 
    #         'Y': 'B', 
    #         'Z': 'A'}
    # print(manual_transl(input,map))

    ## mono-medium
    # AND, ALL, DID, SLAIN, ITS, WITH, WERE, BEWARE, TOOK, THROUGH, LIVE, COME, FOE, PAWS, TOOK, BOY
    # From here we searched for the passage and realized its from alice and wonderland(tumtum tree)
    # so we were able to get the harder words
    # JUBJUB, TOVES
    print()
    map ={
        'A': 'T',
        'B': 'F',
        'C': 'O',
        'D': 'R',
        'E': 'D',
        'F': 'M',
        'G': 'L',
        'H': 'H',
        'I': 'B',
        'J': 'N',
        'K': 'Q',
        'L': 'P',
        'M': 'C',
        'N': 'V',
        'O': 'W',
        'P': 'G',
        'Q': 'Z',
        'R': 'U',
        'S': 'I',
        'T': 'J',
        'U': 'Y',
        'V': 'A',
        'W': 'K',
        'X': 'E',
        'Y': 'S',
        'Z': 'X'}
    print(manual_transl(input,map))


if __name__ == "__main__":
    main()