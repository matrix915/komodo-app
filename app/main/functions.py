# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 16:52:57 2020

@author: Joel
"""

import pandas as pd # manipulate dataframes in python
import pymysql # SQL module
import time


def sqlConn():
    # Connect to DB
    conn = pymysql.connect(host='database-1.cqzevwjqeer7.us-east-2.rds.amazonaws.com', \
                      port=int(3306), \
                      user='demo', \
                      passwd='a6xY&7s#13X4Wq52oO', \
                      db='Komodo')
    return conn

def pymysqlQuery(sql):
    # Start timer
    #tic = time.perf_counter()
    
    # Connect to DB
    conn = sqlConn()

    #Add results to pandas dataframe
    df = pd.read_sql(sql, conn)
    
    # Close DB connection
    conn.close()
    
    # End timer and log query results
    #toc = time.perf_counter()
    
    return df

def useractionLogging (user, action, CUSIP):

    # Connect to DB
    conn = sqlConn()

    if not CUSIP:
        sql = 'INSERT INTO UserActionLog (KeyUser, UserAction) VALUES (' + str(user) + ',"' + str(action)
        sql = sql + '");'
    else:
        sql = 'INSERT INTO UserActionLog (KeyUser, UserAction, CUSIP9) VALUES (' + str(user) + ',"' + str(action)
        sql = sql + '","' + str(CUSIP) + '");'

    #cur = conn.cursor()                                     
    #cur.execute(sql)
    # Execute query
    #conn.commit()
    conn.close()

def formatDataTable(df, header, meta, cssclass):
    
    # Create table
    table = '<table id="basic-datatable" class="table dt-responsive nowrap w-100 ' + cssclass + ' ">'
    
    if not header:
        table = table + '<tbody>'
        
    else:
        # Build header
        table = table + '<thead><tr><th scope="col"></th>'#blank header of first cell
        # Loop through header array
        for h in header:
            table = table + '<th scope="col" class="text-right">' + h + '</th>'
        
        # Prepare for body
        table = table + '</tr></thead><tbody>'
   
    # Row iterator
    i = 0
    
    # Loop dataframe
    for index, row in df.iterrows():
    
        # Row header
        table = table + '<tr><td>' + str(index) + '</td>'
        
        # Loop through rows
        for r in row:
            
            # Format values
            if r is None: # Handle Null SQL values: E.g. Air Quality for 88034URU4
                r =str('NA')
            elif meta[i][1] == 'Percent':  
                r = str("{:.1%}".format(r)) # Single Decimal
            elif meta[i][1] == 'Index':
                r = str("{:.1f}".format(r)) # Single Decimal
            elif meta[i][1] == 'Spacer':
                r = str(r) + '&nbsp;' # Add space
            elif meta[i][1] == 'Integer':
                r= str("{:.0f}".format(r)) # Zero Decimal
            elif meta[i][1] == 'Dollar':
                r= '$' + str("{:,}".format(r)) # Zero Decimal
            else:
                r=str(r) #Convert to string
        
            # Create cell                
            table = table + '<td class="text-right">' + r + '</td>'
        
        # Iterate
        table = table + '</tr>'
        i = i+1
    
    # Complete table
    table = table + '</tbody></table>'
    
    return table

def defineColors():
    
    colors = {
        'primary': [
            '#2c97f0',#komodo blue
            #'#e64a19',#komodo red
            '#f07643',#orange
            '#fbc02d',#komodo yellow
            '#00bfa5',#komodo green
            '#990099',#indigo
            '#3B3EAC',#blue
            '#0099C6'
            ],
        'google': ['#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC'],
        'benchmark': [
            '#FBD678',# yellow
            '#3DCAB7'# green
            #'#FFC000','#FF6220' # Orange and not green
            ]
        }
    
    return colors

def userPortfolio():
    
    # Manually set KeyMuniPortfolio
    # 1 = Wells Fargo
    # 2 = Federated
    KeyMuniPortfolio = 2
    
    # Get Details
    sql0 = 'SELECT MuniPortfolioName, KeyMuniPortfolio FROM Komodo.MuniPortfolio mp WHERE mp.KeyMuniPortfolio = ' +str(KeyMuniPortfolio) + ' LIMIT 1;'
    portfolio_details = pymysqlQuery(sql0)
    
    return portfolio_details