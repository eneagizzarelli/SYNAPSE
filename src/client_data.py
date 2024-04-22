import os
import subprocess
import json
import geoip2.database
import dpkt

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

def capture_traffic(user_ip, interface, sent_output_file, received_output_file):
    # Construct the command to capture sent and received traffic
    sent_cmd = [
        "tcpdump", "-i", interface, "src", user_ip, "-w", sent_output_file
    ]
    received_cmd = [
        "tcpdump", "-i", interface, "dst", user_ip, "-w", received_output_file
    ]

    # Start the tcpdump processes to capture sent and received traffic
    sent_process = subprocess.Popen(sent_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    received_process = subprocess.Popen(received_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    # Return the process objects for both sent and received traffic
    return sent_process, received_process

def stop_capture(sent_process, received_process):
    # Terminate the tcpdump processes
    sent_process.terminate()
    received_process.terminate()
    sent_process.wait()  # Wait for the processes to complete
    received_process.wait()

def read_pcap(file_path):
    sent_packets = 0
    sent_bytes = 0
    received_packets = 0
    received_bytes = 0

    with open(file_path, 'rb') as file:
        pcap = dpkt.pcap.Reader(file)

        # Iterate through each packet in the pcap file
        for timestamp, buf in pcap:
            # Parse Ethernet frame
            eth = dpkt.ethernet.Ethernet(buf)

            # Extract IP packet (if Ethernet frame contains IP packet)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data

                # Check if the IP packet is sent or received
                if eth.src == b'\x00\x00\x00\x00\x00\x00':  # Assuming broadcast or multicast is not considered
                    received_packets += 1
                    received_bytes += len(buf)
                else:
                    sent_packets += 1
                    sent_bytes += len(buf)

    return sent_packets, sent_bytes, received_packets, received_bytes