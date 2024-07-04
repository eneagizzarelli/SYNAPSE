import os
import random
import getpass
from time import sleep
from datetime import datetime

# import client IP address global variable from client_data module
from client_data import client_ip, get_count_classification_history_files
from initializations import load_mysql_prompt, parse_mysql_argument, load_mysql_messages
from ai_requests import *

logs_ip_terminal_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_terminal_history.txt"
logs_ip_mysql_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_mysql_history.txt"
logs_attacks_ip_classification_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_attacks" + "/" + client_ip + "_classification_history_"

today = datetime.now()

def terminal_simulation(terminal_messages):
    """
    Simulation of a Linux OS terminal.

    Parameters:
    list[dict[str, str]]: dictionary of terminal messages.

    Returns: none.

    Raises:
    KeyboardInterrupt: whenever a user press CTRL+C to terminate the SSH connection.
    EOFError: whenever a user press CTRL+D to terminate the SSH connection.
    """
    
    count_classification_history_files = get_count_classification_history_files() # for the current IP address

    # infinite loop to simulate terminal interaction
    while True:
        # get the last command issued by the client
        last_terminal_message = terminal_messages[len(terminal_messages) - 1]["content"].splitlines()[-1]
        dollar_position = last_terminal_message.find("$")

        # check if the client wants to exit the terminal
        if last_terminal_message[dollar_position + 1:].lower().strip().startswith("exit") or last_terminal_message[dollar_position + 1:].lower().strip().startswith("logout"):
            return

        # check if the client wants to connect to MySQL and eventually enter MySQL simulation container function
        if last_terminal_message[dollar_position + 1:].strip().startswith("mysql"):
            run_mysql_simulation(last_terminal_message, count_classification_history_files)
            # make AI think the client issued a simple "cd ." command to re-enter terminal simulation after MySQL one
            terminal_messages.append({"role": "user", "content": "cd ." + f"\t<{datetime.now()}>\n"})

        # check if the client wants to clear the terminal
        if last_terminal_message[dollar_position + 1:].strip().startswith("clear"):
            os.system("clear")

        terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_attacks_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        # generate a response to the last command issued by the client by contacting AI
        terminal_message = generate_response(terminal_messages)
        
        # clean possible wrong AI responses after "cd" command skipping unwanted content
        if "$cd" in terminal_message["content"] or "$ cd" in terminal_message["content"]:
            terminal_message["content"] = terminal_message["content"].split("\n")[1]

        # append AI response to terminal messages list and write it to terminal and classification history files
        terminal_messages.append(terminal_message)
        terminal_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        classification_history.write(terminal_messages[len(terminal_messages) - 1]["content"])
        
        # close files to store changes and re-open them
        terminal_history.close()
        classification_history.close()
        terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_attacks_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
        # check if the client used "sudo" command
        if "will be reported" in terminal_messages[len(terminal_messages) - 1]["content"]:
            # print warning AI response and quit simulation
            print(terminal_messages[len(terminal_messages) - 1]["content"])
            terminal_history.close()
            classification_history.close()
            return

        # check over user trying to ping (print ping messages in a realistic way)
        lines = []
        if "PING" in terminal_message["content"]:
            lines = terminal_message["content"].split("\n")
            print(lines[0])

            # print response lines with random pause to simulate a real ping
            for i in range(1, len(lines)-5):
                print(lines[i])
                sleep(random.uniform(0.1, 0.5))
            
            for i in range(len(lines)-4, len(lines)-1):
                print(lines[i])
            
            # input the next command issued by the user after the ping one
            user_input = input(f'{lines[len(lines)-1]}'.strip() + " ")
            # append the user input to the terminal messages list together with the current timestamp 
            # and write it to the terminal and classification history files
            terminal_messages.append({"role": "user", "content": user_input + f"\t<{datetime.now()}>\n" })
            terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
            classification_history.write(" " + user_input + "\n")
        else:
            # input the next command issued by the user
            user_input = input(f'\n{terminal_messages[len(terminal_messages) - 1]["content"]}'.strip() + " ")
            # append the user input to the terminal messages list together with the current timestamp 
            # and write it to the terminal and classification history files
            terminal_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
            terminal_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
            classification_history.write(" " + user_input + "\n")
        
        terminal_history.close()
        classification_history.close()

