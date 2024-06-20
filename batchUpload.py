
# Reference Documents: 
#  API Doc: https://kc.kobotoolbox.org/hmercader/submission
#            https://kc.kobotoolbox.org/api/v1/?format=json
#  Youtube Video: https://www.youtube.com/watch?v=9q3kVr4m7LY
#  Forum Post: https://community.kobotoolbox.org/t/error-500-on-data-import-with-python/43200

## Generate UUID in LibreOffice with the following Calc:
## =LOWER(CONCATENATE(DEC2HEX(RANDBETWEEN(0,4294967295),8),"-",DEC2HEX(RANDBETWEEN(0,65535),4),"-",DEC2HEX(RANDBETWEEN(0,65535),4),"-",DEC2HEX(RANDBETWEEN(0,65535),4),"-",DEC2HEX(RANDBETWEEN(0,4294967295),8),DEC2HEX(RANDBETWEEN(0,65535),4)))

import requests
import json
import uuid
import csv
from pprint import pprint
import time


def create_uuid():
    return str(uuid.uuid4())

def post_data_to_kobo(formId, formUUID, submissionData, config):
    print("Uploading item number " + str(index))
    url = config["submissionURL"]
    auth = (config["username"], config["password"])

    submissionData["id"] = formId
    submissionData["submission"]["formhub"] = {"uuid": formUUID}

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=submissionData, auth=auth, headers=headers)

        if response.status_code == 201:
            print("Data submission successful!")
        else:
            print(f"Data submission failed with status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred during the data submission:")
        print(e)

def csvToDict(csvFile):
    data = []

    with open(csvFile, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        data = list(csvReader)
    
    return data

def formatKeys(data):
    newDict = {"submission": {}}
    for key in data:
        if "remove" not in key:
            if "/" in key:
                newKeys = key.split("/")
                
                if newKeys[0] == "meta":
                    newDict["submission"][newKeys[0]] = {}
                    newDict["submission"][newKeys[0]][newKeys[1]] = data[key]
                else:
                    if newKeys[0] not in newDict["submission"]:
                        newDict["submission"][newKeys[0]] = {}

                    newDict["submission"][newKeys[0]][newKeys[1]] = data[key]
            
            else:
                newDict["submission"][key] = data[key]

    return newDict

def printForms(config):
    url = config["koboToolboxUrl"]
    auth = (config["username"], config["password"])

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        print("form MetaData request successful!")
        data = response.json()
        pprint(data)
    else:
        print(f"form MetaData request failed with status code: {response.status_code}")
        print(response.text)

    for form in data:
        if form["title"] == title:
            metaData = {"title": title,
                        "formId": form["id_string"],
                        "formUUID": form["uuid"]}
    pprint(metaData)
    return(metaData)          

def getFormMetaData(formData):
    metaData = {"title": formData["title"],
                "formId": formData["id_string"],
                "formUUID": formData["uuid"]}
    pprint(metaData)
    return(metaData)

def getAllForms(config):

    print("fetching list of all forms that you have access to...")
    url = config["koboToolboxUrl"]
    auth = (config["username"], config["password"])

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        print("form MetaData request successful!")
        data = response.json()
        # pprint(data)
    else:
        print(f"form MetaData request failed with status code: {response.status_code}")
        print(response.text)
        exit()  


    return(data)
    
def printAllForms(forms):
    print("index   id                           Title")
    index = 0
    for form in forms:
        print(f'{index}\t{form["id_string"]}\t\t{form["title"]}')
        index+=1
 

if __name__ == "__main__":
    

########  ----------------------------------------------------------------------
    ## Load env data
    with open(".env") as f:
        config = json.load(f)
    
    submissionDataFile = config["dataFile"]

########  ----------------------------------------------------------------------






    forms = getAllForms(config)
    printAllForms(forms)

    formIndex = int(input("Which form would you like to upload data to?  Select the index number: "))

    if (input(f"\n\nyou have selected {forms[formIndex]['title']}.  Is this correct? (Y/N)")).lower() != "y":
        print("please start again!, good bye")
        exit()
    
    # print("Retrieving details about form " + formTitle)
    formMetaData = getFormMetaData(forms[formIndex])

    submissionData = csvToDict(submissionDataFile)
 
    cleansedData = []
    for item in submissionData:
      cleansedData.append(formatKeys(item))
    
    input("'\n\n\n\nPress [enter] if you would like to continue...\n\n\n\n")
    index = 0
    for data in cleansedData:
      

      post_data_to_kobo(formMetaData["formId"], formMetaData["formUUID"], data, config)
      time.sleep(0.1)
      index+=1

