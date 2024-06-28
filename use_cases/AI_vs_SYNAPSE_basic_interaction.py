import sys
import time
import paramiko

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

# create a new SSH client
client = paramiko.SSHClient()
# set policy to auto add the host key
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# minimal prompt definition to instruct the AI
messages = [{"role": 'system', "content": "You are a Linux user interacting with a Linux OS terminal. " +
                                        "You can use not only the terminal, but also a MySQL service where, other than the root, user 'enea' with password 'password' exists. " +
                                        "Issue some commands to interact with the OS file system and the MySQL service. " + 
                                        "Generate just the command you want to execute, nothing else. \n"}]

# connect to the SSH server using the provided credentials and start an interactive shell
client.connect('localhost', 22, 'enea', 'password')
shell = client.invoke_shell()

try:
    while True:
        # read the output from SYNAPSE
        SYNAPSE_output = shell.recv(1024).decode()

        # check if AI tried to use sudo command
        if "will be reported" not in SYNAPSE_output:
            # if not, print the message in a realistic fashion and continue the interaction
            last_command = messages[-1]["content"]
            if SYNAPSE_output.startswith(last_command):
                SYNAPSE_output = SYNAPSE_output[len(last_command):]
            print(SYNAPSE_output, end='')

            # add the output to the list of messages
            messages.append({"role": 'user', "content": SYNAPSE_output})

            # generate the command to input using AI
            AI_input = generate_response(messages)
            print(AI_input["content"], end='')

            # add the input to the list of messages
            messages.append(AI_input)

            # send the command to SYNAPSE
            shell.send(AI_input["content"] + '\n')

            # wait for SYNAPSE to process the command
            time.sleep(5)
        # if yes, print the message and break the loop because SYNAPSE will exit
        else:
            print(SYNAPSE_output, end='')
            print(f"\nScript interrupted by SYNAPSE.")
            break
# handle the case when the user interrupts the script
except KeyboardInterrupt:
    print("\nScript interrupted by user.")
# handle the case when SYNAPSE exits
except OSError as osError:
    print(f"\nScript interrupted by SYNAPSE.")
finally:
    client.close()