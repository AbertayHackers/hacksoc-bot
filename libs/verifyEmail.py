#! /usr/bin/env python3
from libs.loadconf import secrets
import json
import requests
from requests.auth import HTTPBasicAuth
from time import sleep


def valEmail(email, emptyWallet=""):
    accounts = ['One',
                'Two',
                'Three',
                'Four']
    credsURI = 'https://api.verifalia.com/v2.4/credits/balance'
    # check which account has an empty wallet (happens if it returns a 402)
    if emptyWallet:
        accounts.remove(emptyWallet)
    # loop each and check each accounts balances
    for accountNum in accounts:
        authentication = HTTPBasicAuth(
            secrets[f'verifalia{accountNum}ID'], secrets[f'verifalia{accountNum}Key'])
        response = requests.get(credsURI, auth=authentication)
        if response.json()["freeCredits"] >= 1:
            # either true or false
            return verifaliaAPI(email, accountNum)


def verifaliaAPI(email, accountNum):
    # the base url is https://api.verifalia.com/v2.4 as it removes the need
    # for implementing an auto retry system

    # rate limits are 6 https requests per second with a max burst of
    # 15 https requests per second with unlimited concurrent email verification
    # jobs.
    # this rate limit is not likely to be hit by us
    verifyURI = 'https://api.verifalia.com/v2.4/email-validations?waitTime=5000'
    authentication = HTTPBasicAuth(
        secrets[f'verifalia{accountNum}ID'], secrets[f'verifalia{accountNum}Key'])
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
    if response.status_code == 402:
        # responds with 402 if payment is required (when free credits run out)
        return valEmail(email, emptyWallet=accountNum)
    elif response.status_code == 202:
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
            # success and Deliverable indicate the given email address is valid
            # any other combination does not constitute a valid email address
            if entryData["status"] != 'success' and entryData["classification"] != 'Deliverable':
                # print("Invalid Student ID")
                # print(entryData["status"])
                # print(entryData["classification"])
                return False
            else:
                # print("Valid Student ID")
                # print(entryData["status"])
                # print(entryData["classification"])
                return True
        else:
            # if for whatever reason the above checks fail, return false as
            # there is likely a problem with the API... (or most likely my code)
            return False

    elif response.status_code == 200:
        # will contain the verification result
        entryData = response.json()["entries"]["data"][0]
        # success and Deliverable indicate the given email address is valid
        # any other combination does not constitute a valid email address
        if entryData["status"] != 'success' and entryData["classification"] != 'Deliverable':
            # print("Invalid Student ID")
            # print(entryData["status"])
            # print(entryData["classification"])
            return False
        else:
            # print("Valid Student ID")
            # print(entryData["status"])
            # print(entryData["classification"])
            return True
    else:
        # any other response code indicates a failure with the api or the
        # request sent to the api, therefore an email address should be
        # reported as invalid. Hopefully this would prompt someone to reach out
        # to the committee.
        return False
