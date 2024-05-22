import os
import json
import geoip2.database

def get_client_ip():
    ssh_connection_info = os.environ.get("SSH_CLIENT")

    if ssh_connection_info:
        client_ip = ssh_connection_info.split()[0]
    # TODO: handle cases in which IP address not available
    else:
        raise KeyboardInterrupt

    return client_ip

client_ip = get_client_ip()

logs_ip_path = "/home/enea/SYNAPSE/logs/" + client_ip
logs_ip_data_path = logs_ip_path + "/" + client_ip + "_data.json"
database_path = "/home/enea/SYNAPSE/data/GeoLite2-City.mmdb"

def initialize_client_data():
    if not os.path.exists(logs_ip_path):
        os.makedirs(logs_ip_path)

        ssh_connection_info = os.environ.get("SSH_CLIENT")

        if ssh_connection_info:
            client_port = ssh_connection_info.split()[1]
            server_port = ssh_connection_info.split()[2]

        client_geolocation = get_client_geolocation()
        
        data = {
            "ip": client_ip,
            "client_port": client_port,
            "server_port": server_port,
            "geolocation": client_geolocation,
            "number_of_connections": 0,
            "session_durations_in_seconds": []
        }

        with open(logs_ip_data_path, "w") as client_data_file:
            json.dump(data, client_data_file, indent=4)
            client_data_file.write("\n")

def get_client_geolocation():
    reader = geoip2.database.Reader(database_path)

    try:
        response = reader.city(client_ip)
        
        client_geolocation = {
            "country": {
                "name": response.country.name,
                "iso_code": response.country.iso_code
            },
            "region": response.subdivisions.most_specific.name,
            "city": response.city.name,
            "postal_code": response.postal.code,
            "location": {
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "time_zone": response.location.time_zone,
                "accuracy_radius": response.location.accuracy_radius
            },
            "continent": {
                "name": response.continent.name,
                "code": response.continent.code
            }
        }

        return client_geolocation
    except geoip2.errors.AddressNotFoundError:
        return None
    finally:
        reader.close()

def increment_client_number_of_connections():
    with open(logs_ip_data_path, "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["number_of_connections"] += 1

    with open(logs_ip_data_path, "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def write_client_session_duration_in_seconds(session_duration_in_seconds):
    with open(logs_ip_data_path, "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["session_durations_in_seconds"].append(session_duration_in_seconds)

    with open(logs_ip_data_path, "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def get_count_classification_history_files():
    count_classification_history_files = 0

    for classification_file in os.listdir(logs_ip_path):
        if classification_file.startswith(client_ip + "_classification_history_"):
            count_classification_history_files += 1

    return count_classification_history_files