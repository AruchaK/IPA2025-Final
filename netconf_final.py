# --------------------------------------------------------------
# Import libraries and connect to device
# --------------------------------------------------------------

from ncclient import manager
from dotenv import load_dotenv
import xmltodict
import os

load_dotenv()
ROUTER_USER = os.environ.get("ROUTER_USER")
ROUTER_PASS = os.environ.get("ROUTER_PASS")
STUDENT_ID = "66070220"
INTERFACE_NAME = f"Loopback{STUDENT_ID}"

def connect(ip):
    return manager.connect(host=ip, port=830, username=ROUTER_USER, password=ROUTER_PASS, hostkey_verify=False, timeout=10)

# --------------------------------------------------------------
# Core functions
# --------------------------------------------------------------

# Create Loopback66070220 interface
def create(ip):
    # Define Netconf configuration for creating Loopback66070220 interface
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{INTERFACE_NAME}</name>
                    <description>{STUDENT_ID} Loopback interface</description>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>172.2.20.1</ip>
                            <netmask>255.255.255.0</netmask>
                        </address>
                    </ipv4>
                </interface>
            </interfaces>
        </config>
    """

    try:
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception(f"Cannot create: Interface loopback {STUDENT_ID}")
        with connect(ip) as m:
            netconf_reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in str(netconf_reply): 
                return f"Interface loopback {STUDENT_ID} is created successfully using Netconf"
        return f"Cannot create: Interface loopback {STUDENT_ID}"
    except: 
        return f"Cannot create: Interface loopback {STUDENT_ID}"


# Delete Loopback66070220 interface
def delete(ip):
    # Define Netconf configuration for deleting Loopback66070220 interface
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>{INTERFACE_NAME}</name>
                </interface>
            </interfaces>
        </config>
    """

    try:
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception(f"Cannot delete: Interface loopback {STUDENT_ID}")
        with connect(ip) as m:
            netconf_reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in str(netconf_reply): 
                return f"Interface loopback {STUDENT_ID} is deleted successfully using Netconf"
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
    except: return f"Cannot delete: Interface loopback {STUDENT_ID}"


# Enable Loopback66070220 interface
def enable(ip):
    # Define Netconf configuration for enabling Loopback66070220 interface
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{INTERFACE_NAME}</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>true</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception(f"Cannot enable: Interface loopback {STUDENT_ID}")
        with connect(ip) as m:
            netconf_reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in str(netconf_reply): 
                return f"Interface loopback {STUDENT_ID} is enabled successfully using Netconf"
        return f"Cannot enable: Interface loopback {STUDENT_ID}"
    except: 
        return f"Cannot enable: Interface loopback {STUDENT_ID}"

# Enable Loopback66070220 interface
def disable(ip):
    # Define Netconf configuration for disabling Loopback66070220 interface
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{INTERFACE_NAME}</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>false</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception(f"Cannot shutdown: Interface loopback {STUDENT_ID}")
        with connect(ip) as m:
            netconf_reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in str(netconf_reply): 
                return f"Interface loopback {STUDENT_ID} is shutdowned successfully using Netconf"
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"
    except: 
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"



# Get status of Loopback66070220 interface
def status(ip):
    # Define Netconf filter to get interfaces-state information for Loopback66070220
    netconf_filter = f"""
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>{INTERFACE_NAME}</name></interface>
            </interfaces-state>
        </filter>
    """

    try:
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception(f"No Interface loopback {STUDENT_ID} (checked by Netconf)")
        with connect(ip) as m:
            netconf_reply = m.get(filter=netconf_filter)
            netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
            if not (netconf_reply_dict["rpc-reply"]["data"] == None):
                admin_status = netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]["admin-status"]
                oper_status = netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]["oper-status"]
                if admin_status == 'up' and oper_status == 'up':
                    status = "enabled"
                elif admin_status == 'down' and oper_status == 'down':
                    status = "disabled"
                return f"Interface loopback {STUDENT_ID} is {status} (checked by Netconf)"
            else:
                return f"No Interface loopback {STUDENT_ID} (checked by Netconf)"
    except: 
        return f"No Interface loopback {STUDENT_ID} (checked by Netconf)"

# --------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------

# Check if interface Loopback66070220 exists
# Returns: True if exists, False otherwise
def check_interface_exist(ip):
    findInterface = f"""
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>{INTERFACE_NAME}</name></interface>
            </interfaces>
        </filter>
    """
    try:
        with connect(ip) as m:
            interfaceResult = m.get_config(source="running", filter=findInterface).xml
            return (INTERFACE_NAME in interfaceResult)
    except: 
        return False