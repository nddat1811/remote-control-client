import tkinter as tk
import gmail as g

def close_event(main):
    g.send_mail("QUIT")
    main.destroy()
    return

def shutdown():
    g.send_mail("SHUTDOWN")
def logout():
    g.send_mail("LOGOUT")

def shutdown_logout(root):
    window = tk.Toplevel(root)
    window.geometry("190x160")
    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", lambda: close_event(window))
    shutdown_btn = tk.Button(window, text = 'SHUTDOWN', width = 20, height = 2, fg = 'white', bg = 'IndianRed3', command = lambda: shutdown(), padx = 20, pady = 20)
    shutdown_btn.grid(row = 0, column = 0)
    logout_btn = tk.Button(window, text = 'LOGOUT', width = 20, height = 2, fg = 'white', bg = 'royalblue4', command = lambda: logout(), padx = 20, pady = 20)
    logout_btn.grid(row = 1, column = 0)
    window.mainloop()
