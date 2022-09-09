import smtplib
from libs.loadconf import secrets

class SendMail():
    def __enter__(self):
        self.handle = smtplib.SMTP_SSL("smtp.sendgrid.net", 465)
        self.handle.login("apikey", secrets["sendgridAPI"])
        return self

    def __exit__(self, type, value, tb):
        self.handle.quit()

    def sendInviteVerification(self, address, code):
        with open("inviteSite/views/email.template") as msgHandle:
            msg = msgHandle.read().format(address, code)
        self.handle.sendmail("no-reply@hacksoc.co.uk", [address], msg)

    def sendWarning(self, msg):
        self.handle.sendmail("no-reply@hacksoc.co.uk", ["secretary@hacksoc.co.uk"], msg)
