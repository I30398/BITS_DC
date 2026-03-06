# server2.py
import socket
import os

HOST = '0.0.0.0'
PORT = 9002

config = configparser.ConfigParser()
config.read('config.ini')

FILES_DIR = config['FILES_DIR']['SERVER2']

def send_file(conn, filepath):
    if not os.path.exists(filepath):
        conn.sendall(b'NOT_FOUND')
        return
    conn.sendall(b'FOUND')
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.sendall(data)
    conn.sendall(b'EOF')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER2 listening on {PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                pathname = conn.recv(1024).decode()
                filepath = os.path.join(FILES_DIR, pathname)
                send_file(conn, filepath)

if __name__ == '__main__':
    main()

