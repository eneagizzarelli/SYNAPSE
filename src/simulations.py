from ai_requests import generate_response
from time import sleep
from datetime import datetime
import random

from initializations import load_mysql_prompt, parse_mysql_argument, load_mysql_messages

terminal_history_path = "/home/user/SYNAPSE/logs/terminal_history.txt"
mysql_history_path = "/home/user/SYNAPSE/logs/mysql_history.txt"
today = datetime.now()

mysql_prompt = load_mysql_prompt()

def terminal_simulation(terminal_messages):
    while True:
        terminal_history = open(terminal_history_path, "a", encoding="utf-8")

        terminal_message = generate_response(terminal_messages)
        
        if "$cd" in terminal_message["content"] or "$ cd" in terminal_message["content"]:
            terminal_message["content"] = terminal_message["content"].split("\n")[1]

        terminal_messages.append(terminal_message)
        terminal_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        
        terminal_history.close()

        terminal_history = open(terminal_history_path, "a", encoding="utf-8")
        
        # check over user trying to sudo
        if "will be reported" in terminal_messages[len(terminal_messages) - 1]["content"]:
            print(terminal_messages[len(terminal_messages) - 1]["content"])
            terminal_history.close()
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
            # check over user trying to exit
            if "exit" in user_input:
                terminal_history.close()
                raise KeyboardInterrupt
            elif "mysql" in user_input:
                terminal_history.write(" " + "mysql" + f"\t<{datetime.now()}>\n")

                args = parse_mysql_argument(mysql_prompt)
                mysql_messages = load_mysql_messages(args.mysql_personality)
                mysql_simulation(mysql_messages)
                print("Bye")
            else:
                terminal_messages.append({"role": "user", "content": user_input + f"\t<{datetime.now()}>\n" })
                terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        else:
            user_input = input(f'\n{terminal_messages[len(terminal_messages) - 1]["content"]}'.strip() + " ")
            # check over user trying to exit
            if "exit" in user_input:
                terminal_history.close()
                raise KeyboardInterrupt
            elif "mysql" in user_input:
                terminal_history.write(" " + "mysql" + f"\t<{datetime.now()}>\n")

                args = parse_mysql_argument(mysql_prompt)
                mysql_messages = load_mysql_messages(args.mysql_personality)
                mysql_simulation(mysql_messages)
                print("Bye")
            else:
                terminal_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
                terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")

        terminal_history.close()

def mysql_simulation(mysql_messages):
    while True:
        mysql_history = open(mysql_history_path, "a+", encoding="utf-8")

        mysql_message = generate_response(mysql_messages)

        mysql_messages.append(mysql_message)
        mysql_history.write(mysql_messages[len(mysql_messages) - 1]["content"])

        mysql_history.close()

        mysql_history = open(mysql_history_path, "a+", encoding="utf-8")
        
        user_input = input(f'\n{mysql_messages[len(mysql_messages) - 1]["content"]}'.strip() + " ")
        # check over user trying to exit
        if "exit" in user_input or "quit" in user_input:
            mysql_history.write(" " + "exit" + f"\t<{datetime.now()}>\n")
            mysql_history.close()
            break
        else:
            mysql_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
            mysql_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        
        mysql_history.close()