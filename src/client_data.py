import os
import json
import geoip2.database

import subprocess
from scapy.all import sniff, wrpcap, rdpcap

base_path = "/home/user/SYNAPSE/"

def initialize_client_data(client_ip, client_port, server_port, client_geolocation):
    data = {
        "ip": client_ip,
        "client_port": client_port,
        "server_port": server_port,
        "geolocation": client_geolocation,
        "number_of_connections": 0,
        "session_durations_in_seconds": []
    }

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def get_client_geolocation(client_ip):
    database_path = base_path + "data/" + "GeoLite2-City.mmdb"
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

def get_client_ip():
    ssh_connection_info = os.environ.get("SSH_CLIENT")
    
    if ssh_connection_info:
        client_ip = ssh_connection_info.split()[0]
        client_port = ssh_connection_info.split()[1]
        server_port = ssh_connection_info.split()[2]
        
        if not os.path.exists(base_path + "logs/" + client_ip):
            os.makedirs(base_path + "logs/" + client_ip)

            client_geolocation = get_client_geolocation(client_ip)
            initialize_client_data(client_ip, client_port, server_port, client_geolocation)

        return client_ip

def increment_client_number_of_connections(client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["number_of_connections"] += 1

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def write_client_session_duration_in_seconds(session_duration_in_seconds, client_ip):
    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "r") as client_data_file:
        data = json.load(client_data_file)
        
    data["session_durations_in_seconds"].append(session_duration_in_seconds)

    with open(base_path + "logs/" + client_ip + "/" + client_ip + "_data.json", "w") as client_data_file:
        json.dump(data, client_data_file, indent=4)
        client_data_file.write("\n")

def capture_traffic(output_file):
    def process_packet(packet):
        wrpcap(output_file, packet, append=True)

    sniff(prn=process_packet, store=0)

def parse_packets(file_path, user_ip):
    sent_traffic = 0
    received_traffic = 0

    # Read the captured packets from the output file
    packets = rdpcap(file_path)

    # Parse and analyze each packet
    for packet in packets:
        if packet.haslayer('IP'):
            ip = packet['IP']
            if ip.src == user_ip:
                sent_traffic += len(packet)
            elif ip.dst == user_ip:
                received_traffic += len(packet)

    return sent_traffic, received_traffic