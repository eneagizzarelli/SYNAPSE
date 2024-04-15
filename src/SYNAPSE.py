from initializations import load_prompts, parse_arguments, load_terminal_messages, load_mysql_messages
from simulations import terminal_simulation, mysql_simulation

terminal_prompt, mysql_prompt = load_prompts()

def main():
    args = parse_arguments(terminal_prompt, mysql_prompt)

    terminal_messages = load_terminal_messages(args.terminal_personality)
    mysql_messages = load_mysql_messages(args.mysql_personality)

    while True:
        try:
            if "mysql" in terminal_messages[len(terminal_messages) - 1]["content"]:
                try:
                    mysql_messages = mysql_simulation(mysql_messages)
                except KeyboardInterrupt:
                    mysql_messages.append({"role": "user", "content": "\n"})
                    terminal_messages.append({"role": "user", "content": "cd . \n"})
            else:
                try:
                    terminal_messages = terminal_simulation(terminal_messages)
                except KeyboardInterrupt:
                    terminal_messages.append({"role": "user", "content": "\n"})
                    print("")
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()