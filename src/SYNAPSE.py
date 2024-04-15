from initializations import load_prompts, parse_arguments, load_terminal_messages
from simulation import terminal_simulation

terminal_prompt, mysql_prompt = load_prompts()

def main():
    args = parse_arguments(terminal_prompt, mysql_prompt)

    terminal_messages = load_terminal_messages(args)

    while True:
        try:
            if "mysql" in terminal_messages[len(terminal_messages) - 1]["content"]:
                # TODO
                pass
            else:
                terminal_messages = terminal_simulation(terminal_messages)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()