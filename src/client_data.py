import os
import json
import vt
import geoip2.database
from dotenv import dotenv_values

SYNAPSE_path = "/home/enea/SYNAPSE/"

# load .env file and configure VirusTotal API key
config = dotenv_values("/home/enea/.env")
VIRUSTOTAL_API_KEY = config["VIRUSTOTAL_API_KEY"]

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

logs_ip_path = SYNAPSE_path + "logs/" + client_ip + "/"
logs_ip_data_path = logs_ip_path + client_ip + "_data.json"
logs_ip_attacks_path = logs_ip_path + client_ip + "_attacks/"

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
        os.makedirs(logs_ip_attacks_path)

        # get info from SSH_CLIENT environment variable
        ssh_connection_info = os.environ.get("SSH_CLIENT")

        if ssh_connection_info:
            # extract ip information, client port, server port and geolocation for the current IP address
            ip_info = get_client_ip_info()
            client_port = ssh_connection_info.split()[1]
            server_port = ssh_connection_info.split()[2]
            client_geolocation = get_client_geolocation()
            
            # initialize client data structure
            data = {
                "ip": client_ip,
                "ip_info": ip_info,
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

def get_client_ip_info():
    """
    Extract information for the current IP address using VirusTotal APIs.

    Parameters: none.

    Returns:
    dict[str, Any]: dictionary of IP information.

    Raises:
    vt.error.APIError: if there is any error in the VirusTotal APIs.
    """
    
    vt_client = vt.Client(VIRUSTOTAL_API_KEY)

    try:
        # get IP address information from VirusTotal
        ip_info_json = vt_client.get_json("/ip_addresses/{}", client_ip)
        # extract attributes from the JSON response
        attributes = ip_info_json.get("data", {}).get("attributes", {})

        # fill IP information dictionary with relevant fields
        ip_info = {
            "total_votes": attributes.get('total_votes'),
            "whois": attributes.get('whois'),
            "reputation": attributes.get('reputation'),
            "last_analisys_stats": attributes.get('last_analysis_stats'),
            "regional_internet_registry": attributes.get('regional_internet_registry'),
            "as_owner": attributes.get('as_owner')
        }

        return ip_info
    except vt.error.APIError:
        return None
    finally:
        # close VirusTotal client
        vt_client.close()
    
def get_client_geolocation():
    """
    Extract client geolocation for the current IP address using GeoLite2 database.

    Parameters: none.

    Returns:
    dict[str, Any]: dictionary of geolocation information.

    Raises:
    geoip2.errors.AddressNotFoundError: if the IP address is not found in the database.
    """

    reader = geoip2.database.Reader(SYNAPSE_path + "data/GeoLite2-City.mmdb")

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

def write_client_session_duration_in_seconds(session_start_time, session_end_time):
    """
    Write duration of the terminated session for the current IP address.
    
    Parameters:
    float: session start time.
    float: session end time.

    Returns: none.
    """

    # calculate session duration in seconds and round it to 2 decimal places
    session_duration_in_seconds = session_end_time - session_start_time
    session_duration_in_seconds = round(session_duration_in_seconds, 2)
    
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

    # iterate over file in the attacks folder of the current IP address
    for classification_file in os.listdir(logs_ip_attacks_path):
        # if classification history file is found
        if classification_file.startswith(client_ip + "_classification_history_"):
            # increment number of classification history files
            count_classification_history_files += 1

    return count_classification_history_files