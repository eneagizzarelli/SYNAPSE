import os
import yaml
import argparse
from datetime import datetime

from client_data import client_ip

today = datetime.now()

logs_ip_terminal_history_path = "/home/user/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_terminal_history.txt"
logs_ip_mysql_history_path = "/home/user/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_mysql_history.txt"
terminal_personality_path = "/home/user/SYNAPSE/prompts/terminal_personality.yml"
services_personality_path = "/home/user/SYNAPSE/prompts/services_personality.yml"

def load_terminal_prompt():
    terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")

    if os.stat(logs_ip_terminal_history_path).st_size == 0:
        with open(terminal_personality_path, 'r', encoding="utf-8") as personality_file:
            terminal_identity = yaml.safe_load(personality_file)
        terminal_identity = terminal_identity['personality']
        terminal_prompt = terminal_identity['prompt']
    else:
        terminal_history.write("\nHere the session stopped. Now you will start it again from the beginning with the same user. You must respond just with starting message and nothing more. " +
                              "Make sure you use same file and folder names. Ignore date-time in <>. This is not your concern.\n")
        terminal_history.seek(0)
        terminal_prompt = terminal_history.read()

    terminal_history.close()

    return terminal_prompt

def parse_terminal_argument(terminal_prompt):
    parser = argparse.ArgumentParser()

    parser.add_argument("--terminal_personality", type=str, default= terminal_prompt + 
                        f"\nBased on these examples make something of your own (different username and hostname) to be a starting message. Always start the communication in this way and make sure your output ends with '$'. For the last login date use {today} and for ip address use {client_ip}.\n" + 
                        "Ignore date-time in <> after user input. This is not your concern.\n")
        
    args = parser.parse_args()
    
    return args

def load_terminal_messages(terminal_personality):
    initial_prompt = f"You are Linux OS terminal. Your personality is: {terminal_personality}"
    
    terminal_messages = [{"role": "system", "content": initial_prompt}]
    
    terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")

    if os.stat(logs_ip_terminal_history_path).st_size == 0:
        for terminal_message in terminal_messages:
            terminal_history.write(terminal_message["content"])
    else:
        terminal_history.write("The session continues in following lines.\n\n")

    terminal_history.close()

    return terminal_messages

def load_mysql_prompt():
    mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")

    if os.stat(logs_ip_mysql_history_path).st_size == 0:
        with open(services_personality_path, 'r', encoding="utf-8") as services_file:
            mysql_identity = yaml.safe_load(services_file)
        mysql_identity = mysql_identity['services']
        mysql_identity = mysql_identity['mysql']
        mysql_prompt = mysql_identity['prompt']
    else:
        mysql_history.write("\nHere the session stopped. Now you will start it again from the beginning with the same user. You must respond just with starting message and nothing more. " +
                              "Make sure you use same database, tables and folder names. Ignore date-time in <>. This is not your concern.\n")
        mysql_history.seek(0)
        mysql_prompt = mysql_history.read()

    mysql_history.close()
    
    return mysql_prompt

def parse_mysql_argument(mysql_prompt):
    parser = argparse.ArgumentParser()

    parser.add_argument("--mysql_personality", type=str, default= mysql_prompt + 
                        f"\nBased on these examples make something of your own (use different connection id and server version, the rest MUST remain unchanged) to be a starting message. Do not use trivial ids like '12345'. You must generate one similar to real case scenario (example: '12'). Always start the communication in this way and make sure your output ends with 'mysql >'.\n" + 
                        "Ignore date-time in <> after user input. This is not your concern.\n")
    
    args = parser.parse_args()
    
    return args

def load_mysql_messages(mysql_personality):
    initial_prompt = f"You are Linux OS terminal and you are MySQL server. Your personality is: {mysql_personality}"

    mysql_messages = [{"role": "system", "content": initial_prompt}]

    mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")

    if os.stat(logs_ip_mysql_history_path).st_size == 0:
        for mysql_message in mysql_messages:
            mysql_history.write(mysql_message["content"])
    else:
        mysql_history.write("The session continues in following lines.\n\n")
        
    mysql_history.close()

    return mysql_messages