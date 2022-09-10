from easy import *

print("=========================================")
print("------------- Guessing Game -------------")
print("=========================================")
print("What difficulty do you want to play?")
print("1. Easy")
print("2. Medium")
print("3. Hard")
print("=========================================")

while True:
    difficulty = input("Difficulty: ")

    if difficulty == "" or difficulty == " " or int(difficulty) > 3 or int(difficulty) < 1:
        print("========================================")
        print("Please enter a valid difficulty level...")
        time.sleep(3)
        continue

    if type(int(difficulty)) == int:
        difficulty = int(difficulty)

        if difficulty == 1:
            print("========================================")
            easyMode();
            break
        
        if difficulty == 2:
            print("This mode is not available yet.")
            continue

        if difficulty == 3:
            print("This mode is not available yet.")
            continue

        break
