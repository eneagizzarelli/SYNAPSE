import sys
import time
import paramiko

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

messages = [{"role": 'system', "content": "You are a Linux user interacting with a Linux OS terminal. " +
                                        "You can use not only the terminal, but also a MySQL service where, other than the root, user 'enea' with password 'password' exists. " +
                                        "Issue some commands to interact with the OS file system and the MySQL service. " + 
                                        "Generate just the command you want to execute, nothing else. \n"}]

client.connect('localhost', 22, 'enea', 'password')
shell = client.invoke_shell()

try:
    while True:
        if shell.recv_ready():
            SYNAPSE_output = shell.recv(1024).decode()

            if "will be reported" not in SYNAPSE_output:
                last_command = messages[-1]["content"]
                if SYNAPSE_output.startswith(last_command):
                    SYNAPSE_output = SYNAPSE_output[len(last_command):]
                print(SYNAPSE_output, end='')

                messages.append({"role": 'user', "content": SYNAPSE_output})

                AI_input = generate_response(messages)
                print(AI_input["content"], end='')

                messages.append(AI_input)

                shell.send(AI_input["content"] + '\n')

                time.sleep(10)
except KeyboardInterrupt:
    print("\nScript interrupted by user.")
except OSError as osError:
    print(f"\nScript interrupted by SYNAPSE.")
finally:
    client.close()