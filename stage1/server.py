import json
import socket
import os


class Server():
    def __init__(self):
        self.tcp_sock = self.create_tcp_sock()

    def create_tcp_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 9001))
        sock.listen()
        return sock


    def run(self):
        connection, _ = self.tcp_sock.accept()
        print('Listen......')

        file_size = self.receive_first_packet(connection)
        self.receive_second_packet(connection, file_size)
        byte_padding_payload = self.responce_payload()
        print('-----responce ------')
        connection.sendall(byte_padding_payload)

        connection.close()

    def receive_first_packet(self, connection):
        file_size = int.from_bytes(connection.recv(32), 'big')        
        print('total_file_size: {}'.format(file_size))
        return file_size

    def receive_second_packet(self, connection, file_size):
        data_received = b''
        while True:
            data = connection.recv(1400)
            #print(data)
            if not data:
                break
            data_received += data
            if data_received.endswith(b'EOF'):
                data_received = data_received[:-3]
                break
                

        if len(data_received) == file_size :
            current_path = os.getcwd()
            file_name = 'output.mp4'
            with open(current_path + '/uploads/' + file_name, 'wb') as f:
                f.write(data_received)
        else:
            print('---no data---')
            print(data_received)


    def responce_payload(self):
        payload = 'upload finish'
        padding_payload = payload.ljust(16)
        byte_padding_payload = padding_payload.encode('utf-8')
        return byte_padding_payload



if __name__ == '__main__':
    server = Server()
    server.run()