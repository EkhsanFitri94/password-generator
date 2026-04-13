import string
import secrets

MIN_LENGTH = 4
MAX_LENGTH = 128


def generate_password(length, char_pool):
    # Generate the password using the specific pool we give it
    password = "".join(secrets.choice(char_pool) for _ in range(length))
    return password


# This is the main part of the program that runs when you execute the file
if __name__ == "__main__":
    print("=== Welcome to the Password Generator ===")

    try:
        # Ask the user for a length
        user_input = input("Enter password length (default is 12): ")

        # If they just press Enter, use 12
        if user_input.strip() == "":
            length = 12
        else:
            length = int(user_input)

        if length < MIN_LENGTH or length > MAX_LENGTH:
            print(f"Error: Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")
        else:
            difficulty = (
                input("Choose difficulty (easy, medium, hard): ").strip().lower()
            )

            if difficulty == "easy":
                pool = string.ascii_letters
            elif difficulty == "medium":
                pool = string.ascii_letters + string.digits
            else:
                # If they type "hard" or anything else, default to hard
                pool = string.ascii_letters + string.digits + string.punctuation

            new_password = generate_password(length, pool)
            print(f"\nYour {difficulty} secure password is: {new_password}")

    except ValueError:
        print("Error: Please enter a valid number!")
