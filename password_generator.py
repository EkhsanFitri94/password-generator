import string
import secrets

MIN_LENGTH = 4
MAX_LENGTH = 128


def generate_password(length=12):
    # Combine letters, numbers, and symbols
    all_characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password
    password = "".join(secrets.choice(all_characters) for _ in range(length))

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
            # Generate and print the password
            new_password = generate_password(length)
            print(f"\nYour secure password is: {new_password}")

    except ValueError:
        print("Error: Please enter a valid number!")
