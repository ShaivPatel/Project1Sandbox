from collections import deque
from models.persons import Client, Employee
import pandas
class Email():

    def __init__(self,email_rows,employees,clients):
        sender_row = email_rows[0]
        self.id = sender_row.id
        self.subject = sender_row.subject
        self.date = sender_row.date
        self.receivers = []
        self.sender=""

        if sender_row.domain == "macquarie.com":
            if sender_row.email_address not in employees:
                employees[sender_row.email_address] = Employee(sender_row.email_address)

            self.setSender(employees[sender_row.email_address])

            for email_row in email_rows[1:]:
                self.addReceiver(clients[email_row.domain])
        else:


            self.setSender(clients[sender_row.domain])

            for email_row in email_rows[1:]:
                if email_row.email_address not in employees:
                    employees[email_row.email_address] = Employee(email_row.email_address)
                self.addReceiver(employees[email_row.email_address])

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
            dic = {"Date": self.date, "ID": self.id, "Sender": self.sender.name, "Receiver": receiver.name,
             "Subject": self.subject}
            df.append(dic)


        return df

class EmailRow():

    date_index = 0
    id_index = 3
    email_address_index = 2
    type_index = 5
    subject_index = 4
    domain_index = 1

    def __init__(self,row_array):
        self.date = row_array[EmailRow.date_index]
        self.id = row_array[EmailRow.id_index]
        self.email_address = row_array[EmailRow.email_address_index]
        self.type = row_array[EmailRow.type_index]
        self.subject = row_array[EmailRow.subject_index]
        self.domain = row_array[EmailRow.domain_index]

    def __str__(self):
        return f"date:{self.date} | id:{self.id} | email_address:{self.email_address} | type:{self.type} | subject:{self.subject} | domain:{self.domain}"

class EmailThread():

    def __init__(self,first_email):
        self.thread = deque()
        self.first_email = first_email
        self.thread.append(self.first_email)

    def appendEmail(self,email):
        self.thread.append()

