#! /usr/bin/env python3
from libs.loadconf import secrets


def verifaliaAPI(email):
    # the base url is https://api.verifalia.com/v2.4 as it removes the need
    # for implementing an auto retry system

    # rate limits are 6 https requests per second with a max burst of
    # 15 https requests per second with unlimited concurrent email verification jobs
    # if for whatever reason many emails need to be done at once use a single email job
    # this rate limit is not likely to be hit by us
    verifyURI = 'https://api.verifalia.com/v2.4/email-validations?waitTime=5000'
    authentication = HTTPBasicAuth(
        secrets['verifaliaOneID'], secrets['verifaliaOneKey'])
    headers = {'Content-Type': 'application/json'}
    data = {
        "entries": [
            {
                "inputData": f"{email}"
            }
        ]
    }
    response = requests.post(
        verifyURI, auth=authentication, headers=headers, data=json.dumps(data))
    if response.status_code == 202:
        # responds with 202 if request was queued (shouldn't happen often)
        jobID = response.json()["overview"]["id"]
        jobURI = f'https://api.verifalia.com/v2.4/email-validations/{jobID}'
        # submitting a get request to this endpoint returns information about
        # the job such as completion status and validation results for any entries
        response = requests.get(jobURI, auth=authentication)
        # if response is 202 keep checking every second until it isn't
        while response.status_code == 202:
            sleep(1)
            response = requests.get(jobURI, auth=authentication)
        # check if the job is completed
        if response.status_code == 200 and response.json()["overview"]["status"] == "Completed":
            entryData = response.json()["entries"]["data"][0]
            # these two values are all thats required to determine validity of emails
            if entryData["status"] != 'success' and entryData["classification"] != 'Deliverable':
                print("Invalid Student ID")
                print(entryData["status"])
                print(entryData["classification"])
            else:
                print("Valid Student ID")
                print(entryData["status"])
                print(entryData["classification"])

    elif response.status_code == 200:
        # will contain the verification result
        entryData = response.json()["entries"]["data"][0]
        print(response.status_code)
        if entryData["status"] != 'success' and entryData["classification"] != 'Deliverable':
            print("Invalid Student ID")
            print(entryData["status"])
            print(entryData["classification"])
        else:
            print("Valid Student ID")
            print(entryData["status"])
            print(entryData["classification"])
    else:
        print(response)  # print(response.json)
