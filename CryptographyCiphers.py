# 1)
#####

n_of_x = []  # Full set of each occurrence
p_of_x = []  # Percentage frequency set of each occurrence


def calculate_relative_frequency(data):
    data = sorted(data)
    calculate_occurrences(data)
    p_of_x.clear()

    total_n = len(data)
    for set in n_of_x:
        frequency_n = 0

        for _ in set:
            frequency_n += 1

        p_of_x.append("{:0.1%}".format((frequency_n/total_n)).strip("%"))

    return p_of_x


def calculate_occurrences(data):

    n = []  # Individual set of each occurrence
    for index, item in enumerate(data):

        if n and item not in n:
            n_of_x.append(n)
            n = []

        n.append(item)
    n_of_x.append(n)


print(f"1) Relative frequency")
data_set = input("- Enter a set of any characters: ")
print(f"\tYour data set: {data_set}")
relative_frequency = calculate_relative_frequency(data_set)
print(f"\tThe relative frequency for each character AS PERCENTAGE -- {relative_frequency}\n")

# 2)
#####

# Hardcoded values
plaintext_alphabet = "abcdefghijklmnopqrstuvwxyz"
character_stream_instructor = "xultpaajcxitltlxaarpjhtiwtgxktghidhipxciwtvgtpilpitghlxiwiwtxgqadds"
alphabet_index_relation = {}
for i, char in enumerate(plaintext_alphabet):
    alphabet_index_relation.update({char: i})



def encrypt_char_stream(char_stream):

    # Remove any non-plaintext characters
    for char in char_stream:
        if char not in plaintext_alphabet and char != " " and not char.isupper():
            char_stream = char_stream.replace(char, "", 1)
            print(f"\tNOTE: Removed the non-plaintext character '{char}' from your input. New input: {char_stream}")

    # Determining shift key via relative frequency
    relative_frequency = calculate_relative_frequency(char_stream)
    shift_key = max(float(percentage).__round__() for percentage in relative_frequency)
    new_char_stream = ""

    # Encrypting
    for char in char_stream.lower():  # <- no specification on case?

        if char == " ":
            new_char_stream += char
        else:
            index = alphabet_index_relation.get(char)
            encrypted_index = (index + shift_key) % len(plaintext_alphabet)
            for key, value in alphabet_index_relation.items():
                if value == encrypted_index:
                    new_char_stream += key.capitalize()

    return new_char_stream


def decrypt_char_stream(char_stream):

    # Nonplaintext characters already removed

    # Determining shift key via relative frequency
    relative_frequency = calculate_relative_frequency(char_stream)
    shift_key = max(float(percentage).__round__() for percentage in relative_frequency)
    new_char_stream = ""

    # Decrypting
    for char in char_stream.lower():  # <- no specification on case?

        if char == " ":
            new_char_stream += char
        else:
            index = alphabet_index_relation.get(char)
            encrypted_index = (index - shift_key) % len(plaintext_alphabet)
            for key, value in alphabet_index_relation.items():
                if value == encrypted_index:
                    new_char_stream += key.lower()

    return new_char_stream


print(f"2) Ciphertext encryption/decryption")
print(f"(Example: ({character_stream_instructor}) decrypted is: ({decrypt_char_stream(character_stream_instructor)}))")

encrypted = encrypt_char_stream(input("Enter a stream of plaintext characters: "))
decrypted = decrypt_char_stream(encrypted)
print(f"\tYour character stream encrypted: {encrypted}")
print(f"\tYour character stream decrypted: {decrypted}")

# 3
#####

import random
plaintext_alphabet = "abcdefghijklmnopqrstuvwxyz"

class AffineKey:

    def __init__(self):
        self.a = None
        self.b = None

    def return_key_a(self):
        if self.a is None:
            self.a = random.randint(0, len(plaintext_alphabet)-1)
        return self.a

    def return_key_b(self):
        if self.b is None:
            self.b = random.randint(1, len(plaintext_alphabet)-1)
        return self.b


