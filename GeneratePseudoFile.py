from random import randint, shuffle
import datetime
import pandas
domains = ['macquarie.com', 'gmail.com', 'ibm.com', 'amazon.com','stoneridge.com','apple.com','hotmail.com','aol.com','macys.com','suny.edu','cuny.edu','lordtaylor.com']
sf_domains = ['ibm.com', 'amazon.com','stoneridge.com']
fnames = ['John', 'Adam', 'Billy Bob', 'James', 'Anna', 'Lilo', 'Stitch']
lnames = ['Smith', 'Patel', 'de La Cruz', 'O\'Connor']
subjects = ['Junk', 'P&L Statements', 'Balance Sheets', 'Vacation Cruises', 'John\'s Wedding Invite',
            'Weekly Meeting Minutes', 'Invoices for This Month', 'MGL Training']
probs = [1,1,1,1,1,2,2,2,3,3,4]
month = ['10', '11', '12']
day = [str(x).zfill(2) for x in range(1, 30)]
year = ['2018']

email_records = []
sf_contacts = []
contacts = []
emails = []

def id_generator():
    ids = list(range(200000, 300000))
    shuffle(ids)
    for id in ids:
        yield id


idg = id_generator()


class Contact():
    def __init__(self, fname, lname, domain):
        self.fullname = fname + " " + lname
        self.email = self.fullname.replace(' ', '.') + "@" + domain
        self.domain = domain

    def __str__(self):
        return f"fullname : {self.fullname} | email : {self.email}"

    def toDict(self):
        return {"Name" : self.fullname, "Email" : self.email, "Domain" : self.domain}

class Record():
    def __init__(self, email, contact, to_from):
        self.email = email
        self.contact = contact
        self.to_from = to_from

    def __str__(self):
        return f"id : {self.email.id} | date: {self.email.date} | name : {self.contact.fullname}| email : {self.contact.email} | to_from : {self.to_from} | subject : {self.email.subject} | domain:{self.contact.domain}"
    def toDict(self):
        return {"Date" : self.email.date , "ID" : self.email.id ,  "Email" : self.contact.email , "Type" : self.to_from, "Subject" : self.email.subject, "Domain":self.contact.domain}
class Email():
    def __init__(self, subject, date):
        self.subject = subject
        self.date = date
        self.id = next(idg)
    def __str__(self):
        return f"id : {self.id} | date: {self.date} | subject : {self.subject}"


def random(lst):
    index = randint(0, len(lst) - 1)
    return lst[index]


for _ in range(20):
    fname = random(fnames)
    lname = random(lnames)
    domain = random(domains)
    contact = Contact(fname, lname, domain)
    sf_contacts.append(contact)
    contacts.append(contact)
for _ in range(50):
    fname = random(fnames)
    lname = random(lnames)
    domain = random(domains)
    contact = Contact(fname, lname, domain)
    contacts.append(contact)
for _ in range(100):
    date = f"{random(month)}/{random(day)}/{random(year)}"
    subject = random(subjects)
    emails.append(Email(subject,date))

for email in emails:
    prob = random(probs)

    email_record = Record(email,random(contacts),"FROM")
    email_records.append(email_record)

    for _ in range(prob):
        email_record = Record(email,random(contacts),"TO")
        email_records.append(email_record)
print("===============================================\nSalesForce Contacts\n================================================")
for contact in sf_domains:
    print(contact)
print("===============================================\nContacts\n================================================")
for contact in contacts:
    print(contact)
print("===============================================\nEmails\n================================================")
for email in emails:
    print(email)
print("===============================================\nRecords\n================================================")
for record in email_records:
    print(record)


rec_list = (r.toDict() for r in email_records)
sfc_df = pandas.DataFrame({"Domain":sf_domains, "CompanyName":[x.split(".")[0].capitalize() for x in sf_domains]})
rec_df = pandas.DataFrame(rec_list)

sfc_df.to_csv("SalesForcePseudoData.csv",index=False)
rec_df.to_csv("EmailRecordsPseudoData.csv",index=False)