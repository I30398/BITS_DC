# server1.py
import socket
import os

HOST = '0.0.0.0'
PORT = 9001
SERVER2_HOST = '10.241.77.209'
SERVER2_PORT = 9002
FILES_DIR = './server1/'

def receive_file(sock, temp_filename):
    status = sock.recv(6)
    if status == b'NOT_FO':
        sock.recv(3)  # Read the rest of 'NOT_FOUND'
        return False
    with open(temp_filename, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if data.endswith(b'EOF'):
                f.write(data[:-3])
                break
            f.write(data)
    return True

def compare_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while True:
            b1 = f1.read(1024)
            b2 = f2.read(1024)
            if b1 != b2:
                return False
            if not b1:
                break
    return True

def send_file(conn, filepath):
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.sendall(data)
    conn.sendall(b'EOF')

def send_both_files(conn, file1, file2):
    conn.sendall(b'DIFF')
    send_file(conn, file1)
    send_file(conn, file2)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER1 listening on {PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                pathname = conn.recv(1024).decode()
                local_path = os.path.join(FILES_DIR, pathname)
                local_exists = os.path.exists(local_path)

                # Connect to SERVER2
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    try:
                        s2.connect((SERVER2_HOST, SERVER2_PORT))
                        s2.sendall(pathname.encode())
                        server2_temp = 'server2_tempfile'
                        server2_exists = receive_file(s2, server2_temp)
                    except Exception:
                        server2_exists = False

                if not local_exists and not server2_exists:
                    conn.sendall(b'NOT_FOUND')
                elif local_exists and server2_exists:
                    if compare_files(local_path, server2_temp):
                        conn.sendall(b'SAME')
                        send_file(conn, local_path)
                    else:
                        send_both_files(conn, local_path, server2_temp)
                    os.remove(server2_temp)
                elif local_exists:
                    conn.sendall(b'ONLY1')
                    send_file(conn, local_path)
                else:
                    conn.sendall(b'ONLY2')
                    send_file(conn, server2_temp)
                    os.remove(server2_temp)

if __name__ == '__main__':
    main()

