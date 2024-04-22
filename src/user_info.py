import os

base_path = "/home/user/SYNAPSE/logs/"

def get_ssh_client_ip():
    ssh_connection_info = os.environ.get("SSH_CONNECTION")
    
    if ssh_connection_info:
        client_ip = ssh_connection_info.split()[0]
        
        if not os.path.exists(base_path + client_ip):
            os.makedirs(base_path + client_ip)

    return client_ip