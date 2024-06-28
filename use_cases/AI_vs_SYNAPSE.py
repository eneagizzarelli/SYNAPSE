import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect('localhost', 22, 'enea', 'password')

    shell = client.invoke_shell()

    initial_output = shell.recv(1024).decode()

    print(initial_output, end='')

    shell.send('cd ..\n')

    time.sleep(2)

    command_output = shell.recv(1024).decode()
    print(command_output)
finally:
    client.close()