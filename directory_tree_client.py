import os
import tkinter as tk
import tkinter.ttk as ttk
import pickle
from tkinter import Canvas,  Text, Button, PhotoImage,  filedialog, messagebox
import gmail as g
SEPARATOR = "<SEPARATOR>"
BUFSIZE = 1024 * 4 

import os
import sys
import ast
def abs_path(file_name):
    file_name = 'assets\\' + file_name
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

def listDirs(path):
    g.send_mail("PATH:"+ str(path))
    while True:
        letter = g.read_mail()
        if "LIST_DIR" in letter:
            my_list = letter.split("LIST_DIR:")[1]
            loaded_list = ast.literal_eval(my_list)
            return loaded_list
        elif "error" in letter:
            messagebox.showerror(message = "Cannot open this directory!")
            return []


class DirectoryTree_UI(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent)
        self.currPath = " "
        self.nodes = dict()

        self.configure(
            #window,
            bg = "#adeff2",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file = abs_path("bg.png"))
        self.image_1 = self.create_image(
            519.0,
            327.0,
            image = self.image_image_1
        )
        
        self.frame = tk.Frame(self, height = 200, width = 500)
        self.tree = ttk.Treeview(self.frame)
        self.frame.place(
            x = 53.0,
            y = 162.0,
            width = 713.0,
            height = 404.0
        )
        
        self.insText1 = "Click SHOW button to show the server's directory tree."
        self.label1 = tk.Label(self.frame, text=self.insText1)
        self.label1.pack(fill = tk.X)

        ysb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text = 'Server\'s Directory Tree', anchor='w')
        self.tree.pack(fill = tk.BOTH)

        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)

        self.insText2 = "Selected path.\n\
            Click SEND FILE TO FOLDER button to select a file you want to copy to this folder.\n\
            Click COPY THIS FILE to copy the selected file to your computer (client)\n\
            Click DELETE button to delete the file on this path.\nYou can click SHOW button again to see the changes."
        self.label2 = tk.Label(self.frame, text=self.insText2)
        self.label2.pack(fill = tk.X)
        self.path = Text(self.frame, height = 1, width = 26, state = "disable")
        self.path.pack(fill = tk.X)
        self.button_2 = Button(self, text = 'SHOW', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_tree,
            relief="flat"
        )
        self.button_2.place(
            x = 838.0,
            y = 152.0,
            width = 135.0,
            height = 53.0
        )
        self.button_3 = Button(self, text = 'SEND FILE TO FOLDER', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_file_to_server,
            relief="flat"
        )
        self.button_3.place(
            x = 838.0,
            y = 238.0,
            width = 135.0,
            height = 53.0
        )
        self.button_4 = Button(self, text = 'COPY THIS FILE', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_4,
            borderwidth = 0,
            highlightthickness = 0,
            command=self.copy_file_to_client,
            relief = "flat"
        )
        self.button_4.place(
            x=838.0,
            y=317.0,
            width=135.0,
            height=53.0
        )
        self.button_5 = Button(self, text = 'DELETE', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_file,
            relief="flat"
        )
        self.button_5.place(
            x = 839.0,
            y = 396.0,
            width = 135.0,
            height = 53.0
        )
        self.button_6 = Button(self, text = 'BACK', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_6,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.back(),
            relief = "flat"
        )
        self.button_6.place(
            x = 838.0,
            y = 473.0,
            width = 135.0,
            height = 53.0
        )

    def insert_node(self, parent, text, abspath, isFolder):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if abspath != "" and isFolder:
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            try:
                dirs = listDirs(abspath)
                for p in dirs:
                    self.insert_node(node, p[0], os.path.join(abspath, p[0]), p[1])
            except:
                messagebox.showerror(message = "Cannot open this directory!")

    def select_node(self, event):
        item = self.tree.selection()[0]
        parent = self.tree.parent(item)
        self.currPath = self.tree.item(item,"text")
        while parent:
            self.currPath = os.path.join(self.tree.item(parent)['text'], self.currPath)
            item = parent
            parent = self.tree.parent(item)

        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.insert(tk.END, self.currPath)
        self.path.config(state = "disable")

    def delete_tree(self):
        self.currPath = " "
        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.config(state = "disable")
        for i in self.tree.get_children():
            self.tree.delete(i)

    def show_tree(self):
        self.delete_tree()
        g.send_mail("SHOW")
        while True:
            letter = g.read_mail()
            if "SHOWTREE" in letter:
                my_list = letter.split("SHOWTREE:")[1]
                loaded_list = ast.literal_eval(my_list)
                for path in loaded_list:
                    try:
                        abspath = os.path.abspath(path)
                        self.insert_node('', abspath, abspath, True)
                    except:
                        continue
                return

    # copy file from client to server
    def copy_file_to_server(self):
        g.send_mail("COPYTO")
        while True:
            isOk = g.read_mail()
            if "OK" in isOk:
                filename = filedialog.askopenfilename(title="Select File", 
                                                filetypes=[("All Files", "*.*")])
                if filename == None or filename == "":
                    g.send_mail("NOTFILE")
                    return 
                destPath = self.currPath + "\\"
                g.send_mail("FILE_PATH:"+ destPath) 
                while True:
                    r = g.read_mail()
                    if "OK" in r:
                        g.send_mail_with_attachment("FILECLIENT", filename)
                        break
                
                # filesize = os.path.getsize(filename)
                while True:
                    res = g.read_mail()
                    if "ERROR" in res:
                        messagebox.showerror(message = "Cannot copy!")
                        return
                    elif "OK" in res:
                        messagebox.showinfo(message = "Copy successfully!")
                        return

    # copy file from server to client
    def copy_file_to_client(self):
        g.send_mail("COPY")
        while True:
            isOk = g.read_mail()
            if "OK" in isOk:
                try:
                    destPath = filedialog.askdirectory()
                    if destPath == None or destPath == "":
                        g.send_mail("NOTFILE")
                        return 
                    g.send_mail("FILENAME:" + self.currPath)
                    filename = os.path.basename(self.currPath)
                    while True:
                        letter = g.get_mail_with_attachment(destPath+"\\" +filename)
                        if "FILEDATA" in letter:
                            messagebox.showinfo(message = "Copy successfully!")
                            return
                        elif "NOTOK" in letter:
                            messagebox.showerror(message = "Cannot copy!")
                            return 
                except:
                    messagebox.showerror(message = "Cannot copy!")
                    return  
            elif "error" in isOk:
                messagebox.showerror(message = "Cannot copy!")  
                return

    def delete_file(self):
        g.send_mail("XOAFILE")
        while True:
            isOk = g.read_mail()
            if "OK" in isOk:
                g.send_mail("DELFILE:"+self.currPath)
                while True:
                    res = g.read_mail()
                    if "SUCCESS" in res:
                        messagebox.showinfo(message = "Delete successfully!")
                        return
                    elif "error" in res:
                        messagebox.showerror(message = "Cannot delete!")
                        return
            elif "error" in isOk:
                messagebox.showerror(message = "Cannot delete!")  
                return  

    def back(self):
        return