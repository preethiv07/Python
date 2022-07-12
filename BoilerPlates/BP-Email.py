# Read from excel files, process in pandas and store in oracle database
# Email library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# End of Email
import logging
import pandas as pd
from pandas import read_excel
import cx_Oracle
import os
from datetime import datetime, timedelta
import datetime




def sendEmail(note, status):
    body = ''
    if status == 'success':
        subject = "Project Oracle Load Finish: " + note
        body = subject
    elif status == 'fail':
        subject = "Project | EXCEL NOT FOUND | " + note
        body = subject + " | "+log_date
    elif status == 'log':
        subject = f"""Project {log_date} ERROR LOG """
        body = note

    message = MIMEMultipart('mixed')
    message['Subject'] = subject
    message['From'] = ", ".join(fromaddr)
    message['To'] = ", ".join(toaddr)

    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    server = smtplib.SMTP('smtp.org.com', 25) #update org name
    server.ehlo()
    server.starttls()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def data_Processing(today_Devfiles):
    excel_name="file.xlsx"
    note = 'Project'
    excel_full_name = next((s for s in today_Devfiles if excel_name in s), None)
    print("------------ EXCEL FILES------------",'\n',excel_full_name)
    sheetname = 'Sheet1'
    if excel_full_name != None:
        df = read_excel(os.path.join(sterlingDevPath,excel_full_name))
        print("------------DF ------------", '\n', "df head")
    else:
        sendEmail(note, status='fail')

def main():
    # print("today", today)
    today_Devfiles = []
    today_Prodfiles = []
    try:
        for file in os.listdir(sterlingDevPath):
            FileFullName =(sterlingDevPath + "/" +file)
            filetime=datetime.datetime.fromtimestamp(os.path.getmtime(FileFullName))
            if filetime.date()==today:
                # print(file,"---- ",filetime)
                today_Devfiles.append(file)
    # Error When accessing the folder
    except:
        logging.error("Accessing folder ERROR " + path)
    print("------------TODAY FILES------------",'\n',today_Devfiles)

    # Call functions
    data_Processing(today_Devfiles)

if __name__=='__main__':
    # set variables
    env='DEV'
    sterlingDevPath = "//Devfolder/DataAnalytics"
    sterlingProdPath = "//Prodfolder/DataAnalytics"

    if env=='DEV':
        sterlingPath = "//Devfolder/DataAnalytics"
    elif env=='PROD':
        sterlingPath = "//Prodfolder/DataAnalytics"

    # TodayDateSetup
    today=datetime.datetime.now().date()
    log_date: str = today.strftime('%Y-%m-%d')

    #Email Recipients
    fromaddr = ['Preethi_Venkatesan@email.com']
    toaddr = ['Preethi_Venkatesan@email.com']
    main()