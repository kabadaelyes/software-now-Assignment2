# encryption
def encrypt_file(shift1, shift2, input_path, output_path):
    # Read the original text
    encrypted_content = ""

    with open(input_path, "r") as file:
        content = file.read()

    # Encrypt each character
    for char in content:

        # a-n: shift forward by shift1 * shift2
        if "a" <= char <= "n":
            encrypted_content += chr(
                (((ord(char) - 97) + (shift1 * shift2)) % 14) + 97
            )

        # o-z: shift backward by shift1 + shift2
        elif "o" <= char <= "z":
            encrypted_content += chr(
                (((ord(char) - 111) - (shift1 + shift2)) % 12) + 111
            )

        # A-M: shift backward by shift1
        elif "A" <= char <= "M":
            encrypted_content += chr(
                (((ord(char) - 65) - shift1) % 13) + 65
            )

        # N-Z: shift forward by shift2 squared
        elif "N" <= char <= "Z":
            encrypted_content += chr(
                (((ord(char) - 78) + (shift2 ** 2)) % 13) + 78
            )

        # 0-9: shift forward by shift1 - shift2
        elif "0" <= char <= "9":
            encrypted_content += chr(
                (((ord(char) - 48) + (shift1 - shift2)) % 10) + 48
            )

        # Keep other characters unchanged
        else:
            encrypted_content += char

    # Save the encrypted text
    with open(output_path, "w") as file:
        file.write(encrypted_content)


# decryption
def decrypt_file(shift1, shift2, input_path, output_path):
    # Read the encrypted text
    decrypted_content = ""

    with open(input_path, "r") as file:
        content = file.read()

    # Reverse the encryption rules
    for char in content:

        # a-n: reverse shift1 * shift2
        if "a" <= char <= "n":
            decrypted_content += chr(
                (((ord(char) - 97) - (shift1 * shift2)) % 14) + 97
            )

        # o-z: reverse shift1 + shift2
        elif "o" <= char <= "z":
            decrypted_content += chr(
                (((ord(char) - 111) + (shift1 + shift2)) % 12) + 111
            )

        # A-M: reverse shift1
        elif "A" <= char <= "M":
            decrypted_content += chr(
                (((ord(char) - 65) + shift1) % 13) + 65
            )

        # N-Z: reverse shift2 squared
        elif "N" <= char <= "Z":
            decrypted_content += chr(
                (((ord(char) - 78) - (shift2 ** 2)) % 13) + 78
            )

        # 0-9: reverse shift1 - shift2
        elif "0" <= char <= "9":
            decrypted_content += chr(
                (((ord(char) - 48) - (shift1 - shift2)) % 10) + 48
            )

        # Keep other characters unchanged
        else:
            decrypted_content += char

    # Save the decrypted text
    with open(output_path, "w") as file:
        file.write(decrypted_content)


# verification
def verify_files(original_path, decrypted_path):
    # Read both files and compare them
    with open(original_path, "r") as file:
        original = file.read()

    with open(decrypted_path, "r") as file:
        decrypted = file.read()

    # Check if the files are identical
    if original == decrypted:
        print("Decryption successful.")
        return True
    else:
        print("Decryption failed.")
        return False


# main program
def get_shift(prompt):
    # Ask again if the input is invalid
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Shift must be a non-negative integer.")
            else:
                return value

        except ValueError:
            print("Please enter a valid integer.")


# Ask for the shift values
shift1 = get_shift("Enter shift1: ")
shift2 = get_shift("Enter shift2: ")


# Encrypt the original file
encrypt_file(
    shift1,
    shift2,
    "raw_text.txt",
    "encrypted_text.txt"
)

# Decrypt the encrypted file
decrypt_file(
    shift1,
    shift2,
    "encrypted_text.txt",
    "decrypted_text.txt"
)

# Compare the original and decrypted files
verify_files(
    "raw_text.txt",
    "decrypted_text.txt"
)