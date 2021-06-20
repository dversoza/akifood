from tkinter import *

from ui import AkiFoodUI

# Base dishes to start application
dishes_db = [
    {'_name': 'Bolo de chocolate', 'massa': False},
    {'_name': 'Lasanha', 'massa': True}
]

if __name__ == '__main__':
    """Program entry point"""
    ui_root = Tk()
    AkiFoodUI(ui_root, db=dishes_db)
    ui_root.mainloop()
