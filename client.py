import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

class GUI:

    def __init__(self):
        self.Window=Tk()
        self.Window.withdraw()

        self.login_window=Toplevel()
        self.login_window.title("Login ")
        self.login_window.resizable(width=False,height=False)
        self.login_window.configure(width=400,height=400,bg='black')

        self.nickname_req=Label(self.login_window,text="Enter nickname please: ",justify=CENTER,font='Helvetica 15 bold')
        self.nickname_req.place(relheight=0.1,relx=0.2,rely=0.05)

        self.nickname_label=Label(self.login_window,text="Name",font='Calibri 12')
        self.nickname_label.place(relheight=0.1,relx=0.1,rely=0.2)

        self.nickname_input=Entry(self.login_window,font='Calibri 12',fg="white")  
        self.nickname_input.place(relwidth=0.4,relheight=0.1,relx=0.4,rely=0.2)
        self.nickname_input.focus()

        self.enter_button=Button(self.login_window,text="Login", command=lambda:self.login(self.nickname_input.get()),font="Calibri 18",fg="red",borderwidth=2,bg="red")
        self.enter_button.place(relx=0.4,rely=0.5)

        self.Window.mainloop()
    
    def login(self,nickname):
        self.login_window.destroy()

        self.chat_layout(nickname)

        rcv=Thread(target=self.receive)
        rcv.start()
    
    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_msg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def chat_layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("Quiz Room")
        self.Window.configure(width=400, height=500,bg='black')
        self.Window.resizable(width=False,height=False)

        self.name_label=Label(self.Window,bg = "#17202A",fg = "#EAECEE",text = self.name ,font = "Helvetica 13 bold",pady = 5)
        self.name_label.place(relheight=0.1,relwidth=1)

        self.line_label=Label(self.Window,width=400,bg='cyan')
        self.line_label.place(relwidth=1,relheight=0.05,rely=0.05)

        self.text_area=Text(self.Window,width=20,height=2,fg='white',font=("Calibri 12"),padx=5,pady=5)
        self.text_area.place(relheight=0.75,relwidth=1,rely=0.07)

        self.text_input_label=Label(self.Window,bg='black',height=50)
        self.text_input_label.place(relwidth=1,rely=0.8)

        self.text_input=Entry(self.text_input_label,bg='white',fg='red',font=("Calibri 12"))
        self.text_input.place(rely=0.01,relheight=0.8,relwidth=0.7,relx=0.01)
        self.text_input.pack()
        self.text_input.focus()

        self.send_button=Button(self.text_input_label,bg='black',fg='red',text="Send",font=("Calibri 12"),width=10,command=lambda:self.send_msg(self.text_input.get()))
        self.send_button.place(rely=0.01,relheight=0.8,relwidth=0.3,relx=0.71)
        self.text_area.config(cursor='arrow')

        scrollbar=Scrollbar(self.text_area)
        scrollbar.place(relheight=1,relx=0.95)
        scrollbar.config(command=self.text_area.yview)


    def send_msg(self,msg):
        self.text_area.config(state=DISABLED)
        self.msg=msg
        self.text_input.delete(0,END)

        send_msg=Thread(target=self.write)
        send_msg.start()

    def write(self):
        self.text_area.config(state=DISABLED)
        
        while True:
            # message = '{}: {}'.format(self.name, input(''))
            message=(f"{self.name} :   {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_msg(message)
            break

    def show_msg(self,msg):
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END,msg+'\n\n')
        self.text_area.config(state=DISABLED)
        self.text_area.see(END)




print("Connected with the server...")
g=GUI()
