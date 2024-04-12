import os
import yaml
import argparse
from datetime import datetime

terminal_history_path = "/home/user/SYNAPSE/logs/terminal_history.txt"
mysql_history_path = "/home/user/SYNAPSE/logs/mysql_history.txt"

today = datetime.now()

def load_prompts():
    terminal_history = open(terminal_history_path, "a+", encoding="utf-8")
    mysql_history = open(mysql_history_path, "a+", encoding="utf-8")

    if os.stat(terminal_history_path).st_size == 0:
        with open("/home/user/SYNAPSE/personality.yml", 'r', encoding="utf-8") as personality_file:
            terminal_identity = yaml.safe_load(personality_file)
        terminal_identity = terminal_identity['personality']
        terminal_prompt = terminal_identity['prompt']

        with open("/home/user/SYNAPSE/services.yml", 'r', encoding="utf-8") as services_file:
            mysql_identity = yaml.safe_load(services_file)
        mysql_identity = mysql_identity['services']
        mysql_identity = mysql_identity['mysql']
        mysql_prompt = mysql_identity['prompt']
    else:
        terminal_identity.write("\nHere the session stopped. Now you will start it again from the beginning with the same user. You must respond just with starting message and nothing more. " +
                                "Make sure you use same file and folder names. Ignore date-time in <>. This is not your concern.\n")
        terminal_history.seek(0)
        terminal_prompt = terminal_history.read()

        mysql_identity.write("\n TO CHANGE \n")
        mysql_history.seek(0)
        mysql_prompt = mysql_history.read()

    terminal_history.close()
    mysql_history.close()
    
    return terminal_prompt, mysql_prompt

def parse_arguments(terminal_prompt, mysql_prompt):
    parser = argparse.ArgumentParser()

    parser.add_argument("--personality", type=str, default= terminal_prompt + 
                        f"\nBased on these examples make something of your own (different username and hostname) to be a starting message. Always start the communication in this way and make sure your output ends with '$'. For the last login date use {today}\n" + "Ignore date-time in <> after user input. This is not your concern.\n")
    parser.add_argument("--mysql", type=str, default= mysql_prompt + 
                        f"\n ... \n")
    
    args = parser.parse_args()
    return args

def load_terminal_messages(args):
    terminal_history = open(terminal_history_path, "a+", encoding="utf-8")

    initial_prompt = f"You are Linux OS terminal. Your personality is: {args.personality}"
    
    terminal_messages = [{"role": "system", "content": initial_prompt}]
    
    if os.stat(terminal_history_path).st_size == 0:
        for msg in terminal_messages:
            terminal_history.write(msg["content"])
    else:
        terminal_history.write("The session continues in following lines.\n\n")

    terminal_history.close()

    return terminal_messages