import requests
import csv
from datetime import time 
from time import time
import zipfile
import os.path

organization_id = ""
destinations_url = "https://reports.api.umbrella.com/v2/organizations/" + organization_id + "/top-destinations/dns"
client_id = ""
client_secret = ""
token_url = "https://management.api.umbrella.com/auth/v2/oauth2/token"

# Retrieve access_token from Umbrella Management API; lasts 1 hour.
def get_access_token():
    response = requests.post(url=token_url,auth=(client_id,client_secret))
    access_token = response.json()['access_token']
    return access_token

# Get the Top Destinations visited. 
def get_top_destinations(access_token):  
    
    headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
    } 
    
    # Current time in Epoch ms
    current_time = time() * 1000
    # Epoch ms since Monday
    past_week_time = current_time - (604800 * 1000)
    # Determine what limit should be - must be an integer

    params = {
        "from": int(past_week_time),
        "to": int(current_time),
        "offset": "0",
        "limit": 10
    }
    
    top_destinations = requests.get(destinations_url, headers=headers,params=params)
    response_data = top_destinations.json()    
    return response_data
        
# Write each domain in Top Destinations as a new line in a CSV.
def write_top_destinations(response_data):

        csvfile = open('dest_list.csv', 'w')
        filewriter = csv.writer(csvfile, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for domain in response_data['data']: 
            print(domain['domain'])
            filewriter.writerows(domain['domain'])
        csvfile.close()
        
        return csvfile
            
# Download the Umbrella top 1 million destinations. 
def get_top_million(): 
    file_path = 'C:\\Users\\erdietri\\Downloads\\'
    get_file = requests.get("http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip")
    top_million = os.path.join(file_path, 'top-1m.csv.zip')
    
    ##################################
    ##################################
    # How do I figure out how to save the file to my desktop so that I can unzip it???
    with zipfile.ZipFile('C:\\Users\\erdietri\\Downloads\\top-1m.csv.zip', 'r') as zip_ref: 
        zip_ref.extractall('C:\\Users\\erdietri\\Downloads')
    
    return top_million       
    
# Iterates over the top 1 million csv_file to determine if any Top Destinations do not match; returns those that do not match.
def iterator(csvfile, top_million):
    with open ("dest_list.csv", 'r') as f1, open("top_million", 'r') as f2:
        fileone = f1.readlines()
        filetwo = f2.readlines() 
    with open("differences.csv", 'w') as output: 
        for line in fileone: 
            if line not in filetwo: 
                output.write(line)        
    print(output)
    return output

top_million = get_top_million()
#access_token = get_access_token()
#response_data = get_top_destinations(access_token)
#csvfile = write_top_destinations(response_data)
#output = iterator(csvfile,top_million)
