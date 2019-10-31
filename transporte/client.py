from socket import *

serverName = "127.0.0.1"
serverPort = 8689

client_socket = socket(AF_INET, SOCK_DGRAM)
dest = (serverName, serverPort)

operation_sentence = input('Operação: ')
client_socket.sendto(operation_sentence.encode('utf-8'), dest)

response = client_socket.recvfrom(1024)

print(response[0].decode('utf-8'))
