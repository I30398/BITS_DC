# client.py
import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SERVER1_HOST = config['SERVER1']['HOST']
SERVER1_PORT = int(config['SERVER1']['PORT'])

# SERVER1_HOST = '10.241.77.221'
# SERVER1_PORT = 9001


def receive_file_until_eof(sock, filename):
    with open(filename, 'wb') as f:
        buffer = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            buffer += data
            eof_index = buffer.find(b'EOF')
            if eof_index != -1:
                f.write(buffer[:eof_index])
                # Remove everything up to and including EOF for next file
                buffer = buffer[eof_index+3:]
                return buffer  # Return leftover buffer for next file
            else:
                f.write(buffer)
                buffer = b''

def receive_two_files(sock, file1, file2):
    leftover = receive_file_until_eof(sock, file1)
    # Now, use leftover buffer for second file
    with open(file2, 'wb') as f:
        buffer = leftover
        while True:
            if buffer:
                eof_index = buffer.find(b'EOF')
                if eof_index != -1:
                    f.write(buffer[:eof_index])
                    break
                else:
                    f.write(buffer)
                    buffer = b''
            data = sock.recv(1024)
            if not data:
                break
            buffer += data

def receive_file(sock, filename):
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if data.endswith(b'EOF'):
                f.write(data[:-3])
                break
            f.write(data)
        print("Recieved file:", filename)



def main():
    while True:
        pathname = input("Enter file name to request (or type 'exit' to quit): ").strip()
        if pathname.lower() == 'exit':
            print("Exiting client.")
            break

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((SERVER1_HOST, SERVER1_PORT))
                s.sendall(pathname.encode())
                status = s.recv(6)
                if status == b'NOT_FO':
                    print("File not found on both servers.")
                    s.recv(3)  # Read the rest of 'NOT_FOUND'
                elif status == b'SAME':
                    print("File is the same on both servers. Downloading...")
                    receive_file(s, 'received_file'+ pathname + '_same')
                elif status == b'ONLY1':
                    print("File found only on SERVER1. Downloading...")
                    receive_file(s, 'received_file'+ pathname + '_server1')
                elif status == b'ONLY2':
                    print("File found only on SERVER2. Downloading...")
                    receive_file(s, 'received_file'+ pathname + '_server2')
                elif status == b'DIFF':
                    print("Files differ on SERVER1 and SERVER2. Downloading both...") 
                    receive_two_files(s, 'received_file'+ pathname + '_server1', 'received_file'+ pathname + '_server2')
                else:
                    print("Unknown response from server.")
            except Exception as e:
                print(f"Error: {e}")

        # Ask user if they want to continue or exit
        while True:
            choice = input("Do you want to request another file? (y/n): ").strip().lower()
            if choice == 'n':
                print("Exiting client.")
                return
            elif choice == 'y':
                break
            else:
                print("Please enter 'y' to continue or 'n' to exit.")


if __name__ == '__main__':
    main()

