import csv
import email
import imaplib
import os
import zipfile
from datetime import datetime

from tqdm import tqdm

# Load settings from .jobs file
with open(".jobs", "r") as file:
    settings = file.readline().strip().split(",")

# Parse the settings
imap_server, imap_port = settings[0].split(":")
username = settings[1]
password = settings[2]
folder = settings[3]
start_date = settings[4]

# Convert the start date to a datetime object
start_date = datetime.strptime(start_date, "%Y-%m-%d")

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL(imap_server, imap_port)
imap.login(username, password)

# Select the specified folder
response = imap.select(folder)
if response[0] != "OK":
    print(f"Failed to select folder {folder}. {response[1]}. Exiting.")
    exit()

# Search for emails after the specified date
_, message_numbers = imap.search(None, f'SINCE "{start_date.strftime("%d-%b-%Y")}"')

# Create a set to store unique email addresses
email_addresses = set()

# Iterate over the message numbers
for num in tqdm(message_numbers[0].split()):
    # Fetch the email message
    _, msg_data = imap.fetch(num, "(BODY.PEEK[HEADER])")

    # Parse the email message
    email_message = email.message_from_bytes(msg_data[0][1])

    # Extract the sender's email address
    sender = email_message["From"]

    # Split the sender's email address into name and email address
    name, email_address = email.utils.parseaddr(sender)

    sender = (name, email_address)

    # Add the sender details to the set
    email_addresses.add(sender)

# Close the IMAP connection
imap.close()
imap.logout()

# Clean the folder name by removing double-quotes
folder = folder.replace('"', "")

# Save the email addresses to a CSV file
csv_file = f"{folder}-{start_date.strftime('%Y-%m-%d')}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-contacts.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email Address"])
    writer.writerows(email_addresses)

# Zip the CSV file
zip_file = f"{csv_file}.zip"
with zipfile.ZipFile(zip_file, "w") as zip:
    zip.write(csv_file)

# Remove the CSV file
os.remove(csv_file)

print(f"Contact list saved to {zip_file}")
