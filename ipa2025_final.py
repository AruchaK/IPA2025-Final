#######################################################################################
# Yourname: Arucha Khematharonon
# Your student ID: 66070220
# Your GitHub Repo: https://github.com/AruchaK/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import os
import time
import json
import requests
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder
from enum import Enum

import restconf_final
import netconf_final
from netmiko_final import get_motd
from ansible_banner import set_motd
import glob

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

load_dotenv()

ACCESS_TOKEN = os.environ["WEBX_ACCESS_TOKEN"]

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

class Method(Enum):
    RESTCONF = "restconf"
    NETCONF = "netconf"

current_method = None


# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    os.environ["ROOM_ID"]
)

def is_ip(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        num = int(p)
        if num < 0 or num > 255:
            return False
    return True

def validate_ip(ip):
    """Validate if IP is in range 10.0.15.61-65"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        if parts[0] == '10' and parts[1] == '0' and parts[2] == '15':
            last_octet = int(parts[3])
            return 61 <= last_octet <= 65
        return False
    except:
        return False

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer " + ACCESS_TOKEN}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070220"):

        parts = message.split()

        if len(parts) == 1:
            responseMessage = "Error: No method specified"
        # Check if method selection (restconf/netconf)
        elif len(parts) == 2:
            method_str = parts[1].lower()
            if method_str == "restconf":
                current_method = Method.RESTCONF
                responseMessage = "Ok: Restconf"
            elif method_str == "netconf":
                current_method = Method.NETCONF
                responseMessage = "Ok: Netconf"
            elif is_ip(method_str):
                responseMessage = "Error: No command found"
            elif method_str in ["create", "delete", "enable", "disable", "status", "showrun", "gigabit_status"]:
                responseMessage = "No IP specified"
            else:
                responseMessage = "Error: No command found"

        elif len(parts) == 3:
            ip = parts[1]
            command = parts[2]

            if not validate_ip(ip):
                responseMessage = "Error: IP out of range"
            elif command == "motd":
                responseMessage = get_motd(ip)
            elif current_method is None:
                responseMessage = "Error: No method specified"
            else:
                if current_method == Method.RESTCONF:
                    if command == "create":
                        responseMessage = restconf_final.create(ip)
                    elif command == "delete":
                        responseMessage = restconf_final.delete(ip)
                    elif command == "enable":
                        responseMessage = restconf_final.enable(ip)
                    elif command == "disable":
                        responseMessage = restconf_final.disable(ip)
                    elif command == "status":
                        responseMessage = restconf_final.status(ip)
                    else:
                        responseMessage = "Error: Unknown command"
                elif current_method == Method.NETCONF:
                    if command == "create":
                        responseMessage = netconf_final.create(ip)
                    elif command == "delete":
                        responseMessage = netconf_final.delete(ip)
                    elif command == "enable":
                        responseMessage = netconf_final.enable(ip)
                    elif command == "disable":
                        responseMessage = netconf_final.disable(ip)
                    elif command == "status":
                        responseMessage = netconf_final.status(ip)
                    else:
                        responseMessage = "Error: Unknown command"
        elif len(parts) >= 4:
            ip = parts[1]
            command = parts[2]
            motd_message = " ".join(parts[3:])

            if not validate_ip(ip):
                responseMessage = "Error: IP out of range"
            else:
                if command == "motd":
                    responseMessage = set_motd(ip, motd_message)
                    print(f"Set motd response: {responseMessage}")
                else:
                    responseMessage = "Error: Unknown command"

        # other commands only send text, or no attached file.
        postData =  {"roomId": roomIdToGetMessages, "text": responseMessage}
        postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        HTTPHeaders = {
            "Authorization": "Bearer " + ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
