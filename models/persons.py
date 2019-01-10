class Contact():
    def __init__(self,name,email):
        self.name = name
        self.email = email
        self.receivedEmails = []
        self.sentEmails = []

    def __str__(self):
        return f"name : {self.name} | email : {self.email}"


class Client(Contact):
    def __init__(self, account_name, domain):
        super().__init__(account_name,domain)
        self.macquarie_contacts = set()



class Employee(Contact):
    def __init__(self,email):
        name = email.split("@")[0].replace("."," ").title()
        super().__init__(name,email)