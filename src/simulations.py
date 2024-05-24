import os
import random
import getpass
from time import sleep
from datetime import datetime

from client_data import client_ip, get_count_classification_history_files
from initializations import load_mysql_prompt, parse_mysql_argument, load_mysql_messages
from ai_requests import *

logs_ip_terminal_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_terminal_history.txt"
logs_ip_mysql_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_mysql_history.txt"
logs_ip_classification_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_classification_history_"

today = datetime.now()

def terminal_simulation(terminal_messages):
    count_classification_history_files = get_count_classification_history_files()

    while True:
        last_terminal_message = terminal_messages[len(terminal_messages) - 1]["content"].splitlines()[-1]

        # check over user trying to exit
        if "exit" in last_terminal_message or "logout" in last_terminal_message:
            return

        if "mysql" in last_terminal_message:
            run_mysql_simulation(count_classification_history_files, last_terminal_message)
            terminal_messages.append({"role": "user", "content": "cd ." + f"\t<{datetime.now()}>\n"})

        if "clear" in last_terminal_message:
            os.system("clear")

        terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        terminal_message = generate_response(terminal_messages)
        
        if "$cd" in terminal_message["content"] or "$ cd" in terminal_message["content"]:
            terminal_message["content"] = terminal_message["content"].split("\n")[1]

        terminal_messages.append(terminal_message)
        terminal_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        classification_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        
        terminal_history.close()
        classification_history.close()

        terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
        # check over user trying to sudo
        if "will be reported" in terminal_messages[len(terminal_messages) - 1]["content"]:
            print(terminal_messages[len(terminal_messages) - 1]["content"])
            terminal_history.close()
            classification_history.close()
            return

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

def run_mysql_simulation(count_classification_history_files, last_terminal_message):
    user = "enea"
    parts = last_terminal_message.split()[:-2]

    if "-u" in parts:
        user_index = parts.index('-u') + 1
        if user_index < len(parts):
            user = parts[user_index]
        else:
            print("mysql: [ERROR] mysql: option '-u' requires an argument.")
            return

    if "-p" not in last_terminal_message or "-p" in user:
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: NO)")
        return

    password = getpass.getpass("Enter password: ")
    if user != "enea" or password != "password":
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: YES)")
        return

    mysql_prompt = load_mysql_prompt()
    args = parse_mysql_argument(mysql_prompt)
    mysql_messages = load_mysql_messages(args.mysql_personality)

    try:
        mysql_simulation(mysql_messages, count_classification_history_files)
    except KeyboardInterrupt:
        print("\n", end="")
    except EOFError:
        print("\n", end="")
    print("Bye")

def mysql_simulation(mysql_messages, count_classification_history_files):
    while True:
        last_mysql_message = mysql_messages[len(mysql_messages) - 1]["content"].splitlines()[-1]

        if "exit" in last_mysql_message or "quit" in last_mysql_message or "\q" in last_mysql_message:
            break

        mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        mysql_message = generate_response(mysql_messages)

        mysql_messages.append(mysql_message)
        mysql_history.write(mysql_messages[len(mysql_messages) - 1]["content"])
        classification_history.write(mysql_messages[len(mysql_messages) - 1]["content"])

        mysql_history.close()
        classification_history.close()

        mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
        user_input = input(f'\n{mysql_messages[len(mysql_messages) - 1]["content"]}'.strip() + " ")
        mysql_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
        mysql_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        classification_history.write(" " + user_input + "\n")
        
        mysql_history.close()
        classification_history.close()