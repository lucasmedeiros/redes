from socket import *

server = '127.0.0.1'
port = 8689

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((server, port))

print('Servidor rodando...')

while 1:
    operation_sentence, client = server_socket.recvfrom(1024)
    elements = operation_sentence.decode('utf-8').split()
    print("RECEBIDO >", elements)

    response = 0

    val1 = int(elements[1])
    val2 = int(elements[2])

    if elements[0] == 'ADD':
        response = val1 + val2
    if elements[0] == 'SUB':
        response = val1 - val2
    if elements[0] == 'MULT':
        response = val1 * val2
    if elements[0] == 'DIV':
        if val2 == 0:
            response = 'INVÁLIDO'
        else:
            response = val1 / val2
    if elements[0] == 'EXP':
        response = val1 ** val2

    server_socket.sendto(str(response).encode('utf-8'), client)
