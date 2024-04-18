import os
import yaml
import argparse
from datetime import datetime

terminal_history_path = "/home/user/SYNAPSE/logs/terminal_history.txt"
mysql_history_path = "/home/user/SYNAPSE/logs/mysql_history.txt"
today = datetime.now()

def load_terminal_prompt():
    terminal_history = open(terminal_history_path, "a+", encoding="utf-8")

    print("ciao")
    if os.stat(terminal_history_path).st_size == 0:
        print("ciao1")
        with open("/home/user/SYNAPSE/terminal_personality.yml", 'r', encoding="utf-8") as personality_file:
            terminal_identity = yaml.safe_load(personality_file)
        terminal_identity = terminal_identity['personality']
        terminal_prompt = terminal_identity['prompt']
    else:
        print("ciao2")
        terminal_history.seek(0)
        terminal_history.write("\nHere the session stopped. Now you will start it again from the beginning with the same user. You must respond just with starting message and nothing more. Make sure you use same file and folder names. Ignore date-time in <>. This is not your concern {ue}.\n".format(ue = os.stat(terminal_history_path).st_size))
        terminal_prompt = terminal_history.read()

    terminal_history.close()

    return terminal_prompt

def load_mysql_prompt():
    if os.stat(mysql_history_path).st_size == 0:
        with open("/home/user/SYNAPSE/services_personality.yml", 'r', encoding="utf-8") as services_file:
            mysql_identity = yaml.safe_load(services_file)
        mysql_identity = mysql_identity['services']
        mysql_identity = mysql_identity['mysql']
        mysql_prompt = mysql_identity['prompt']
    else:
        with open(mysql_history_path, 'a+', encoding="utf-8") as mysql_history:
            mysql_history.write("\nHere the session stopped. Now you will start it again from the beginning with the same user. You must respond just with starting message and nothing more. Make sure you use same database, table and column names. Ignore date-time in <>. This is not your concern.\n")
            mysql_history.seek(0)
            mysql_prompt = mysql_history.read()
    
    return mysql_prompt

def parse_terminal_argument(terminal_prompt):
    parser = argparse.ArgumentParser()

    parser.add_argument("--terminal_personality", type=str, default= terminal_prompt + 
                        f"\nBased on these examples make something of your own (different username and hostname) to be a starting message. Always start the communication in this way and make sure your output ends with '$'. For the last login date use {today}\n" + "Ignore date-time in <> after user input. This is not your concern.\n")
        
    args = parser.parse_args()
    return args

def parse_mysql_argument(mysql_prompt):
    parser = argparse.ArgumentParser()

    parser.add_argument("--mysql_personality", type=str, default= mysql_prompt + 
                        f"\nBased on these examples make something of your own (different connection id and server version) to be a starting message. Always start the communication in this way and make sure your output ends with 'mysql >'.\n")
    
    args = parser.parse_args()
    return args

def load_terminal_messages(terminal_personality):
    terminal_history = open(terminal_history_path, "a+", encoding="utf-8")

    initial_prompt = f"You are Linux OS terminal. Your personality is: {terminal_personality}"
    
    terminal_messages = [{"role": "system", "content": initial_prompt}]
    
    if os.stat(terminal_history_path).st_size == 0:
        for msg in terminal_messages:
            terminal_history.write(msg["content"])
    else:
        terminal_history.write("The session continues in following lines.\n\n")

    terminal_history.close()

    return terminal_messages

def load_mysql_messages(mysql_personality):
    mysql_history = open(mysql_history_path, "a+", encoding="utf-8")

    initial_prompt = f"You are Linux OS terminal and you are MySQL server. Your personality is: {mysql_personality}"

    mysql_messages = [{"role": "system", "content": initial_prompt}]

    if os.stat(mysql_history_path).st_size == 0:
        for msg in mysql_messages:
            mysql_history.write(msg["content"])
    else:
        mysql_history.write("The session continues in following lines.\n\n")

    mysql_history.close()

    return mysql_messages