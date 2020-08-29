# Builds descending and ascending pyramids for Mario with user-define height
# NataliaSaz problem set 1-3 "Mario" more comfortable level


def main():
    height = get_user_input()
    print_hashes(int(height))

# Prompt user for height between [1:8] inclusive


def get_user_input():
    while True:
        height = input("Height: ")
        if (height.isdigit() and int(height) in range(1, 9)):
            break
    return height

# Prints ascending & descending pyramids of hatches and spaces


def print_hashes(height):
    i = 0
    j = 0
    for i in range(height):
        # Prints left ascending pyramid
        for j in range(height):
            if j < height - i - 1:
                print(" ", end="")
            else:
                print("#", end="")
            j += 1
        # Prints two spaces between pyramids
        for j in range(height, height + 2):
            print(" ", end="")
            j += 1
        # Prints right descending pyramid
        for j in range(height + 2, 2 * height + 2):
            if j <= i + height + 2:
                print("#", end="")
                j += 1
        print("")
        i += 1


if __name__ == "__main__":
    main()

