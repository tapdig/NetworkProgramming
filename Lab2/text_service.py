import argparse
import socket
import json
import pickle
import sys

MAX_BYTES = 65535

class Server:
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port

    # function to swap one word with another in text according to json file
    def change_text(self, text_, json_):
        swaps = json.loads(json_)
        for word in swaps.keys():
            text_ = text_.replace(word, swaps[word])
        return text_      
            
    # Vernam cipher implementation; OTP
    def encode_decode(self, text, key):
        result = ""
        ptr = 0
        for char in text:
            result += chr(ord(char) ^ ord(key[ptr]))
            ptr += 1
            if ptr == len(key):
                ptr = 0
        return result

    def server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)
        print(f"Listening at {sock.getsockname()}")
        print('Waiting to accept a new connection')
        print("----------------------------------")
        
        while True:
            sc, sockname = sock.accept()
            print(f"We have accepted a connection from {sockname}")
            print(f"Socket name: {sc.getsockname()}")
            print(f"Socket peer: {sc.getpeername()}")

            n = 0
            while True:
                request = sc.recv(MAX_BYTES)
                if not request:
                    break
                message = pickle.loads(request)

                mode, file1, file2 = message[0], message[1], message[2]

                if mode == "change_text":
                    changed = self.change_text(file1.decode('utf-8'), file2.decode('utf-8'))
                    sc.sendall(changed.encode('utf-8'))
                    print(f"Changed text sent to client: {changed.encode('utf-8')}")
                    print("-------------------------------------------------------")

                elif mode == "encode_decode":
                    en_de_code = self.encode_decode(file1.decode('utf-8'), file2.decode('utf-8'))
                    sc.sendall(en_de_code.encode('utf-8'))
                    print(f"Encoded-Decoded text sent to client: {en_de_code}")
                    print("-------------------------------------------------------")

                n += len(request)
                print(f"\r {n} bytes processed so far", end=' ')
                sys.stdout.flush()

            print()
            sc.close()
            print("Socket closed.")

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def client(self, mode, file1, file2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        print('Client has been assigned socket name ', sock.getsockname())
        print("---------------------------------------------------------")

        text_file = open(file1, "rb")
        text_content = text_file.read()
        text_file.close()
        json_or_key_file = open(file2, "rb")
        json_or_key = json_or_key_file.read()
        json_or_key_file.close()

        sent = (mode, text_content, json_or_key)
        pickle_sent = pickle.dumps(sent)
        sock.sendall(pickle_sent)

        response = sock.recv(MAX_BYTES)
        with open(file1, "wb") as file_changed:
            file_changed.write(response)
        print(f"Server responded with: {response.decode('utf-8')}")

        sock.close()

if __name__ == "__main__":
    choices = {"server": Server, "client": Client}
    parser = argparse.ArgumentParser(description="change or encrypt-decrypt text file over TCP")
    parser.add_argument('role', choices=choices, help="which role to play")
    parser.add_argument('host', help='interface the server listens at; host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default: 1060)')
    
    if sys.argv[1] == "client":
        parser.add_argument('--mode', type=str, help="change text or encode-decode text")
        parser.add_argument('file1', help="path to the first file (text file)")
        parser.add_argument('file2', help="path to the second file (json file for swapping; key text file for encrypting-decrypting)")

    args = parser.parse_args()
    class_ = choices[args.role]

    if args.role == "server":
        class_(args.host, args.p).server()

    elif args.role == "client":
        class_(args.host, args.p).client(args.mode, args.file1, args.file2)