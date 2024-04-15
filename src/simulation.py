from ai_requests import generate_response
from time import sleep
from datetime import datetime
import random

terminal_history_path = "/home/user/SYNAPSE/logs/terminal_history.txt"
mysql_history_path = "/home/user/SYNAPSE/logs/mysql_history.txt"
today = datetime.now()

def terminal_simulation(terminal_messages):
    try:
        terminal_history = open(terminal_history_path, "a+", encoding="utf-8")

        terminal_message = generate_response(terminal_messages)

        if "$cd" in terminal_message["content"] or "$ cd" in terminal_message["content"]:
            terminal_message["content"] = terminal_message["content"].split("\n")[1]

        terminal_messages.append(terminal_message)
        terminal_history.write(terminal_messages[len(terminal_messages) - 1]["content"])

        terminal_history.close()

        terminal_history = open(terminal_history_path, "a+", encoding="utf-8")
        
        # check over user trying to exit
        if "exit" in terminal_messages[len(terminal_messages) - 1]["content"]:
            print("logout")
            raise KeyboardInterrupt
        
        # check over user trying to sudo
        if "will be reported" in terminal_messages[len(terminal_messages) - 1]["content"]:
            print(terminal_messages[len(terminal_messages) - 1]["content"])
            raise KeyboardInterrupt

        # check over user trying to ping: print ping messages in a coherent way (pause between each ping message)
        lines = []
        if "PING" in terminal_message["content"]:
            lines = terminal_message["content"].split("\n")
            print(lines[0])

            for i in range(1, len(lines)-5):
                print(lines[i])
                sleep(random.uniform(0.1, 0.5))
            
            for i in range(len(lines)-4, len(lines)-1):
                print(lines[i])
            
            user_input = input(f'{lines[len(lines)-1]}'.strip() + " ")
            terminal_messages.append({"role": "user", "content": user_input + f"\t<{datetime.now()}>\n" })
            terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        else:
            user_input = input(f'\n{terminal_messages[len(terminal_messages) - 1]["content"]}'.strip() + " ")
            terminal_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
            terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        
        terminal_history.close()
        return terminal_messages
    except KeyboardInterrupt:
        terminal_messages.append({"role": "user", "content": "\n"})
        print("")
        terminal_history.close()
        raise KeyboardInterrupt