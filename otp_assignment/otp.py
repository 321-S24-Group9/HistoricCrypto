import string, random, os
from Crypto.Random import get_random_bytes

## task 1

def xor_string(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("The strings must be equal length\n")

    s1_byte = bytearray(s1, 'utf-8')
    s2_byte = bytearray(s2, 'utf-8')

    result = bytearray()
    for b1,b2 in zip(s1_byte,s2_byte):
        result.append(b1 ^ b2)

    return result.decode('utf-8')   

def xor(b1,b2):
    if len(b1) != len(b2):
        raise ValueError("The inputs must be equal length\n")

    result = bytearray()
    for b1,b2 in zip(b1,b2):
        result.append(b1 ^ b2)
    return result

 

## task 2
    
def otp_string(filename):
    with open(filename) as raw_data:
        plaintext = raw_data.read()
    length = len(plaintext)
    characters = string.ascii_letters
    key = ''.join(random.choices(characters, k=length))
    ciphertext = xor_string(plaintext,key)
    # check if xor works both ways
    plaintext_backwards = xor_string(ciphertext,key)
    if plaintext_backwards == plaintext:
        new_file_name, ext = os.path.splitext(filename)
        new_file = new_file_name + "_ciphertext" + ext
        with open(new_file,'w') as file:
            file.write(ciphertext)
        return ciphertext
    else:
        raise ValueError("OTP key didn't work both ways, try again")
    
## task 3

def otp_image(filename):
    with open(filename, 'rb') as file:
        header = file.read(54)
        plaintext = file.read()
    length = len(plaintext)
    key = get_random_bytes(length)
    ciphertext = xor(plaintext,key)
    plaintext_backwards = xor(ciphertext,key)
    if plaintext_backwards == plaintext:
        new_file_name, ext = os.path.splitext(filename)
        new_file = new_file_name + "_ciphertext" + ext
        with open(new_file,'wb') as file:
            file.write(header)
            file.write(ciphertext)
        return ciphertext
    else:
        raise ValueError("OTP key didn't work both ways, try again")

## task 4

def two_time_pad(filename1,filename2):
    with open(filename1, 'rb') as file:
        header1 = file.read(54)
        plaintext1 = file.read()
    
    with open(filename2, 'rb') as file:
        header2 = file.read(54)
        plaintext2 = file.read()
    
    if len(plaintext1) == len(plaintext2):
        key = get_random_bytes(len(plaintext1)) #equal to lenght of plaintext2
    else:
        raise ValueError("imput files must be same length")
    
    ciphertext1 = xor(plaintext1, key)
    ciphertext2 = xor(plaintext2, key)
    new_file_name1, ext = os.path.splitext(filename1)
    new_file = new_file_name1 + "_encrypted" + ext
    with open(new_file,'wb') as file:
        file.write(header1)
        file.write(ciphertext1)
    new_file_name2, ext = os.path.splitext(filename2)
    new_file = new_file_name2 + "_encrypted" + ext
    with open(new_file,'wb') as file:
        file.write(header2)
        file.write(ciphertext2)
    p1xorp2 = xor(ciphertext1,ciphertext2)
    new_file = new_file_name1 + "_" + os.path.basename(filename2) + ext
    with open(new_file,'wb') as file:
        file.write(header1)
        file.write(p1xorp2)
    return p1xorp2
    
    


if __name__ == "__main__":
    s1 = "Darlin dont you go"
    s2 = "and cut your hair!"
    print(xor_string(s1,s2).encode().hex())
    
    filename = "./otp_assignment/example.txt"
    print(otp_string(filename))

    filename1 = "./otp_assignment/cp-logo.bmp"
    otp_image(filename1)
    filename2 = "./otp_assignment/mustang.bmp"
    otp_image(filename2)

    two_time_pad(filename1, filename2)