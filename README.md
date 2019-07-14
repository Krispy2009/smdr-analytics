# SMDR call log analytics

A package to help us run some analytics on our call logs we've been collecting for the past few years. By collecting I mean sending to my email and forgetting all about them.

## Installation
We use pipenv to manage virtual environments and dependencies. Just `pipenv install` to create a virtualenv if it doesn't exist and install all dependencies.

## Running the program
To actually connect to your email and download attachments sent by the iPECS you have to have some environment variables set up:
```
EMAIL_USER: your email address,
EMAIL_PASS: your password,
EMAIL_SERVER: your email host
EMAIL_FOLDER: The email folder where your SMDR attachments are
```
I use the excellent [direnv](https://direnv.net/) utility to manage my env variables per folder and keep them out of source control :)

After setting up the env variables just run `python process.py` to run the program. It doesn't do much other than download attachments at the moment but watch this space for updates!

:tada:
