# Email library
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
# cx_Oracle.init_oracle_client(lib_dir=r"C:\Oracle\instantclient_19_11")

def checkLog():
    with open(log_file) as f:
        contents = f.readlines()
    today_error = [val for idx, val in enumerate(contents) if log_date in val]
    if len(today_error) >0:
        todayErrorStr = '\n '.join(today_error)
        sendEmail(todayErrorStr, status='log' )

def trunc_table(conn_str,tablename):
    conn = cx_Oracle.connect(conn_str)
    cursor = conn.cursor()
    print('TRUNCATING TABLE ' + tablename)
    delete = f""" DELETE FROM  schema.{tablename} WHERE  report_d = TO_DATE('{today_str}','MM-DD-YYYY')  """
    print(delete)
    cursor.execute(delete)
    conn.commit()
    cursor.close()
    conn.close()

# Funtion to Email
def sendEmail(note, status):
    body = ''
    if status == 'success':
        subject = " Oracle Load Finish: " + note
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

    server = smtplib.SMTP('smtp.org.com', 25)
    server.ehlo()
    server.starttls()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Format Dataframe
def formatData(df):
    ############
    # Formatdata
    print("------------BEFORE FORMAT------------", '\n', df.head(3))
    df.rename(columns=df.iloc[0], inplace=True)  # use first cell to replace header
    df.drop(df.index[0], inplace=True)  # drop the first cell
    df.columns = df.columns.fillna('to_drop')

    # drop empty columns
    try:
        df.columns = df.columns.fillna('to_drop')
        df.drop('to_drop', axis=1, inplace=True)
    except:
        pass

    # remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # Cast to date
    datecols = [s for s in list(df.columns.str.upper()) if "Date" in s]
    for i in datecols:
        print("------------DATE FORMAT------------", '\n', i)
        df[i] = pd.to_datetime(df[i], errors='coerce').dt.strftime('%m/%d/%Y %H:%M:%S')
        print('done')


    # Remove Ascii characters
    for i in df.columns:
        if 'Date' not in i:
            try:
                df[i] = df[i].str.encode('ascii', 'ignore').str.decode('ascii')
            except:
                print('EXCEPT ' + i)
                pass

        # trim column header spaces
    df = df.rename(columns=lambda x: x.strip().upper())

    return df


