from tkinter import *
import time

class StopWatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.timedisplay = StringVar()
        self.elapsedtime = 0.0
        self.start = 0.0
        self.lapmod1 = 0
        self.lapmod2 = 0
        self.laps = []
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
     
    def Widgets(self):
        # Stop Watch Timer
        Label_StopWatchTime = Label(textvariable=self.timedisplay)
        self.record_StopWatch(self.elapsedtime)
        Label_StopWatchTime.place(x=180, y=185, height=25, width=150)
        
        # Laps
        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lapmod1 = Listbox(self, selectmode=EXTENDED, height = 8),
                         yscrollcommand=scrollbar.set)
        self.lapmod1.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.lapmod1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def update(self):
        self.elapsedtime = time.time() - self.start
        self.record_StopWatch(self.elapsedtime)
        self.timer = self.after(50, self.update)
        
    def record_StopWatch(self, SWelapsedtime):
        SWhour = int(SWelapsedtime/3600) 
        SWminute = int(SWelapsedtime/60 - SWhour*60.0)
        SWsecond = int(SWelapsedtime - SWhour*3600.0 - SWminute*60.0)
        SWmillisecond = int((SWelapsedtime - SWhour*3600.0 - SWminute*60.0 - SWsecond)*100)
        self.timedisplay.set('%02d:%02d:%02d.%02d' % (SWhour, SWminute, SWsecond, SWmillisecond))
        
    def record_Lap(self, SWelapsedtime):
        SWhour = int(SWelapsedtime/3600) 
        SWminute = int(SWelapsedtime/60)
        SWsecond = int(SWelapsedtime - SWminute*60.0)
        SWmillisecond = int((SWelapsedtime - SWminute*60.0 - SWsecond)*100)
        return '%02d:%02d:%02d.%02d' % (SWhour, SWminute, SWsecond, SWmillisecond)
    
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
            
    def command_Reset(self):
        self.start = time.time()
        self.elapsedtime = 0.0
        self.record_StopWatch(self.elapsedtime)
       
    def command_Lap(self):
        tempo = self.elapsedtime - self.lapmod2
        if self.running:
            self.laps.append(self.record_Lap(tempo))
            self.lapmod1.insert(END, self.laps[-1])
            self.lapmod1.yview_moveto(1)
            self.lapmod2 = self.elapsedtime

    def command_Save(self):
        archive = str(self.entry.get()) + ' - '
        with open(archive + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))
                
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
    Button_Reset = Button(text="Reset", command=sw.command_Reset)
    Button_Lap = Button(text="Lap", command=sw.command_Lap)
    Button_Save = Button(text="Save", command=sw.command_Save)
    
    # Buttons Positions
    Button_Start.place(x=12,y=250, width=100, height=50)
    Button_Stop.place(x=12,y= 310, width=100, height=50)
    Button_Reset.place(x=390, y=250, width=100, height=50)
    Button_Split.place(x=12,y=370, width=100, height=50)
    Button_Save.place(x=390,y=310, width=100, height=50)
    
    root.mainloop()
