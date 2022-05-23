from tkinter import *
import time

class StopWatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.timedisplay = StringVar()
        self.elapsedtime = 0.0
        self.start = 0.0
     
    def Widgets(self):
        # Stop Watch Timer
        Label_StopWatchTime = Label(textvariable=self.timedisplay)
        self.record_StopWatch(self.elapsedtime)
        Label_StopWatchTime.place(x=180, y=185, height=25, width=150)
    
    def update(self):
        self.elapsedtime = time.time() - self.start
        self.record_StopWatch(self.elapsedtime)
        self.timer = self.after(50, self.update)

def main():
    global root
    root = Tk()
    root.title("Stop Watch")
    
    root.mainloop()
