# Returns minimum number of coins with which that change can be made


from cs50 import get_float


def main():
    i = get_positive_float("Change: $ ")
    print_coins(i)

# Prompt user for change


def get_positive_float(prompt):
    while True:
        n = get_float(prompt)
        if n > 0:
            break
    return n

# Count how many coins will be given in change


def print_coins(change):
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1
    quarters = int(change * 100 / quarter)
    dimes = int((change * 100 - quarter * quarters)/dime)
    nickels = int((change * 100 - quarter * quarters - dimes * dime)/nickel)
    pennies = int((change * 100 - quarter * quarters - dimes * dime - nickel * nickels)/penny)
    # Total coins

    print(quarters + dimes + nickels + pennies)


if __name__ == "__main__":
    main()