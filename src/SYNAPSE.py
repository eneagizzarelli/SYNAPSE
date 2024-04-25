import time

from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation
from client_data import get_client_ip, increment_client_number_of_connections, write_client_session_duration_in_seconds

client_ip = get_client_ip()

def main():
    increment_client_number_of_connections(client_ip)
    
    terminal_prompt = load_terminal_prompt(client_ip)
    args = parse_terminal_argument(terminal_prompt, client_ip)
    terminal_messages = load_terminal_messages(args.terminal_personality, client_ip)

    session_start_time = time.time()

    try:
        terminal_simulation(terminal_messages, client_ip)
    except KeyboardInterrupt:
        print("\nlogout")
    except EOFError:
        print("\nlogout")

    session_end_time = time.time()
    session_duration_in_seconds = session_end_time - session_start_time
    session_duration_in_seconds = round(session_duration_in_seconds, 2)
    write_client_session_duration_in_seconds(session_duration_in_seconds, client_ip)

if __name__ == "__main__":
    main()