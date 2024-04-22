import os
import json
import geoip2.database

base_path = "/home/user/SYNAPSE/"

def get_client_ip():
    ssh_connection_info = os.environ.get("SSH_CONNECTION")
    
    if ssh_connection_info:
        client_ip = ssh_connection_info.split()[0]
        client_port = ssh_connection_info.split()[1]
        server_port = ssh_connection_info.split()[3]
        
        if not os.path.exists(base_path + "logs/" + client_ip):
            os.makedirs(base_path + "logs/" + client_ip)

            initialize_client_data(client_ip, client_port, server_port)

        return client_ip

def initialize_client_data(client_ip, client_port, server_port):
    data = {
        "ip": client_ip,
        "client_port": client_port,
        "server_port": server_port,
        "geolocation": None,
        "number_of_connections": 0,
        "session_durations_in_seconds": []
    }

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")

def write_client_geolocation(client_ip):
    database_path = base_path + "data/" + "GeoLite2-City.mmdb"
    reader = geoip2.database.Reader(database_path)

    try:
        response = reader.city(client_ip)

        print(response)
        
        # Extract relevant information from the response
        country = response.country.name
        city = response.city.name
        latitude = response.location.latitude
        longitude = response.location.longitude
        
        # Construct geolocation data
        geolocation_data = {
            "country": country,
            "city": city,
            "latitude": latitude,
            "longitude": longitude
        }
        
        return geolocation_data
    except geoip2.errors.AddressNotFoundError:
        return None
    finally:
        reader.close()

def increment_client_number_of_connections(client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["number_of_connections"] += 1

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")

def write_client_session_duration_in_seconds(session_duration_in_seconds, client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["session_durations_in_seconds"].append(session_duration_in_seconds)

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file)
        client_data_file.write("\n")