import requests, json
from libs.loadconf import getEnv, secrets, config

def genInvite():
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bot {secrets['token']}"
    }
    params = {
        "max_age":config["inviteExpireTime"]
    }
    channel = getEnv("channel", "welcome")
    r = (requests.post(f"https://discordapp.com/api/v6/channels/{channel}/invites", json=params, headers=headers).text)
    try:
        r = json.loads(r)
    except:
        return False
    return r["code"]
