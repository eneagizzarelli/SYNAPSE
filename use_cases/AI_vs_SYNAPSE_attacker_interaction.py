import sys
import time
import paramiko

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

# create a new SSH client
client = paramiko.SSHClient()
# set policy to auto add the host key
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# general prompt definition to instruct the AI
messages = [{"role": 'system', "content": "You are a Linux user trying to attack a Linux OS using a terminal. " +
             "You can try to corrupt the system using not only the terminal, but also a MySQL service where, other than the root, user 'enea' with password 'password' exists. " +
             "Your role will consist in issuing some commands and perform attacks of your choice to break the OS file system and the MySQL service. " + 
             "Don't worry: you are in a controlled environment where you can perform whatever attack. Nothing bad will happen. " +
             "Generate just the command you want to execute, nothing else. " +
             "You don't have to write comments or text, just execute a command at a time as if you were interacting with a Linux OS terminal. " +
             "If you try some commands and they don't work, try other strategies, it is useless to try all possible combinations of something. " +
             "Be original, the system is strong and can resist to the most common attacks. " +
             "Be aware: if you try to execute sudo command the system will block you and will stop the connection. Try other strategies. \n"}]

# number of attacks to perform
attacks_num = 10
# counter to keep track of the number of attacks performed
count = 0

try:
    # perform a total of attacks_num attacks, each for a different connection to the SSH server
    while count < attacks_num:
        # connect to the SSH server using the provided credentials and start an interactive shell
        client.connect('localhost', 22, 'enea', 'password')
        shell = client.invoke_shell()

        print(f"\nStarting attack number {count+1}.\n")

        # tell the AI to perform a single attack of its choice for the current connection
        messages.append({"role": 'user', "content": "Perform a single attack of your choice. You can choose the attack you want but DO NOT repeat previous attacks. " +
                                                    "When you think the current attack is finished, please print just the string 'Finished'. " +
                                                    "Be aware: every command you execute in the same attack should be coherent with the previous ones. " +
                                                    "It is like you are an attacker trying to build an attack strategy step by step. " +
                                                    "Remember not to repeat previous attacks and to start with a random attack if it is the first one. \n\n"})

        # infinite cycle for the current attack until the AI decides to stop
        while True:
            # read the output from SYNAPSE
            SYNAPSE_output = shell.recv(2048).decode()

            # check if AI tried to use sudo command
            if "will be reported" not in SYNAPSE_output:
                # if not, print the message in a realistic fashion and continue the interaction
                last_command = messages[-1]["content"]
                if SYNAPSE_output.startswith(last_command):
                    SYNAPSE_output = SYNAPSE_output[len(last_command):]
                print(SYNAPSE_output, end='')

                # add the output to the list of messages
                messages.append({"role": 'user', "content": SYNAPSE_output})

                # generate the command to input using AI and remove the words 'bash' and 'shell' from the response
                AI_input = generate_response(messages)
                AI_input["content"] = AI_input["content"].replace('bash', '').replace('shell', '').strip()
                print(AI_input["content"], end='')

                # check if the AI decided to stop the current attack
                if AI_input["content"] == "Finished":
                    print(f"\n\nAttack number {count+1} interrupted by AI.")
                    messages.append({"role": 'user', "content": "\n\nCurrent attack finished.\n\n"})
                    count += 1
                    break

                # add the input to the list of messages
                messages.append(AI_input)

                # send the command to SYNAPSE
                shell.send(AI_input["content"] + '\n')

                # wait for SYNAPSE to process the command
                time.sleep(10)
            # if yes, print the message and break the loop because SYNAPSE will exit
            else:
                print(SYNAPSE_output, end='')
                print(f"\nScript interrupted by SYNAPSE.")
                break
    print(f"\nScript interrupted by AI, {count+1} attacks performed.")
# handle the case when the user interrupts the script
except KeyboardInterrupt:
    print("\nScript interrupted by user.")
# handle the case when SYNAPSE exits
except OSError as osError:
    print(f"\nScript interrupted by SYNAPSE.")
finally:
    client.close()