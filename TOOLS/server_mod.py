import os
import json
from hdfs import InsecureClient
from hdfs import util

class DataProcessor:

    def __init__(self, data_path = None):
        if data_path == None:
            self.data_path = r'./config/connect_info.json'
        else:
            assert type(data_path) == str
            self.data_path = data_path
        if not os.path.exists(self.data_path):
            self.data_path = r'./connect_info.json'

        with open(self.data_path) as data_file:
            data = json.load(data_file)
            self.hdfs_client = InsecureClient(url = 'http://' + data['namenode_url'] + ':' + str(data['port']), user = data['user'], root = data['root_path'])
            self.img_dir = data['img_dir']

        if self.img_dir[-1] != '/':
            self.img_dir += '/'
        else:
            pass
        
        self.file_name = 1
    
    def InitImgDir(self):
        try:
            list_rslt = self.hdfs_client.list(self.img_dir)
            if len(list_rslt) > 0:
                for name in list_rslt:
                    file_path = self.img_dir + name
                    self.hdfs_client.delete(file_path)

        except util.HdfsError:
            self.hdfs_client.makedirs(self.img_dir)

        return True

    def DataProcess(self, data, append = False, file_name = None):
        assert type(data) == str
        if file_name == None:
            file_name = self.img_dir + str(self.file_name)
        else:
            assert(type(file_name)) == str
        print("File_name: ", file_name)
        self.hdfs_client.write(file_name, data, overwrite = True,  replication = 1, append = append)
        return True

    def Upload(self, file_path, threads = 2):
        self.hdfs_client.upload(hdfs_path = self.img_dir[:-1], local_path = file_path, n_threads = threads, overwrite = True)
        return 0