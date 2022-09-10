import random
import time

def easyMode():
    while True:
        number = input("How many numbers do you want to play with?")

        if number == "" or number == " ":
                print("========================================")
                print("Please enter a valid number...")
                time.sleep(3)
                continue
        if type(int(number)) == int:
            number = int(number)
            break

    num = random.randint(1, number)
    numGuesses = 0;
    guessing = True

    while guessing:
        guess = int(input(f"Guess a number from 1 to {number}:  "))
        numGuesses += 1

        if guess == num:
            print("========================================")
            print("--------------- YOU WIN! ---------------")
            print("========================================")
            print(f"It took you {numGuesses} to guess the number {num}.")
            time.sleep(3)
            answer = input("Whant to play again? (y/n): ")

            if answer == "n" or answer == "no":
                print("Thank you for playing. Program will end in a couple of seconds.")
                time.sleep(3)
                quit()
            else:
                print("Great! Let's play again.")
                time.sleep(3)
                print("========================================")
                continue
        
        elif guess > num:
            print("========================================")
            print(f"Your guess of {guess} is too high. Please try again...")
            time.sleep(3)
            continue

        elif guess < num:
            print("========================================")
            print(f"Your guess of {guess} is too low. Please try again...")
            time.sleep(3)
            continue