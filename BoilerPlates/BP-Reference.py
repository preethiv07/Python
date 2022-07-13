
import cx_Oracle
import os
from pandas import read_excel
from datetime import datetime, timedelta
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.encoders import encode_base64
import logging
cx_Oracle.init_oracle_client(lib_dir=r"C:\Oracle\instantclient_19_11")


def sendEmail(note, status):
    body = ''
    if status == 'success':
        subject = "Crew Hire Oracle Load Finish: " + note
        body = subject
    elif status == 'fail':
        subject = "Crew Hire EXCEL NOT FOUND: " + note
        body = subject
    elif status == 'log':
        subject = f"""Crew Hire {log_date} ERROR LOG """
        body = note

    message = MIMEMultipart('mixed')
    message['Subject'] = subject
    message['From'] = ", ".join(fromaddr)
    message['To'] = ", ".join(toaddr)

    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    server = smtplib.SMTP('smtp.csx.com', 25)
    server.ehlo()
    server.starttls()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def checkLog():
    with open(log_file) as f:
        contents = f.readlines()
    today_error = [val for idx, val in enumerate(contents) if log_date in val]
    if len(today_error) >0:
        todayErrorStr = '\n '.join(today_error)
        sendEmail(todayErrorStr, status='log' )

def trunc_table(conn_str, note):
    conn = cx_Oracle.connect(conn_str)
    cursor = conn.cursor()
    print('TRUNCATING TABLE ' + note )

    if note == 'Crew Hire Diversity':
        delete = f""" DELETE FROM  H7853.CREW_HIRE_DIVERSITY WHERE  SYSTEM_d = TO_DATE('{today1}','MM-DD-YYYY')  """
    if note == 'Crew Hire Referral':
        delete = f""" DELETE FROM  H7853.CREW_HIRE_REFERRAL WHERE  SYSTEM_d = TO_DATE('{today1}','MM-DD-YYYY')  """
    if note == 'Crew Hire Referral Active':
        delete = """ TRUNCATE TABLE  H7853.CREW_HIRE_REFERRAL_ACTIVE  """

    if note == 'Candidates Processing':
        delete = f""" DELETE FROM   H7853.CREW_HIRE_CANDIDATES WHERE  SYSTEM_d = TO_DATE('{today1}','MM-DD-YYYY') AND SOURCE_N = '{note}'  """
    if note == 'New Candidates':
        delete = f""" DELETE FROM   H7853.CREW_HIRE_CANDIDATES WHERE  SYSTEM_d = TO_DATE('{today1}','MM-DD-YYYY') AND SOURCE_N = '{note}'  """
    if note == 'Hired Candidates':
        delete = f""" DELETE FROM   H7853.CREW_HIRE_CANDIDATES WHERE  SYSTEM_d = TO_DATE('{today1}','MM-DD-YYYY') AND SOURCE_N = '{note}'  """
    if note == 'Fallout':
        delete = f""" DELETE FROM   H7853.CREW_HIRE_CANDIDATES WHERE  SYSTEM_d = TO_DATE('{today1}','MM-DD-YYYY') AND SOURCE_N = '{note}'  """

    print(delete)
    cursor.execute(delete)
    conn.commit()
    cursor.close()
    conn.close()

