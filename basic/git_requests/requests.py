import socket
import os
import time
import zipfile
from threading import Thread, Lock
from ttkbootstrap import *
import basic.NCE as NCE


SERVER_HOST = "archives.hlhtstudios.com"
SERVER_PORT = 105*50+3714
DOWNLOAD_PORT = 2204
ACCOUNT_PORT = 7812
MSG_PORT = 3380
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
LOCK = Lock()
SALT = NCE.encryption_key("HLHT Studios", "3714")


class NetPath:

    def __init__(self, _type, real_name, upload_time, size, encrypted, public="false"):
        self.type = _type
        self.path = real_name
        self.upload_time = float(upload_time)
        self.size = int(size)
        self.encrypted = encrypted
        self.public = public


class NetTree:

    def __init__(self, master, items: list):
        self.items = []
        self.master = master
        self.folders = []
        self.files = []
        for i in items:
            if i:
                file = NetPath(*i.split(":"))
                if file.type == "folder":
                    self.folders.append(file)
                else:
                    self.files.append(file)
        self.path = self

    def isdir(self, path):
        for i in self.folders:
            if path == i.path:
                return True
        return False

    def isfile(self, path):
        for i in self.files:
            if path == i.path:
                return True
        return False

    def listdir(self, path):
        final = []
        for i in self.folders:
            if os.path.dirname(i.path) == path:
                final.append(i.path)

        for i in self.files:
            if os.path.dirname(i.path) == path:
                final.append(i.path)

        final.sort()

        return final

    def list_root(self):
        final = []
        for i in self.folders:
            if "\\" not in i.path:
                final.append(i.path)

        for i in self.files:
            if "\\" not in i.path:
                final.append(i.path)

        return final

    def get_item(self, path):
        if self.isdir(path):
            for i in self.folders:
                if i.path == path:
                    return i
        elif self.isfile(path):
            for i in self.files:
                if i.path == path:
                    return i
        return 0

    def basename(self, path):
        for file in self.files:
            if file.path == path:
                return os.path.basename(file.path)
        for folder in self.folders:
            if folder.path == path:
                return os.path.basename(folder.path)
        return ""

    def dirname(self, path):
        return os.path.dirname(path)

    def rename(self, path, name):
        dirname = self.dirname(path)
        self.get_item(path).path = f"{dirname}\\{name}"
        self.master.rename(path, f"{dirname}\\{name}")

    def getsize(self, filename):
        for file in self.files:
            if file.path == filename:
                return file.size

    def get_total_size(self):
        total_size = 0
        for file in self.files:
            total_size += file.size

        return total_size


class NetFileSystem:

    def __init__(self, username, auth):
        self.username = username
        self.auth = auth
        self.msg = ""
        self.recv_msg = False

    def upload_file(self, local_path, path: str, progress: Progressbar):

        def upload(filename, dirname):
            tcp_s = socket.socket()
            file_path = filename.replace(dirname, '').lstrip('\\') if dirname else os.path.basename(filename)
            print(file_path+"\n")
            server_filename = f"{path}\\{file_path}"
            file_size = os.path.getsize(file)

            # get the file size

            tcp_s.connect((SERVER_HOST, SERVER_PORT))

            tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}{server_filename}{SEPARATOR}{file_size}{SEPARATOR}false".encode())

            tcp_s.recv(BUFFER_SIZE)  # start

            with open(filename, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    tcp_s.sendall(bytes_read)
                    progress['value'] += len(bytes_read)

            tcp_s.close()

        dirname = local_path if isinstance(local_path, str) else ""
        local_path = self.extract_files(local_path)

        progress['maximum'] = 0
        for file in local_path:
            filesize = os.path.getsize(file)
            progress['maximum'] += filesize
        progress['value'] = 0

        for file in local_path:
            # thread = Thread(target=upload, args=[file])
            # thread.start()
            upload(file, dirname)

    def extract_files(self, files):
        if isinstance(files, list):
            return files
        elif isinstance(files, str):
            total = []
            if os.path.isdir(files):
                for path, dirs, files2 in os.walk(files):
                    for filename in files2:
                        if filename not in ["desktop.ini"]:
                            total.append(f"{path}\\{filename}")
            elif os.path.isfile(files):
                total.append(files)
            return total
        return ""

    def receive_file(self, name, tdr, option, progress: Progressbar):
        tcp_s = socket.socket()

        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))

        tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}{option}{SEPARATOR}{name}".encode())

        # receive_tcp = socket.socket()
        # receive_tcp.bind(("0.0.0.0", 33380))
        connection = tcp_s

        received = connection.recv(BUFFER_SIZE)
        received = received.decode()

        name, size = received.split(SEPARATOR)
        original_name = name
        if option == "get_folder":
            name = name.replace("\\", "_")
            name = f"{name}.zip"
        size = int(size)

        progress['maximum'] = size
        progress['value'] = 0

        connection.sendall("start".encode())

        # if not os.path.exists(f"{tdr}\\{os.path.dirname(name)}"):
        #     os.mkdir(f"{tdr}\\{os.path.dirname(name)}")
        with open(f"{tdr}\\{os.path.basename(name)}", "wb") as f:
            while True:
                bytes_read = connection.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress['value'] += len(bytes_read)

        tcp_s.close()

        if option == "get_folder":
            if not os.path.exists(f"{tdr}\\{os.path.basename(original_name)}"):
                os.makedirs(f"{tdr}\\{os.path.basename(original_name)}")
            with zipfile.ZipFile(f"{tdr}\\{name}") as zfile:
                zfile.extractall(f"{tdr}\\{os.path.basename(original_name)}")
            os.remove(f"{tdr}\\{name}")

    def share(self, name):
        tcp_s = socket.socket()
        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))
        tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}share{SEPARATOR}{name}".encode())
        tcp_s.close()

    def delete(self, name):
        tcp_s = socket.socket()
        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))
        tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}delete{SEPARATOR}{name}".encode())
        tcp_s.close()

    def copy(self, name, tdr, option):
        content = f"{name}:{tdr}"
        tcp_s = socket.socket()
        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))
        tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}{option}{SEPARATOR}{content}".encode())
        tcp_s.close()

    def move(self, name, tdr, option):
        content = f"{name}:{tdr}"
        tcp_s = socket.socket()
        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))
        tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}{option}{SEPARATOR}{content}".encode())
        tcp_s.close()

    def get_tree(self):
        tcp_s = socket.socket()

        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))

        tcp_s.sendall(f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}get_tree{SEPARATOR}none".encode())

        tree_content = ""
        tcp_s.recv(BUFFER_SIZE)
        while True:
            bytes_read = tcp_s.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            tree_content += bytes_read.decode()
        tree = tree_content.splitlines(False)
        self.recv_msg = False
        return NetTree(self, tree)

    def rename(self, file, name):

        rename_content = f"{file}:{name}"
        tcp_s = socket.socket()

        # get the file size

        tcp_s.connect((SERVER_HOST, DOWNLOAD_PORT))

        tcp_s.sendall(
            f"{self.username}{SEPARATOR}{self.auth}{SEPARATOR}rename{SEPARATOR}{rename_content}".encode())
        tcp_s.recv(BUFFER_SIZE)
        tcp_s.close()

    def msg_port(self):
        self.recv_msg = True
        Thread(target=self._msg_port).start()

    def _msg_port(self):
        tcp_s = socket.socket()

        # get the file size

        tcp_s.connect((SERVER_HOST, MSG_PORT))

        tcp_s.sendall(
            f"{self.username}{SEPARATOR}{self.auth}".encode())
        while self.recv_msg:
            message = tcp_s.recv(BUFFER_SIZE)
            self.msg = message.decode()


