# UmbrellaUncommonDomains
This script allows Cisco Umbrella users to better understand their DNS traffic. The script retrieves the Top Destinations reported by your Umbrella account over the past week (up to 1000 domains), filters for domains only (no IP addresses), and compares it to Umbrella's Top 1 Million Domains. The result is a CSV containing "uncommon domains" in your network, aka, DNS requests in your network that are not part of Umbrella's Top 1 Million. 

## Use Case
Umbrella customers have a vested interest in DNS visibility and security. While most companies could use assistance filtering the massive amounts of internet traffic going in and out of their network, this particular use case was inspired by the aftermath of the <a href="https://www.bbc.com/news/technology-57063636">2021 colonial pipeline attack in the U.S.</a>

Afterward, the TSA issued (and has since re-issued) a <a href="https://www.tsa.gov/sites/default/files/tsa-sd-pipeline-2021-02d-w-memo_07_27_2023.pdf">Security Directive</a> for oil and natural gas pipeline cybersecurity that challenged utility companies to better understand their DNS traffic.

Umbrella customers using this script can quickly and easily discover uncommon DNS requests to proactively investigate without the overwhelm.

## Requirements
* Access to active Cisco Umbrella account OR Cisco DevNet Umbrella sandbox:
* Umbrella Admin API key with minimum scope of Reports > Aggregation (Read-Only).
* VS Code 1.87.0 (or IDE of your choice)
* Python 3.12.1
* Python libraries listed in '''requirements.txt''' (see below, Run Project, to install)

## Installation & Usage
### Install VS Code & Python
* If you do not have VS Code or another IDE, you may download and install VS Code for your OS here: ```https://code.visualstudio.com/download```.
* If you do not have Python3, choose your OS and download python here: ```https://www.python.org/downloads/```. Then, follow the installation instructions here based on your OS: ```https://kinsta.com/knowledgebase/install-python/#how-to-install-python```.

### Create Umbrella Admin API Key
1. Login to the Umbrella dashboard:
 * Umbrella customers: ```https://login.umbrella.com/```
 * Umbrella sandbox users: ```https://devnetsandbox.cisco.com/DevNet/catalog/umbrella-secure-internet-gateway```
2. In the leftside menu, navigate to Admin > API Keys
3. Click the plus symbol in the top right of the screen that says “Add.”
4. For the Key Scope, at a minimum, you’ll need to check Reports > Aggregation with Read-Only Access.
5. Choose a date that isn't today for the API expiration date (or click “Never expires”).
6. Save the generated API Key and Key Secret, as we will be using this in the project.
    
### Run Project
* Clone this repository:
```git clone https://github.com/erdietri/UmbrellaUncommonDomains.git```
* Navigate to the project directory:
```cd umbrellauncommondomains```
* Install the dependencies:
```pip install -r requirements.txt```
* Add your API Key and Key Secret values to the .env file. (Simply copy/paste. They do not need to be formatted as strings.)
* Run the Python script:
```python3 umbrella_uncommon_domains.py```
* Upon completion, the terminal will display the message "Uncommon domains have been written to uncommon_domains.csv in your current directory." You should see a CSV named uncommon_domains.csv in the same directory, which you can open to see your network's uncommon domains.

## Testing
This script has been tested on Windows 11 and Sanoma 14.3 (Mac) but should work on any OS. This repository contains an example of the resulting output after running this script called example_uncommon_domains.csv.

## Contributors
Erika Dietrick

## License
Copyright 2024 Erika Dietrick

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

