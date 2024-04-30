import socket
import os
import video_packet_helper


class Client():
    def __init__(self):
        self.tcp_sock = self.create_tcp_sock()
        self.video_packet_helper = video_packet_helper.Video_packet_helper()
        

    def create_tcp_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock


    def run(self):
        self.tcp_sock.connect(('127.0.0.1', 9001))

        while True: 
            self.input_file()
            try:
                first_send_data_size = self.video_packet_helper.generate_first_send_data_size()
                self.tcp_sock.sendall(first_send_data_size)

                with open(self.video_packet_helper.get_file_full_path(), 'rb') as f:
                    while (chunk := f.read(1400)):
                        #print(chunk)
                        self.tcp_sock.sendall(chunk)


                    print('----send finsh ----')
                    self.tcp_sock.sendall(b'EOF')


                self.receive_sock()
                break

            except ValueError as e:
                print(e)


    def receive_sock(self):
        print('----receive----')
        while True:
            data = self.tcp_sock.recv(16)
            if data:
                print('----receive decode----')
                data_decode = data.decode('utf-8').strip()
                print('responce: {}'.format(data_decode))
                break



    def input_file(self):
        while True:
            self.file_path = input('mp4ファイルを指定してください: ')
            if self.file_path.endswith('mp4'):
                current_directory = os.getcwd()
                self.file_path = current_directory + '/video/' + self.file_path
                self.video_packet_helper.set_flie(self.file_path) 
                break




if __name__ == '__main__':
    client = Client()
    client.run()