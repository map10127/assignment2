import socket
import sys

def webServer(port=13331):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("", port))
    serverSocket.listen(1)

    print(f"Web server running on port {port}...")

    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()

        try:
            # Receive the client's request
            message = connectionSocket.recv(1024).decode()

            if not message:
                connectionSocket.close()
                continue

            # Extract the filename from the request message
            filename = message.split()[1]

            try:
                # Open and read the requested file
                with open(filename[1:], 'r') as f:  # Remove the leading '/'
                    outputdata = f.read()

                # Create HTTP response header
                header = "HTTP/1.1 200 OK\r\n"
                header += "Content-Type: text/html\r\n"
                header += f"Content-Length: {len(outputdata)}\r\n"
                header += "Server: CustomPythonServer/1.0\r\n"
                header += "Connection: close\r\n"  # Ensures connection closes after response
                header += "\r\n"

                # Send the entire response (header + body) at once
                response = header + outputdata
                connectionSocket.sendall(response.encode())

            except IOError:
                # Send HTTP response message for file not found
                header = "HTTP/1.1 404 Not Found\r\n"
                header += "Content-Type: text/html\r\n"
                header += "Server: CustomPythonServer/1.0\r\n"
                header += "Connection: close\r\n"
                header += "\r\n"
                body = "<html><body><h1>404 Not Found</h1></body></html>"

                response = header + body
                connectionSocket.sendall(response.encode())

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the client socket
            connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