def insert2Oracle(conn_str, df_final, note) :

    conn = cx_Oracle.connect(conn_str)
    cursor = conn.cursor()

    if df_final.empty == False:
        dataList = df_final.values.tolist()

    if note == 'Crew Hire Diversity':
        insert = """INSERT INTO h7853.CREW_HIRE_DIVERSITY (REQ_CREATION_D, REQ_I, REQ_TITLE_N, CITY_N, STATE_N, 
                        OPENINGS_COUNT_Q, HIRED_ON_REQ_COUNT_Q, RECRUITER_N, HIRING_MANAGER_N, CURRENT_STATUS_C, 
                        RACE_C, GENDER_C, HISTORICAL_STEP_N, CURRENT_STEP_STATUS_X, SUBMISSION_COMPL_WEEK_D, SUBMISSIONS_COUNT_Q, SYSTEM_D)
                    VALUES ( to_date(:0, 'MM/DD/YYYY HH24:MI:SS'), :1,  :2, :3,:4,:5,:6, :7, :8, :9, :10, :11, :12, 
                            :13, to_date(:14, 'MM/DD/YYYY'), :15, to_date(:17,  'MM/DD/YY' )  )"""

        for index, elem in enumerate(dataList):
            print('Inserting to Oracle Diversity')
            print(index, elem)
            try:
                cursor.execute(insert, {'0': dataList[index][0], '1': dataList[index][1], '2': dataList[index][2],
                                        '3': dataList[index][3], '4': dataList[index][4], '5': dataList[index][5],
                                        '6': dataList[index][6], '7': dataList[index][7], '8': dataList[index][8],
                                        '9': dataList[index][9], '10': dataList[index][10], '11': dataList[index][11],
                                        '12': dataList[index][12], '13': dataList[index][13], '14': dataList[index][14],
                                        '15': dataList[index][15], '17': dataList[index][17]})
            except:
                logging.error(f""" {note} Oracle Insert Failed : index - {index}, elem - {elem} """)
            conn.commit()

    elif note == 'Crew Hire Referral':
        insert = """INSERT INTO h7853.CREW_HIRE_REFERRAL (REFERRER_EE_I, EMPLOYEE_FULL_N, REFERRAL_D, CANDIDATE_I, 
                        REFERRED_CANDIDATE_N, JOB_SUBMISSIONS_COMPLETE_COUNT_Q , REQ_I , SYSTEM_D)
                    VALUES (  :0,  :1, to_date(:2, 'MM/DD/YYYY HH24:MI:SS') ,:3, :4, :5, :6,  to_date(:7,  'MM/DD/YY' )  )"""

        for index, elem in enumerate(dataList):
            print('Inserting to Oracle Referral')
            print(index, elem)
            try:
                cursor.execute(insert, {'0': dataList[index][0], '1': dataList[index][1], '2': dataList[index][2],
                                        '3': dataList[index][3], '4': dataList[index][4], '5': dataList[index][5],
                                        '6': dataList[index][6], '7': dataList[index][7] })
            except:
                logging.error(f""" {note} Oracle Insert Failed : index - {index}, elem - {elem} """)
            conn.commit()

    elif note == 'Crew Hire Referral Active':
        x = 1
        insert = """insert into   H7853.CREW_HIRE_REFERRAL_ACTIVE (req_i, candidate_i, active_d )
                    select req_i, candidate_i, max(system_d) from  H7853.CREW_HIRE_REFERRAL
                    group by req_i, candidate_i"""
        try:
            cursor.execute(insert)
        except:
            logging.error(f""" {note} Oracle Insert Failed """)
        conn.commit()

    cursor.close()
    conn.close()

def formatData(df):

    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)

    try:
        df.columns = df.columns.fillna('to_drop')
        df.drop('to_drop', axis=1, inplace=True)
    except:
        pass

    df = df.loc[:, ~df.columns.duplicated()]

    datecols = [s for s in list(df.columns) if "Date" in s]
    for i in datecols:
        print(i)
        df[i] = pd.to_datetime(df[i], errors='coerce').dt.strftime('%m/%d/%Y %H:%M:%S')
        print('done')

    df = df.rename(columns=lambda x: x.strip())

    for i in df.columns:
        if 'Date' not in i:
            try:
                df[i] = df[i].str.encode('ascii', 'ignore').str.decode('ascii')
            except:
                print('EXCEPT ' + i)
                pass

    return df

