string = "Alexander the Great was a successful ruler because his actions created long lasting effects on cultures that continue to the present day. One example of his legacy was the creation of a Hellenistic society. Hellenism was the combination of Greek, Persian, and Egyptian cultures. During this remarkable time period, people were encouraged to pursue a formal education and produce many different kinds of art. New forms of math, science, and design made a great impact on society."
ioc = 0.066287384519025
eng_alphabet = "abcdefghijklmnopqrstuvwxyz"


def determine_frequency_count():

    character_occurences = {}

    for char in string.lower():
        num_occurences = 1
        if char in eng_alphabet:
            if char in character_occurences and char != " ":
                num_occurences = character_occurences.get(char)+1
                character_occurences.pop(char)
            character_occurences.update({char: num_occurences})

    individual_occurences = []
    for key, value in character_occurences.items():
        individual_occurences.append(value)

    ioc_ = len(character_occurences)/(len(individual_occurences)*len(individual_occurences)-1)
    print(f"Index of coincidence: {ioc_}")

# Affine cipher


alphabet_index_relation = {}
for i, char in enumerate(eng_alphabet):
    alphabet_index_relation.update({char: i})

import random
plaintext_alphabet = "abcdefghijklmnopqrstuvwxyz"


class AffineKey:

    def __init__(self):
        self.a = 7
        self.b = 13

    def return_key_a(self):
        if self.a is None:
            self.a = random.randint(0, len(plaintext_alphabet) - 1)
        return self.a

    def return_key_b(self):
        if self.b is None:
            self.b = random.randint(1, len(plaintext_alphabet) - 1)
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
                new_index = ((alphabet_index_relation.get(char) * alpha) + beta) % len(plaintext_alphabet)
                for letter, index in alphabet_index_relation.items():
                    if new_index == index:
                        encrypted_str += letter

        self.final_encryption = encrypted_str
        print(f"Final encryption: {self.final_encryption}")

    def set_plaintext(self, user_input):
        for char in user_input:
            if char not in plaintext_alphabet and char != " " and not char.isupper():
                user_input = user_input.replace(char, "", 1)
                # print(f"Your text contained the non-plaintext character '{char}'. Your new input: {user_input}")

        self.plaintext = user_input

determine_frequency_count()
affine_crypter = AffineKeyTester()
affine_keys = AffineKey()
affine_crypter.set_plaintext(string)
affine_crypter.encrypt(affine_keys.return_key_a(), affine_keys.return_key_b())
