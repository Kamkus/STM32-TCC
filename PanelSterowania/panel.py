from turtle import Screen, title
from tkinter import *
from serialport import SerialPort
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
VALUES = {
    'yREF': '0'
}
COMMANDS={
    'SET_TEMPERATURE' : lambda panel, message : panel.sendTempSetting(),
    'SHOW_PLOT' : lambda panel, message : panel.showPlot(message),
    'CLEAR_DATA': lambda panel,message : panel.clearData()
}

class Panel:
    def __init__(self, width, height, port):
        self.screen = Screen()
        self.screen.setup(width=width, height=height)
        title("Panel sterowania")
        self.serialPort = SerialPort(port, 9600, 1)
        self.yRef = StringVar(value = "0")
        self.uS = StringVar(value="0")
        self.e = StringVar(value="10")
        self.plot = False
        self.data = {
            'PWM': [],
            'UCHYB' : [],
            'TEMP' : [],
            'TIME' : [],
        }
    def createButton(self,text, command, commandValue, posX, posY):
        button = Button(self.screen.getcanvas().master, text=text, command=lambda : COMMANDS[command](self, commandValue))
        button.pack()
        button.place(x=posX, y=posY)
    def createInputBox(self, label, value, posX, posY, inputState):
        label = Label(self.screen.getcanvas().master, text=label, width=10)
        label.pack()
        label.place(x=posX, y=posY)
        # print(self[value])
        entry = Entry(self.screen.getcanvas().master, textvariable=value, state=inputState)
        entry.pack()
        entry.place(x=posX+70, y=posY)
    def readLine(self):
        values = self.serialPort.readMessage()
        us = int(values[1])/10
        e = abs((int(values[2]))/(25*10))
        temp = int(values[0])/1000
        self.data['PWM'].append(us)
        self.data['UCHYB'].append(e)
        self.data['TEMP'].append(temp)
        if len(self.data['TIME']) > 0:
            self.data['TIME'].append(self.data['TIME'][len(self.data['TIME']) -1] + 0.3)
        else:
            self.data['TIME'].append(0.3)
        self.uS.set(str(us))
        self.e.set(str(e))
    def showPlot(self, Data):
        newfigure = Figure()
        plt.plot(self.data['TIME'], self.data[Data])
        plt.show()
    def clearData(self):
        self.data = {
            'PWM': [],
            'UCHYB' : [],
            'TEMP' : [],
            'TIME' : [],
        }
    def sendTempSetting(self):
        valueToSend = float(self.yRef.get())
        if valueToSend > 45.0:
            self.yRef.set('45.0')
        elif valueToSend < 25.0:
            self.yRef.set('25.0')
        self.serialPort.sendMessage(str(self.yRef.get()))