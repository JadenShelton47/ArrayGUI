
from turtle import update
from pylogix import PLC
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *
from pandastable import Table
import pandas as pd
import asyncio
import threading
import queue


value = 1111
tableSize = 15
dataTable = np.zeros([tableSize, tableSize], dtype=np.int16)
dt = np.zeros([tableSize, tableSize], dtype=np.int16)
with PLC() as plc:
    plc.IPAddress = '10.80.3.240'
class theWindow:
    def __init__(self):
        window = Tk()
        window.title ("User Input")
        window.configure(background="white")
        window_width = window.winfo_screenwidth()
        window_height = window.winfo_screenheight()
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        window.resizable(False, False)

        centerx = int(screenwidth / 2 - window_width / 2)
        centery = int(screenheight / 2 - window_height / 2)
        window.geometry(f'{window_width}x{window_height}+{centerx}+{centery}')
        button1 = ttk.Button(window,text= "Read",command=lambda: readNumpy())
        button1.pack( padx = (100,0) , side=tk.LEFT, expand=False)


        button2 = ttk.Button(window,text= "Write",command=lambda: write())
        button2.pack( side=tk.LEFT, expand=False)

        frame = tk.Frame(window)
        frame.pack(fill='both', expand=True)

        df = pd.DataFrame(data= dataTable)

        pt = Table(frame, dataframe= df)
        pt.show()
        time.sleep(1)
        print("ready")
        pt.update()
        window.after(1000, update)
        window.mainloop()
      
       

def readNumpy():#Read 1 value at a time in two loops
        print("trying read....")
        try:
                for X_axis in range(0,tableSize):
                    for Y_axis in range(0,tableSize):
                        ret = plc.Read('multiArray[{},{}]'.format(X_axis, Y_axis))
                        print(Y_axis)
                        dataTable[X_axis, Y_axis] = ret.Value
                    plc.Read('multiArray[{},{}]'.format(X_axis, Y_axis))
                print("Read Done")
                print(dataTable)       
        except:
            print("unable to complete read")

def write():# write one at a time with two for loops
    print("trying...")
    try:
        for X_axis in range(0, tableSize):
            for Y_axis in range(0,tableSize):
                plc.Write('multiArray[{},{}]'.format(X_axis, Y_axis), value)
                print(Y_axis)
            plc.Write('multiArray[{},{}]'.format(X_axis, Y_axis), value)
            print(X_axis)
        print("Write Done")
        plc.Write('WriteTags', False)
        
    except:
        print("Opppppps")

if __name__ == '__main__':
    window = theWindow()
    window.__init__()

        




