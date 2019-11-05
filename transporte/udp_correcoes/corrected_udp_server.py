import socket
from threading import Thread


class UDPServer(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self.socket.bind((self.ip, self.port))
        print("Servidor UDP rodando...")

        while True:
            operation, client = self.socket.recvfrom(1024)

            Thread(target=self.req_handle,
                   args=(operation, client, )).start()

    def req_handle(self, operation, client):
        self.socket.sendto('ACK'.encode('utf-8'), client)

        elements = operation.decode('utf-8').split()

        try:
            operation = elements[0]
            first_value = int(elements[1])
            second_value = int(elements[2])
            response = 'VALOR INVALIDO'

            if operation == 'ADD':
                response = str(first_value + second_value)
            elif operation == 'SUB':
                response = str(first_value - second_value)
            elif operation == 'MULT':
                response = str(first_value * second_value)
            elif operation == 'EXP':
                response = str(first_value ** second_value)
            elif operation == 'DIV ' and second_value != 0:
                response = str(first_value / second_value)

            print(elements, response)
        except:
            response = 'Requisição inválida'

        self.socket.sendto(str(response).encode('utf-8'), client)


if __name__ == "__main__":

    UDPServer('localhost', 5000).run()
