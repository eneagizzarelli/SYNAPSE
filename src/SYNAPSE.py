from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation
from user_info import get_ssh_client_ip

client_ip = get_ssh_client_ip()

terminal_prompt = load_terminal_prompt(client_ip)

def main():
    args = parse_terminal_argument(terminal_prompt, client_ip)

    terminal_messages = load_terminal_messages(args.terminal_personality, client_ip)

    try:
        terminal_simulation(terminal_messages, client_ip)
    except KeyboardInterrupt:
        print("logout")

if __name__ == "__main__":
    main()