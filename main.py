import requests as re
import csv
import pandas as pd
import json
from tqdm import tqdm
import os

def main():

    APIkey = input("Enter your API key: ")
    url = input("Enter the URL for the research outputs endpoint of your Pure instance: ")
    
    get_headers = {'accept': 'application/json', 'api-key': APIkey}
    put_headers = {'accept': 'application/json', 'api-key': APIkey, "content-type": "application/json"}

    datafile = input("Enter the file path to the csv file of research outputs you would like to update (exported from Pure): ")
    uuid_col = input("Enter the name of the column in the csv file that contains the UUID for each output: ")

    while not os.path.isfile(datafile):
        print(datafile, 'is not a valid file. Please enter a valid file name (any slashes should be forward slashes and no quotation marks).')
        datafile = input("Enter the file path to the csv file of research outputs you would like to update: ")

    df = pd.read_csv(datafile, usecols = [uuid_col])

    out_folder = input("Enter a path where the program should place error logs: ")

    get_errors = open(f"{out_folder}/get_errors.txt", "w+")
    put_errors = open(f"{out_folder}/put_errors.txt", "w+")
    get_error_count = 0
    put_error_count = 0
    update_count = 0

    '''
    First, the program makes a GET request to the Pure API for each research output in the excel file. This request is made to get the current "version"
    number of the output in Pure, which is required in order to later make updates. If there is an error in the GET request, the "try - except" blocks
    will handle it and print the error to the error log then continue to the next iteration in the loop, as the PUT request would also fail in this case. 

    Next, if the GET request was a success, the program makes a PUT request for the same research output and copies the Funding Text information on the record
    to the Bibliographic Note field. 

    Finally, the program closes the error logs and prints an exit report to the console with the number of research outputs updated.
    '''

    for i in tqdm(range(len(df))):
        try:
            get_response = re.get(f'{url}{df.loc[i, uuid_col]}', headers = get_headers, timeout = 10)
            get_response.raise_for_status()
        except re.exceptions.HTTPError as errh:
            print("HTTP Error: ", errh)
            get_error_count += 1
            get_errors.write("HTTP Error: " + str(errh) + '\n' + str(get_response.status_code) + '\n' + str(get_response.url) + '\n' + str(get_response.text) + '\n' + str(get_response.headers) + '\n\n')
        except re.exceptions.ConnectionError as errc:
            print("Error Connecting: ", errc)
            get_error_count += 1
            get_errors.write("Error Connecting: " + str(errc) + '\n' + str(get_response.status_code) + '\n' + str(get_response.url) + '\n' + str(get_response.text) + '\n' + str(get_response.headers) + '\n\n')
        except re.exceptions.Timeout as errt:
            print("Timeout Error: ", errt)
            get_error_count += 1
            get_errors.write("Timeout Error: " + str(errt) + '\n' + str(get_response.status_code) + '\n' + str(get_response.url) + '\n' + str(get_response.text) + '\n' + str(get_response.headers) + '\n\n')
        except re.exceptions.RequestException as err:
            print("Something went wrong: ", err)
            get_error_count += 1
            get_errors.write("Something went wrong: " + str(err) + '\n' + str(get_response.status_code) + '\n' + str(get_response.url) + '\n' + str(get_response.text) + '\n' + str(get_response.headers) + '\n\n')
        else:
            print('get request went through...')
            print(get_response.url)

            get_response_json = get_response.json()
            version = get_response_json['version']

            funding_text = get_response_json['fundingText']['en_US']

            values = json.dumps({
                "version": version,

                "bibliographicalNote": {
                    "en_US": funding_text
                }
            })

            try:
                put_response = re.put(f'{url}{df.loc[i, uuid_col]}', headers = put_headers, data = values, timeout = 10)
                put_response.raise_for_status()
            except re.exceptions.HTTPError as errh:
                print("HTTP Error: ", errh)
                put_error_count += 1
                put_errors.write("HTTP Error: " + str(errh) + '\n' + str(put_response.status_code) + '\n' + str(put_response.url) + '\n' + str(put_response.text) + '\n' + str(put_response.headers) + '\n\n')
            except re.exceptions.ConnectionError as errc:
                print("Error Connecting: ", errc)
                put_error_count += 1
                put_errors.write("Error Connecting: " + str(errc) + '\n' + str(put_response.status_code) + '\n' + str(put_response.url) + '\n' + str(put_response.text) + '\n' + str(put_response.headers) + '\n\n')
            except re.exceptions.Timeout as errt:
                print("Timeout Error: ", errt)
                put_error_count += 1
                put_errors.write("Timeout Error: " + str(errt) + '\n' + str(put_response.status_code) + '\n' + str(put_response.url) + '\n' + str(put_response.text) + '\n' + str(put_response.headers) + '\n\n')
            except requests.exceptions.RequestException as err:
                print("Something went wrong: ", err)
                put_error_count += 1
                put_errors.write("Something went wrong: " + str(err) + '\n' + str(put_response.status_code) + '\n' + str(put_response.url) + '\n' + str(put_response.text) + '\n' + str(put_response.headers) + '\n\n')
            else:
                print('put request went through...')
                print(put_response.url)
                update_count += 1

    get_errors.write(str(get_error_count) + ' get request errors occurred')
    put_errors.write(str(put_error_count) + ' put request errors occurred')
    put_errors.close()
    get_errors.close()
    print(str(update_count) + " research outputs were updated.")

main()
