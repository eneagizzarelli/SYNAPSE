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
logs_ip_classification_history_path = "/home/enea/SYNAPSE/logs/" + client_ip + "/" + client_ip + "_classification_history_"

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

        # check if the client wants to exit the terminal
        if "exit" in last_terminal_message or "logout" in last_terminal_message:
            return

        # check if the client wants to connect to MySQL and eventually enter MySQL simulation container function
        if "mysql" in last_terminal_message:
            run_mysql_simulation(last_terminal_message, count_classification_history_files)
            # make AI think the client issued a simple "cd ." command to re-enter terminal simulation after MySQL one
            terminal_messages.append({"role": "user", "content": "cd ." + f"\t<{datetime.now()}>\n"})

        # check if the client wants to clear the terminal
        if "clear" in last_terminal_message:
            os.system("clear")

        terminal_history = open(logs_ip_terminal_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

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
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
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

    # check if the user provided a password for MySQL or if the user is "-p" 
    # (wrong login command format, e.g. "mysql -u -p")
    if "-p" not in last_terminal_message or "-p" in user:
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: NO)")
        return
    
    # get the password in a realistic way
    password = getpass.getpass("Enter password: ")
    if user != "enea" or password != "password":
        # if user is not "enea" or password is not "password", print corresponding error message and return
        print(f"ERROR 1045 (28000): Access denied for user '{user}'@'localhost' (using password: YES)")
        return
    
    # the following functions have self-explanatory names and are executed for the 
    # IP address of the client that is currently connected
    mysql_prompt = load_mysql_prompt()
    args = parse_mysql_argument(mysql_prompt)
    mysql_messages = load_mysql_messages(args.mysql_personality)

    try:
        # start mysql simulation
        mysql_simulation(mysql_messages, count_classification_history_files)
    except KeyboardInterrupt:
        print("\n", end="")
    except EOFError:
        print("\n", end="")
    # simulate exit from mysql
    print("Bye")

def mysql_simulation(mysql_messages, count_classification_history_files):
    """
    Simulation of a MySQL server.

    Parameters:
    list[dict[str, str]]: dictionary of mysql messages.
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

        # check if the client wants to exit mysql
        if "exit" in last_mysql_message or "quit" in last_mysql_message or "\q" in last_mysql_message:
            break

        mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")

        # generate a response to the last mysql command issued by the client by contacting AI
        mysql_message = generate_response(mysql_messages)

        # append AI response to mysql messages list and write it to mysql and classification history files
        mysql_messages.append(mysql_message)
        mysql_history.write(mysql_messages[len(mysql_messages) - 1]["content"])
        classification_history.write(mysql_messages[len(mysql_messages) - 1]["content"])

        # close files to store changes and re-open them
        mysql_history.close()
        classification_history.close()
        mysql_history = open(logs_ip_mysql_history_path, "a+", encoding="utf-8")
        classification_history = open(logs_ip_classification_history_path + str(count_classification_history_files) + ".txt", "a+", encoding="utf-8")
        
        # input the next mysql command issued by the user
        user_input = input(f'\n{mysql_messages[len(mysql_messages) - 1]["content"]}'.strip() + " ")
        # append the user input to the mysql messages list together with the current timestamp 
        # and write it to the mysql and classification history files
        mysql_messages.append({"role": "user", "content": " " + user_input + f"\t<{datetime.now()}>\n"})
        mysql_history.write(" " + user_input + f"\t<{datetime.now()}>\n")
        classification_history.write(" " + user_input + "\n")
        
        mysql_history.close()
        classification_history.close()