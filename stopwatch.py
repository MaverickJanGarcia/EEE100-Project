from tkinter import *
import time

class StopWatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)

def main():
    global root
    root = Tk()
    root.title("Stop Watch")
    
    root.mainloop()
