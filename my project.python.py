import socket
import threading

# अपना निकनेम चुनें
nickname = input("अपना नाम चुनें: ")

# सर्वर से जुड़ने के लिए सेटिंग्स
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# सर्वर से मैसेज सुनने के लिए
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# सर्वर को मैसेज भेजने के लिए
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# थ्रेड्स शुरू करें ताकि सुनना और लिखना साथ में हो सके
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()