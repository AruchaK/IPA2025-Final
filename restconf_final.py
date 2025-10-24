import os
import json
import requests
from dotenv import load_dotenv
requests.packages.urllib3.disable_warnings()

load_dotenv()

HOST = os.environ.get("ROUTER_HOST")

# Router IP Address is 10.0.15.61-65
api_url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }

basicauth = ("admin", "cisco")
studentID = "66070220"
interfaceName = "Loopback66070220"
call_url = f"{api_url}/interface={interfaceName}"
api_url_check_status = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces-state/interface={interfaceName}"


def create():
    yangConfig = {
            "ietf-interfaces:interface": {
            "name": interfaceName,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.2.20.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    resp = requests.put(
        call_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth,
        headers=headers, 
        verify=False
    )
    
    if (resp.status_code == 204):
        return "Cannot create: Interface loopback {}".format(studentID)
    elif (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback {} is created successfully".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback {}".format(studentID)


def delete():
    resp = requests.delete(
        call_url, 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json" }, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback {} is deleted successfully".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback {}".format(studentID)


def enable():
    isExist = check_interface_is_exist()
    if not (isExist):
        return "Cannot enable: Interface loopback {}".format(studentID)

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": interfaceName,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }

    resp = requests.put(
            call_url, 
            data=json.dumps(yangConfig), 
            auth=basicauth,
            headers=headers,
            verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback {} is enabled successfully".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback {}".format(studentID)


def disable():
    isExist = check_interface_is_exist()
    if not (isExist):
        return "Cannot enable: Interface loopback {}".format(studentID)

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": interfaceName,
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.put(
        call_url,
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback {} is shutdowned successfully".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback {}".format(studentID)


def status():
    resp = requests.get(
        api_url_check_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback {} is enabled".format(studentID)
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback {} is disabled".format(studentID)
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback {}".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))

def check_interface_is_exist():
    check_interface = requests.get(
        f"{api_url}/interface={interfaceName}", 
        auth=basicauth,
        headers=headers,
        verify=False
    )
    
    return not (check_interface.status_code == 404)