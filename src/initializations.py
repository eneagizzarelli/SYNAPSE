import os
import yaml
import argparse
from datetime import datetime

# import client IP address global variable from client_data module
from client_data import client_ip

today = datetime.now()

logs_ip_terminal_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_terminal_history.txt"
logs_ip_mysql_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_mysql_history.txt"
terminal_personality_path = "/home/enea/SYNAPSE/prompts/terminal_personality.yml"
services_personality_path = "/home/enea/SYNAPSE/prompts/services_personality.yml"

def load_terminal_prompt():
    """
    Load terminal prompt from scratch if it is the first session for the current IP address.
    Load terminal prompt from the last session if it is not the first session for the current IP address.

    Parameters: none.

    Returns:
    str: terminal history string.
    """
    
    # open or create terminal history file
    terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")

    # if empty (first session for the current IP address)
    if os.stat(logs_ip_terminal_history_path).st_size == 0:
        with open(terminal_personality_path, 'r', encoding="utf-8") as personality_file:
            terminal_identity = yaml.safe_load(personality_file)
        terminal_identity = terminal_identity['personality']
        # extract terminal prompt text
        terminal_prompt = terminal_identity['prompt']
    # if not empty (continuation of the previous session)
    else:
        # write message to the terminal history file to inform AI about continuation
        terminal_history.write("\nHere the session stopped. " + 
                               "Now you will start it again from the beginning with the same user. " + 
                               "You must respond just with starting message and nothing more. " +
                               "Make sure you use same files and folders names as in the previous sessions. " + 
                               "Ignore date-time in <> after user input. This is not your concern.\n")
        # move the cursor to the beginning of the terminal history file and read content
        terminal_history.seek(0)
        terminal_prompt = terminal_history.read()

    terminal_history.close()

    return terminal_prompt

def parse_terminal_argument(terminal_prompt):
    """
    Parse terminal personality argument.

    Parameters: 
    str: terminal prompt string.

    Returns:
    Namespace: parsed args.
    """

    parser = argparse.ArgumentParser()

    # add terminal personality argument to the parser using the terminal prompt as default value 
    # and instructing the AI to use current date and IP address for the last login message
    parser.add_argument("--terminal_personality", type=str, default= terminal_prompt + 
                        f"\nBased on these examples make something of your own (different hostname) to be a starting message. " + 
                        f"Always start the communication in this way and make sure your output ends with '$'. " + 
                        f"For the last login date use {today} and for the ip address use {client_ip}. " + 
                        f"Ignore date-time in <> after user input. This is not your concern.\n\n")
    
    args = parser.parse_args()
    return args

def load_terminal_messages(terminal_personality):
    """
    Load terminal messages and write them to terminal history file if it is the first session for the current IP address.
    Load terminal messages and inform AI about session continuation if it is not the first session for the current IP address.

    Parameters: 
    str: terminal personality string.

    Returns:
    list[dict[str, str]]: dictionary of terminal messages.
    """
    
    # create initial prompt for AI using the terminal personality previously parsed
    initial_prompt = f"You are Linux OS terminal. Your personality is: {terminal_personality}"
    
    # create a list of terminal messages with the initial prompt as the first message
    terminal_messages = [{"role": "system", "content": initial_prompt}]
    
    terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")
    
    # if terminal history file is empty (first session for the current IP address)
    if os.stat(logs_ip_terminal_history_path).st_size == 0:
        # write terminal messages to the terminal history file
        for terminal_message in terminal_messages:
            terminal_history.write(terminal_message["content"])
    # if not empty (continuation of the previous session)
    else:
        # write message to the terminal history file to inform AI about continuation
        terminal_history.write("The session continues in following lines.\n\n")

    terminal_history.close()

    return terminal_messages

def load_mysql_prompt():
    """
    Load mysql prompt from scratch if it is the first session for the current IP address.
    Load mysql prompt from the last session if it is not the first session for the current IP address.

    Parameters: none.

    Returns:
    str: mysql history string.
    """
    
    # open or create mysql history file
    mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")

    # if empty (first session for the current IP address)
    if os.stat(logs_ip_mysql_history_path).st_size == 0:
        with open(services_personality_path, 'r', encoding="utf-8") as services_file:
            mysql_identity = yaml.safe_load(services_file)
        # extract mysql prompt text
        mysql_identity = mysql_identity['services']
        mysql_identity = mysql_identity['mysql']
        mysql_prompt = mysql_identity['prompt']
    # if not empty (continuation of the previous session)
    else:
        # write message to the mysql history file to inform AI about continuation
        mysql_history.write("\nHere the session stopped. " + 
                            "Now you will start it again from the beginning with the same user. " + 
                            "You must respond just with starting message and nothing more. " + 
                            "Make sure you use same databases, tables and folders names. " + 
                            "Ignore date-time in <>. This is not your concern.\n")
        # move the cursor to the beginning of the mysql history file and read content
        mysql_history.seek(0)
        mysql_prompt = mysql_history.read()

    mysql_history.close()
    
    return mysql_prompt

def parse_mysql_argument(mysql_prompt):
    """
    Parse mysql personality argument.

    Parameters: 
    str: mysql prompt string.

    Returns:
    Namespace: parsed args.
    """
    
    parser = argparse.ArgumentParser()

    # add mysql personality argument to the parser using the mysql prompt as default value 
    # and instructing the AI to use current date and IP address for the welcome message
    parser.add_argument("--mysql_personality", type=str, default= mysql_prompt + 
                        f"\nBased on these examples make something of your own (different connection ID and server version) to be a starting message. " + 
                        f"Do not use trivial IDs like '12345'. You must generate one similar to real case scenarios ('12' for example). " + 
                        f"Always start the communication in this way and make sure your output ends with 'mysql>'. " + 
                        f"Ignore date-time in <> after user input. This is not your concern.\n\n")
    
    args = parser.parse_args()
    return args

def load_mysql_messages(mysql_personality):
    """
    Load mysql messages and write them to mysql history file if it is the first session for the current IP address.
    Load mysql messages and inform AI about session continuation if it is not the first session for the current IP address.

    Parameters: 
    str: mysql personality string.

    Returns:
    list[dict[str, str]]: dictionary of mysql messages.
    """
    
    # create initial prompt for AI using the mysql personality previously parsed
    initial_prompt = f"You are MySQL server inside Linux OS terminal. Your personality is: {mysql_personality}"

    # create a list of mysql messages with the initial prompt as the first message
    mysql_messages = [{"role": "system", "content": initial_prompt}]

    mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")

    # if mysql history file is empty (first session for the current IP address)
    if os.stat(logs_ip_mysql_history_path).st_size == 0:
        # write mysql messages to the mysql history file
        for mysql_message in mysql_messages:
            mysql_history.write(mysql_message["content"])
    # if not empty (continuation of the previous session)
    else:
        # write message to the mysql history file to inform AI about continuation
        mysql_history.write("The session continues in following lines.\n\n")
        
    mysql_history.close()

    return mysql_messages