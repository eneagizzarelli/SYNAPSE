import time

from client_data import initialize_client_data, increment_client_number_of_connections, write_client_session_duration_in_seconds
from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation

def main():
    # the following functions have self-explanatory names and are executed for the 
    # IP address of the client that is currently connected
    initialize_client_data()
    increment_client_number_of_connections()
    
    terminal_prompt = load_terminal_prompt()
    args = parse_terminal_argument(terminal_prompt)
    terminal_messages = load_terminal_messages(args.terminal_personality)

    # start session timer
    session_start_time = time.time()

    try:
        # start terminal simulation
        terminal_simulation(terminal_messages)
    except KeyboardInterrupt:
        print("\n", end="")
    except EOFError:
        print("\n", end="")
    # simulate exit from terminal
    print("logout")

    # end session timer
    session_end_time = time.time()
    
    write_client_session_duration_in_seconds(session_start_time, session_end_time)

if __name__ == "__main__":
    main()