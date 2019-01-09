from collections import deque
import pandas
class Email():

    def __init__(self,df):
        self.id = df.iloc[0]["ID"]
        self.sender = ""
        self.subject = df.iloc[0]["Subject"]
        self.date = df.iloc[0]["Date"]
        self.receivers = []


    def addReceiver(self,receiver):
        self.receivers.append(receiver)
        receiver.receivedEmails.append(self)

    def setSender(self,sender):
        sender.sentEmails.append(self)
        self.sender = sender

    def __str__(self):
        return f"id : {self.id} | date: {self.date} | subject : {self.subject} | sender : {self.sender.email}"

    def toDF(self):
        df = []
        for receiver in self.receivers:
            dic = {"Date": self.date, "ID": self.id, "Sender": self.sender.email, "Receiver": receiver.email,
             "Subject": self.subject}
            df.append(dic)

        return df
class EmailThread():

    def __init__(self,first_email):
        self.thread = deque()
        self.first_email = first_email
        self.thread.append(self.first_email)

    def appendEmail(self,email):
        self.thread.append()

