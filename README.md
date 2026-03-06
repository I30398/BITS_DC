# How to Run the Distributed File System Application

Follow the steps below to start the client and servers.

---

## 1. Modify the Configuration

Edit the **config.ini** file and ensure the correct storage directories are set.

Example:
[SERVER1]
SERVER1_HOST = 10.241.77.221
SERVER1_PORT = 9001

[SERVER2]
SERVER2_HOST = 10.241.77.209
SERVER2_PORT = 9002

[FILES_DIR]
SERVER1 = ./server1/
SERVER2 = ./server2/


These directories will store the files used by each server.

---

## 2. Prepare Storage Directories

Create the directories specified in **config.ini**.

Example:
server1/
server2/


Place test files in these folders as needed.

- `server1/` → files for **Server1**
- `server2/` → files for **Server2**

Example structure:
project/
│
├── client.py
├── server1.py
├── server2.py
├── config.ini
│
├── server1/
│ └── example.txt
│
└── server2/
└── example.txt


---

## 3. Start Server2

Run the secondary server first.

python server2.py


Server2 will start listening for requests from **Server1**.

---

## 4. Start Server1

Run the primary server.

python server1.py


Server1 will:

- Accept requests from the **client**
- Contact **Server2** when needed
- Compare files between both servers

---

## 5. Start the Client

Run the client program.

python client.py

The client will:

1. Ask for a file name
2. Send request to **Server1**
3. Download the file(s) based on the response.

---

## 6. File Placement

Place test files in the directories specified in **config.ini**.

Example:
server1/test_1
server2/test_1


Possible cases:

| Case | Result |
|-----|------|
| File exists in both folders and same | Client downloads one file |
| File exists only in server1 | Client downloads Server1 file |
| File exists only in server2 | Client downloads Server2 file |
| File exists in both but different | Client downloads both versions |

---

## Example Run Order
python server2.py

python server1.py

python client.py


---

## Notes

- Start **Server2 first**, then **Server1**, then **Client**.
- Ensure ports configured in the code are not blocked.
- Make sure storage directories exist before starting the servers.


