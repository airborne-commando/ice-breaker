import random
import string
import os
from datetime import datetime, timedelta

# Path to the local file for storing names
local_file_path = "first-names.txt"

# Function to load names from the local file
def load_names(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        print("Please download the file from the following URL and place it in the same directory as this script:")
        print("https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/fea1da1a3c4ce5c8e470f679a8e1bc741281a609/first-names.txt")
        exit(1)
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Load names from the local file
first_names = load_names(local_file_path)
last_names = first_names  # Assuming the same file contains both first and last names

# List of U.S. states for state of birth (SOB)
states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

domains = [
    "earthlink.net", "verizon.net", "msn.com", "yahoo.com", "aol.com", 
    "protonmail.com", "icloud.com", "outlook.com", "zoho.com", "mail.com", 
    "yandex.com", "fastmail.com", "rocketmail.com", "gmx.com", "tutanota.com", 
    "mail.ru", "hushmail.com", "guerrillamail.com", "inbox.com", "sendinblue.com", 
    "lavabit.com", "lycos.com", "aol.co.uk", "myway.com", "bluebottle.com", 
    "unseen.is", "chime.com", "walla.com", "mindspring.com", "gawab.com", 
    "openmailbox.org", "rediffmail.com", "epix.net", "gmail.com", "hotmail.com", 
    "live.com", "yahoo.co.uk", "icloud.co.uk", "outlook.co.uk", "mailchimp.com", 
    "zoho.co.uk", "aol.com.au", "msn.co.uk", "seznam.cz", "t-online.de", 
    "orange.fr", "bellsouth.net", "comcast.net", "btinternet.com", "charter.net", 
    "cox.net", "shaw.ca", "telus.net", "sbcglobal.net", "att.net", "roadrunner.com",
    
    # Government Domains
    "usa.gov", "gov.uk", "canada.ca", "gov.au", "gov.in", "gov.sg", 
    "gov.za", "gov.ph", "gov.br", "gov.de", "gov.fr", "gov.it", "gov.jp",
    
    # Military Domains
    "army.mil", "navy.mil", "af.mil", "usmc.mil", "uscg.mil", "spaceforce.mil",
    
    # Educational Domains
    "harvard.edu", "stanford.edu", "mit.edu", "ox.ac.uk", "cam.ac.uk", 
    "berkeley.edu", "umich.edu", "columbia.edu", "yale.edu", "princeton.edu", 
    "ucla.edu", "nyu.edu", "utexas.edu", "uchicago.edu", "upenn.edu",
    "caltech.edu", "duke.edu", "northwestern.edu", "uw.edu", "gatech.edu",
]

# Function to generate a random email
def generate_email(first_name, last_name):
    domain = random.choice(domains)
    email_format = random.choice([f"{first_name}.{last_name}", f"{first_name}{last_name}", f"{first_name[0]}{last_name}"])
    email = f"{email_format}@{domain}"
    return email.lower()

# Function to generate a random password
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password_length = random.randint(8, 16)
    password = "".join(random.choices(chars, k=password_length))
    return password

# Function to generate a random reasonable DOB (between 18 and 70 years ago)
def generate_dob():
    today = datetime.today()
    start_date = today - timedelta(days=70 * 365)  # 70 years ago
    end_date = today - timedelta(days=18 * 365)    # 18 years ago
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

# Function to generate a random state of birth (SOB) with a 50% chance
def generate_sob():
    if random.random() < 0.5:  # 50% chance
        return random.choice(states)
    return "N/A"  # Return "N/A" if no SOB is generated

# Function to generate a random phone number
def generate_phone_number():
    if random.random() < 0.7:  # 70% chance
        return f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    return "N/A"  # Return "N/A" if no phone number is generated

# Function to generate a random 9-digit number with heavy obscuration
def generate_9_digit_number():
    if random.random() < 0.5:  # 50% chance
        number = f"{random.randint(100000000, 999999999)}"
        # Replace 6 out of 9 digits with *
        indices_to_obscure = random.sample(range(9), 6)  # Randomly select 6 indices to obscure
        number_list = list(number)
        for index in indices_to_obscure:
            number_list[index] = "*"
        return "".join(number_list)
    return "N/A"  # Return "N/A" if no 9-digit number is generated

# Function to generate a single line of fake data
def generate_line():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = generate_email(first_name, last_name)
    password = generate_password()
    dob = generate_dob()
    sob = generate_sob()
    phone_number = generate_phone_number()
    nine_digit_number = generate_9_digit_number()
    return f"{first_name} {last_name} | {email} | {password} | {dob} | {sob} | {phone_number} | {nine_digit_number}\n"

# Function to generate a file of a specified size
def generate_file(filename, size_bytes):
    with open(filename, "w") as file:
        written_size = 0
        while written_size < size_bytes:
            line = generate_line()
            file.write(line)
            written_size += len(line.encode("utf-8"))  # Account for byte size
            print(f"Written: {written_size / (1024 * 1024):.2f} MB", end="\r")

# Run the script
if __name__ == "__main__":
    # Ask the user for the desired file size
    size_input = float(input("Enter the desired file size (e.g., 1 for 1GB, 0.5 for 500MB, 0.1 for 100MB): "))
    
    # Convert the size to bytes and determine the appropriate unit for the filename
    if size_input >= 1:
        size_bytes = size_input * 1024 * 1024 * 1024  # Convert GB to bytes
        size_label = f"{int(size_input)}gb" if size_input.is_integer() else f"{size_input}gb"
    else:
        size_bytes = size_input * 1024 * 1024  # Convert MB to bytes
        size_label = f"{int(size_input * 1000)}mb" if (size_input * 1000).is_integer() else f"{size_input * 1000}mb"
    
    # Adjust the filename based on the size
    filename = f"fake_data_{size_label}.txt"
    
    print(f"Generating {size_label.upper()} of fake data in '{filename}'...")
    generate_file(filename, size_bytes)
    print("\nDone! File generated successfully.")
