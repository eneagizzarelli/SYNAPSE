from ai_requests import *
from time import sleep
from datetime import datetime
import random
import os

from client_data import client_ip, get_count_classification_history_files
from initializations import load_mysql_prompt, parse_mysql_argument, load_mysql_messages

base_path = "/home/user/SYNAPSE/logs/"
today = datetime.now()

def terminal_simulation(terminal_messages):
    count_classification_history_files = get_count_classification_history_files()

    while True:
        # check over user trying to exit
        if "exit" in terminal_messages[len(terminal_messages) - 1]["content"].splitlines()[-1] or "logout" in terminal_messages[len(terminal_messages) - 1]["content"].splitlines()[-1]:
            raise KeyboardInterrupt

        if "mysql" in terminal_messages[len(terminal_messages) - 1]["content"].splitlines()[-1]:
            run_mysql_simulation()
            print("\nBye")
            terminal_messages.append({"role": "user", "content": "cd ." + f"\t<{datetime.now()}>\n"})

        if "clear" in terminal_messages[len(terminal_messages) - 1]["content"].splitlines()[-1]:
            os.system("clear")

        terminal_history = open(base_path + client_ip + "/" + client_ip + "_terminal_history.txt", "a+", encoding="utf-8")
        classification_history = open(base_path + client_ip + "/" + client_ip + "_classification_history_" + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        terminal_message = generate_response(terminal_messages)
        
        if "$cd" in terminal_message["content"] or "$ cd" in terminal_message["content"]:
            terminal_message["content"] = terminal_message["content"].split("\n")[1]

        terminal_messages.append(terminal_message)
        terminal_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        classification_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        
        terminal_history.close()
        classification_history.close()

        terminal_history = open(base_path + client_ip + "/" + client_ip + "_terminal_history.txt", "a+", encoding="utf-8")
        classification_history = open(base_path + client_ip + "/" + client_ip + "_classification_history_" + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
        # check over user trying to sudo
        if "will be reported" in terminal_messages[len(terminal_messages) - 1]["content"]:
            print(terminal_messages[len(terminal_messages) - 1]["content"])
            terminal_history.close()
            classification_history.close()
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
            classification_history.write(" " + user_input + "\n")
        else:
            user_input = input(f'\n{terminal_messages[len(terminal_messages) - 1]["content"]}'.strip() + " ")
            terminal_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
            terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
            classification_history.write(" " + user_input + "\n")

        terminal_history.close()
        classification_history.close()

def run_mysql_simulation():
    mysql_prompt = load_mysql_prompt()

    args = parse_mysql_argument(mysql_prompt)

    mysql_messages = load_mysql_messages(args.mysql_personality)

    try:
        mysql_simulation(mysql_messages)
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass

def mysql_simulation(mysql_messages):
    count_classification_history_files = get_count_classification_history_files()
    
    while True:
        if "exit" in mysql_messages[len(mysql_messages) - 1]["content"].splitlines()[-1] or "quit" in mysql_messages[len(mysql_messages) - 1]["content"].splitlines()[-1] or "\q" in mysql_messages[len(mysql_messages) - 1]["content"].splitlines()[-1]:
            break

        mysql_history = open(base_path + client_ip + "/" + client_ip + "_mysql_history.txt", "a+", encoding="utf-8")
        classification_history = open(base_path + client_ip + "/" + client_ip + "_classification_history_" + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        mysql_message = generate_response(mysql_messages)

        mysql_messages.append(mysql_message)
        mysql_history.write(mysql_messages[len(mysql_messages) - 1]["content"])
        classification_history.write(mysql_messages[len(mysql_messages) - 1]["content"])

        mysql_history.close()
        classification_history.close()

        mysql_history = open(base_path + client_ip + "/" + client_ip + "_mysql_history.txt", "a+", encoding="utf-8")
        classification_history = open(base_path + client_ip + "/" + client_ip + "_classification_history_" + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
        user_input = input(f'\n{mysql_messages[len(mysql_messages) - 1]["content"]}'.strip() + " ")
        mysql_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
        mysql_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        classification_history.write(" " + user_input + "\n")
        
        mysql_history.close()
        classification_history.close()