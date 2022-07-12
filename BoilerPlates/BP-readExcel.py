# Import libraries
from pandas import read_excel
import pandas as pd
import os
from datetime import datetime, timedelta
import datetime
import logging

def crew_hire_diversity(today_files):
    # print('starting crew hire diversity')
    excel_name = 'Excelname'
    sheetname = 'Sheel1'
    excel_full_name = next((s for s in today_files if excel_name in s), None)
    print("EXCEL:",excel_full_name)
    if excel_full_name != None:
        df = read_excel(os.path.join(path, excel_full_name), header=None, sheet_name=sheetname)
        # print('READ EXCEL ' + sheetname)
        print("HEAD",df.head(5))

def main():
    today_files = []
    today = datetime.datetime.now().date()
    # Run through the folder and only select the files with time as today
    try:
        for file in os.listdir(path):
            filetime = datetime.datetime.fromtimestamp(
                os.path.getmtime(path + "/" + file))
            # print(filetime)
            if filetime.date() == today: # et the files only when the date is today
                # print('today ' + file)
                today_files.append(file)
    except:
        logging.error("Accessing folder ERROR " + path)

    print("Today: ", today_files)
    crew_hire_diversity(today_files)



if __name__ == '__main__':
    # Set up variables
    path = "//source/DataAnalytics"
    # Call main function
    main()


