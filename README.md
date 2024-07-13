# GmailAttachmentDownload

1. Set up a Google Cloud project and enable the Gmail API:
    - Go to the Google Cloud Console.
    - Create a new project.
    - Enable the Gmail API for your project.
        - Go to the API Library.
        - In the search bar, type "Gmail API" and select it from the results.
        - Click the Enable button.
    - Create OAuth 2.0 credentials for desktop applications.
    - Download the credentials JSON file
    - Rename the file to credentials.json

2. Setup virtualenv and install necessary Python libraries:

3. In download.py change address you want to search (currently expale@gmail.com) and directory to where you want download attachments (currently attachments).

4. Make sure you have the credentials.json file in the same directory as your script.

5. Run python download.py