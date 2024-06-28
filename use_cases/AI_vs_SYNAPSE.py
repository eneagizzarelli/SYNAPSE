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

client.connect('localhost', 22, 'enea', 'password')
shell = client.invoke_shell()

while True:
    try:
        SYNAPSE_output = ""
        while shell.recv_ready():
            part = shell.recv(1024).decode()
            SYNAPSE_output += part
            time.sleep(0.1)

        print(SYNAPSE_output, end='')

        messages.append({"role": 'user', "content": SYNAPSE_output})

        AI_input = generate_response(messages)
        print(AI_input["content"])

        messages.append(AI_input)

        shell.send(AI_input["content"])
    except KeyboardInterrupt:
        client.close()
        break

print(messages)