def run_mysql_simulation(last_terminal_message, count_classification_history_files):
    """
    Container function to run MySQL server simulation.

    Parameters:
    str: last terminal message (issued mysql login command).
    int: number of classification history files.

    Returns: none.
    """
    
    # default username and password are respectively "enea" and "password"

    user = "enea"
    parts = last_terminal_message.split()[:-2]

    # check if the user provided a username for MySQL
    if "-u" in parts:
        user_index = parts.index('-u') + 1
        if user_index < len(parts):
            # get the username from the parts list
            user = parts[user_index]
        # if the username index is out of bounds, print corresponding error message and return
        else:
            print("mysql: [ERROR] mysql: option '-u' requires an argument.")
            return
    
    # check if the user is "-p" (wrong login command format, e.g. "mysql -u -p")
    if "-p" in user:
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: NO)")
        return

    # check if the user provided a password
    if "-p" not in last_terminal_message and "-ppassword" not in last_terminal_message:
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: NO)")
        return
    
    # get the password in a realistic way
    if "-ppassword" not in last_terminal_message:
        password = getpass.getpass("Enter password: ")
    else:
        password = "password"

    # if user is not "enea" or password is not "password", print corresponding error message and return
    if user != "enea" or password != "password":
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: YES)")
        return
        
    command = ""
    
    # check if the user provided a command to execute after logging in
    if "-e" in parts:
        command_index = parts.index('-e') + 1
        if command_index < len(parts):
            # get the command from the parts list
            if parts[command_index].startswith('"'):
                command_parts = []
                # build the command from the parts list until the closing quote is found
                for part in parts[command_index:]:
                    command_parts.append(part)
                    if part.endswith('"') or parts.index(part) >= len(parts) - 1:
                        break
                command = ' '.join(command_parts)[1:-1] # remove the surrounding quotes
            else:
                # if no quotes are found, get just the first string after the "-e" option
                command = parts[command_index]
        else:
            print("mysql: [ERROR] mysql: option '-e' requires an argument.")
            return
    
    # the following functions have self-explanatory names and are executed for the 
    # IP address of the client that is currently connected
    mysql_prompt = load_mysql_prompt()
    args = parse_mysql_argument(mysql_prompt)
    mysql_messages = load_mysql_messages(args.mysql_personality)

    try:
        # start mysql simulation
        mysql_simulation(mysql_messages, command, count_classification_history_files)
    except KeyboardInterrupt:
        print("\n", end="")
    except EOFError:
        print("\n", end="")
    # simulate exit from mysql
    if command == "":
        print("Bye")

def mysql_simulation(mysql_messages, command, count_classification_history_files):
    """
    Simulation of a MySQL server.

    Parameters:
    list[dict[str, str]]: dictionary of mysql messages.
    str: command to execute after logging in (if any).
    int: number of classification history files.

    Returns: none.

    Raises:
    KeyboardInterrupt: whenever a user press CTRL+C to terminate the MySQL connection.
    EOFError: whenever a user press CTRL+D to terminate the MySQL connection.
    """
    
    # infinite loop to simulate MySQL terminal interaction
    while True:
        # get the last mysql command issued by the client
        last_mysql_message = mysql_messages[len(mysql_messages) - 1]["content"].splitlines()[-1]
        mysql_position = last_mysql_message.find("mysql")

        # check if the client wants to exit mysql
        if last_mysql_message[mysql_position + 2:].lower().strip().startswith("exit") or last_mysql_message[mysql_position + 2:].lower().strip().startswith("quit") or last_mysql_message[mysql_position + 2:].lower().strip().startswith("\q"):
            break

        mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_attacks_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        # generate a response to the last mysql command issued by the client by contacting AI
        mysql_message = generate_response(mysql_messages)

        # append AI response to mysql messages list and write it to mysql and classification history files
        mysql_messages.append(mysql_message)
        mysql_history.write(mysql_messages[len(mysql_messages) - 1]["content"])
        classification_history.write(mysql_messages[len(mysql_messages) - 1]["content"])

        # close files to store changes and re-open them
        mysql_history.close()
        classification_history.close()

        # if command to execute after login was provided and parsed, print the last message content and exit
        if command == "end":
            last_message_content = mysql_messages[len(mysql_messages) - 1]["content"]
            lines = last_message_content.split('\n')
            # skip the last "mysql> " line
            for line in lines[:-1]:
                print(line)
            break

        mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_attacks_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        user_input = ""
        # check if command to execute after login was provided
        if command != "":
            user_input = command
            command = "end"
        else:
            # input the next mysql command issued by the user
            user_input = input(f'\n{mysql_messages[len(mysql_messages) - 1]["content"]}'.strip() + " ")

        # append the user input to the mysql messages list together with the current timestamp 
        # and write it to the mysql and classification history files
        mysql_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
        mysql_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        classification_history.write(" " + user_input + "\n")
        
        mysql_history.close()
        classification_history.close()