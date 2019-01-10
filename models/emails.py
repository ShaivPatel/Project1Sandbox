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
                employee_email = sender_row.email_address
                employee_name = employee_email.split("@")[0].replace("."," ").title()
                employees[sender_row.email_address] = Employee(employee_name,employee_email)

            self.setSender(employees[email_rows.email_address])

            for email_row in email_rows[1:]:
                self.addReceiver(clients[email_row.domain])



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
    id_index = 1
    email_address_index = 2
    type_index = 3
    subject_index = 4
    domain = 5

    def __init__(self,row_array):
        self.date = row_array[EmailRow.date_index]
        self.id = row_array[EmailRow.id_index]
        self.email_address = row_array[EmailRow.email_address_index]
        self.type = row_array[EmailRow.type_index]
        self.subject = row_array[EmailRow.subject_index]
        self.domain = row_array[EmailRow.domain_index]

class EmailThread():

    def __init__(self,first_email):
        self.thread = deque()
        self.first_email = first_email
        self.thread.append(self.first_email)

    def appendEmail(self,email):
        self.thread.append()

