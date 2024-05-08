import time
import subprocess

from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation
from client_data import get_client_ip, initialize_client_data, increment_client_number_of_connections, write_client_session_duration_in_seconds

def run_SYNAPSE_to_MITRE_script():
    script_path = "/home/user/SYNAPSE/scripts/startSYNAPSE-to-MITRE.sh"
    client_ip = get_client_ip()
    
    subprocess.Popen(["bash", script_path, client_ip], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    initialize_client_data()
    increment_client_number_of_connections()
    
    terminal_prompt = load_terminal_prompt()
    args = parse_terminal_argument(terminal_prompt)
    terminal_messages = load_terminal_messages(args.terminal_personality)

    session_start_time = time.time()

    try:
        terminal_simulation(terminal_messages)
    except KeyboardInterrupt:
        print("\nlogout")
    except EOFError:
        print("\nlogout")

    session_end_time = time.time()
    session_duration_in_seconds = session_end_time - session_start_time
    session_duration_in_seconds = round(session_duration_in_seconds, 2)
    write_client_session_duration_in_seconds(session_duration_in_seconds)

    run_SYNAPSE_to_MITRE_script()

if __name__ == "__main__":
    main()