def data_Processing(today_Devfiles):
    excel_name="Processing.xlsx"
    note = 'Processing'
    source = 'OneSource'
    excel_full_name = next((s for s in today_Devfiles if excel_name in s), None)
    print("------------EXCEL FILES------------",'\n',excel_full_name)
    sheetname = 'Sheet1'
    if excel_full_name != None:
        df = read_excel(os.path.join(sterlingDevPath,excel_full_name),header=None,sheet_name=sheetname)

        # Drop ROWS :Filenames within cells
        if df[0][0] == "Processing Report":
            df.drop(df.index[0], inplace=True)
            # print("------------DF DA READ EXCEL------------", '\n', df.head(3))

        # call formatfunction to clean data
        formatData(df)
        #uppper case column names as call from function is not working
        df = df.rename(columns=lambda x: x.upper())

        # ADD COLUMNS
        df['REPORT_D'] = pd.to_datetime(today).strftime("%m/%d/%Y")
        df['SOURCE_N'] = source

        # Case Fix
        df['CITY'] = df['CITY'].str.upper()


        #Fill NAN
        df.fillna('', inplace=True) #Employee #

        #Check Primary key constraint
        pk_cols = ['REPORT_D', 'SOURCE_N']
        duplicateRows = df[df.duplicated(pk_cols, keep='last')]
        print("------------DUPLICATE ROWS------------",'\n',duplicateRows)
        if len(duplicateRows) >= 1:
            df.drop_duplicates(subset=pk_cols, keep='last', inplace=True)


        # Field mapping :  Excel to Oracle table
        colsDict = {'REPORT_D': 'REPORT_D',
                    'SOURCE_N': 'SOURCE_N',
                    'field1': 'field_1'

                    }



        # Map excel and oracle column names
        excelColsList = list(iter(colsDict))
        excelColNames = ', '.join([str(elem) for elem in excelColsList]) #create comma separated list of excel col names
        df_final = df[excelColsList]
        dataList = df_final.values.tolist()
        # print("------------datalist------------", '\n',dataList[0:3])

        #oracle column names
        colsDict_values = list(colsDict.values())
        oracleColNames = ', '.join([str(elem) for elem in colsDict_values])

        # print("------------EXCEL COL NAMES-----------", '\n',excelColNames)
        # print("------------ORALE COL NAMES-----------", '\n', oracleColNames)

        ###########
        # Step#2: Insert into oracle tables(Setup structure)
        # conn = cx_Oracle.connect('h7853/H7853@ORACL29T:1521/EDWD')
        conn = cx_Oracle.connect(conn_str)
        cursor = conn.cursor()

        #DELETE that day before inserting
        trunc_table(conn_str,'TABLE_NAME')


        #                     VALUES ( to_date(:0,  'MM/DD/YY' )  ,:1,  :2, :3,:4,:5,:6, :7, :8, :9, :10, :11, :12, :13, :14, :15, to_date(:16,  'MM/DD/YY' ),
        #                     :17,:18,:19, :20, :21)"""

        insert = f"""INSERT INTO schema.TABLE_NAME ({oracleColNames}) 
                                  VALUES ( to_date(:0,  'MM/DD/YY' )  ,:1, :2, :3,:4,:5,:6, :7, :8, :9, :10, :11, :12, :13, :14, :15, to_date(:16,  'MM/DD/YY' ), :17,:18,:19, :20, :21,:22, 
                                  to_date(:23,  'MM/DD/YY' ) )"""

        print("------------LOADING  TABLE------------", '\n')
        for index, elem in enumerate(dataList):
            # print(index, elem)
            try:
                cursor.execute(insert, {'0': dataList[index][0],
                                    '1': dataList[index][1],
                                    '2': dataList[index][2],
                                    '3': dataList[index][3],
                                    '4': dataList[index][4],
                                    '5': dataList[index][5],
                                    '6': dataList[index][6],
                                    '7': dataList[index][7],
                                    '8': dataList[index][8],
                                    '9': dataList[index][9],
                                    '10': dataList[index][10],
                                    '11': dataList[index][11],
                                    '12': dataList[index][12],
                                    '13': dataList[index][13],
                                    '14': dataList[index][14],
                                    '15': dataList[index][15],
                                    '16': dataList[index][16],
                                    '17': dataList[index][17],
                                    '18': dataList[index][18],
                                    '19': dataList[index][19],
                                    '20': dataList[index][20],
                                    '21': dataList[index][21],
                                    '22': dataList[index][22],
                                    '23': dataList[index][23]
                                    })
            except:
                logging.error(f"""failed  index - {index}, elem - {elem} """)
            conn.commit()

        # Close connection
        cursor.close()
        conn.close()


        df.to_excel(
            "//../Output/ProcessingOut.xlsx",
            engine='xlsxwriter')
        print("------------OUTPUT TO EXCEL: SUCCESS------------", '\n')

        # set option to show all columns and display
        pd.set_option('display.max_columns', None)
        # print("------------AFTER  FORMAT------------", '\n', df.head(3))


    # Alert when file is not updated
    else:
        sendEmail(note, status='fail')

def main():
    # print("path",sterlingPath)
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
    checkLog()

if __name__=='__main__':
    # set variables
    env='DEV'
    sterlingDevPath = "//devsource/DataAnalytics"
    sterlingProdPath = "//prodsource/DataAnalytics"

    if env=='DEV':
        sterlingPath = "//devsource/DataAnalytics"
    elif env=='PROD':
        sterlingPath = "//prodsource/DataAnalytics"

    # setting logging path
    LOG_PATH = os.getcwd() + '\\Logs'
    log_file = os.path.join(LOG_PATH, 'loaddata.txt')
    logging.basicConfig(filename=log_file, level=logging.DEBUG, filemode='a',
                        format='%(asctime)s %(message)s')


    # TodayDateSetup
    today=datetime.datetime.now().date()
    today_str =today.strftime('%m-%d-%Y')
    log_date: str = today.strftime('%Y-%m-%d')

    #Email Recipients
    fromaddr = ['Preethi_Venkatesan@email.com']
    toaddr = ['Preethi_Venkatesan@email.com']

    # oracle connection
    conn_str='user/pswd@host:1521/alias'
    main()
