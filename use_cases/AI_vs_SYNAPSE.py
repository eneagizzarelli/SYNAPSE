import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect('localhost', 22, 'enea', 'password')

    shell = client.invoke_shell()

    time.sleep(1)

    if shell.recv_ready():
        initial_output = shell.recv(1024).decode()
        print(initial_output)
    else:
        print('No data received')

    shell.send('cd ..\n')

    time.sleep(1)

    if shell.recv_ready():
        command_output = shell.recv(1024).decode()
        print(command_output)
    else:
        print('No data received')
finally:
    client.close()