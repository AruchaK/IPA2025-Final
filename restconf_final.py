import os
import json
import requests
from dotenv import load_dotenv
requests.packages.urllib3.disable_warnings()

load_dotenv()

HOST = os.environ.get("ROUTER_HOST")

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
ROUTER_USER = os.environ.get("ROUTER_USER", "admin")
ROUTER_PASS = os.environ.get("ROUTER_PASS", "cisco")
basicauth = (ROUTER_USER, ROUTER_PASS)

studentID = "66070220"
interfaceName = f"Loopback{studentID}"

def get_call_url(ip):
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces"
    call_url = f"{api_url}/interface={interfaceName}"
    return call_url

def get_url_status(ip):
    api_url_check_status = f"https://{ip}/restconf/data/ietf-interfaces:interfaces-state/interface={interfaceName}"
    return api_url_check_status

def create(ip):
    call_url = get_call_url(ip)

    isExist = check_interface_is_exist(ip)
    if isExist:
        return "Cannot create: Interface loopback {}".format(studentID)

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
        verify=False,
        timeout=10
    )
    
    if (resp.status_code == 204):
        return "Cannot create: Interface loopback {}".format(studentID)
    elif (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback {} is created successfully using Restconf".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback {}".format(studentID)


def delete(ip):
    call_url = get_call_url(ip)

    isExist = check_interface_is_exist(ip)
    if not isExist:
        return "Cannot delete: Interface loopback {}".format(studentID)

    resp = requests.delete(
        call_url, 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json" }, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback {} is deleted successfully using Restconf".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback {}".format(studentID)


def enable(ip):
    call_url = get_call_url(ip)

    isExist = check_interface_is_exist(ip)
    if not (isExist):
        return "Cannot enable: Interface loopback {}".format(studentID)

    current_status = get_interface_status(ip)
    if current_status and current_status['admin'] == 'up' and current_status['oper'] == 'up':
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
        return "Interface loopback {} is enabled successfully using Restconf".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback {}".format(studentID)


def disable(ip):
    call_url = get_call_url(ip)

    isExist = check_interface_is_exist(ip)
    if not (isExist):
        return "Cannot enable: Interface loopback {}".format(studentID)

    current_status = get_interface_status(ip)
    if current_status and current_status['admin'] == 'down' and current_status['oper'] == 'down':
        return "Cannot shutdown: Interface loopback {} (checked by Restconf)".format(studentID)

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
        return "Interface loopback {} is shutdowned successfully using Restconf".format(studentID)
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback {}".format(studentID)


def status(ip):
    api_url_check_status = get_url_status(ip)

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

def check_interface_is_exist(ip):
    call_url = get_call_url(ip)
    check_interface = requests.get(
        call_url,
        auth=basicauth,
        headers=headers,
        verify=False
    )
    
    return not (check_interface.status_code == 404)

def get_interface_status(ip):
    api_url_check_status = get_url_status(ip)
    try:
        resp = requests.get(
            api_url_check_status, 
            auth=basicauth, 
            headers=headers, 
            verify=False
        )
        
        if resp.status_code >= 200 and resp.status_code <= 299:
            response_json = resp.json()
            admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
            oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
            return {'admin': admin_status, 'oper': oper_status}
        return None
    except:
        return None