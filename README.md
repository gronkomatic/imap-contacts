# imap-contacts
A Python script that connects to an IMAP server and extracts email addresses from the emails in a specified folder.

## Setup

1. Rename `.jobs.template` to `.jobs` and fill in your IMAP server details, username, password, folder, and start date in the format `YYYY-MM-DD`.

## Usage

Run the script with Python:

```sh
python imap-contacts.py
```

## Requirements
Install the required Python packages with:

```sh
pip install -r requirements.txt
```

## Note
This script only reads the email headers, it does not download the entire email.

## License
This project is open source and available under the [GNU General Public License v3.0](LICENSE).
