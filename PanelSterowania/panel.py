from turtle import Screen, title
from tkinter import *
from serialport import SerialPort
from matplotlib.figure import Figure
import csv
import matplotlib.pyplot as plt
import re
VALUES = {
    'yREF': '0'
}
COMMANDS={
    'SET_TEMPERATURE' : lambda panel, message : panel.sendTempSetting(),
    'SHOW_PLOT' : lambda panel, message : panel.showPlot(message),
    'CLEAR_DATA': lambda panel,message : panel.clearData(),
    'SAVE_DATA': lambda panel,message : panel.saveData(),
}

def checkFormat(string):
    pattern = re.compile(r'^\d{2}\.\d$')
    return pattern.match(string)



class Panel:
    def __init__(self, width, height, port):
        self.screen = Screen()
        self.screen.setup(width=width, height=height)
        title("Panel sterowania")
        self.serialPort = SerialPort(port, 9600, 1)
        self.yRef = StringVar(value = "25.0")
        self.uS = StringVar(value="0")
        self.e = StringVar(value="10")
        self.curTemp = StringVar(value = "20")
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
            self.data['TIME'].append(self.data['TIME'][len(self.data['TIME']) -1] + 0.1)
        else:
            self.data['TIME'].append(0.1)
        self.uS.set(str(us))
        self.e.set(str(e))
        self.curTemp.set(str(temp))
    def showPlot(self, Data):
        plt.close()
        newfigure = Figure()
        plt.plot(self.data['TIME'], self.data[Data])
        plt.xlabel("Time [s]")
        if Data=="UCHYB":
            wanterError = [1] * len(self.data['TIME'])
            plt.plot(self.data['TIME'], wanterError)
            plt.legend(['Uchyb rzeczywisty', 'Uchyb Docelowy'])
            plt.title("Wykres uchybu")
            plt.ylabel("Uchyb [%]")
        elif Data=="TEMP":
            wanterTemp = [float(self.yRef.get())] * len(self.data['TIME'])
            plt.plot(self.data['TIME'], wanterTemp)
            plt.title("Wykres temperatury")
            plt.legend(['Temperatura rzeczywista', 'Temperatura docelowa'])
            plt.ylabel("Temperatura [°C]")
        elif Data=="PWM":
            plt.title("Wykres sygnału sterującego")
            plt.ylabel("Wypełnienie PWM [%]")
        plt.show()
    def clearData(self):
        self.data = {
            'PWM': [],
            'UCHYB' : [],
            'TEMP' : [],
            'TIME' : [],
        }
    def sendTempSetting(self):
        if not checkFormat(self.yRef.get()):
            print("Nieporawny format temperatury. Powinno być dd.d")
            return
        valueToSend = float(self.yRef.get())
        if valueToSend > 45.0:
            self.yRef.set('45.0')
        elif valueToSend < 25.0:
            self.yRef.set('25.0')
        self.serialPort.sendMessage(str(self.yRef.get()))
    def saveData(self):
        with open("data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["TIME", "PWM", "UCHYB", "TEMP"])
            for i in range(len(self.data['TIME'])):
                writer.writerow([self.data['TIME'][i], self.data['PWM'][i], self.data["UCHYB"][i], self.data["TEMP"][i]]);