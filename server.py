import socket, email, sys, configparser, re

# set up rewrite config
config = configparser.ConfigParser()
config.read('url_rewrite.ini')

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000


def request_parser(request):
    """parse request from clients"""

    url = request.split('\r\n', 1)[0]
    headers = request.split('\r\n', 1)[1]
    http_method = url.split()[0]
    path = url.split()[1]

    #redirect root request to /index.html
    if path == "/":
        path = "/index.html"

    # construct a message from the request string
    message = email.message_from_string(headers)
    # construct a dictionary containing the headers
    headers = dict(message.items())
    
    data = message.get_payload()

    return {"url":url,
            "headers":headers,
            "method":http_method,
            "path":path,
            "data":data}


def url_rewrite(path):
    """Rewrite urls paths"""

    new_path = ""
    #checks for rewrite rule that matches the path
    for urls in (config.items("RewriteRule")):
        if re.match(urls[1].split()[0], path):
            # get argument names from rules and argument values from url path
            new_path = urls[1].split()[1]
            arg_names = re.findall(r"\$\d",(new_path))
            arg_values = path.split("/")[1:]

            #check if all arguments were passed
            if len(arg_names) != len(arg_values):
                return ""
            
            # replace each argument name in the new path with the corresponding value
            for i in range(len(arg_names)):
                new_path = re.sub('\\'+arg_names[i], arg_values[i], new_path)

    return new_path





def main(argv):
    if argv:
        SERVER_PORT = int(argv[0])

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:    
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        request = request_parser(request)
        
        response = ''

        # process GET request
        if request["method"] == "GET":
            
            content = url_rewrite(request["path"][1:])
            if content:
                response = 'HTTP/1.0 200 OK\n\n' + content
            else:
                try:
                    # Get the content of the file
                    file = open('templates' + request["path"])
                    content = file.read()
                    file.close()
                    response = 'HTTP/1.0 200 OK\n\n' + content
                except FileNotFoundError:
                    response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

        # process POST request
        elif request["method"] == "POST":
            content = request["data"]
            response = 'HTTP/1.0 200 OK\n\n' + content
        
        else:
            response = 'HTTP/1.0 405 Method Not Allowed\n\nOnly accepts GET and POST requests '

        # # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()

    # Close socket
    server_socket.close()

if __name__ == "__main__":
   main(sys.argv[1:])
