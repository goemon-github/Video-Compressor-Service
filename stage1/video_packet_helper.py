import os

class Video_packet_helper:
    PACKET_MAX_SIZE = 1400

    

    def generate_first_send_data_size(self):
        if self.is_file_size_within_4GB():
            raise ValueError('file size over limit 4GB')
        else:
            file_size = os.stat(self.file_full_path).st_size
            byte_file_size = file_size.to_bytes(32, 'big') 

            return byte_file_size


    def get_file_name(self):
        self.file_name = os.path.basename(self.file)
            
    def get_file_full_path(self):
        return self.file_full_path

    def set_flie(self, file_path):
        self.file_full_path = os.path.abspath(file_path) 
        print(self.file_full_path)
        self.file_name = os.path.basename(self.file_full_path)
        print(self.file_name)
        self.dir_path = os.path.dirname(self.file_full_path)
        print(self.dir_path)

        print(os.getcwd())

    def is_file_size_within_4GB(self):
        print(os.stat('video'))
        print(os.path.exists(self.file_full_path))
        file_size = os.stat(self.file_full_path).st_size

        return  file_size > 4 * 1024 * 1024 * 1024
            


