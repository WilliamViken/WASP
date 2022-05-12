#Author: Andreas Isaksen, andrisa@stud.ntnu.no
import pandas as pd
import sqlite3
import functools
import operator

from selection import selectVessel

def ReadDatabase(dbName):

    dbPath = './'
    con = sqlite3.connect(dbPath + dbName)
    cur = con.cursor()
    cur.execute('SELECT name from sqlite_master where type= "table"') #'SELECT name from sqlite_master where type= "table"'
    vessels = cur.fetchall()
    choice = selectVessel(vessels)
    choice = functools.reduce(operator.add, choice)



    print('\n you chosed: ' + str(choice))
    string = 'SELECT * FROM ' + choice + ' Posts ORDER BY dt ASC'
    df = pd.read_sql(string, con)
    df.head(5)
    # Changing the dtype from "object" to "datetime64"
    df['dt'] = pd.to_datetime(df['dt'])
    #cleaning and resorting data
    df = df.loc[df['lat'] < 62]
    df = df[df['sog'] < 25]
    df = df.drop_duplicates(keep='last')
    df.sort_values(by='dt', inplace=True)
    df.reset_index(drop=True, inplace=True)


    return df