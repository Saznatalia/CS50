from sys import argv


# Crypting input text
# Saznatalia problem set 6-4


def main():
    if (len(argv) == 2 and argv[1].isalpha()):
        original = input("plaintext: ")
        crypting(original, argv[1])
    else:
        print("Usage veginere.py keyword")
        exit(1)


# Crypting function


def crypting(input, keyword):
    print("ciphertext: ", end='')

    # Creating array of key
    key_array = []
    for char in keyword:
        key = shift(char)
        key_array.append(key)

    # Crypting
    i = 0
    for letter in input:
        if letter.isalpha():
            shifting(letter, key_array[i])
            i += 1
        else:
            print(letter, end="")

        # Check if reaches end of array
        if i == len(keyword):
            i = 0

    print("")

# Shifting letter in keyword into numbers/key


def shift(c):
    if c.isupper():
        c = ord(c) - 65
    else:
        c = ord(c) - 97
    return c


# Printing cripted letter as output


def shifting(c, key):
    if c.isupper():
        print_char = (ord(c) + key - 65) % 26 + 65
        print(chr(print_char), end="")
    else:
        print_char = (ord(c) + key - 97) % 26 + 97
        print(chr(print_char), end="")


main()
if __name__ == "__main":
    main()