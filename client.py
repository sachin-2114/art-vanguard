import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

class ChatClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.sock.connect((host, port))
        except Exception as e:
            print(f"Server से कनेक्ट नहीं हो पाया: {e}")
            return

        msg = tkinter.Tk()
        msg.withdraw()

        # यूजर से उसका नाम पूछना
        self.nickname = simpledialog.askstring("Nickname", "अपना नाम चुनें:", parent=msg)
        if not self.nickname:
            self.nickname = "Anonymous"

        self.gui_done = False
        self.running = True

        # GUI और नेटवर्क सुनने के लिए अलग-अलग थ्रेड्स
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title(f"Vanguard Chat - {self.nickname}") 
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        # यहाँ UTF-8 का इस्तेमाल किया गया है
        raw_message = self.input_area.get('1.0', 'end').strip()
        if raw_message:
            message = f"{self.nickname}: {raw_message}\n"
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                # UTF-8 में डिकोड करना
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(f"Error: {e}")
                self.sock.close()
                break

# यहाँ अपना लैपटॉप का सही IP Address डालें
client = ChatClient('192.168.1.9', 55555)