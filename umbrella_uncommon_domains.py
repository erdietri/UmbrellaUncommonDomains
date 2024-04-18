import requests
import csv
import zipfile
import pandas
from dotenv import load_dotenv 
import os
import pandas
import zipfile
from IPy import IP

# This script is written under the assumption that it will be run on a weekly basis.
# Access token generation also requires that the user has a valid Umbrella API Key and Secret: https://developer.cisco.com/docs/cloud-security/#!authentication/manage-api-keys

load_dotenv()

# Environmental variables should contain your org's values in .env file.
client_key = os.environ['API_KEY']
client_secret = os.environ['KEY_SECRET']

# Relevant v2 Umbrella API endpoints
base_url = "https://api.umbrella.com"
access_token_endpoint = f"{base_url}/auth/v2/token"
top_destinations_endpoint = f"{base_url}/reports/v2/top-destinations"

# Generate new access token as these expire after 1 hour. Requires a valid and unexpired Umbrella API Key and Key Secret.
def generate_access_token():

    response = requests.post(url=access_token_endpoint,auth=(client_key,client_secret))
    access_token = response.json()['access_token']

    return access_token

# Get the Top Destinations visited from 7 days ago until now. Top 1000 domains are returned.
def get_top_destinations(access_token):  
    
    headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
    } 
    
    params = {
        "from": "-7days",
        "to": "now",
        "offset": "0",
        "limit": 1000
    }
    
    top_destinations_request = requests.get(top_destinations_endpoint, headers=headers,params=params)
    top_destinations = top_destinations_request.json()

    return top_destinations


# Check that destination in Top Destinations is a domain.

def isIP(str):
    try:
        IP(str)
    except ValueError:
        return False
    return True 

# If destination in Top Destinations is a domain, write it as a new line in a CSV called top_destinations.csv.
def top_destinations_to_csv(top_destinations):

    destinations_list = []

    for destination in top_destinations['data']:
        if not isIP(destination['domain']):
            destinations_list.append(destination['domain'])

    top_destinations_csvfile = open('top_destinations.csv', 'w')

    with open('top_destinations.csv', 'w', newline='') as top_destinations_csvfile: 
        filewriter = csv.writer(top_destinations_csvfile, delimiter=',',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for destination in destinations_list: 
            filewriter.writerow([destination])
        top_destinations_csvfile.close()
                
    return top_destinations_csvfile
            
# Download the Umbrella top 1 million destinations, unzip file, format file. 
def get_top_million():

    # API call to get Umbrella Top 1 Million as a zip file
    get_top_1million_zip = requests.get("https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip")

    # Write the zip file to disk
    open('top-1m.csv.zip', 'wb').write(get_top_1million_zip.content)

    # Create a new CSV file to write the cleaned up Top 1 Million to
    top_1million_csv = 'top-1m.csv'
    
    # Unzip the file
    with zipfile.ZipFile('top-1m.csv.zip', 'r') as zip_ref: 
        zip_ref.extractall('.')
        
    # Removing rank order in first column so that we can compare domains to Top Destinations. 
    top_1million_csv = pandas.read_csv('top-1m.csv')
    first_column = top_1million_csv.columns[0]
    top_1million_csv = top_1million_csv.drop([first_column], axis=1)
    top_1million_csv.to_csv('top_1million_csv', index=False)

    return top_1million_csv
    
# Compares each domain in top_destinations.csv to top-1m.csv (Umbrella's Top 1 Million) and returns any domains that are not in the Top 1 Million.
def find_uncommon_domains():

    top_destinations_file_path = "./top_destinations.csv"
    top_1million_file_path = "./top_1million_csv"
        
    uncommon_domains_file_path = "./uncommon_domains.csv"

    with open(uncommon_domains_file_path, 'w') as uncommon_domains_csv:

        top_destinations = open(top_destinations_file_path).readlines()
        top_1million = open(top_1million_file_path).readlines()

        for domain in top_destinations:
            if domain not in top_1million: 
                uncommon_domains_csv.write(domain)

    print(f"Uncommon domains have been written to uncommon_domains.csv in your current directory.")

    return uncommon_domains_csv

# Clean up files used to determine uncommon domains.
def clean_up_files():
    os.remove('top-1m.csv.zip')
    os.remove('top-1m.csv')
    os.remove('top_destinations.csv')
    os.remove('top_1million_csv')

# Main function
def main():

    access_token = generate_access_token()
    top_destinations = get_top_destinations(access_token)
    top_destinations_csvfile = top_destinations_to_csv(top_destinations)
    cleaned_top_1million_csv = get_top_million()
    uncommon_domains_csv = find_uncommon_domains()
    clean_up_files()

    return uncommon_domains_csv

if __name__ == "__main__":
    main()