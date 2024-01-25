from panel import Panel
from turtle import done, mainloop
from tkinter import *
from time import sleep
import threading
import matplotlib.pyplot as plot
closed = False
def showPlot(screen):
    while not closed:
        screen.readLine()
        sleep(0.1)
    


# screen.exitonclick()
screen = Panel(600, 250, "COM3")
# button = Button(screen.screen.getcanvas().master, text="Exit", command=showPlot)
# button.pack()
screen.createInputBox("yREF[°C]", screen.yRef, 20, 100-70, "normal")
screen.createButton("Ustaw", 'SET_TEMPERATURE','', 220, 100-70)
screen.createInputBox("PWM[%]", screen.uS, 20, 130-70, "readonly")
screen.createInputBox("Uchyb[%]", screen.e, 20, 160-70, "readonly")
screen.createInputBox("Temp[°C]", screen.curTemp, 20, 190-70, "readonly")
screen.createButton("Wyczyść Dane", 'CLEAR_DATA','ALL', 20, 220-70)
screen.createButton("Wykres [Temp]", 'SHOW_PLOT','TEMP', 110, 220-70)
screen.createButton("Wykres [Uchyb]", 'SHOW_PLOT','UCHYB', 205, 220-70)
screen.createButton("Wykres [PWM]", 'SHOW_PLOT','PWM', 305, 220-70)
# screen.createButton("Wykres [PWm]", 'CLEAR_DATA','DUPA', 200, 190)
x = threading.Thread(target=showPlot, args=[screen])
x.start()
mainloop()
closed = True