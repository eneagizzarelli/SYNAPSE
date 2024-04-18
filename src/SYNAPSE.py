from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation

terminal_history_path = "/home/user/SYNAPSE/logs/terminal_history.txt"

terminal_history = open(terminal_history_path, "a+", encoding="utf-8")

terminal_prompt = load_terminal_prompt(terminal_history)


def main():
    args = parse_terminal_argument(terminal_prompt)

    terminal_messages = load_terminal_messages(args.terminal_personality, terminal_history)

    try:
        terminal_simulation(terminal_messages, terminal_history)
    except KeyboardInterrupt:
        print("logout")

if __name__ == "__main__":
    main()