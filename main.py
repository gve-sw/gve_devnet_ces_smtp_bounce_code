# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Trevor Maco <tmaco@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Imports
from urllib.error import HTTPError
from dotenv import load_dotenv
import requests, os, base64, csv, sys, json


# load environment variables
load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
BASE_URL = os.getenv('BASE_URL')
BASE_PORT = os.getenv('BASE_PORT')

# Generate base64 encoded string for API request headers
usernamePassword = f"{USERNAME}:{PASSWORD}"
b64Val = base64.b64encode(usernamePassword.encode()).decode()

# Base Url
base_url = f'https://{BASE_URL}:{BASE_PORT}/sma/api/v2.0/'
   
# Read csv data
def read_csv(filename):

    print(f'Reading {filename}...')

    with open(filename, 'r') as file:
        csv_data = csv.DictReader(file)

        # Extract each row of data (representing a bounced email)
        emails = []
        for email in csv_data:
            emails.append(email)

    print(f'{filename} successfully read')

    return emails

# Obtain individual message details
def get_message_details(mid, hostname):
    message_url = 'message-tracking/details'
    headers = {"Accept": 'application/json', "Authorization": "Basic %s" % b64Val}
    
    # Extract mid and hostname for message 
    query_parms = {'mid': mid, 'hostName': hostname}
    
    try:
        # API call provides details about message (from host name, sender ip, message trace, etc.)
        response = requests.get(url=f'{base_url}{message_url}', headers=headers, params=query_parms)
        
        if response.status_code == 200:
            print(f'GET {mid} message details successful!')
            return response.json()['data']
        else:
            print(f'GET message failed: {response.text}')
            sys.exit(1)
    except HTTPError as e:
        print(f'Connection Error: {e}')
        sys.exit(1) 
        
  
# Update the 'last state' to be the final bounce state (showing bounce message and SMTP code)
def process_email(writer, email):
     
    # Get list of MIDs
    mids = [mid.strip() for mid in email['MID'].split(',')]
    
    # get hostname
    hostname = email['Host'].split(' ')[0]
    
    # Check every MID for bounce messages
    for mid in mids:
           
        # Error check
        if not mid.isdigit():
            print('Error: mid id not an integer!')
            return
    
        print(f'mid:hostname - {mid}:{hostname}')
    
        # get message trace (showing the exchange of messages)
        message_trace = get_message_details(mid, hostname)['messages']
        
        # Flag to control if we are on the right MID or not
        bounce_flag = False
        
        # Check each message per MID
        for message in message_trace['summary']:
            description = message['description']
            
            # If we find 'bounce' int he description
            if 'bounced' in  description:
                # clear last state field
                email['Last State'] = ''        
                        
                email['Last State'] = email['Last State'] + description + '\n'
                
                bounce_flag = True
          
        # If we are on the right mid, no need to process the rest!   
        if bounce_flag:
            break
                    
    # Print message contents 
    print(json.dumps(email, sort_keys=False, indent=4))
    
    # write processes message to csv
    writer.writerow(email)

 
def main(): 
    
    # Sanity checking a csv file was provided
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.csv'):
        print('Error: please input a valid.csv file')
        sys.exit(1)
    
    # filename is set from CLI argument
    filename = sys.argv[1]
    
    # Read in csv data
    emails = read_csv(filename)
             
    # csv headers (fields based on downloadable report from GUI)
    fieldnames = list(emails[0].keys())
    
    # Read the input csv and open the new csv file 
    with open('bounced_messages.csv', 'w') as fp:        
        # Create csv writer
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        
        # Create csv file headers
        writer.writeheader()
        
        # Iterate through each returned message, process the message
        for email in emails:
            process_email(writer, email)
            
        print('bounced_messages.csv written!')
         
    print('All emails processed!')
       
                   
    
if __name__ == "__main__":    
    main()