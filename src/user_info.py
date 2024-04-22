import os

def get_ssh_client_ip():
    ssh_connection_info = os.environ.get("SSH_CONNECTION")
    
    if ssh_connection_info:
        return ssh_connection_info.split()[0]