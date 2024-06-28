import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect('localhost', 22, 'enea', 'password')

    shell = client.invoke_shell()

    initial_output = shell.recv(1024).decode()

    print(initial_output)

    shell.send('ls -l\n')
    while not shell.recv_ready():
        pass
    command_output = shell.recv(1024).decode()
    print(command_output)
finally:
    client.close()