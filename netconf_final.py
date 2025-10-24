# --------------------------------------------------------------
# Import libraries and connect to device
# --------------------------------------------------------------

from ncclient import manager
from dotenv import load_dotenv
import xmltodict
import os

load_dotenv()

m = manager.connect(
        host=os.environ.get("ROUTER_HOST"),
        port=830,
        username=os.environ.get("ROUTER_USER"),
        password=os.environ.get("ROUTER_PASS"),
        hostkey_verify=False
    )


# --------------------------------------------------------------
# Core functions
# --------------------------------------------------------------

# Create Loopback66070220 interface
def create():
    # Define Netconf configuration for creating Loopback66070220 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070220</name>
                    <description>66070220 Loopback interface</description>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>172.2.17.1</ip>
                            <netmask>255.255.255.0</netmask>
                        </address>
                    </ipv4>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070220 already exists
        checkExist = check_interface_exist()
        if (checkExist):
            raise Exception("Interface already exist.")
        
        # Apply Netconf edit-config operation to create the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if ('<ok/>' in xml_data):
            return "Interface loopback 66070220 is created successfully"
    except:
        print("Error!")
        return "Cannot create: Interface loopback 66070220"


# Delete Loopback66070220 interface
def delete():
    # Define Netconf configuration for deleting Loopback66070220 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>Loopback66070220</name>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070220 exists
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception("Interface Loopback66070220 doesn't exist")
        
        # Apply Netconf edit-config operation to delete the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070220 is deleted successfully"
    except:
        print("Error!")
        return "Cannot delete: Interface loopback 66070220"

# Enable Loopback66070220 interface
def enable():
    # Define Netconf configuration for enabling Loopback66070220 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070220</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>true</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070220 exists
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception("Interface Loopback66070220 doesn't exist")
        
        # Apply Netconf edit-config operation to enable the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070220 is enabled successfully"
    except:
        print("Error!")
        return "Cannot enable: Interface loopback 66070220"

# Enable Loopback66070220 interface
def disable():
    # Define Netconf configuration for disabling Loopback66070220 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070220</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>false</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070220 exists
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception("Interface Loopback66070220 doesn't exist")

        # Apply Netconf edit-config operation to disable the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070220 is shutdowned successfully"
    except:
        print("Error!")
        return "Cannot shutdown: Interface loopback 66070220"

# Get status of Loopback66070220 interface
def status():
    # Define Netconf filter to get interfaces-state information for Loopback66070220
    netconf_filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070220</name></interface>
            </interfaces-state>
        </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if not (netconf_reply_dict["rpc-reply"]["data"] == None):
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]["admin-status"]
            oper_status = netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]["oper-status"]
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070123 is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070123 is disabled"
        else: # no operation-state data
            return "No Interface loopback 66070123"
    except:
       print("Error!")


# --------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------

# Applying Netconf edit-config operation
def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)

# Getting configuration data using Netconf get-config operation
def netconf_get_config(netconf_config):
    return m.get_config(source="running", filter=netconf_config)

# Check if interface Loopback66070220 exists
# Returns: True if exists, False otherwise
def check_interface_exist():
    findInterface = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070220</name></interface>
            </interfaces>
        </filter>
    """
    
    interfaceResult = netconf_get_config(findInterface).xml
    return ("Loopback66070220" in interfaceResult)