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