def crew_hire_candidates_processing(today_files):
    excel_name = 'Freight Conductors - Crew Hiring Stats'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    sheetname = 'Candidates Processing'
    note = 'Crew Hire Candidates Processing'
    if excel_full_name != None:
        trunc_table(conn_str, sheetname)
        df = read_excel(os.path.join(path, excel_full_name), header=None, sheet_name=sheetname)
        if df[0][0] == sheetname:
            df.drop(df.index[0], inplace=True)

        df = formatData(df)

        df['System_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df['Source_N'] = sheetname
        df['Work City'] = df['Work City'].str.upper()
        df['Work State'] = df['Work State'].str.upper()
        df.fillna('', inplace=True)
        if len([c for c in df.columns if 'Template Job Code' in c]) == 2:
            df = df.drop('Req Template Job Code', 1)

        pk_cols = ['System_D', 'Req #', 'Candidate Identifier', 'Source_N']
        duplicateRows = df[df.duplicated(pk_cols, keep='last')]
        if len(duplicateRows) >= 1:
            df.drop_duplicates(subset=pk_cols, keep='last', inplace=True)

        colsDict = {'Req #': 'REQ_I', 'Level 2': 'LEVEL_2_X', 'Level 3': 'LEVEL_3_X', 'Level 4': 'LEVEL_4_X',
                    'Level 5 - Name': 'REGION_N', 'Position Title': 'POSITION_TITLE_N', 'FC Agreement': 'FC_AGREEMENT_C',
                    'Position Number Value': 'POSITION_NUM_VALUE_I', 'Work City': 'WORK_CITY_N',
                    'Work State': 'WORK_STATE_N', 'Hiring Manager': 'HIRING_MANAGER_N', 'Pay Group': 'PAY_GROUP_C',
                    'Band': 'BAND_C', 'First Sourced Date': 'FIRST_SOURCED_D', 'Recruiter': 'RECRUITER_N',
                    'Application is Internal': 'INTERNAL_APPLICATION_FLAG_S', 'Candidate Identifier': 'CANDIDATE_I',
                    'Offer Extended Date': 'OFFER_EXTENDED_D', 'Offer Actual Start Date': 'OFFER_ACTUAL_START_D',
                    'Req. Creation Date': 'REQ_CREATION_D', 'Candidate Name': 'CANDIDATE_N', 'Email': 'EMAIL_X',
                    'Employee Number': 'EMPLOYEE_I', 'Current Step Name': 'CURRENT_STEP_X',
                    'Current Status Name': 'CURRENT_STEP_STATUS_X', 'Recruiter Assistant': 'RECRUITER_ASSISTANT_N',
                    'MTP?': 'JOB_TITLE_N', 'Mgmt / Union': 'MGMT_UNION_C', 'Craft Code': 'CRAFT_C',
                    'Current Status': 'CURRENT_STATUS_C', 'Template Job Code': 'REQ_TEMPLATE_JOB_C',
                    'Submission Completed Date': 'SUBMISSION_COMPLETED_D',
                    'Current Status Start Date': 'CURRENT_STATUS_START_D', 'Source_N': 'SOURCE_N', 'System_D': 'SYSTEM_D'}

        excelColsList = list(iter(colsDict))
        excelColNames = ', '.join([str(elem) for elem in excelColsList])
        df_final = df[excelColsList]

        dataList = df_final.values.tolist()
        colsDict_values = list(colsDict.values())
        oracleColNames = ', '.join([str(elem) for elem in colsDict_values])

        env = 'DEV'
        if env == 'DEV':
            conn = cx_Oracle.connect('h7853/h7853@ORACL19T:1521/EDWD')
        cursor = conn.cursor()

        insert = f"""INSERT INTO h7853.CREW_HIRE_CANDIDATES ( {oracleColNames} ) 
                    VALUES ( :0, :1,  :2, :3,:4,:5,:6, :7, :8, :9, :10, :11, :12, to_date(:13, 'MM/DD/YYYY HH24:MI:SS'), 
                    :14, :15, :16, to_date(:17, 'MM/DD/YYYY HH24:MI:SS'), to_date(:18, 'MM/DD/YYYY HH24:MI:SS'),
                     to_date(:19, 'MM/DD/YYYY HH24:MI:SS'), :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30 , 
                     to_date(:31,  'MM/DD/YYYY HH24:MI:SS' ),  to_date(:32,  'MM/DD/YYYY HH24:MI:SS' ), :33,  to_date(:34,  'MM/DD/YY' )  )"""

        for index, elem in enumerate(dataList):
            print(index, elem)
            try:
                cursor.execute(insert, {'0': dataList[index][0], '1': dataList[index][1], '2': dataList[index][2],
                                        '3': dataList[index][3], '4': dataList[index][4], '5': dataList[index][5], '6': dataList[index][6],
                                        '7': dataList[index][7], '8': dataList[index][8], '9': dataList[index][9], '10': dataList[index][10],
                                        '11': dataList[index][11], '12': dataList[index][12], '13': dataList[index][13], '14': dataList[index][14],
                                        '15': dataList[index][15], '16': dataList[index][16], '17': dataList[index][17], '18': dataList[index][18],
                                        '19': dataList[index][19], '20': dataList[index][20], '21': dataList[index][21], '22': dataList[index][22],
                                        '23': dataList[index][23], '24': dataList[index][24], '25': dataList[index][25], '26': dataList[index][26],
                                        '27': dataList[index][27], '28': dataList[index][28], '29': dataList[index][29], '30': dataList[index][30],
                                        '31': dataList[index][31], '32': dataList[index][32], '33': dataList[index][33], '34': dataList[index][34]})
            except:
                logging.error(f""" {sheetname} Oracle Insert Failed : index - {index}, elem - {elem} """)
            conn.commit()

        cursor.close()
        conn.close()

        sendEmail(note, status='success')
    else:
        sendEmail(note, status='fail')

def crew_hire_candidates_new_candidates(today_files):
    excel_name = 'Freight Conductors - Crew Hiring Stats'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    sheetname = 'New Candidates'
    note = 'Crew Hire New Candidates'
    if excel_full_name != None:
        trunc_table(conn_str, sheetname)
        df = read_excel(os.path.join(path, excel_full_name), header=None, sheet_name=sheetname)

        if df[0][0] == sheetname:
            df.drop(df.index[0], inplace=True)

        df = formatData(df)

        df['System_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df['Source_N'] = sheetname
        df['Work City'] = df['Work City'].str.upper()
        df['Work State'] = df['Work State'].str.upper()
        df.fillna('', inplace=True)
        if len([c for c in df.columns if 'Template Job Code' in c]) == 2:
            df = df.drop('Req Template Job Code', 1)

        pk_cols = ['System_D', 'Req #', 'Candidate Identifier', 'Source_N']
        duplicateRows = df[df.duplicated(pk_cols, keep='last')]
        if len(duplicateRows) >= 1:
            df.drop_duplicates(subset=pk_cols, keep='last', inplace=True)

        colsDict = {'Req #': 'REQ_I', 'Level 2': 'LEVEL_2_X', 'Level 3': 'LEVEL_3_X', 'Level 4': 'LEVEL_4_X',
                    'Level 5 - Name': 'REGION_N', 'Position Title': 'POSITION_TITLE_N', 'FC Agreement': 'FC_AGREEMENT_C',
                    'Work City': 'WORK_CITY_N', 'Work State': 'WORK_STATE_N', 'Hiring Manager': 'HIRING_MANAGER_N',
                    'First Sourced Date': 'FIRST_SOURCED_D', 'Recruiter': 'RECRUITER_N',
                    'Application is Internal': 'INTERNAL_APPLICATION_FLAG_S', 'Candidate Identifier': 'CANDIDATE_I',
                    'Req. Creation Date': 'REQ_CREATION_D', 'Candidate Name': 'CANDIDATE_N', 'Email': 'EMAIL_X',
                    'Employee Number': 'EMPLOYEE_I', 'Current Step Name': 'CURRENT_STEP_X',
                    'Current Status Name': 'CURRENT_STEP_STATUS_X', 'Recruiter Assistant': 'RECRUITER_ASSISTANT_N',
                    'MTP?': 'JOB_TITLE_N', 'Current Status': 'CURRENT_STATUS_C', 'Template Job Code': 'REQ_TEMPLATE_JOB_C',
                    'Submission Completed Date': 'SUBMISSION_COMPLETED_D',
                    'Source_N': 'SOURCE_N', 'System_D': 'SYSTEM_D'}

        excelColsList = list(iter(colsDict))
        excelColNames = ', '.join([str(elem) for elem in excelColsList])
        df_final = df[excelColsList]

        dataList = df_final.values.tolist()
        colsDict_values = list(colsDict.values())
        oracleColNames = ', '.join([str(elem) for elem in colsDict_values])

        env = 'DEV'
        if env == 'DEV':
            conn = cx_Oracle.connect('h7853/h7853@ORACL19T:1521/EDWD')
        cursor = conn.cursor()

        insert = f"""INSERT INTO h7853.CREW_HIRE_CANDIDATES ( {oracleColNames} ) 
                    VALUES ( :0, :1,  :2, :3,:4,:5,:6, :7, :8, :9, to_date(:10, 'MM/DD/YYYY HH24:MI:SS'), :11, :12, :13, 
                    to_date(:14, 'MM/DD/YYYY HH24:MI:SS'), :15, :16, :17, :18 , :19 , :20, :21, :22, :23, to_date(:24,  'MM/DD/YYYY HH24:MI:SS' ), 
                    :25, to_date(:26,  'MM/DD/YYYY' )  )"""

        for index, elem in enumerate(dataList):
            print(index, elem)
            try:
                cursor.execute(insert, {'0': dataList[index][0], '1': dataList[index][1], '2': dataList[index][2],
                                        '3': dataList[index][3], '4': dataList[index][4], '5': dataList[index][5], '6': dataList[index][6],
                                        '7': dataList[index][7], '8': dataList[index][8], '9': dataList[index][9], '10': dataList[index][10],
                                        '11': dataList[index][11], '12': dataList[index][12], '13': dataList[index][13], '14': dataList[index][14],
                                        '15': dataList[index][15], '16': dataList[index][16], '17': dataList[index][17], '18': dataList[index][18],
                                        '19': dataList[index][19], '20': dataList[index][20], '21': dataList[index][21], '22': dataList[index][22],
                                        '23': dataList[index][23], '24': dataList[index][24], '25': dataList[index][25], '26': dataList[index][26]})
            except:
                logging.error(f""" {sheetname} Oracle Insert Failed : index - {index}, elem - {elem} """)
            conn.commit()

        cursor.close()
        conn.close()

        sendEmail(note,status='success')
    else:
        sendEmail(note, status='fail')

def crew_hire_candidates_hired(today_files):
    excel_name = 'Freight Conductors - Crew Hiring Stats'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    sheetname = 'Hired Candidates'
    note = 'Crew Hire Hired Candidates'
    if excel_full_name != None:
        trunc_table(conn_str, sheetname)
        df = read_excel(os.path.join(path, excel_full_name), header=None, sheet_name=sheetname)
        if df[0][0] == sheetname:
            df.drop(df.index[0], inplace=True)

        df = formatData(df)
        df['System_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df['Source_N'] = sheetname
        df['Work City'] = df['Work Location'].str.split(',', 1).str[0]
        df['Work State'] = df['Work Location'].str.split(',', 1).str[1]
        df['Work City'] = df['Work City'].str.upper()
        df['Work State'] = df['Work State'].str.upper()
        df.fillna('', inplace=True)
        if len([c for c in df.columns if 'Template Job Code' in c]) == 2:
            df = df.drop('Req Template Job Code', 1)

        pk_cols = ['System_D', 'Req. Identifier', 'Candidate Identifier', 'Source_N']
        duplicateRows = df[df.duplicated(pk_cols, keep='last')]
        if len(duplicateRows)>=1:
            df.drop_duplicates( subset=pk_cols, keep='last', inplace=True)

        colsDict = {'Submission Identifier': 'SUBMISSION_I', 'Start Date': 'OFFER_ACTUAL_START_D',
                    'Flying or Driving': 'FLYING_DRIVING_X', 'Transferring Dept': 'TRANSFERRING_DEPT_N',
                    'Employee Number': 'EMPLOYEE_I',
                    'RACF': 'EMPLOYEE_RACF_I', 'Last Name': 'EMPLOYEE_LAST_N', 'First Name': 'EMPLOYEE_FIRST_N',
                    'Middle Initial': 'EMPLOYEE_MIDDLE_N', 'Address of Residence': 'EMPLOYEE_ADDRESS_X',
                    'Phone': 'EMPLOYEE_PHONE_X',
                    'Email': 'EMAIL_X', 'Date of Birth': 'EMPLOYEE_BIRTH_D', 'Job Title': 'JOB_TITLE_N',
                    'Work City': 'WORK_CITY_N', 'Work State': 'WORK_STATE_N', 'Hiring Manager': 'HIRING_MANAGER_N',
                    'Hiring Manager ID': 'HIRING_MANAGER_I', 'Hiring Manager PH#': 'HIRING_MANAGER_PHONE_X',
                    'Apprentice/Journeyman Status': 'APPRENTICE_JOURNEYMAN_STATUS_C', 'Union': 'UNION_N',
                    'Bargaining Unit': 'BARGAINING_UNIT_X', 'Agreement': 'FC_AGREEMENT_C', 'Req. Identifier': 'REQ_I',
                    'Candidate Identifier': 'CANDIDATE_I', 'Current Status': 'CURRENT_STATUS_C',
                    'Submission Completed Date': 'SUBMISSION_COMPLETED_D', 'Current Step Name': 'CURRENT_STEP_X',
                    'Current Status Name': 'CURRENT_STEP_STATUS_X', 'Current Status Start Date': 'CURRENT_STATUS_START_D',
                    'Hire Start Date': 'HIRE_START_D', 'Offer Accepted Date': 'OFFER_ACCEPTED_D', 'Source_N': 'SOURCE_N',
                    'System_D': 'SYSTEM_D'}

        excelColsList = list(iter(colsDict))
        excelColNames = ', '.join([str(elem) for elem in excelColsList])
        df_final = df[excelColsList]

        dataList = df_final.values.tolist()
        colsDict_values = list(colsDict.values())
        oracleColNames = ', '.join([str(elem) for elem in colsDict_values])

        env = 'DEV'
        if env == 'DEV':
            conn = cx_Oracle.connect('h7853/h7853@ORACL19T:1521/EDWD')
        cursor = conn.cursor()

        insert = f"""INSERT INTO h7853.CREW_HIRE_CANDIDATES ( {oracleColNames} ) 
                    VALUES ( :0, to_date(:1, 'MM/DD/YYYY HH24:MI:SS'), :2,  :3,:4 , :5, :6, :7, :8, :9, :10, :11, 
                    to_date(:12, 'MM/DD/YYYY HH24:MI:SS'), :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25 ,
                     to_date(:26, 'MM/DD/YYYY HH24:MI:SS'), :27, :28, to_date(:29, 'MM/DD/YYYY HH24:MI:SS'),  
                     to_date(:30, 'MM/DD/YYYY HH24:MI:SS'),  to_date(:31, 'MM/DD/YYYY HH24:MI:SS'), :32,  to_date(:33, 'MM/DD/YYYY') )"""

        for index, elem in enumerate(dataList):
            print(index, elem)
            try:
                cursor.execute(insert,
                               {'0': dataList[index][0], '1': dataList[index][1], '2': dataList[index][2],
                                '3': dataList[index][3], '4': dataList[index][4], '5': dataList[index][5], '6': dataList[index][6],
                                '7': dataList[index][7], '8': dataList[index][8], '9': dataList[index][9], '10': dataList[index][10],
                                '11': dataList[index][11], '12': dataList[index][12], '13': dataList[index][13], '14': dataList[index][14],
                                '15': dataList[index][15], '16': dataList[index][16], '17': dataList[index][17], '18': dataList[index][18],
                                '19': dataList[index][19], '20': dataList[index][20], '21': dataList[index][21], '22': dataList[index][22],
                                '23': dataList[index][23], '24': dataList[index][24], '25': dataList[index][25], '26': dataList[index][26],
                                '27': dataList[index][27], '28': dataList[index][28], '29': dataList[index][29], '30': dataList[index][30],
                                '31': dataList[index][31], '32': dataList[index][32], '33': dataList[index][33]})
            except:
                logging.error( f""" {sheetname} Oracle Insert Failed : index - {index}, elem - {elem} """ )
            conn.commit()

        cursor.close()
        conn.close()

        sendEmail(note,status='success')
    else:
        sendEmail(note, status='fail')

def crew_hire_fallouts(today_files):
    excel_name = 'Freight Conductors - Fallout - Crew Hiring Stats'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    sheetname = 'Fallout'
    note = 'Crew Hire Fallout'
    if excel_full_name != None:
        trunc_table(conn_str, sheetname)
        df = read_excel(os.path.join(path, excel_full_name), header=None)
        if df[0][0] == sheetname:
            df.drop(df.index[0], inplace=True)

        df = formatData(df)
        df['System_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df['Source_N'] = sheetname
        df['City'] = df['City'].str.upper()
        df.fillna('', inplace=True)
        if len([c for c in df.columns if 'Template Job Code' in c]) == 2:
            df = df.drop('Req Template Job Code', 1)

        df = df[~df['Req. Identifier'].str.contains('Grand Total', na=False)]

        pk_cols =  ['System_D', 'Req. Identifier', 'Candidate Identifier', 'Source_N']
        duplicateRows = df[df.duplicated(pk_cols, keep='last')]
        if len(duplicateRows)>=1:
            df.drop_duplicates( subset=pk_cols, keep='last', inplace=True)

        colsDict = {'Req. Identifier': 'REQ_I', 'Region': 'REGION_N', 'City': 'WORK_CITY_N',
                    'Candidate Identifier': 'CANDIDATE_I', 'Current Step Name': 'CURRENT_STEP_X',
                    'Current Status Name': 'CURRENT_STEP_STATUS_X',
                    'Submission Completed Date': 'SUBMISSION_COMPLETED_D', 'Source_N': 'SOURCE_N', 'System_D': 'SYSTEM_D'}

        excelColsList = list(iter(colsDict))
        excelColNames = ', '.join([str(elem) for elem in excelColsList])
        df_final = df[excelColsList]

        dataList = df_final.values.tolist()
        colsDict_values = list(colsDict.values())
        oracleColNames = ', '.join([str(elem) for elem in colsDict_values])

        env = 'DEV'
        if env == 'DEV':
            conn = cx_Oracle.connect('h7853/h7853@ORACL19T:1521/EDWD')
        cursor = conn.cursor()

        insert = f"""INSERT INTO h7853.CREW_HIRE_CANDIDATES ( {oracleColNames} ) 
                    VALUES ( :0, :1, :2,  :3,:4 , :5,  to_date(:6, 'MM/DD/YYYY HH24:MI:SS'), :7,  to_date(:8, 'MM/DD/YYYY HH24:MI:SS') )"""

        for index, elem in enumerate(dataList):
            print(index, elem)
            try:
                cursor.execute(insert,
                               {'0': dataList[index][0], '1': dataList[index][1], '2': dataList[index][2], '3': dataList[index][3],
                                '4': dataList[index][4], '5': dataList[index][5], '6': dataList[index][6],
                                '7': dataList[index][7], '8': dataList[index][8]})
            except:
                logging.error(f""" {sheetname} Oracle Insert Failed : index - {index}, elem - {elem} """)

            conn.commit()

        cursor.close()
        conn.close()

        sendEmail(note, status='success')
    else:
        sendEmail(note, status='fail')


def crew_hire_diversity(today_files):
    print('starting crew hire diversity')
    excel_name = 'Freight Conductors - Crew Hiring Stats'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    sheetname = 'Diversity Data - Historical'
    note = 'Crew Hire Diversity'
    if excel_full_name != None:
        trunc_table(conn_str, note)
        df = read_excel(os.path.join(path, excel_full_name), header=None, sheet_name=sheetname)
        print('READ EXCEL ' + sheetname)
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace=True)
        df['System_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df = df[~df['Req. Creation Date'].str.contains('Grand Total', na=False)]
        df['Req. Creation Date'] = pd.to_datetime(df['Req. Creation Date'])
        df['Req. Creation Date'] = df['Req. Creation Date'].apply(lambda x: x.strftime('%m/%d/%Y %H:%M:%S'))
        df['Submission Week Start Date'] = pd.to_datetime(df['Submission Week Start Date'])
        df['Submission Week Start Date'] = df['Submission Week Start Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        df[['Gender', 'Race']] = df[['Gender', 'Race']].fillna(value='Not Provided')
        df['Gender'] = df['Gender'].astype(str).map(lambda x: x.lstrip('Gender - '))
        # df['City - Name'] = df['City - Name'].str.upper()
        # df['State - Name'] = df['State - Name'].str.upper()
        df['Historical Status Name'] = df['Historical Status Name'].fillna('N/A')
        df['Submission Week Start Date'] = df['Submission Week Start Date'].fillna(pd.to_datetime("01/01/1900").strftime("%m/%d/%Y"))
        df.fillna('', inplace=True)

        pk_cols = ['Req. Creation Date', 'Req. Identifier', 'Race', 'Gender', 'Historical Step Name', 'Current Status', 'Historical Status Name', 'Submission Week Start Date']
        duplicateRows = df[df.duplicated( pk_cols, keep='last')]
        if len(duplicateRows)>=1:
            df.drop_duplicates( subset=pk_cols, keep='last', inplace=True)

        print('CALLING ORACLE FUNC')
        insert2Oracle(conn_str, df, note)

        sendEmail(note, status='success')
    else:
        sendEmail(note, status='fail')


def crew_hire_referral_active():
    note = 'Crew Hire Referral Active'
    trunc_table(conn_str, note)
    df = pd.DataFrame()
    insert2Oracle(conn_str, df, note)
    sendEmail(note, status='success')

def crew_hire_referral(today_files):
    excel_name = 'Referral Report - Freight Conductors for Crew Hiring Dashboard'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    note = 'Crew Hire Referral'
    if excel_full_name != None:
        trunc_table(conn_str, note)
        df = read_excel(os.path.join(path, excel_full_name), header=None)
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace=True)
        df['System_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df['Referral Date'] = pd.to_datetime(df['Referral Date'])
        df['Referral Date'] = df['Referral Date'].apply(lambda x: x.strftime('%m/%d/%Y %H:%M:%S'))
        df.fillna('', inplace=True)

        pk_cols = ['System_D', 'Req. Identifier', 'Candidate Identifier']
        duplicateRows = df[df.duplicated(pk_cols, keep='last')]
        if len(duplicateRows) >= 1:
            df.drop_duplicates(subset=pk_cols, keep='last', inplace=True)

        print('CALLING ORACLE FUNC')
        insert2Oracle(conn_str, df, note)
        sendEmail(note, status='success')
    else:
        sendEmail(note, status='fail')


def main():
    today_files = []
    print('list dir in path')
    try:
        for file in os.listdir(path):
            filetime = datetime.datetime.fromtimestamp(
                os.path.getmtime(path + "/" + file))
            print(filetime)
            if filetime.date() == today:
                print('today ' + file)
                today_files.append(file)
    except:
        logging.error("Accessing folder ERROR " + path)
        sendEmail(note='Accessing folder ERROR', status='fail')

    crew_hire_diversity(today_files)
    crew_hire_referral(today_files)
    crew_hire_referral_active()
    crew_hire_candidates_processing(today_files)
    crew_hire_candidates_new_candidates(today_files)
    crew_hire_candidates_hired(today_files)
    crew_hire_fallouts(today_files)
    checkLog()

if __name__ == '__main__':
    LOG_PATH = os.getcwd() + '\\Logs'
    log_file = os.path.join(LOG_PATH, 'crew_hire_loaddata.txt')

    if os.path.exists(log_file) == False:
        os.mkdir(LOG_PATH)

    logging.basicConfig(filename=log_file, level=logging.DEBUG, filemode='a',
                        format='%(asctime)s %(message)s')

    env = 'DEV'
    if env == 'DEV':
        conn_str = 'h7853/h7853@ORACL19T:1521/EDWD'
    today = datetime.datetime.now().date()
    today1 = today.strftime('%m-%d-%Y')
    log_date = today.strftime('%Y-%m-%d')
    yest = (today - timedelta(days=1))      # ONLY USED FOR TESTING

    #path = "//devshare/DataAnalytics"
    path = "//appshare/DataAnalytics"
    fromaddr = ['Tatini_Gandham@csx.com']
    toaddr =  ['Tatini_Gandham@csx.com', 'Preethi_Venkatesan@csx.com']

    main()

