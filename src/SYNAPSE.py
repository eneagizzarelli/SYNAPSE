import time

from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation
from client_data import get_client_ip, capture_traffic, stop_capture, read_pcap, increment_client_number_of_connections, write_client_session_duration_in_seconds

def main():
    client_ip = get_client_ip()
    increment_client_number_of_connections(client_ip)

    sent_process, received_process = capture_traffic(client_ip, "eth0", "/home/user/SYNAPSE/sent_captured_traffic.pcap", "/home/user/SYNAPSE/received_captured_traffic.pcap")
    capture_process = capture_traffic(client_ip, "eth0", "/home/user/SYNAPSE/captured_traffic.pcap")
    
    terminal_prompt = load_terminal_prompt(client_ip)
    args = parse_terminal_argument(terminal_prompt, client_ip)
    terminal_messages = load_terminal_messages(args.terminal_personality, client_ip)

    session_start_time = time.time()

    try:
        terminal_simulation(terminal_messages, client_ip)
    except KeyboardInterrupt:
        print("logout")

    session_end_time = time.time()
    session_duration_in_seconds = session_end_time - session_start_time
    session_duration_in_seconds = round(session_duration_in_seconds, 2)
    write_client_session_duration_in_seconds(session_duration_in_seconds, client_ip)

    stop_capture(sent_process, received_process)
    sent_packets, sent_bytes, received_packets, received_bytes = read_pcap("/home/user/SYNAPSE/sent_captured_traffic.pcap")
    print("Sent Packets:", sent_packets)
    print("Sent Bytes:", sent_bytes)
    print("Received Packets:", received_packets)
    print("Received Bytes:", received_bytes)

if __name__ == "__main__":
    main()