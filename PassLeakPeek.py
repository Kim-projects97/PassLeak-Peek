import hashlib
import requests
import re
import secrets
import string
import platform
import sys
import urllib.request
import random 
import os

# Function to check if the OS is Windows or MacOS
def check_os():
    if platform.system() not in ("Windows", "Darwin"):
        print("This script is designed to run on Windows or MacOS.")
        sys.exit(1) 
    else:
        print("Windows environment verified, continuing...")

# Function to check if the user has internet connection
def check_internet_connection_http():
    try:
        urllib.request.urlopen("https://api.pwnedpasswords.com/range/AAAAA", timeout=3)
        print("Internet connection verified...")
    except Exception:
        print("ERROR: No internet connection detected,.")
        sys.exit(1)

# Function to mask password for security reasons
def mask_password(password):
    if len(password) <= 2:
        return "*" * random.randint(3, 8)

    first = password[0]
    last = password[-1]

    mask_length = random.randint(5, 12) 
    mask = "*" * mask_length

    return f"{first}{mask}{last}"

# Function to hash password 
def hash_password(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

# Function to check password hash with the API on haveibeenpwned
def check_hash_with_api(password):
    sha1_hash = hash_password(password)
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    r = requests.get(url)
    if r.status_code != 200:
        print("API error:", r.status_code)
        return None
    for line in r.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            print(f"Your password has been leaked ({count} times).")
            validate_password(password)
            save_leaked_password(password, count)
            return True
    print("Not found in database.")
    save_leaked_password(password, 0)
    return False

# Function to save leaked password info to a text file
def save_leaked_password(password, leak_count):
    masked = mask_password(password)

    file_exists = os.path.exists("PasswordLeaked.txt")

    with open("PasswordLeaked.txt", "a", encoding="utf-8") as f:

        # Write header note only if the file is being created for the first time
        if not file_exists:
            f.write("======================================================================================================\n")
            f.write("NOTE: The programm added * to mask your password for security reasons.\n")
            f.write("So dont be alarmed if you see too many/few * in your password and focus only on first and last symbol\n")
            f.write("======================================================================================================\n")

        
        f.write(f"{masked} | Leaked: {leak_count} times\n")




# Function to validate password strength
def validate_password(Userpassword):
    has_upper = re.search(r"[A-Z]", Userpassword)
    has_digit = re.search(r"[0-9]", Userpassword)
    has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", Userpassword)
    has_length = len(Userpassword) >= 8

# Print results of the validation
    if has_upper and has_digit and has_special:
        print("The password meets the requirements.")
        return True
    else:
        print(" ❗ \033[1mThe password does not meet the safety requirements.\033[0m❗")
        if not has_upper:
            print("- ⚠️  Password is missing an uppercase letter")
        if not has_digit:
            print("- ⚠️  The password is missing a digit")
        if not has_special:
            print("- ⚠️  Password is missing a special character")
        if not has_length:
            print("- ⚠️  Password is too short (minimum 8 characters)")
        return False


                # Function to generate a strong password
def generate_password(length):
    characters = string.ascii_letters + string.digits
                    
     # List with symbols to exclude from the passwordgenerator for safety reasons
    forbidden = [' ', '"', "'", '´', '¨', '^', '<', '>', '\\', '/',',', ';', ':', '`', '~','.']
    allowed_symbols = ''.join(ch for ch in string.punctuation if ch not in forbidden)           
     # adds special characters to the pool of regular characters
    characters += allowed_symbols             
      # Generate the password randomly from the character and allowed_symbols
    return ''.join(secrets.choice(characters) for _ in range(length))

def password_generator_menu():
    while True:
        print("======================================================================================")
        print("\n--- Password Generator Menu ---")
        print("1. Generate 8-character password")
        print("2. Generate 12-character password")
        print("3. Generate 16-character password")
        print("4. Exit program")
        print("======================================================================================")
        # Stops the program from crashing if the user inputs a letter instead of a number
        try:
            choice = int(input("Choose an option (1-4): "))
            if choice < 1 or choice > 4:
                print("Invalid input. Please enter a number between 1 and 4.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue


        if choice == 1:
            print("Your new 8-character password:", generate_password(8))
            print("======================================================================================")

        elif choice == 2:
            print("Your new 12-character password:", generate_password(12))
            print("======================================================================================")

        elif choice == 3:
            print("Your new 16-character password:", generate_password(16))
            print("======================================================================================")

        elif choice == 4:
            print("Ending the program...")
            print("======================================================================================")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 4.")
            print("======================================================================================")
        while True:
            again = input("Do you want to generate another password? (y/n): ").strip().lower()
            if again == "y":
                break   # Goes back to the start of the password generator menu loop
            elif again == "n":
                print("Exiting the password generator.")
                return   # Ends the password generator menu function and returns to the main menu
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

# Function for the main menu
def main_menu():
       while True:
            print("======================================================================================")
            print("Welcome to PassLeak Peek!")
            print("This script will look through known leaked passwords and check if it can find\nyour password in any of the leaked lists.")
            print("If your password is found, it is highly recommended to change it immediately.")
            print("You can also use this tool to check the strength of your password against known leaks,")
            print("and generate a new strong password if needed.")
            print("======================================================================================")
            print("Choose an option:")
            print("1. Check a password")
            print("2. Generate a new strong password")
            print("3. What makes a strong password?")
            print("4. Why should I check my password?")
            print("5. Exit program")
            print("Type -h for help or -v for version information")
            print("======================================================================================")
            


            
            choice = input(str("Enter your choice (1, 2, 3, 4 or 5): "))
            
            if choice == "-h":
                print("\nHelp:")
                print("1 - Check if a password has been leaked")
                print("2 - Generate a secure password")
                print("-v - Show version information")
                print("-h - Show this help menu")
                continue


            if choice == "-v":
                print("\nPassLeakPeek version 1.0.10")
                print("Developed by Kim-Projects97")
                continue

            
            
            if choice == "1":
                if choice == "1":
                    while True:
                        user_password = input("Write the password you want to check and press enter: ")
                        check_hash_with_api(user_password)
                        again = input("Do you want to check another password? (y/n): ").strip().lower()
                        if again != "y":
                            print("Exiting password check. Stay safe!")
                            break
            
            elif choice == "2":
                if __name__ == "__main__":
                    password_generator_menu()
            
            # Write information about strong passwords
            elif choice == "3":
               while True:
                    print("======================================================================================")
                    print("A strong password typically includes:")
                    print("- At least 12 characters in length")
                    print("- A mix of uppercase and lowercase letters")
                    print("- Inclusion of numbers and special characters")
                    print("- Avoidance of common words or easily guessable information")
                    print("Using a combination of these elements helps enhance the security of your password.")
                    print("======================================================================================")
                    input("Press Enter to return to the main menu...")
                    break

            # Write information about why checking passwords is important   
            elif choice == "4":
                while True:
                    print("======================================================================================")
                    print("Checking your password against known leaks is crucial because:")
                    print("- It helps identify if your password has been compromised in data breaches")
                    print("- Using a leaked password puts your accounts at risk of unauthorized access")
                    print("- Regularly checking ensures you maintain strong security practices")
                    print("- It encourages the use of unique passwords for different accounts")
                    print("By staying vigilant, you can protect your personal information and online presence.")
                    print("======================================================================================")
                    input("Press Enter to return to the main menu...")
                    break

            elif choice == "5":
                print("Exiting the program. Stay safe!")
                print("======================================================================================")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4 or 5")
check_os()
check_internet_connection_http()
main_menu()