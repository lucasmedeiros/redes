import socket
from threading import Thread
from queue import Queue


class UDPServer():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.response = "VALOR INVALIDO"

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

            if operation == 'ADD':
                self.response = str(first_value + second_value)
            elif operation == 'SUB':
                self.response = str(first_value - second_value)
            elif operation == 'MULT':
                self.response = str(first_value * second_value)
            elif operation == 'EXP':
                self.response = str(first_value ** second_value)
            elif operation == 'DIV ' and second_value != 0:
                self.response = str(first_value / second_value)

        except:
            self.response = 'Requisição inválida'

        acks = Queue()

        while True:
            self.socket.sendto(str(self.response).encode('utf-8'), client)
            waiting_thread = Thread(
                target=self.wait_for_client_ack, args=(acks,))
            waiting_thread.start()
            waiting_thread.join(timeout=0.1)

            if acks.qsize() > 0 and acks.get()[0].decode('utf-8') == 'ACK':
                print('ACK do cliente recebido...')
                break

    def wait_for_client_ack(self, acks):
        print('Esperando ACK do cliente...')
        message = self.socket.recvfrom(1024)
        acks.put(message)


if __name__ == "__main__":

    UDPServer('localhost', 5000).run()
