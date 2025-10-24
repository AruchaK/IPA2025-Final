import os
from netmiko import ConnectHandler
from dotenv import load_dotenv
import re

load_dotenv()

ROUTER_USER = os.environ.get("ROUTER_USER")
ROUTER_PASS = os.environ.get("ROUTER_PASS")

def get_motd(ip):

    device_params = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": ROUTER_USER,
        "password": ROUTER_PASS,
    }

    try:
        with ConnectHandler(**device_params) as connection:
            banner_output = connection.send_command("show banner motd", use_textfsm=False)
            
            if banner_output and banner_output.strip():
                return banner_output.strip()
            else:
                return "Error: No MOTD Configured"
    except Exception as e:
        return "Error: No MOTD Configured"