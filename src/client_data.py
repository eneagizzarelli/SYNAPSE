import os
import json
import geoip2.database

def get_client_ip():
    """
    Extract client IP address from SSH_CLIENT environment variable.

    Parameters: none.

    Returns:
    str: client IP string.
    """

    # get info from SSH_CLIENT environment variable
    ssh_connection_info = os.environ.get("SSH_CLIENT")

    if ssh_connection_info:
        # extract and return client IP address
        client_ip = ssh_connection_info.split()[0]
        return client_ip
    
    # TODO: handle case when SSH_CLIENT is not available
    return None

# get client IP address as a global variable when this module is imported
client_ip = get_client_ip()

logs_ip_path = "/home/enea/SYNAPSE/logs/" + client_ip
logs_ip_data_path = logs_ip_path + "/" + client_ip + "_data.json"
database_path = "/home/enea/SYNAPSE/data/GeoLite2-City.mmdb"

def initialize_client_data():
    """
    Initialize client data structure for the current IP address.

    Parameters: none.

    Returns: none.
    """

    # check if folder for current client's IP address already exists (already initialized)
    if not os.path.exists(logs_ip_path):
        # if not, create it
        os.makedirs(logs_ip_path)
        # create a subfolder for attacks
        os.makedirs(logs_ip_path + "/" + client_ip + "_attacks")

        # get info from SSH_CLIENT environment variable
        ssh_connection_info = os.environ.get("SSH_CLIENT")

        if ssh_connection_info:
            # extract client port, server port and geolocation for the current IP address
            client_port = ssh_connection_info.split()[1]
            server_port = ssh_connection_info.split()[2]
            client_geolocation = get_client_geolocation()
            
            # initialize client data structure
            data = {
                "ip": client_ip,
                "client_port": client_port,
                "server_port": server_port,
                "geolocation": client_geolocation,
                "number_of_connections": 0,
                "session_durations_in_seconds": []
            }

            # write client data structure to a JSON file in the previously created folder
            with open(logs_ip_data_path, "w") as client_data_file:
                json.dump(data, client_data_file, indent=4)
                client_data_file.write("\n")
        
        # TODO: handle case when SSH_CLIENT is not available
        return None
    
def get_client_geolocation():
    """
    Extract client geolocation for the current IP address using GeoLite2 database.

    Parameters: none.

    Returns:
    dict[str, Any]: dictionary of geolocation information.

    Raises:
    geoip2.errors.AddressNotFoundError: if the IP address is not found in the database.
    """

    reader = geoip2.database.Reader(database_path)

    try:
        # get geolocation object for the current IP address
        response = reader.city(client_ip)
        
        # extract and return subset of geolocation information
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
        # close GeoLite2 database
        reader.close()

def increment_client_number_of_connections():
    """
    Increment total number of connections for the current IP address.
    
    Parameters: none.

    Returns: none.
    """

    with open(logs_ip_data_path, "r") as client_data_file:
        # load client data structure
        data = json.load(client_data_file)
    
    # increment the total number of connections
    data["number_of_connections"] += 1

    # write updated client data structure to the same JSON file
    with open(logs_ip_data_path, "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def write_client_session_duration_in_seconds(session_duration_in_seconds):
    """
    Write duration in seconds of the terminated session for the current IP address.
    
    Parameters:
    float: duration in seconds of the terminated session.

    Returns: none.
    """
    
    with open(logs_ip_data_path, "r") as client_data_file:
        # load client data structure
        data = json.load(client_data_file)
    
    # append session duration in seconds to the list of session durations
    data["session_durations_in_seconds"].append(session_duration_in_seconds)

    # write updated client data structure to the same JSON file
    with open(logs_ip_data_path, "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def get_count_classification_history_files():
    """
    Get number of classification history files for the current IP address.
    
    Parameters: none.

    Returns:
    int: number of classification history files.
    """

    count_classification_history_files = 0

    # iterate over files in the logs attacks folder for the current IP address
    for classification_file in os.listdir(logs_ip_path + "/" + client_ip + "_attacks"):
        # if classification history file is found
        if classification_file.startswith(client_ip + "_classification_history_"):
            # increment number of classification history files
            count_classification_history_files += 1

    return count_classification_history_files