from socket import *

# AF_INET --> Internet Protocol v4 addresses
# SOCK_STREAM --> for TCP
# SOCK_DGRAM --> for UDP
serverSocket = socket(AF_INET, SOCK_STREAM)

# assigns an IP address and a port number to a socket
serverSocket.bind(('127.0.0.1', 1200))

# server begins listening for incoming TCP requests
serverSocket.listen(1)

while True:
    print("Server is running")
    # server waits on accept() for incoming requests, new socket created on return
    connectionSocket, addr = serverSocket.accept()
    try:
        # read bytes from socket (but not address as in UDP)
        message = connectionSocket.recv(1024)
        print(message)

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1].decode('utf-8').strip("/")
        print(filename)
        f = open(filename)
        outputdata = f.read()
        f.close()

        # Send the HTTP response header line to the connection socket
        # Format: "HTTP/1.1 code-for-successful-request\r\n\r\n"
        connectionSocket.send('HTTP/1.0 200 OK\r\n\r\n'.encode())

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.close()

    except IOError:
        connectionSocket.send('404 Not Found'.encode())
        connectionSocket.close()

serverSocket.close()