import requests
import csv
from datetime import time 
from time import time
import zipfile
import os.path


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
    print(response_data)  
    return response_data
        
# Write each domain in Top Destinations as a new line in a CSV.
def write_top_destinations(response_data):

    dest_list = []
    for domain in response_data['data']: 
        dest_list.append(domain['domain'])
    csvfile = open('C:\\dest_list.csv', 'w')
    with open('C:\\dest_list.csv', 'w', newline='') as csvfile: 
        filewriter = csv.writer(csvfile, delimiter=',',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for domain in dest_list: 
            filewriter.writerow([domain])
        csvfile.close()
        
    return csvfile
            
# Download the Umbrella top 1 million destinations to C: and unzip file. 
def get_top_million(): 
    file_path = 'C:\\'
    get_file = requests.get("http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip")
    top_million_zip = os.path.join(file_path, 'top-1m.csv.zip')
    top_million = os.path.join(file_path, 'top-1m.csv')
    
    with open(top_million_zip, 'wb') as f: 
        f.write(get_file.content)
        
    with zipfile.ZipFile(top_million_zip, 'r') as zip_ref: 
        zip_ref.extractall(file_path)
        
    #with open(top_million, 'w') as edit: 
    data = pandas.read_csv(top_million)
    first_column = data.columns[0]
    # Delete first
    data = data.drop([first_column], axis=1)
    data.to_csv(top_million, index=False)
    return data       
    
# Iterates over the top 1 million csv_file to determine if any Top Destinations do not match; returns those that do not match.
def iterator():
    f1path = "C:\\dest_list.csv"
    f2path = "C:\\top-1m.csv"
    
    #df1 = pandas.read_csv("C:\\dest_list.csv")
    #df2 = pandas.read_csv("C:\\top-1m.csv")
    #a = df1[df1.eq(df2).all(axis=1) == False]
    #a.index += 1
    #result = a.to_string(index=False)
        
    finalpath = "C:\\differences.csv"
    with open(finalpath, 'w') as output:
        fileone = (open(f1path)).readlines()
        filetwo = (open(f2path)).readlines()
        for line in fileone:
            print(line)
            if line not in filetwo: 
                output.write(line)
        #for line in fileone: 
            #if line not in filetwo: 
                #output.write(line)  
        #file_path = 'C:\\differences.csv'
        #differences = os.path.join(file_path, 'differences.csv')
        print(output)
    return output

final = get_top_million()
access_token = get_access_token()
response_data = get_top_destinations(access_token)
csvfile = write_top_destinations(response_data)
output = iterator()
