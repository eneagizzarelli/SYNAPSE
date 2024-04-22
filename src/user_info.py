import os
import json

base_path = "/home/user/SYNAPSE/"

def get_ssh_client_ip():
    ssh_connection_info = os.environ.get("SSH_CONNECTION")
    
    if ssh_connection_info:
        client_ip = ssh_connection_info.split()[0]
        
        if not os.path.exists(base_path + "logs/" + client_ip):
            os.makedirs(base_path + client_ip)

        return client_ip

def write_ssh_client_ip(client_ip):
    data = {"ip": client_ip}

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "a+") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")