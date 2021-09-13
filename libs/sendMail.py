import smtplib

class SendMail():
    def __init__(self):
        self.handle = smtplib.SMTP_SSL("localhost")

    def sendInviteVerification(self, address, code):
        with open("inviteSite/views/email.template") as msgHandle:
            msg = msgHandle.read().format(address, code)
        self.handle.sendmail("no-reply@hacksoc.co.uk", [address], msg)

    def sendWarning(self, msg):
        self.handle.sendmail("no-reply@hacksoc.co.uk", ["secretary@hacksoc.co.uk"], msg)