class AffineKeyTester:

    def __init__(self):
        self.plaintext = ""
        self.final_encryption = ""
        self.final_decryption = ""

    def encrypt(self, alpha, beta):

        encrypted_str = ""
        for char in self.plaintext.lower():
            if char == " ":
                encrypted_str += " "
            else:
                new_index = ((alphabet_index_relation.get(char)*alpha) + beta) % len(plaintext_alphabet)
                for letter, index in alphabet_index_relation.items():
                    if new_index == index:
                        encrypted_str += letter

        self.final_encryption = encrypted_str
        print(f"\tFinal encryption: {self.final_encryption}")

    def decrypt(self, alpha, beta):

        decrypted_str = ""
        alpha_inverse = self.modulo_multiplicative_inverse(alpha, len(plaintext_alphabet))
        for char in self.final_encryption:
            if char == " ":
                decrypted_str += " "
            else:
                new_index = ((alphabet_index_relation.get(char) - beta) * alpha_inverse) % len(plaintext_alphabet)
                for letter, index in alphabet_index_relation.items():
                    if new_index == index:
                        decrypted_str += letter

        self.final_decryption = decrypted_str

        print(f"\tFinal decryption: {self.final_decryption}")

        if self.final_decryption != self.plaintext:
          print(f"\t(NOTE (README): Decrypted plaintext did not match. If you were to try running the function with the EXACT SAME entered plaintext, the final decryption may return correctly. This may be because Python was unable to calculate the modulo inverse, as there is no built in function. Python seems to be unable to reliably return the correct value, no matter my attempts nor anyone else's source code. See source code.)")
        # NOTE: Decrypted plaintext did not match original plaintext. If you were to try running the function with the EXACT SAME entered plaintext, the final decryption may return correctly. This may be because Python was unable to calculate the modulo inverse, as there is no built in function. Python seems to be unable to reliably return the correct value, no matter my attempts nor anyone else's source code. See source code.

    def set_plaintext(self, user_input):
        for char in user_input:
            if char not in plaintext_alphabet and char != " " and not char.isupper():
                user_input = user_input.replace(char, "", 1)
                print(f"Your text contained the non-plaintext character '{char}'. Your new input: {user_input}")

        self.plaintext = user_input

    # Not my code. Reference and author credited below.
    def modulo_multiplicative_inverse(self, A, M):
        """
        Assumes that A and M are co-prime
        Returns multiplicative modulo inverse of A under M
        """
        # Find gcd using Extended Euclid's Algorithm
        gcd, x, y = self.extended_euclid_gcd(A, M)

        # In case x is negative, we handle it by adding extra M
        # Because we know that multiplicative inverse of A in range M lies
        # in the range [0, M-1]
        if x < 0:
            x += M
        
        return x

    def extended_euclid_gcd(self, a, b):
        """
        Returns a list `result` of size 3 where:
        Referring to the equation ax + by = gcd(a, b)
            result[0] is gcd(a, b)
            result[1] is x
            result[2] is y 
        """
        s = 0; old_s = 1
        t = 1; old_t = 0
        r = b; old_r = a

        while r != 0:
            quotient = old_r//r # In Python, // operator performs integer or floored division
            # This is a pythonic way to swap numbers
            # See the same part in C++ implementation below to know more
            old_r, r = r, old_r - quotient*r
            old_s, s = s, old_s - quotient*s
            old_t, t = t, old_t - quotient*t
        return [old_r, old_s, old_t]

    # Inverse modulo function author reference:
    # Ojha, R., & Ojha, R. (2017, January 28). How to find Multiplicative Inverse of a number modulo M? Retrieved from https://www.rookieslab.com/posts/how-to-find-multiplicative-inverse-of-a-number-modulo-m-in-python-cpp#brute-force-python-code-to-find-multiplicative-inverse-of-a-number-modulo-m---om



affine_crypter = AffineKeyTester()
affine_keys = AffineKey()

print(f"\n3) Affine Cipher")
affine_crypter.set_plaintext(input("Enter plaintext to be encrypted and decrypted using Affine Cipher: "))
affine_crypter.encrypt(affine_keys.return_key_a(), affine_keys.return_key_b())
affine_crypter.decrypt(affine_keys.return_key_a(), affine_keys.return_key_b())

# 4
#####
plaintext_alphabet = "abcdefghijklmnopqrstuvwxyz"
class VigenereKeys:

    def __init__(self):
        self.key_1 = None
        self.key_2 = None

    def return_key_1(self):
        if self.key_1 is None:
            self.key_1 = [random.randint(0, len(plaintext_alphabet)-1), random.randint(0, len(plaintext_alphabet)-1)]
        return self.key_1

    def return_key_2(self):
        if self.key_2 is None:
            self.key_2 = [random.randint(0, len(plaintext_alphabet)-1), random.randint(0, len(plaintext_alphabet)-1)]
        return self.key_2


class VigenereCryption:

    def __init__(self):
        self.plaintext = "Hellenism was the combination of Greek, Persian, and Egyptian cultures. During this remarkable time period, people were encouraged to pursue a formal education and produce many different kinds of art. New forms of math, science, and design made a great impact on society."
        self.encrypted = ""
        self.decrypted = ""

    def encrypt(self, key):
        self.encrypted = ""

        print(f"\nEncrypting plaintext: {self.plaintext}")

        # Filtering
        for i, char in enumerate(self.plaintext):
            if char == " ":
                self.plaintext = self.plaintext.replace(char, "", 1)
            elif char not in plaintext_alphabet and not char.isupper():
                self.plaintext = self.plaintext.replace(char, "", 1)


        i = 0
        # Substitute letter accordingly
        for char in self.plaintext.lower():
            new_index = (alphabet_index_relation.get(char) + key[i]) % len(plaintext_alphabet)

            # Cycle the key values
            if i == len(key)-1:
              i = 0
            else:
              i += 1

            for letter, index in alphabet_index_relation.items():
                if new_index == index:
                    self.encrypted += letter

        print(f"\n\tFinal encryption: {self.encrypted}")

    def decrypt(self, key):
        self.decrypted = ""

        # Grabbing dictionary
        letter_index_relation = {}
        for i, letter in enumerate(plaintext_alphabet):
            letter_index_relation.update({letter: i})

        i = 0
        # Substitute letter accordingly
        for char in self.encrypted:
            new_index = (letter_index_relation.get(char) - key[i]) % len(plaintext_alphabet)

            # Cycle the key values
            if i == len(key)-1:
              i = 0
            else:
              i += 1

            for letter, index in letter_index_relation.items():
                if new_index == index:
                    self.decrypted += letter

        print(f"\n\tFinal decryption: {self.decrypted}")


vigenere_keys = VigenereKeys()
vigenere_crypter = VigenereCryption()

print(f"\n4) Vigenere Cryption")
print(f"\nUsing key set 1 {vigenere_keys.return_key_1()}:")
vigenere_crypter.encrypt(vigenere_keys.return_key_1())
vigenere_crypter.decrypt(vigenere_keys.return_key_1())

print(f"\nUsing key set 2 {vigenere_keys.return_key_2()}:")
vigenere_crypter.encrypt(vigenere_keys.return_key_2())
vigenere_crypter.decrypt(vigenere_keys.return_key_2())