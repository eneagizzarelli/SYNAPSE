import sys
import time
import paramiko

sys.path.append("/home/enea/SYNAPSE/src")
from ai_requests import generate_response

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

messages = [{"role": 'system', "content": "You are a normal Linux user interacting with a Linux OS terminal. " + 
                                        "Issue some commands to interact with the OS file system. " + 
                                        "Generate just the command you want to execute, nothing else. \n"}]

while True:
    try:
        client.connect('localhost', 22, 'enea', 'password')
        shell = client.invoke_shell()

        SYNAPSE_output = shell.recv(1024).decode()
        print(SYNAPSE_output, end='')

        messages.append({"role": 'user', "content": SYNAPSE_output})

        print(messages)

        AI_input = generate_response(messages)
        print(AI_input["content"])

        messages.append(AI_input)

        print(messages)

        shell.send(AI_input)

        time.sleep(3)
    except KeyboardInterrupt:
        client.close()
        break

print(messages)