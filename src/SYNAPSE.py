import os

from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation

terminal_prompt = load_terminal_prompt()

def get_ssh_client_ip():
    ssh_connection_info = os.environ.get("SSH_CONNECTION")
    if ssh_connection_info:
        return ssh_connection_info.split()[0]

def main():
    client_ip = get_ssh_client_ip()
    if client_ip:
        print("SSH connection from:", client_ip)
    else:
        print("Not connected via SSH.")
        
    args = parse_terminal_argument(terminal_prompt)

    terminal_messages = load_terminal_messages(args.terminal_personality)

    try:
        terminal_simulation(terminal_messages)
    except KeyboardInterrupt:
        print("logout")

if __name__ == "__main__":
    main()