import socket
import tkinter as tk
import tkinter.messagebox
import entrance_ui as ui1
import main_ui as ui2
import mac_address_client as mac
import shutdown_logout_client as sl
import directory_tree_client as dt
import live_screen_client as lsc
import app_process_client as ap
import registry_client as rc
import keylogger_client as klc
import gmail as g

#global variables
BUFSIZE = 1024 * 4
root = tk.Tk()
root.geometry("1000x600") #1000 la nguyen ban
root.configure(bg = "#FFFFFF")
root.title('Client')
root.resizable(False, False)

f1 = ui1.Entrance_UI(root)

def back(ui):
    ui.place_forget()
    f2.place(x = 0, y = 0)
    g.send_mail("QUIT")

def disconnect():
    f2.place_forget()
    f1.place(x = 0, y = 0)
    return
# 1 Xem địa chỉ MAC (MAC Address)
def mac_address():
    g.clear_all_msg()
    g.send_mail("MAC")
    mac.mac_address()
    return
# 2 Lắng nghe phím (Keylogger)
def keylogger():
    g.clear_all_msg()
    g.send_mail("KEYLOG")
    tmp = klc.Keylogger_UI(root)
    tmp.button_6.configure(command = lambda: back(tmp))
    return
# 3 Xem cây thư mục (Directory Tree)
def back_directory_tree(ui):
    ui.place_forget()
    ui.tree.pack_forget()
    f2.place(x = 0, y = 0)
    g.send_mail("QUIT")

def directory_tree():
    g.clear_all_msg()
    g.send_mail("DIRECTORY")
    tmp = dt.DirectoryTree_UI(root)
    tmp.button_6.configure(command = lambda: back_directory_tree(tmp))
    return
# 4 Xem màn hình trực tiếp (Live Screen)
def live_screen():
    g.clear_all_msg()
    g.send_mail("LIVESCREEN")
    tmp = lsc.Desktop_UI(root)
    if tmp.status == False:
        back(tmp)
    return
# 5	Xem ứng dụng hoặc tiến trình (Application/Process)
def app_process():
    g.clear_all_msg()
    g.send_mail("APP_PRO")
    tmp = ap.App_Process_UI(root)
    tmp.button_6.configure(command = lambda: back(tmp))
    return
# 6 Xem Registry (Registry)
def back_reg(ui):
    ui.place_forget()
    f2.place(x = 0, y = 0)

def registry():
    g.clear_all_msg()
    g.send_mail("REGISTRY")
    tmp = rc.Registry_UI(root)
    tmp.btn_back.configure(command=lambda: back_reg(tmp))
    return
# # 7 Tắt máy hoặc thoát khỏi màn hình desktop (Shutdown/Logout)
def shutdown_logout():
    g.clear_all_msg()
    g.send_mail("SD_LO")
    sl.shutdown_logout(root)
    return

def disconnect():
    f2.place_forget()
    f1.place(x = 0, y = 0)
    g.send_mail("QUIT")
    return
def show_main_ui():
    f1.place_forget()
    global f2
    f2 = ui2.Main_UI(root)
    f2.button_mac_addr.configure(command = mac_address)
    f2.button_keylogger.configure(command = keylogger)
    f2.button_directory_tree.configure(command = directory_tree)
    f2.button_livescreen.configure(command = live_screen)
    f2.button_app_process.configure(command = app_process)    
    f2.button_registry.configure(command = registry)    
    f2.button_shudown_logout.configure(command = shutdown_logout)
    f2.button_disconnect.configure(command = disconnect)
    return


def connect():
    g.authorization()
    show_main_ui()   
    return
f1.button_connect.configure(command = connect)
root.mainloop()