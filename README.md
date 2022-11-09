# CES SMTP Bounce Code Retrieval

This script retrieves the SMTP code information for bounced emails reported by CES. The code is appended to existing reports, centralizing information for bounced emails at scale.

## Contacts
* Trevor Maco
* Jorge Banegas

## Solution Components
* CES (AsyncOS 14.2)
* Python 3.10


## Installation/Configuration

1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_ces_smtp_bounce_code` and open the directory of the root repository.

2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).

3. Install the required Python libraries with the command:
   ``` bash
   pip3 install -r requirements.txt
   ```

4. Ensure the API is enabled and configured on the Secure Cloud Email and Web Manager dashboard.

    <br />**Note**: This may be enabled already by default with url: `<sma dashboard url>` and port: `4431`. Try this first before consulting the instructions.

    <br />Instructions for enabling the API can be found [here](https://www.cisco.com/c/en/us/td/docs/security/security_management/sma/sma14-2/api_getting_started_guide/b_sma_api_guide_14_2/m_overview_of_sma_apis.html) under the `Enabling AsyncOS API` section (best practice is to use the management IP/port).

5. In `config.py` add the sma url and port from step 4. Add the credentials of a administrator, email administrator, cloud administrator, or operator account.
    
    ``` python
    BASE_URL = "<url>" # Url
    BASE_PORT = "<port>" # Port
    USERNAME = "<username>" # Username
    PASSWORD = "<password>" # Password
    ```


## Usage

1. Before running this script, obtain the input csv file from CES with the following steps (refer to the screenshots for more information):

   1. Access the dashboard and navigate to `Tracking`
   2. Apply any necessary filters plus the 'Hard Bounced' filter to get bounced emails.
   3. Click the top right drop down menu on the page and click `All Results` to download a csv file of your filtered messages.

2. Copy the csv file to the main project folder.
   * **Note**: The field we are interested in is the 'Last State' field (seen in the input data screenshot)

3. To run the script enter the command followed by the csv file.

    ``` bash
    python3 main.py sample.csv
    ```

4. An output file is generated called `bounced_messages.csv`, which contains a similar report to that which was downloaded. However, this report has the bounce message and smtp code in the 'Last State' field (seen in output data screenshot)

# Additional Resources

* Async OS
  * Async API: https://www.cisco.com/c/en/us/td/docs/security/security_management/sma/sma14-2/api_getting_started_guide/b_sma_api_guide_14_2/m_overview_of_sma_apis.html
  * Async API Supporting Documents: https://www.cisco.com/c/en/us/support/security/email-security-appliance/products-programming-reference-guides-list.html
* Python: 
  * Main Tutorial: https://www.w3schools.com/python/

# Screenshots

Message Tracking page:

![/IMAGES/Message_Tracking.png](/IMAGES/Message_Tracking.png)

Apply message filters:

![/IMAGES/Message_Filters.png](/IMAGES/Message_Filters.png)

Download messages returned from query (applying any filters as necessary):

![/IMAGES/Download_CSV.png](/IMAGES/Download_CSV.png)

Sample csv input data downloaded from Email and Web Manager dashboard:

![/IMAGES/Input_Data.png](/IMAGES/Input_Data.png)

Sample csv output with bounced message and smtp code:

![/IMAGES/Output_Data.png](/IMAGES/Output_Data.png)

![/IMAGES/0image.png](/IMAGES/0image.png)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
