import shutil
import subprocess

def set_motd(host_ip, message):
    playbook_path = 'banner_playbook.yaml'
    inventory_path = 'hosts'
    ansible_executable = shutil.which('ansible-playbook')
    
    if not ansible_executable:
        return "Error: playbook not found."

    command_args = [
        ansible_executable,
        "-i", inventory_path,
        playbook_path,
        "--limit", host_ip,
        "-e", f"motd_message='{message}'"
    ]
