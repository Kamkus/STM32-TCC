import serial
class SerialPort:
    def __init__(self, port, baund_rate, timeout):
        self.serial = serial.Serial(port, baund_rate, timeout=timeout)
        self.curValues = []
    def sendMessage(self, message):
        self.serial.write(message.encode())
    def readMessage(self):
        values = self.serial.readline().decode().replace('\r\n', '').split(', ')
        if len(values) == 0:
            if len(self.curValues) == 0:
                return ["0", "0", "0"]
            else:
                return self.curValues
        self.curValues = values
        return values


