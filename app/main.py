import argparse
import socket
import threading
from os import path

class MyServer:
    HOST = None
    PORT = None

    def __init__(self, host="localhost", port=4221, directory=None):
        """Initialize socket with host and port."""
        self.HOST = host
        self.PORT = port
        self.directory = directory
        self.server_socket = socket.create_server((self.HOST, self.PORT), reuse_port=True)
    
    def start(self):
        """Start server to handle request."""
        print(f"Running server on {self.HOST}:{self.PORT}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_request, args=(client_socket, client_address))
                thread.start()
        except KeyboardInterrupt:
            print("Stopping server")
        finally:
            self.server_socket.close()
    
    def handle_request(self, client_socket, client_address):
        """Logic to handle request."""
        request_line = client_socket.recv(1024).decode()
        request_content = request_line.split('\r\n')
        headers = {}
        for i, content in enumerate(request_content):
            if i == 0 : 
                request_type, url, http_version = content.split(" ")
            elif i == len(request_content) -1:
                body = content
            elif content and ':' in content:
                key, val = content.split(": ")
                headers[key] = val
            
        url = url.strip()
        # Add Failsafe condition to return 404 in all cases not implemented
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        if request_type == 'GET':
            if url == '/':
                response = "HTTP/1.1 200 OK\r\n\r\n"
            elif url.startswith('/echo'):
                response = self.do_echo(url)
            elif url.startswith('/user-agent'):
                response = self.get_user_agent(headers.get("User-Agent", ""))
            elif url.startswith('/files/'):
                response = self.get_files(url)
        elif request_type == 'POST':
            if url.startswith('/files/'):
                response = self.create_files(url, body)
        client_socket.sendall(str.encode(response))
        client_socket.close()
    
    def do_echo(self, url):
        """
        Implement the /echo/{str} endpoint, which accepts a string and returns it in the response body.
        Request GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
        Response 
        HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
        Here's a breakdown of the response:

        // Status line
        HTTP/1.1 200 OK
        \r\n                          // CRLF that marks the end of the status line

        // Headers
        Content-Type: text/plain\r\n  // Header that specifies the format of the response body
        Content-Length: 3\r\n         // Header that specifies the size of the response body, in bytes
        \r\n                          // CRLF that marks the end of the headers

        // Response body
        abc                           // The string from the request

        """
        string = url.replace('/echo/', "").split('/')[0]
        length = len(string)
        response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {length}\r\n\r\n{string}"""
        return response
    
    def get_user_agent(self, user_agent):
        """
        Implement the /user-agent endpoint, which reads the User-Agent request header and returns it in the response body.
        // Request line
        GET
        /user-agent
        HTTP/1.1
        \r\n

        // Headers
        Host: localhost:4221\r\n
        User-Agent: foobar/1.2.3\r\n  // Read this value
        Accept: */*\r\n
        \r\n

        // Request body (empty)
        -----------------------------------------------

        Here is the expected response:

        // Status line
        HTTP/1.1 200 OK               // Status code must be 200
        \r\n

        // Headers
        Content-Type: text/plain\r\n
        Content-Length: 12\r\n
        \r\n

        // Response body
        foobar/1.2.3                  
        """
        
        length = len(user_agent)
        response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {length}\r\n\r\n{user_agent}"""
        return response
    
    def get_files(self, url):
        """
        Request: 
        curl -i http://localhost:4221/files/foo
        Response:
        HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 14\r\n\r\nHello, World!
        """
        filepath = path.join(self.directory, url.split('/')[2])
        
        if path.exists(filepath):
            with open(filepath) as file:
                content = file.read()
                response = f"""HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}"""
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
        return response

    def create_files(self, url, content):
        """
        // Request line
        POST /files/number HTTP/1.1
        \r\n

        // Headers
        Host: localhost:4221\r\n
        User-Agent: curl/7.64.1\r\n
        Accept: */*\r\n
        Content-Type: application/octet-stream  // Header that specifies the format of the request body
        Content-Length: 5\r\n                   // Header that specifies the size of the request body, in bytes
        \r\n

        // Request Body
        12345

        Response HTTP/1.1 201 Created\r\n\r\n
        """
        with open(path.join(self.directory, url.split('/')[2]), 'w') as write_file:
            write_file.write(content)
        return "HTTP/1.1 201 Created\r\n\r\n"




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='My Simple Server',
                    description='This program runs a small server with limited functionalities')
    parser.add_argument('-d', '--directory')  
    args = parser.parse_args()
    server = MyServer(directory=args.directory)
    server.start()
