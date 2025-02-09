import threading 
import socket
import customtkinter as tk

class connection:
    global conn,addr
    connectUsr=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    message=str()
    
    mode=str()
    def __init__(self,port,ipaddr):
        mode=input("Enter the mode: ")
        if(mode.lower()=="server"):
            self.connectUsr.bind((str(ipaddr),int(port)))
            self.connectUsr.listen()
            self.conn,self.addr=self.connectUsr.accept()
            self.mode="server"
        elif(mode.lower()=="client"):
            self.connectUsr.connect((ipaddr,port))
            self.mode="client"
            

    def replyHandler(self):
        while True:
            if(self.mode=="server"):
                self.message=str(self.conn.recv(1024).decode())
            else:
                self.message=str(self.connectUsr.recv(1024).decode())
            if(len(self.message)>0):
                tk.CTkLabel(application.messagesFrame,text=f"Them: {self.message}").pack(side="top")
    
    def messageSender(self,message):
        if(self.mode=="server"):
            self.conn.sendall(message.encode())
        else:
            self.connectUsr.sendall(message.encode())

class page:
    def __init__(self):
        tk.set_appearance_mode("system")
        tk.set_window_scaling(1.0)
        self.app = tk.CTk()
        self.app.geometry("600x600")
        self.MainFrame = tk.CTkFrame(self.app, border_width=0)
        self.MainFrame.pack(fill="y")
        self.LbMain = tk.CTkLabel(self.MainFrame, text="Chat App")
        self.LbMain.pack(side="top")
        self.messagesFrame=tk.CTkScrollableFrame(self.MainFrame, border_width=0,height=400)
        self.messagesFrame.pack(fill="x", side="top")
        self.textbox=tk.CTkTextbox(self.MainFrame,corner_radius=10, bg_color="#293840", height=30, width=700)
        self.textbox.pack(side="top", anchor="w", fill="x")
        self.sendButton=tk.CTkButton(self.MainFrame,text="Send",fg_color="#2b405f",corner_radius=18,border_width=0,command=self.messageSender)
        self.sendButton.pack(side="right",padx=5, pady=10)

    def messageSender(self):
        temp=self.textbox.get("1.0", "end-1c")
        self.textbox.delete("1.0", "end-1c")
        tk.CTkLabel(self.messagesFrame,text=f"You: {temp}").pack(side="top")
        con.messageSender(temp)
        


global application,con

application=page()
con=connection(int(input("Enter the port: ")),str(input("Enter the IP address: ")))
thread1=threading.Thread(target=con.replyHandler,name="Reply Handler")
thread1.start()
application.app.mainloop()