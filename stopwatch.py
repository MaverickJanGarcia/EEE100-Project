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
        
    def record_StopWatch(self, SWelapsedtime):
        SWhour = int(SWelapsedtime/3600) 
        SWminute = int(SWelapsedtime/60)
        SWsecond = int(SWelapsedtime - SWminute*60.0)
        SWmillisecond = int((SWelapsedtime - SWminute*60.0 - SWsecond)*100)
        self.timedisplay.set('%02d:%02d:%02d.%02d' % (SWhour, SWminute, SWsecond, SWmillisecond))
        
    def command_Start(self):
        if not self.running:            
            self.start = time.time() - self.elapsedtime
            self.update()
            self.running = 1

    def command_Stop(self):                                    
        if self.running:
            self.after_cancel(self.timer)            
            self.elapsedtime = time.time() - self.start    
            self.record_StopWatch(self.elapsedtime)
            self.running = 0


def main():
    global root
    root = Tk()
    root.title("Stop Watch")
    
    # Main Widget Frame
    Positions = Frame(root)

    # Lapbox Position
    sw = StopWatch(Positions)
    sw.grid(row=0, column=0)
    
    # Buttons Functions
    Button_Start = Button(text="Start", command=sw.command_Start)
    Button_Stop = Button(text="Stop", command=sw.command_Stop))
    
    # Buttons Positions
    Button_Start.place(x=12,y=250, width=100, height=50)
    Button_Stop.place(x=12,y= 310, width=100, height=50)
    
    root.mainloop()
