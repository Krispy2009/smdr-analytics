# SMDR call log analytics

A package to help us run some analytics on our call logs we've been collecting for the past few years. By collecting I mean sending to my email and forgetting all about them :sweat_smile:

## Installation
Create or activate your virtualenv and then run `pip install -r requirements.txt`.
If you want some additional dev dependencies: `pip install -r requirements_dev.txt` 


## Running the program
To actually connect to your email and download attachments sent by the iPECS you have to have some environment variables set up in a `.env` or `.envrc` file:
```
export EMAIL_USER="your email address"
export EMAIL_PASS="your password"
export EMAIL_SERVER="your email server"
export EMAIL_FOLDER="the folder emails are in"
```
I use the excellent [direnv](https://direnv.net/) utility to manage my env variables per folder and keep them out of source control :slightly_smiling_face:

After setting up the env variables just run `python process.py` to run the program. 

:tada:
