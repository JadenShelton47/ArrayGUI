
from pylogix import PLC
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *
from pandastable import Table
import pandas as pd
with PLC() as plc:
    trimmer='10.87.28.2'
    plc.IPAddress = trimmer
tableSize = 25
a='backLog_baseArray[{},{}]'
b='evenEnding_baseArray[{},{}]'
x='backLog_frontFill'
y='backLog_rearFill'




def update(x,y):
        rearFill = plc.Read(x)
        frontFill = plc.Read(y)
        text1= frontFill.Value
        text2= rearFill.Value
        Text1.config(text= text1)
        Text2.config(text= text2)

def callback():#update which array to load and write to
    selection= tkVarOM.get()
    print(selection)
    return selection
        

def readBacklog(selection):#Read 1 value at a time in two loops
        print("trying read....")
        selection= tkVarOM.get()
        try:
            for X_axis in range(0,tableSize):
                for Y_axis in range(0,tableSize):
                    ret = plc.Read(selection.format(X_axis, Y_axis))
                    print(Y_axis)
                    dataTable[X_axis, Y_axis] = ret.Value 
                plc.Read(selection.format(X_axis, Y_axis))
            print("Read Done")
            print(dataTable)
            pt.update()
            pt.redraw()
            print(selection)
        except:
            print("unable to complete read")

def writeBacklog():# write one at a time with two for loops
        selection= tkVarOM.get()
        print("trying...")
        print(df)
        dt = df.to_numpy()
        try:
            print("entering Loop")
            print(dt)
            for X_axis in range(0, tableSize):
                for Y_axis in range(0,tableSize):
                    plc.Write(selection.format(X_axis, Y_axis), dt[X_axis, Y_axis])
                    print(Y_axis)
                plc.Write(selection.format(X_axis, Y_axis), dt[X_axis, Y_axis])
                print(X_axis)
            print("Write Done")
            pt.redraw()
            
        except:
            print("Opppppps")

def write100():# write one at a time with two for loops
        print("trying...")
        print(df)
        dt = df.to_numpy()
        try:
            print("entering Loop")
            print(dt)
            for X_axis in range(0, tableSize):
                for Y_axis in range(0,tableSize):
                    plc.Write('backLog_baseArray[{},{}]'.format(X_axis, Y_axis), 100)
                    print(Y_axis)
                plc.Write('backLog_baseArray[{},{}]'.format(X_axis, Y_axis), 100)
                print(X_axis)
            print("Write Done")
            pt.redraw()
            
        except:
            print("Opppppps")

window = Tk()
window.title("User Input")
window.configure(background="white")
window.resizable(True, True)

window_width = window.winfo_screenwidth()
window_height = window.winfo_screenheight()
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
centerx = int(screenwidth / 2 - window_width / 2)
centery = int(screenheight / 2 - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{centerx}+{centery}')


dataTable = np.zeros([tableSize, tableSize], dtype=np.int16)
button1 = ttk.Button(window, text= "Read",command=lambda: readBacklog(a))
button1.pack( padx = (25,0), side=tk.LEFT, expand=False)
button2 = ttk.Button(window, text= "Write",command=lambda: writeBacklog())
button2.pack( side=tk.LEFT, expand=False)
#button3 = ttk.Button(window, text= "submit", command=lambda: callback())
#button3.pack( side=tk.LEFT, expand=False)

Text1 = ttk.Button(window, text= "text1",command=lambda: write100())
Text1.pack( side=tk.LEFT, expand=False)
Text2 = ttk.Button(window, text= "text2",command=lambda: write100())
Text2.pack( side=tk.LEFT, expand=False)

#selects between arrays "a" and "b"
OPTIONS= [a, b]
tkVarOM = StringVar(window)
tkVarOM.set(OPTIONS[0])
om = OptionMenu(window,tkVarOM, *OPTIONS)
om.pack(side=tk.LEFT, expand=False)

frame = tk.Frame(window)
frame.pack(fill='both', expand=True)

frame1 = tk.Frame(window, padx=10, width= 200)
frame1.pack(fill='y', expand=False)

#data frame
df = pd.DataFrame(data= dataTable)
pt = Table(frame, dataframe= df)


while True:# loop used to keep the tk mainloop from blocking all of the other functions from updating
    
    frame.update()
    frame.update_idletasks()
    pt.show()
    pt.redraw()
    #callback()
    update(x,y)
    time.sleep(.1)
    