if __name__ == '__main__':
    def initSize(size):
        final = 0
        if size < 1024:
            final = f"{size}bytes"
        elif 1024 <= size < 1024 * 1024:
            final = f"{round(size / 1024, 2)}KB"
        elif 1024 * 1024 <= size < 1024 * 1024 * 1024:
            final = f"{round(size / 1024 / 1024, 2)}MB"
        elif 1024 * 1024 * 1024 <= size < 1024 * 1024 * 1024 * 1024:
            final = f"{round(size / 1024 / 1024 / 1024, 2)}GB"
        return final


    def update_progress(progress, per_bar):
        count = 0
        while True:
            percentage = f"{round(progress['value'] / progress['maximum'] * 100, 2)} %" if progress['maximum'] != 0 else "0 %"
            speed = f"{initSize(count * 2)}/s"
            per_bar.configure(text=f"{percentage} | {speed} | {initSize(progress['value'])}/{initSize(progress['maximum'])}")
            per_bar.pack()
            start_mark = progress['value']
            time.sleep(0.5)
            end_mark = progress['value']
            count = end_mark - start_mark

    _auth = "f5b4851d5acc5ab1b11f9646c3802a7b1cc85be8551d4f3ee4bbec2218e89dcd"
    user = "Hold Wind"
    net = NetFileSystem(user, _auth)
    root = Window()
    aaa = Progressbar(root)
    aaa.pack()
    per = Label(root)
    per.pack()
    bbb = Progressbar(root)
    bbb.pack()
    per2 = Label(root)
    per2.pack()
    # net.receive_file("Image\\ImageTest2", "C:\\Users\\Hold Wind\\Downloads", "get_folder", aaa)
    # net.receive_file("Image\\ImageTest\\khl20230523144654086.png", "C:\\Users\\Hold Wind\\Downloads", "get_file", aaa)
    # net.copy("Image\\ImageTest", "Image\\ImageTest2", "copy_folder")
    # Thread(target=net.upload_file,
    #        args=["H:\\Videos\\Apex Legends\\Apex Legends 2023.08.20 - 06.04.49.05.DVR.mp4", "Videos\\VideoTest", aaa]).start()
    # Thread(target=net.upload_file,
    #        args=["C:\\Users\\Hold Wind\\Pictures", "Images", aaa]).start()
    # Thread(target=net.upload_file,
    #        args=["C:\\Users\\Hold Wind\\Pictures", "Images\\TestImages", bbb]).start()

    # net.share("Image\\ImageTest")
    # net.delete("Images\\TestImages")

    tree = net.get_tree()
    for i in tree.files:
        upload_time = time.localtime(i.upload_time)
        up_time = f"{upload_time.tm_year}/{upload_time.tm_mon}/{upload_time.tm_mday} {upload_time.tm_hour}:{upload_time.tm_min}:{upload_time.tm_sec}"
        print(f"FILE : {i.path} | {up_time} | {initSize(i.size)} | {i.encrypted} | {i.public}")
    for i in tree.folders:
        print(f"FOLDER : {i.path} | {i.encrypted} | {i.public}")

    # print(initSize(tree.get_total_size()))
    # print(tree.list_root())


    # net.copy("Image\\ImageTest", "ImageTest", "copy_folder")

    # Thread(target=net.receive_file, args=["Image", "C:\\Users\\Hold Wind\\Downloads", "get_folder", aaa]).start()
    # Thread(target=net.receive_file, args=["Image\\ImageTest2", "C:\\Users\\Hold Wind\\Downloads", "get_folder", bbb]).start()
    Thread(target=update_progress, args=[aaa, per]).start()
    Thread(target=update_progress, args=[bbb, per2]).start()
    root.mainloop()



