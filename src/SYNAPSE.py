from initializations import load_terminal_prompt, parse_terminal_argument, load_terminal_messages
from simulations import terminal_simulation

def main():
    terminal_prompt = load_terminal_prompt()

    print("ciao")

    args = parse_terminal_argument(terminal_prompt)

    terminal_messages = load_terminal_messages(args.terminal_personality)

    try:
        terminal_simulation(terminal_messages)
    except KeyboardInterrupt:
        print("logout")

if __name__ == "__main__":
    main()