import os
import json

base_path = "/home/user/SYNAPSE/"

def get_client_ip():
    ssh_connection_info = os.environ.get("SSH_CONNECTION")
    
    if ssh_connection_info:
        client_ip = ssh_connection_info.split()[0]
        
        if not os.path.exists(base_path + "logs/" + client_ip):
            os.makedirs(base_path + "logs/" + client_ip)

        return client_ip

def initialize_client_data(client_ip):
    data = {
        "ip": client_ip,
        "number_of_connections": 0,
        "session_durations": []
    }

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "a+") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")

def increment_client_number_of_connections(client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["number_of_connections"] += 1

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")

def write_client_session_duration(session_duration, client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["session_durations"].append(session_duration)

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")