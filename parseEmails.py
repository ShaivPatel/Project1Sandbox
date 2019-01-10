import sys
import pandas
from models.persons import Client, Employee
from models.emails import Email
from openpyxl import load_workbook

################## Column Names #######################
company_name = "CompanyName"
company_domain = "Domain"

email_date = "Date"
email_domain = "Domain"
email_address = "Email"
email_id = "ID"
email_subject = "Subject"
email_type = "Type"
################## Column Names #######################




################## Reading Files #######################

email_records_file_path =  "EmailRecordsPseudoData.csv"
sales_force_contacts_path =  "SalesForcePseudoData.csv"

#email_records_file_path = sys.argv[1]
#sales_force_contacts_path = sys.argv[2]


email_records_df = pandas.read_csv(email_records_file_path)
salesforce_contacts_df = pandas.read_csv(sales_force_contacts_path)

#ws = load_workbook(filename = email_records_file_path, read_only=True)
################## Reading Files #######################


# for row in ws.rows:
#     print(row)
#
#
#






def parseSalesForce(df):
    clients = {}
    for row_index, row in df.iterrows():
        companyName = row[company_name]
        companyDomain = row[company_domain]
        clients[companyDomain] = Client(companyName, companyDomain)
    return clients


def splitDataFrame(df,client_domains):

    sub_frames = []
    sub_frame = []
    isClient = False
    isEmployee = False
    containsClient = False

    for row_index, row in df.iterrows():

        if row["Type"]=="FROM":
            if len(sub_frame)>1 and (isClient or containsClient):
                sub_frames.append(pandas.DataFrame(sub_frame))
            isEmployee = False
            isClient = False
            sub_frame=[]
            if row["Domain"] == "macquarie.com":
                isEmployee = True
                sub_frame.append(row)
            if row["Domain"] in client_domains:
                isClient = True
                sub_frame.append(row)
        elif isClient:
            if row["Domain"] == "macquarie.com":
                sub_frame.append(row)
        elif isEmployee:
            if row["Domain"] in client_domains:
                sub_frame.append(row)
                containsClient= True




    return sub_frames


if __name__ == "__main__":

    # Create empty dataFrame to populate with matched records
    matched_records = pandas.DataFrame()
    # Create a dict of clients from SalesForce csv
    clients = parseSalesForce(salesforce_contacts_df)
    # Create a dict of employees
    employees = {}
    # Get list of each email in the form of a data frame
    email_dfs = splitDataFrame(email_records_df, clients.keys())
    # Create a dict of emails
    emails = {}

    for email_df in email_dfs:

        if email_df.iloc[0][email_domain] == 'macquarie.com':
            if email_df.iloc[0][email_address] not in employees:
                new_employee = Employee(email_df.iloc[0][email_address])
                employees[new_employee.email] = new_employee

            employee = employees[email_df.iloc[0][email_address]]
            new_email = Email(email_df)
            new_email.setSender(employee)

            for i in range(1, email_df.shape[0]):
                if email_df.iloc[i][email_domain] in clients:
                    new_email.addReceiver(clients[email_df.iloc[i][email_domain]])

            emails[new_email.id] = new_email
        else:
            # is client
            client = clients[email_df.iloc[0][email_domain]]

            new_email = Email(email_df)
            new_email.setSender(client)

            for i in range(1, email_df.shape[0]):
                if email_df.iloc[0][email_address] not in employees:
                    new_employee = Employee(email_df.iloc[0][email_address])
                    employees[new_employee.email] = new_employee
                new_email.addReceiver(employees[email_df.iloc[0][email_address]])
            emails[new_email.id] = new_email

    matches = []
    for email in emails:
        print(emails[email].toDF())
        matches.extend(emails[email].toDF())

    matches_df = pandas.DataFrame(matches)

    matches_df.to_csv("MatchedRecords.csv", index=False)
