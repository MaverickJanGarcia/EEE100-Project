from tkinter import *
import time

class StopWatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.elapsedtime = 0.0
        self.start = 0.0
        self.running = 0
        self.lapmod2 = 0
        self.timedisplay = StringVar()
        self.laps = []
        self.Widgets()
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
     
    def Widgets(self):
        # Stop Watch Timer
        Label_StopWatchTime = Label(textvariable=self.timedisplay)
        self.record_StopWatch(self.elapsedtime)
        Label_StopWatchTime.place(x=180, y=185, height=25, width=150)
        
        # File Creator
        Label_FileName = Label(text="File Name")
        Label_FileName.place(x=100,y=70, width=300, height=40)
        self.entry = Entry(self)
        self.entry.place(x=100, y=100, height=30, width=300)        
        
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
        SWminute = int(SWelapsedtime/60 - SWhour*60.0)
        SWsecond = int(SWelapsedtime - SWhour*3600.0 - SWminute*60.0)
        SWmillisecond = int((SWelapsedtime - SWhour*3600.0 - SWminute*60.0 - SWsecond)*100)
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
        global PopUp_Reset
        self.start = time.time()         
        self.record_StopWatch(self.elapsedtime)
        self.after_cancel(self.timer)            
        self.elapsedtime = time.time() - self.start    
        self.record_StopWatch(self.elapsedtime)
        self.running = 0
        self.lapmod1.delete(0, 'end')
        self.lapmod2 = 0
        PopUp_Reset.destroy()
       
    def command_Lap(self):
        
        tempo = self.elapsedtime - self.lapmod2
        if self.running:
            self.laps.append(self.record_Lap(tempo))
            self.lapmod1.insert(END, self.laps[-1])
            self.lapmod1.yview_moveto(1)
            self.lapmod2 = self.elapsedtime

    def command_Save(self):
        global root
        archive = str(self.entry.get()) + ' - '
        if archive == ' - ':
            PopUp_InvalidSave = Toplevel(root)
            PopUp_InvalidSave.title("")
            PopUp_InvalidSave.geometry("310x50+95+200")
            PopUp_InvalidSave.resizable(False, False)
            Label_InvalidSave = Label(PopUp_InvalidSave, text="Please Input a File Name!", font=("Arial", 13))
            Label_InvalidSave.place(x=60,y=15)
        else:
            with open(archive + self.today + '.txt', 'wb') as lapfile:
            
                for lap in self.laps:
                    lapfile.write((bytes(str(lap) + '\n', 'utf-8')))
            
            self.entry.delete(0, 'end')
            self.start = time.time()         
            self.record_StopWatch(self.elapsedtime)
            self.after_cancel(self.timer)            
            self.elapsedtime = time.time() - self.start    
            self.record_StopWatch(self.elapsedtime)
            self.running = 0
            self.lapmod1.delete(0, 'end')
            self.lapmod2 = 0
            
            PopUp_Save = Toplevel(root)
            PopUp_Save.title("")
            PopUp_Save.geometry("200x50+130+200")
            PopUp_Save.resizable(False, False)
            Label_Save = Label(PopUp_Save, text="File Saved!", font=("Arial", 13))
            Label_Save.place(x=60,y=15)
                
def main():
    global root
    root = Tk()
    root.title("Stop Watch")
    
    # Clock and Date
    def clock():
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        meridiem = time.strftime("%p")

        Label_Clock.config(text=hour + ":" + minute + ":" + second + " " + meridiem)
        Label_Clock.after(1000, clock)

    def date():
        month = time.strftime("%B")
        day = time.strftime("%d")
        year = time.strftime("%Y")

        Label_Date.config(text=month + " / " + day + " / " + year)
        Label_Date.after(1000, clock)

    # Pop Up Windows
    def ResetWindow():
        global PopUp_Reset
        PopUp_Reset = Toplevel(root)
        PopUp_Reset.title("")
        PopUp_Reset.geometry("200x100+130+200")
        PopUp_Reset.resizable(False, False)
        Label_AskReset = Label(PopUp_Reset, text="Are you sure you want \nto Reset?")
        Label_AskReset.place(x=15,y=10)

        Button_Yes = Button(PopUp_Reset, text="Yes", command=sw.command_Reset)
        Button_Yes.place(x=35,y=70, height=20, width=50)
        Button_No = Button(PopUp_Reset, text="No", command=PopUp_Reset.destroy)
        Button_No.place(x=115,y=70, height=20, width=50)
     
    def QuitWindow():
        PopUp_Quit = Toplevel(root)
        PopUp_Quit.title("")
        PopUp_Quit.geometry("200x100+130+200")
        PopUp_Quit.resizable(False, False)
        Label_AskQuit = Label(PopUp_Quit, text="Are you sure you want \nto Quit?", font=("Arial", 13))
        Label_AskQuit.place(x=15,y=10)

        Button_Yes = Button(PopUp_Quit, text="Yes", command=root.quit, font=("Arial", 10))
        Button_Yes.place(x=35,y=70, height=20, width=50)
        Button_No = Button(PopUp_Quit, text="No", command=PopUp_Quit.destroy, font=("Arial", 10))
        Button_No.place(x=115,y=70, height=20, width=50)
    
    # Main Widget Frame
    Positions = Frame(root)

    # Lapbox Position
    sw = StopWatch(Positions)
    sw.grid(row=0, column=0)
    
    # Buttons Functions
    Button_Start = Button(text="Start", command=sw.command_Start)
    Button_Stop = Button(text="Stop", command=sw.command_Stop))
    Button_Reset = Button(text="Reset", command=ResetWindow)
    Button_Lap = Button(text="Lap", command=sw.command_Lap)
    Button_Save = Button(text="Save", command=sw.command_Save)
    Button_Quit = Button(text='Quit', bg="black",fg="white",command=QuitWindow, font=("Arial", 13, "bold italic"))
    
    # Call Clock and Date Function
    clock()
    date()
    
    # Buttons Positions
    Button_Start.place(x=12,y=250, width=100, height=50)
    Button_Stop.place(x=12,y= 310, width=100, height=50)
    Button_Reset.place(x=390, y=250, width=100, height=50)
    Button_Split.place(x=12,y=370, width=100, height=50)
    Button_Save.place(x=390,y=310, width=100, height=50)
    Button_Quit.place(x=390,y=370, width=100, height=50)
    
    root.mainloop()
