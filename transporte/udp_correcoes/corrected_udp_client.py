import socket
from threading import Thread
from queue import Queue


class UDPClient():

    def __init__(self, server_ip, server_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (server_ip, server_port)

    def run(self):
        user_input = input('Informe a operação: ')

        self.user_input = user_input

        while True:
            responses = Queue()

            main_thread = Thread(target=self.req_handle, args=(responses,))
            main_thread.start()
            main_thread.join(timeout=2)
            main_thread._stop()

            if responses.qsize() > 0:
                break

    def req_handle(self, responses):
        acks = Queue()

        while True:
            self.socket.sendto(self.user_input.encode('utf-8'), self.dest)

            waiting_thread = Thread(
                target=self.wait_for_server_ack, args=(acks, ))
            waiting_thread.start()
            waiting_thread.join(timeout=0.1)

            if acks.qsize() > 0 and acks.get()[0].decode('utf-8') == 'ACK':
                print('ACK do servidor recebido...')
                break

        response = self.socket.recvfrom(1024)

        if response[0].decode('utf-8') != 'ACK':
            print(response[0].decode('utf-8'))
            responses.put(response)
            self.socket.sendto('ACK'.encode('utf-8'), self.dest)

    def wait_for_server_ack(self, acks):
        print('Esperando ACK do servidor...')
        message = self.socket.recvfrom(1024)
        acks.put(message)


if __name__ == '__main__':

    UDPClient("localhost", 5000).run()
