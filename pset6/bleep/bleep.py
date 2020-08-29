# Bleeping input text
# Saznatalia problem set 6-5


import os
from cs50 import get_string
from sys import argv


def main():
    # Check that program used correctly and dictionary of banned words presented

    if (len(argv) != 3):
        file = open(argv[1])

        # Check that dictionary is not empty

        if os.stat(argv[1]).st_size == 0:
            print("File is empty")
            exit(2)
        else:
            # read the file, split the string into words, check that ipunt word in dictionary

            dictionary = file.read()
            tokens = dictionary.split("\n")
            message = input("What message would you like to censor?\n")
            i = 0
            bleep_list = []

            # if word is in dictionary means it's banned then replace each letter with asteriks

            for word in message.split():
                if word.lower() in tokens:
                    replacement = ["*" for i in list(word)]
                    new_word = ''
                    bleep_list.append(new_word.join(replacement))

            # If word is NOT in dictionary then can print as is

                else:
                    bleep_list.append(word)
                i += 1
            print(' '.join(bleep_list))
    else:
        print("Usage: python bleep.py dictionary")
        exit(1)


if __name__ == "__main__":
    main()