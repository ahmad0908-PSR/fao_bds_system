"""
One-off helper: generates a bcrypt hash for your Data Entry App login password.

Run it once from the project root:
    python -m shared.generate_password_hash

Copy the printed hash into your .env file as:
    ENTRY_APP_PASSWORD_HASH=<the hash>
"""

import getpass
import bcrypt


def main():
    password = getpass.getpass("Enter the password you want to use for the Data Entry App: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match. Try again.")
        return

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    print("\nAdd this line to your .env file:\n")
    print(f"ENTRY_APP_PASSWORD_HASH={hashed.decode('utf-8')}")


if __name__ == "__main__":
    main()
