# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 19:32:06 2020

@author: Joel
"""

# Flask Modules
from flask import render_template
from app.decorators import requires_auth

# Misc Modules
import pandas as pd # manipulate dataframes in python
#import pymysql # SQL module
#import time

# Application Modules
from app.main import bp # import blueprint

# Import helper funcitons
from app.main.functions import pymysqlQuery, useractionLogging, formatDataTable, defineColors, userPortfolio


#@app.route('/')
#@app.route('/index')
@bp.route('/')
@bp.route('/index')
@requires_auth
def index():
    
    # Color object
    colors = defineColors()

    # Portfolio Object
    portfolio_details = userPortfolio()

    # Log User Action
    useractionLogging(1, 'Index Page', '') # (user, action, CUSIP)

    # Portfolio Statistics data
    sql = '''
		SELECT
        	mp.MuniPortfolioName 
            ,e.`Year`
        	,CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	,CAST(AVG(e.CommunityScore) AS DECIMAL(3,1)) AS 'CommunityScore'
        	,CAST(AVG(e.HealthScore) AS DECIMAL(3,1)) AS 'HealthScore'
        	,CAST(AVG(e.WealthScore) AS DECIMAL(3,1)) AS 'WealthScore'
        	,CAST(AVG(e.EnvironmentScore) AS DECIMAL(3,1)) AS 'EnvironmentScore'
        	,CAST(AVG(e.GovernanceScore) AS DECIMAL(3,1)) AS 'GovernanceScore'
        FROM Komodo.ESGScores e 
        INNER JOIN Komodo.GeoEntity ge on ge.GeoID = e.GeoID
        INNER JOIN Komodo.MuniEntity me ON me.KeyGeoEntity = ge.KeyGeoEntity 
        INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.KeyMuniEntityObligor = me.KeyMuniEntity 
        INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.CUSIP9 = mpc.CUSIP9 
        INNER JOIN Komodo.MuniPortfolio mp ON mph.KeyMuniPortfolio = mp.KeyMuniPortfolio
        WHERE mph.KeyMuniPortfolio = ''' + str(portfolio_details['KeyMuniPortfolio'][0]) +''' AND e.`Year` IN (2015, 2016, 2017, 2018)
        GROUP BY e.`Year`
        ORDER BY e.`Year` DESC
    '''
    portfolio_df = pymysqlQuery(sql)
    
        
    sql = '''
        SELECT
        	'S&P Muni Bond' AS 'MuniPortfolioName'
            ,e.`Year`
        	,CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	,CAST(AVG(e.CommunityScore) AS DECIMAL(3,1)) AS 'CommunityScore'
        	,CAST(AVG(e.HealthScore) AS DECIMAL(3,1)) AS 'HealthScore'
        	,CAST(AVG(e.WealthScore) AS DECIMAL(3,1)) AS 'WealthScore'
        	,CAST(AVG(e.EnvironmentScore) AS DECIMAL(3,1)) AS 'EnvironmentScore'
        	,CAST(AVG(e.GovernanceScore) AS DECIMAL(3,1)) AS 'GovernanceScore'
        FROM Komodo.ESGScores e 
        INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
        WHERE ge.SummaryLevel = '050' AND e.`Year` IN (2015, 2016, 2017, 2018)
        GROUP BY e.`Year`
        ORDER BY e.`Year` DESC
     '''
    bench1_df = pymysqlQuery(sql)
           
    sql = '''            
        SELECT
        	'S&P Muni Green Bond' AS 'MuniPortfolioName'
            ,e.`Year`
        	,CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	,CAST(AVG(e.CommunityScore) AS DECIMAL(3,1)) AS 'CommunityScore'
        	,CAST(AVG(e.HealthScore) AS DECIMAL(3,1)) AS 'HealthScore'
        	,CAST(AVG(e.WealthScore) AS DECIMAL(3,1)) AS 'WealthScore'
        	,CAST(AVG(e.EnvironmentScore) AS DECIMAL(3,1)) AS 'EnvironmentScore'
        	,CAST(AVG(e.GovernanceScore) AS DECIMAL(3,1)) AS 'GovernanceScore'
        FROM Komodo.ESGScores e 
        INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID
        WHERE ge.StateCode = '51' AND e.`Year` IN (2015, 2016, 2017, 2018)
        GROUP BY e.`Year`
        ORDER BY e.`Year` DESC
    '''
    bench2_df = pymysqlQuery(sql)

    esgScoreChart = {
        #'labels': [portfolio_df['MuniPortfolioName'][0],bench1_df['MuniPortfolioName'][0]],bench2_df['MuniPortfolioName'][0],
        'datasets': [{
            'label': portfolio_df['MuniPortfolioName'][0],
            'data': [portfolio_df['ESGScore'][0]],
            'borderColor': colors['primary'][0],
            'backgroundColor': colors['primary'][0],
            'borderWidth': 1

            },{
            'label': bench1_df['MuniPortfolioName'][0],
            'data': [bench1_df['ESGScore'][0]],
            'borderColor': colors['primary'][1],
            'backgroundColor': colors['primary'][1],
            'borderWidth': 1
            },{
            'label': bench2_df['MuniPortfolioName'][0],
            'data': [bench2_df['ESGScore'][0]],
            'borderColor': colors['primary'][2],
            'backgroundColor': colors['primary'][2],
            'borderWidth': 1
            }]
    }
    
    # Data for the Detailed bar chart
    esgScoreDetailedChart = {
        'labels': ['Wealth', 'Health', 'Community', 'Environmental', 'Governance'],
        'datasets': [{
            'label': portfolio_df['MuniPortfolioName'][0],
            'data': [
                portfolio_df['WealthScore'][0],
                portfolio_df['HealthScore'][0],
                portfolio_df['CommunityScore'][0],
                portfolio_df['EnvironmentScore'][0],
                portfolio_df['GovernanceScore'][0]
                ],
            'borderColor': colors['primary'][1],
            'backgroundColor': colors['primary'][1],
            'borderWidth': 1

            },{
            'label': bench1_df['MuniPortfolioName'][0],
            'data': [
                bench1_df['WealthScore'][0],
                bench1_df['HealthScore'][0],
                bench1_df['CommunityScore'][0],
                bench1_df['EnvironmentScore'][0],
                bench1_df['GovernanceScore'][0]
                ],
            'borderColor': colors['primary'][2],
            'backgroundColor': colors['primary'][2],
            'borderWidth': 1
            },{
            'label': bench2_df['MuniPortfolioName'][0],
            'data': [
                bench2_df['WealthScore'][0],
                bench2_df['HealthScore'][0],
                bench2_df['CommunityScore'][0],
                bench2_df['EnvironmentScore'][0],
                bench2_df['GovernanceScore'][0]
                ],
            'borderColor': colors['primary'][3],
            'backgroundColor': colors['primary'][3],
            'borderWidth': 1
            }]
    }

    # Data for the Detailed bar chart - alternative ordering
    esgScoreDetailedChart2 = {
        'labels': [portfolio_df['MuniPortfolioName'][0],bench1_df['MuniPortfolioName'][0],bench2_df['MuniPortfolioName'][0]],
        'datasets': [{
            'label': 'Wealth',
            'data': [
                portfolio_df['WealthScore'][0],
                bench1_df['WealthScore'][0],
                bench2_df['WealthScore'][0],
                ],
            'borderColor': colors['primary'][1],
            'backgroundColor': colors['primary'][1],
            'borderWidth': 1
            },{
            'label': 'Health',
            'data': [
                portfolio_df['HealthScore'][0],
                bench1_df['HealthScore'][0],
                bench2_df['HealthScore'][0],
                ],
            'borderColor': colors['primary'][2],
            'backgroundColor': colors['primary'][2],
            'borderWidth': 1
            },{
            'label': 'Community',
            'data': [
                portfolio_df['HealthScore'][0],
                bench1_df['HealthScore'][0],
                bench2_df['HealthScore'][0],
                ],
            'borderColor': colors['primary'][3],
            'backgroundColor': colors['primary'][3],
            'borderWidth': 1
            },{
            'label': 'Environment',
            'data': [
                portfolio_df['EnvironmentScore'][0],
                bench1_df['EnvironmentScore'][0],
                bench2_df['EnvironmentScore'][0],
                ],
            'borderColor': colors['primary'][4],
            'backgroundColor': colors['primary'][4],
            'borderWidth': 1
            },{
            'label': 'Governance',
            'data': [
                portfolio_df['GovernanceScore'][0],
                bench1_df['GovernanceScore'][0],
                bench2_df['GovernanceScore'][0],
                ],
            'borderColor': colors['primary'][5],
            'backgroundColor': colors['primary'][5],
            'borderWidth': 1
            }]
    }
    

    # Radar chart data
    esgScoreDetailedChartRadar = {
        'labels': ['Wealth', 'Health', 'Community', 'Environmental', 'Governance'],
        'datasets': [{
            'label': portfolio_df['MuniPortfolioName'][0],
            'data': [portfolio_df['WealthScore'][0],portfolio_df['HealthScore'][0],portfolio_df['CommunityScore'][0],portfolio_df['EnvironmentScore'][0],portfolio_df['GovernanceScore'][0]],
            'borderColor': colors['primary'][0],
            'pointBackgroundColor': colors['primary'][0],
            'pointBorderColor': colors['primary'][0],
            'backgroundColor': 	colors['primary'][0],#https://www.w3schools.com/colors/colors_converter.asp
            'fill': False
        }, {
            'label': bench1_df['MuniPortfolioName'][0],
            'data': [bench1_df['WealthScore'][0],bench1_df['HealthScore'][0],bench1_df['CommunityScore'][0],bench1_df['EnvironmentScore'][0],bench1_df['GovernanceScore'][0]],
            'borderColor': colors['benchmark'][0],
            'pointBackgroundColor': colors['benchmark'][0],
            'pointBorderColor': colors['benchmark'][0],
            'backgroundColor': colors['benchmark'][0],
            'fill': False
        },{
            'label': bench2_df['MuniPortfolioName'][0],
            'data': [bench2_df['WealthScore'][0],bench2_df['HealthScore'][0],bench2_df['CommunityScore'][0],bench2_df['EnvironmentScore'][0],bench2_df['GovernanceScore'][0]],
            'borderColor': colors['benchmark'][1],
            'pointBackgroundColor': colors['benchmark'][1],
            'pointBorderColor': colors['benchmark'][1],
            'backgroundColor': colors['benchmark'][1],
            'fill': False
        }]
     }
            
    esgTrendChart = {
        'labels': ['2015', '2016', '2017', '2018'],
        'datasets': [{
            'label': portfolio_df['MuniPortfolioName'][0],
            'data': portfolio_df.sort_values(by='Year', ascending=True)['ESGScore'].tolist(),
            'borderColor': colors['primary'][0],
            'backgroundColor': colors['primary'][0],
            'pointBackgroundColor': colors['primary'][0],
            'borderWidth': 4,
            'fill': False
            },{
            'label': bench1_df['MuniPortfolioName'][0],
            'data': bench1_df.sort_values(by='Year', ascending=True)['ESGScore'].tolist(),
            'borderColor': colors['benchmark'][0],
            'backgroundColor': colors['benchmark'][0],
            'pointBackgroundColor': colors['benchmark'][0],
            'borderWidth': 4,
            'fill': False
            },{
            'label': bench2_df['MuniPortfolioName'][0],
            'data': bench2_df.sort_values(by='Year', ascending=True)['ESGScore'].tolist(),
            'borderColor': colors['benchmark'][1],
            'backgroundColor': colors['benchmark'][1],
            'pointBackgroundColor': colors['benchmark'][1],
            'borderWidth': 4,
            'fill': False
            }]
        }
                
    # Asset allocation chart
    assetAllocationChart = {
        #'labels': ['General Obligation','Education','Health','Housing','Utilities','Water & Sewer'],
        'labels': [portfolio_df['MuniPortfolioName'][0],bench1_df['MuniPortfolioName'][0],bench2_df['MuniPortfolioName'][0]],
        'datasets': [{
            'label': portfolio_df['MuniPortfolioName'][0],
            'data': [40,12,8,20,10,10],
            'backgroundColor': colors['primary'][0]
            },{
            'label': bench1_df['MuniPortfolioName'][0],
            'data': [35,14,12,10,15,14],
            'backgroundColor': colors['benchmark'][0]
            },{
            'label': bench2_df['MuniPortfolioName'][0],
            'data': [42,8,15,15,8,12],
            'backgroundColor': colors['benchmark'][1]
            }]
        
        }                

    # Asset allocation chart
    assetAllocationChart2 = {
        #'labels': ['General Obligation','Education','Health','Housing','Utilities','Water & Sewer'],
        'labels': [portfolio_df['MuniPortfolioName'][0],bench1_df['MuniPortfolioName'][0],bench2_df['MuniPortfolioName'][0]],
        'datasets': [{
            'label': 'General Obligation',
            'data': [40,35,42],
            'backgroundColor': colors['primary'][1]
            },{
            'label': 'Education',
            'data': [12,14,8],
            'backgroundColor': colors['primary'][2]
            },{
            'label': 'Health',
            'data': [8,12,15],
            'backgroundColor': colors['primary'][3]
            },{
            'label': 'Housing',
            'data': [20,10,15],
            'backgroundColor': colors['primary'][4]
            },{
            'label': 'Utilities',
            'data': [10,15,8],
            'backgroundColor': colors['primary'][5]
            },{
            'label': 'Water & Sewer',
            'data': [10,14,12],
            'backgroundColor': colors['primary'][6]
            }]
        
        }      
    # Break down specific sectors
    sql = '''
        SELECT 
        	Supersector AS 'Sector'
        	,CAST((RAND() * 20) + 40 AS DECIMAL(3,1)) AS `''' + portfolio_details['MuniPortfolioName'][0] + '''`
        	,CAST((RAND() * 20) + 40 AS DECIMAL(3,1)) AS 'S&P Muni'
        	,CAST((RAND() * 20) + 40 AS DECIMAL(3,1)) AS 'S&P Green'
        FROM Lookup.MorningstarSuperSectors mss 
        WHERE KeyMorningstarSuperSector IN (1,5,6,7,10,11)
        
        UNION
        
        SELECT 
        	'Total' AS 'Sector'
        	,(
        	SELECT CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	FROM Komodo.ESGScores e
        	INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
        	INNER JOIN Komodo.MuniEntity me ON me.KeyGeoEntity = ge.KeyGeoEntity 
        	INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.KeyMuniEntityObligor = me.KeyMuniEntity 
        	INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.CUSIP9 = mpc.CUSIP9 
        	INNER JOIN Komodo.MuniPortfolio mp ON mph.KeyMuniPortfolio = mp.KeyMuniPortfolio 
        	WHERE mph.KeyMuniPortfolio = 2 AND e.`Year` = 2018
        	) AS 'Portfolio'
        	,(SELECT CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	FROM Komodo.ESGScores e 
        	INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
        	WHERE e.`Year` = 2018 AND ge.SummaryLevel = '050'
        	) AS 'S&P Muni'
        	,(SELECT CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	FROM Komodo.ESGScores e 
        	INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID
        	WHERE e.`Year` = 2018 AND ge.StateCode = '51'
        	) AS 'S&P Green'
    '''
    sector_df = pymysqlQuery(sql)

    # Break down specific ratings
    sql = '''
        SELECT 
        	a.Rating
        	,CAST((RAND() * 20) + 40 AS DECIMAL(3,1)) AS `''' + portfolio_details['MuniPortfolioName'][0] + '''`
        	,CAST((RAND() * 20) + 40 AS DECIMAL(3,1)) AS 'S&P Muni'
        	,CAST((RAND() * 20) + 40 AS DECIMAL(3,1)) AS 'S&P Green'
        FROM (
        	SELECT 'AAA' AS 'Rating'
        	UNION SELECT 'AA'
        	UNION SELECT 'A'
        	UNION SELECT 'BBB'
        	UNION SELECT 'Non-IG'
        ) a
        
        UNION
        
        SELECT 
        	'Total' AS 'Sector'
        	,(
        	SELECT CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	FROM Komodo.ESGScores e 
        	INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
        	INNER JOIN Komodo.MuniEntity me ON me.KeyGeoEntity = ge.KeyGeoEntity 
        	INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.KeyMuniEntityObligor = me.KeyMuniEntity  
        	INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.CUSIP9 = mpc.CUSIP9 
        	INNER JOIN Komodo.MuniPortfolio mp ON mph.KeyMuniPortfolio = mp.KeyMuniPortfolio 
        	WHERE mph.KeyMuniPortfolio = 2 AND e.`Year` = 2018
        	) AS 'Portfolio'
        	,(SELECT CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	FROM Komodo.ESGScores e 
        	INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
        	WHERE e.`Year` = 2018 AND ge.SummaryLevel = '050'
        	) AS 'S&P Muni'
        	,(SELECT CAST(AVG(e.ESGScore) AS DECIMAL(3,1)) AS 'ESGScore'
        	FROM Komodo.ESGScores e 
        	INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID
        	WHERE e.`Year` = 2018 AND ge.StateCode = '51'
        	) AS 'S&P Green'
    '''
    rating_df = pymysqlQuery(sql)
    
    #meta = []
    #for s in sector_df['Sector']:    
    #    meta = meta + [[s, 'Index']]
    #sector_df = sector_df[['Portfolio','S&P Muni','S&P Green']]
    #header = sector_df.columns.tolist()
    #sector_table = formatDataTable(sector_df, header, meta, 'table-striped')
    
    return render_template('index.html'
                           ,portfolio_details=portfolio_details
                           ,esgScoreDetailedChart=esgScoreDetailedChart
                           ,esgScoreChart=esgScoreChart
                           ,esgScoreDetailedChart2=esgScoreDetailedChart2
                           ,esgScoreDetailedChartRadar=esgScoreDetailedChartRadar
                           ,esgTrendChart=esgTrendChart
                           ,assetAllocationChart=assetAllocationChart
                           ,assetAllocationChart2=assetAllocationChart2
                           ,sector_df=sector_df
                           ,rating_df=rating_df
                           ,colors=colors
                           )

@bp.route('/portfoliodetails')
def portfoliodetails():

    # Portfolio Object
    portfolio_details = userPortfolio()
    
    # Log User Action
    useractionLogging(1, 'Index Page', '') # (user, action, CUSIP)
    
    # Portfolio data
    sql = '''
     SELECT DISTINCT 
     	mph.CUSIP9 AS 'CUSIP'
     	,ge.GeographyName AS 'Matched Issuer'
     	,'Local GO' AS 'Sector'
        ,60 AS 'Use Of Proceeds'
        ,we2.ESGScore AS 'ESG Score'
        ,ROUND(PERCENT_RANK() OVER (ORDER BY we2.ESGScore) * 100, 0) AS 'ESG Rank'
        ,ROUND(we2.ESGScore - we3.ESGScore,1) AS 'Score Improvement'
        ,ROUND(PERCENT_RANK() OVER (ORDER BY we3.ESGScore) * 100, 0) AS 'Prior ESG Rank'
     FROM Komodo.MuniPortfolio mp 
     INNER JOIN Komodo.MuniPortfolioHolding mph ON mp.KeyMuniPortfolio = mph.KeyMuniPortfolio 
     INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.CUSIP9 = mph.CUSIP9  
	 INNER JOIN Komodo.MuniEntity me ON me.KeyMuniEntity = mpc.KeyMuniEntityObligor    	
     INNER JOIN Komodo.GeoEntity ge ON ge.KeyGeoEntity = me.KeyGeoEntity
     INNER JOIN Komodo.ESGScores we2 ON ge.GeoID =we2.GeoID 
     LEFT JOIN Komodo.ESGScores we3 ON we3.GeoID =we2.GeoID AND we3.Year = (we2.Year-1)
     WHERE we2.`Year` = 2018
    	 AND mp.KeyMuniPortfolio = ''' + str(portfolio_details['KeyMuniPortfolio'][0]) + ' ORDER BY we2.ESGScore DESC'
    portfolio_df = pymysqlQuery(sql)
    #portfolio_df = (portfolio_df.transpose()).drop('Year') # pivot and drop year column   
    return render_template('portfoliodetails.html'
                           ,portfolio_df=portfolio_df
                           ,portfolio_details=portfolio_details
                           )
    
#@app.route('/issuer/<slug>')
@bp.route('/issuer/<slug>')
def issuer(slug):

    # Color object
    colors = defineColors()
    
    # Portfolio Object
    portfolio_details = userPortfolio()
    
    # Set GeoID
    if slug is None:
        #GeoID = '0500000US40047'
        CUSIP = '30382ADL3'
    else:
        CUSIP = slug
    
    # Log User Action
    useractionLogging(1, 'Index Page', CUSIP) # (user, action, CUSIP)
    
    # Get Bond Details
    sql = '''
    SELECT 
        ge.GeoID
        ,meo.EntityName AS 'ObligorName'
        ,mei.EntityName AS 'IssuerName'
        ,ge.GeographyName AS 'ObligorGeoName'
    FROM Komodo.MuniCUSIPMatch mpc
    INNER JOIN Komodo.MuniEntity meo ON  meo.KeyMuniEntity = mpc.KeyMuniEntityObligor 
    INNER JOIN Komodo.MuniEntity mei ON mei.KeyMuniEntity = mpc.KeyMuniEntityIssuer 
	INNER JOIN Komodo.GeoEntity ge ON ge.KeyGeoEntity = meo.KeyGeoEntity 
    WHERE mpc.CUSIP9="''' + CUSIP +'" LIMIT 1;'

    geoDetails_df = pymysqlQuery(sql)
    GeoID = geoDetails_df['GeoID'][0]
    
    # Get Scores and Rankings
    sql1 = '''
    SELECT DISTINCT
    	e1.GeoID
    	,e1.GeographyName
    	,e1.`Year`
    	,ROUND(e1.WealthScore,0) AS 'WealthScore'
    	,ROUND(e1.EnvironmentScore,0) AS 'EnvironmentScore'
    	,ROUND(e1.HealthScore,0) AS 'HealthScore'
    	,ROUND(e1.CommunityScore,0) AS 'CommunityScore'
    	,ROUND(e1.GovernanceScore,0) AS 'GovernanceScore'
    	,ROUND(e1.UseOfProceedsScore,0) AS 'UseOfProceedsScore'
    	,ROUND(e1.ESGScore,0) AS 'ESGScore'
    	,sl.Description AS 'GeoLevel'
        ,ROUND(e1.NationalRank,0) AS 'NationalRank'
        ,ROUND(e1.NationalGeoCount,0) AS 'NationalGeoCount'
        ,ROUND(e1.NationalPerc,0) AS 'NationalPerc'
        ,ROUND(e1.RegionalRank,0) AS 'RegionalRank'
        ,ROUND(e1.RegionalGeoCount,0) AS 'RegionalGeoCount'
        ,ROUND(e1.RegionalPerc,0) AS 'RegionalPerc'
        ,ROUND(e1.StateRank,0) AS 'StateRank'
        ,ROUND(e1.StateGeoCount,0) AS 'StateGeoCount'
        ,ROUND(e1.StatePerc,0) AS 'StatePerc'
        ,ROUND(e1.ESGScore - e2.ESGScore,0) AS 'ScoreImprovement'
    FROM Komodo.ESGScores e1
    INNER JOIN Lookup.CensusSummaryLevel sl ON sl.SummaryLevel = e1.SummaryLevel
    INNER JOIN Komodo.ESGScores e2 ON e1.GeoID = e2.GeoID AND e2.Year = '2017'
    WHERE e1.YEAR=2018 AND e1.GeoID= "''' + str(GeoID) + '" LIMIT 1;'

    esgScores_df = pymysqlQuery(sql1)

    # Get Bond Details
    sql2 = '''
    SELECT DISTINCT 
        meo.EntityName AS 'Issuer'
        ,mei.EntityName AS 'Obligor'
        ,mph.CUSIP9 AS 'CUSIP'
        ,mph.ClientTitle AS 'Title'
        ,'General Obligation**' AS 'BondType'
        ,'New Money**' AS 'IssueType'
        ,'Public Improvement**' AS 'UseOfProceeds'
        , 'Local GO' AS 'Sector' 
    FROM Komodo.MuniPortfolioHolding mph 
    INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.CUSIP9 = mph.CUSIP9
    INNER JOIN Komodo.MuniEntity meo ON meo.KeyMuniEntity = mpc.KeyMuniEntityObligor 
    INNER JOIN Komodo.MuniEntity mei ON mei.KeyMuniEntity = mpc.KeyMuniEntityIssuer 
    WHERE mph.CUSIP9 = "''' + CUSIP + '" LIMIT 1;'
    issue_df = pymysqlQuery(sql2)
    
    # Get Issuer Details
    sql3 = '''
    SELECT 
        ge.GeographyName
        ,csl.Description 
        , '99%**' AS 'UrbanArea'
        , cay.Population
        , ROUND(cayc.UnemploymentRate*100,1) AS 'UnemploymentRate'
        , cay.MedianHouseholdIncome
        , ROUND(cayc.PovertyRate*100,1) AS 'PovertyRate' 
    FROM Komodo.GeoEntity ge 
    INNER JOIN Lookup.CensusSummaryLevel csl ON csl.SummaryLevel = ge.SummaryLevel 
    INNER JOIN DataSource.CensusACS5Year cay ON ge.GeoID =cay.GeoID AND cay.`Year` = 2018
    INNER JOIN DataSource.CensusACS5YearCalc cayc ON ge.GeoID = cayc.GeoID AND cayc.Year=cay.`Year` 
    WHERE ge.GeoID = "''' + GeoID + '";'
    issuer_df = pymysqlQuery(sql3)   

    # Get ESG Chart data
    sql4 = 'SELECT we.YEAR, we.ESGScore FROM Komodo.ESGScores we WHERE we.GeoID =  "' + GeoID + '" AND Year IN (''2015'', ''2016'', ''2017'', ''2018'') ORDER BY `Year` ASC'
    sql5 = 'SELECT we.YEAR, we.ESGScore FROM Komodo.ESGScores we WHERE we.GeoID =  "0100000US" AND Year IN (''2015'', ''2016'', ''2017'', ''2018'') ORDER BY `Year` ASC'
    issuer_trend = pymysqlQuery(sql4) 
    issuer_trend = (issuer_trend.transpose()).drop('YEAR') # pivot and drop year column
    national_trend = pymysqlQuery(sql5)  
    national_trend = (national_trend.transpose()).drop('YEAR') # pivot and drop year column
    # colors = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']
    
    esgChartData = {
        'labels': ['2015','2016','2017','2018'],
        'datasets': [{
            'label': geoDetails_df['ObligorName'][0],
            'data': issuer_trend.astype(float).round(1).values.tolist()[0],
            'borderColor': colors['primary'][0],
            'backgroundColor': colors['primary'][0],
            'pointBackgroundColor': colors['primary'][0],
            'borderWidth': 4,
            'fill': False
            },{
            'label': 'National Average',
            'data': national_trend.astype(float).round(1).values.tolist()[0],
            'borderColor': colors['benchmark'][0],
            'backgroundColor': colors['benchmark'][0],
            'pointBackgroundColor': colors['benchmark'][0],
            'borderWidth': 4,
            'fill': False
            }]
        
    }
                
    # Query specifically for pillars chart
    sql6 = "SELECT ROUND(EnvironmentScore,0) AS 'Environment', ROUND(CommunityScore,0) AS 'Community', ROUND(WealthScore,0) AS 'Wealth', ROUND(HealthScore,0) AS 'Health', ROUND(GovernanceScore,0) AS 'Governance', ROUND(UseOfProceedsScore,0) AS 'Use Of Proceeds' FROM Komodo.ESGScores WHERE YEAR=2018 AND GeoID= '" + str(GeoID) + "';"        
    pillars_df = pymysqlQuery(sql6)
    pillars_df = pillars_df.transpose()
        
    # Get Portfolio Rank
    sql7 = '''
    SELECT DISTINCT
    	d.CUSIP9
    	,d.GeoID
    	,d.PortfolioRank
    	,d.Rank2018
    	,d.Rank2017
        ,(SELECT COUNT(*) 
        FROM Komodo.MuniCUSIPMatch mpc 
    	INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.CUSIP9 = mpc.CUSIP9 
    	INNER JOIN Komodo.MuniPortfolio mp ON mp.KeyMuniPortfolio = mph.KeyMuniPortfolio 
    	WHERE mp.KeyMuniPortfolio =''' + str(portfolio_details['KeyMuniPortfolio'][0]) + ''') AS 'PortfolioCount'
    	,CAST(d.Rank2017 AS FLOAT) - CAST(d.Rank2018 AS FLOAT) AS 'RankChange'
    FROM (
    	SELECT DISTINCT
    		c.CUSIP9
    		,c.GeoID
    		,c.PortfolioRank
    		,c.Rank2018
    		,RANK() OVER(ORDER BY b.ESGScore DESC) AS 'Rank2017'
    		,b.ESGScore
    	FROM
    		(SELECT DISTINCT
    			a.CUSIP9
    			,a.GeoID
    			,PERCENT_RANK() OVER (ORDER BY a.ESGScore ASC)  AS `PortfolioRank`
    			,RANK() OVER(ORDER BY a.ESGScore DESC) AS 'Rank2018'
    		FROM  (
    			SELECT DISTINCT
    				e.GeoID
    				,mph.CUSIP9 
    				,e.ESGScore
    				,mph.KeyMuniPortfolio 
    			FROM Komodo.ESGScores e
    			INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
    			INNER JOIN Komodo.MuniEntity me ON me.KeyGeoEntity = ge.KeyGeoEntity 
    			INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.KeyMuniEntityObligor = me.KeyMuniEntity 
    			INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.CUSIP9 = mpc.CUSIP9 
    			INNER JOIN Komodo.MuniPortfolio mp ON mp.KeyMuniPortfolio = mph.KeyMuniPortfolio 
    			WHERE mp.KeyMuniPortfolio =''' + str(portfolio_details['KeyMuniPortfolio'][0]) + ''' AND e.Year = 2018
    		) a
    	) c
    	LEFT JOIN (
    		SELECT DISTINCT
    			e.GeoID
    			,mph.CUSIP9 
    			,e.ESGScore
    			,mph.KeyMuniPortfolio 
    		FROM Komodo.ESGScores e
    		INNER JOIN Komodo.GeoEntity ge ON ge.GeoID = e.GeoID 
    		INNER JOIN Komodo.MuniEntity me ON me.KeyGeoEntity = ge.KeyGeoEntity 
    		INNER JOIN Komodo.MuniCUSIPMatch mpc ON mpc.KeyMuniEntityObligor = me.KeyMuniEntity 
    		INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.CUSIP9 = mpc.CUSIP9 
    		INNER JOIN Komodo.MuniPortfolio mp ON mp.KeyMuniPortfolio = mph.KeyMuniPortfolio 
    		WHERE mp.KeyMuniPortfolio =''' + str(portfolio_details['KeyMuniPortfolio'][0]) + ''' AND e.Year = 2017
    	) b ON b.CUSIP9 = c.CUSIP9
    ) d
    WHERE d.CUSIP9 = "''' + CUSIP + '";'
    portfoliorank_df = pymysqlQuery(sql7)
    
    return render_template('issuer.html'
                           ,geoDetails_df=geoDetails_df
                           ,esgScores_df=esgScores_df
                           ,issue_df=issue_df
                           ,issuer_df=issuer_df
                           ,esgChartData=esgChartData
                           ,CUSIP=CUSIP
                           ,pillars_df=pillars_df
                           ,portfoliorank_df=portfoliorank_df
                           ,portfolio_details=portfolio_details)

#@app.route('/issuerdetails/<slug>')
@bp.route('/issuerdetails/<slug>')
def issuerdetails(slug):
    
    colors = defineColors()
    
    # Portfolio Object
    portfolio_details = userPortfolio()
    
    # Set GeoID
    if slug is None:
        #GeoID = '0500000US40047'
        CUSIP = '30382ADL3'
    else:
        CUSIP = slug
    
    # Log User Action
    useractionLogging(1, 'Index Page', CUSIP) # (user, action, CUSIP)
    
    # Get Bond Details
    sql = '''
    SELECT 
        ge.GeoID
        ,meo.EntityName AS 'ObligorName'
        ,mei.EntityName AS 'IssuerName'
    FROM Komodo.MuniCUSIPMatch mpc
    INNER JOIN Komodo.MuniEntity meo ON  meo.KeyMuniEntity = mpc.KeyMuniEntityObligor 
    INNER JOIN Komodo.MuniEntity mei ON mei.KeyMuniEntity = mpc.KeyMuniEntityIssuer 
    INNER JOIN Komodo.GeoEntity ge ON ge.KeyGeoEntity = meo.KeyGeoEntity
    WHERE mpc.CUSIP9="''' + CUSIP +'" LIMIT 1;'

    geoDetails_df = pymysqlQuery(sql)
    GeoID = geoDetails_df['GeoID'][0]
    
    # Get Environmental Score Table
    sql1 = '''
    SELECT 
    	we.`Year`
    	,we.PublicTransportationPerc AS 'Public Transporation Usage (%)'
    	,we2.PublicTransportationPerc AS 'vs. National Usage (%)'
    	,'' AS ''
    	,we.AQIAverage AS 'Air Quality Index'
    	,we2.AQIAverage AS 'vs. National Index'
    	,'' AS ''
    	,we.DroughtNonConsecutiveWeeks AS 'Weeks of Drought in Year'
    	,we2.DroughtNonConsecutiveWeeks AS 'vs. National Weeks'
    FROM Komodo.ESGScores we
    INNER JOIN Komodo.ESGScores we2 ON we2.Year=we.Year AND we2.GeoID = '0100000US'
    WHERE we.`Year`IN (2014, 2015, 2016, 2017, 2018) AND
        we.GeoID =  "''' + GeoID + '";'
        
    environment_df = pymysqlQuery(sql1)
    environment_df = (environment_df.transpose()).drop('Year') # pivot and drop year column
    meta = [
        ['Public Transporation Usage (%)','Percent'],  
        ['vs. National Usage (%)','Percent'], 
        ['','Spacer'], 
        ['Air Quality Index','Index'],
        ['vs. National Index','Index'],
        ['','Spacer'],
        ['Weeks of Drought in Year','Integer'],
        ['vs. National Weeks','Integer']
    ]
    header = ['2014','2015','2016','2017','2018']
    environment_table = formatDataTable(environment_df, header, meta, 'table-hover')
    
    # Get Community Score Table
    sql2 = '''
    SELECT 
    	we.`Year`
    	,we.HousingOccupiedOwnerPerc AS 'Housing Owner Occupied (%)'
    	,we2.HousingOccupiedOwnerPerc AS 'vs. National Owner Occupied (%)'
    	,' ' AS ' '
    	,we.EducationalAttainment AS 'Educational Attainment Index'
    	,we2.EducationalAttainment AS 'vs. National Index '
    	,'' AS ''
    	,we.CommuteTime30PlusPerc AS 'Commute Difficulty Index'
    	,we2.CommuteTime30PlusPerc AS 'vs. National Index'
    FROM Komodo.ESGScores we -- 417
    INNER JOIN Komodo.ESGScores we2 ON we2.Year=we.Year AND we2.GeoID = '0100000US'
    WHERE we.`Year`IN (2014, 2015, 2016, 2017, 2018)
    	AND we.GeoID =  "''' + GeoID + '";'
    community_df = pymysqlQuery(sql2)
    community_df = (community_df.transpose()).drop('Year') # pivot and drop year column
    meta = [
        ['Housing Owner Occupied (%)','Percent'],  
        ['vs. National Owner Occupied (%)','Percent'], 
        ['','Spacer'], 
        ['Educational Attainment Index','Index'],
        ['vs. National Index','Index'],
        ['','Spacer'],
        ['Commute Difficulty Index','Index'],
        ['vs. National Index','Index']
    ]
    header = ['2014','2015','2016','2017','2018']
    community_table = formatDataTable(community_df, header, meta, 'table-hover')

    
    # Get Wealth Score Table
    sql3 = '''
    SELECT 
    	we.`Year`
    	,we.UnemploymentRate AS 'Unemployment Rate (%)'
    	,we2.UnemploymentRate AS 'vs. National Rate (%)'
    	,'' AS ''
    	,we.HouseholdValueMedian AS 'Median Household Value ($)'
    	,we2.HouseholdValueMedian AS 'vs. National Median Value ($)'
    	,'' AS ''
    	,we.MedianHouseholdIncomeGrowth1Year AS 'Median Household Income Growth (%)'
    	,we2.MedianHouseholdIncomeGrowth1Year AS 'vs. National Growth (%)'
    FROM Komodo.ESGScores we -- 417
    INNER JOIN Komodo.ESGScores we2 ON we2.Year=we.Year AND we2.GeoID = '0100000US'
    WHERE we.`Year`IN (2014, 2015, 2016, 2017, 2018)
    	AND we.GeoID =  "''' + GeoID + '";'
    wealth_df = pymysqlQuery(sql3)
    wealth_df = (wealth_df.transpose()).drop('Year') # pivot and drop year column   
    meta = [
        ['Unemployment Rate (%)','Percent'],  
        ['vs. National Rate (%)','Percent'], 
        ['','Spacer'], 
        ['Median Household Value ($)','Dollar'],
        ['vs. National Median Value ($)','Dollar'],
        ['','Spacer'],
        ['Median Household Income Growth (%)','Percent'],
        ['vs. National Growth (%)','Percent']
    ]
    header = ['2014','2015','2016','2017','2018']
    wealth_table = formatDataTable(wealth_df, header, meta, 'table-hover')
    
    # Get Health Score Table
    sql4 = '''
    SELECT 
    	we.`Year`
    	,we.PovertyRate AS 'Poverty Rate (%)'
    	,we2.PovertyRate AS 'vs. National Rate (%)'
    	,'' AS ''
    	,we.UnemploymentEqualityIndex AS 'Unemployment Equality Index'
    	,we2.UnemploymentEqualityIndex AS 'vs. National Equality Index'
    	,'' AS ''
    	,(we.DiabetesPercentage/100) AS 'Population with Diabetes (%)'
    	,(we2.DiabetesPercentage/100) AS 'vs. National (%)'
    FROM Komodo.ESGScores we
    INNER JOIN Komodo.ESGScores we2 ON we2.Year=we.Year AND we2.GeoID = '0100000US'
    WHERE we.`Year`IN (2014, 2015, 2016, 2017, 2018)
    	AND we.GeoID =  "''' + GeoID + '";'
    health_df = pymysqlQuery(sql4)
    health_df = (health_df.transpose()).drop('Year') # pivot and drop year column
    meta = [
        ['Poverty Rate (%)','Percent'],  
        ['vs. National Rate (%)','Percent'], 
        ['','Spacer'], 
        ['Unemployment Equality Index','Index'],
        ['vs. National Equality Index','Index'],
        ['','Spacer'],
        ['Population with Diabetes (%)','Percent'],
        ['vs. National (%)','Percent']
    ]
    header = ['2014','2015','2016','2017','2018']
    health_table = formatDataTable(health_df, header, meta, 'table-hover')
    
    
    # Get Governance Score Table
    sql5 = '''
    SELECT 
    	we.`Year`
    	,EnvironmentScore AS 'Environment Score'
        ,CommunityScore AS 'Community Score'
        ,WealthScore  AS 'Wealth Score'
    	,HealthScore AS 'Health Score'
    FROM Komodo.ESGScores we
    WHERE we.`Year`IN (2014, 2015, 2016, 2017, 2018)
    	AND we.GeoID =  "''' + GeoID + '" ORDER BY `Year` ASC'
    governance_df = pymysqlQuery(sql5)
    governance_df = (governance_df.transpose()).drop('Year') # pivot and drop year column
    meta = [
        ['Environment Score','Index'],  
        ['Community Score','Index'], 
        ['Wealth Score','Index'], 
        ['Health Score','Index'],
    ]
    header = ['2014','2015','2016','2017','2018']
    governance_table = formatDataTable(governance_df, header, meta, 'table-hover')
    
    # Get Issue Details
    sql6 = '''
    SELECT 
        	mph.CUSIP9 AS 'CUSIP'
        	,mph.ClientTitle AS 'Title'
        	,'General Obligation**' AS 'BondType'
        	,'New Money**' AS 'IssueType'
        	,'Public Improvement**' AS 'UseOfProceeds'
        	, 'Local GO' AS 'Sector' 
    FROM Komodo.MuniPortfolio mp 
    INNER JOIN Komodo.MuniPortfolioHolding mph ON mph.KeyMuniPortfolio = mp.KeyMuniPortfolio 
    WHERE mph.CUSIP9 = "''' + CUSIP + '" LIMIT 1;'
    issue_df = pymysqlQuery(sql6)
    
    # Dynamic formatting test
    # Get Chart for ESG Details page
    esgDetailsTrendChart    = {
        'labels': ['2014','2015','2016','2017','2018'],
        'datasets': [{
            'label': 'Public Transporation Usage (%)',#geoDetails_df['ObligorName'][0],
            'data': environment_df[0:1].values.tolist()[0],
            'borderColor': colors['primary'][0],
            'backgroundColor': colors['primary'][0],
            'pointBackgroundColor': colors['primary'][0],
            'borderWidth': 4,
            'fill': False
            },{
            'label': 'National Average',
            'data': environment_df[1:2].values.tolist()[0],
            'borderColor': colors['benchmark'][0],
            'backgroundColor': colors['benchmark'][0],
            'pointBackgroundColor': colors['benchmark'][0],
            'borderWidth': 4,
            'fill': False
            }]
        
    }
    public_transport_df = environment_df[0:2]
    
    return render_template('issuerdetailsold.html'
                           ,geoDetails_df=geoDetails_df
                           ,public_transport_df=public_transport_df
                           ,issue_df=issue_df
                           #,esgScores_df=esgScores_df
                           #,esgChartData=esgChartData
                           ,environment_table=environment_table
                           ,community_table=community_table
                           ,wealth_table=wealth_table
                           ,health_table=health_table
                           ,governance_table=governance_table
                           ,esgDetailsTrendChart=esgDetailsTrendChart
                           ,CUSIP=CUSIP
                           ,portfolio_details=portfolio_details
                           )

@bp.route('/detailsenvironment/<slug>')
def detailsenvironment(slug):
    
    colors = defineColors()
    
    # Portfolio Object
    portfolio_details = userPortfolio()
    
    # Set GeoID
    if slug is None:
        #GeoID = '0500000US40047'
        CUSIP = '30382ADL3'
    else:
        CUSIP = slug
    
    # Log User Action
    useractionLogging(1, 'Index Page', CUSIP) # (user, action, CUSIP)
    
    # Get Bond Details
    sql = '''
    SELECT 
        	mpc.GeoID
        	,COALESCE(mpc.ObligorName, geo.GeographyName) AS 'ObligorName'
        	,COALESCE(mpc.IssuerName, gei.GeographyName) AS 'IssuerName'
    FROM Komodo.MuniPortfolioCUSIPMatch mpc
    INNER JOIN Komodo.GeoEntity geo ON geo.GeoID = mpc.GeoID 
    INNER JOIN Komodo.GeoEntity gei ON gei.GeoID = mpc.GeoID
    WHERE mpc.CUSIP9="''' + CUSIP +'" LIMIT 1;'

    geoDetails_df = pymysqlQuery(sql)
    GeoID = geoDetails_df['GeoID'][0]
    
    # Get Environmental Score Table
    sql1 = '''
    SELECT 
    	we.`Year`
    	,we.PublicTransportationPerc AS 'Public Transporation Usage (%)'
    	,we2.PublicTransportationPerc AS 'vs. National Usage (%)'
    	,'' AS ''
    	,we.AQIAverage AS 'Air Quality Index'
    	,we2.AQIAverage AS 'vs. National Index'
    	,'' AS ''
    	,we.DroughtNonConsecutiveWeeks AS 'Weeks of Drought in Year'
    	,we2.DroughtNonConsecutiveWeeks AS 'vs. National Weeks'
    FROM Komodo.ESGScores we
    INNER JOIN Komodo.ESGScores we2 ON we2.Year=we.Year AND we2.GeoID = '0100000US'
    WHERE we.`Year`IN (2014, 2015, 2016, 2017, 2018) AND
        we.GeoID =  "''' + GeoID + '";'
    environment_df = pymysqlQuery(sql1)
    environment_df = (environment_df.transpose()).drop('Year') # pivot and drop year column

    
    # Dynamic formatting test
    # Get Chart for ESG Details page
    esgDetailsTrendChart    = {
        'labels': ['2014','2015','2016','2017','2018'],
        'datasets': [{
            'label': 'Public Transporation Usage (%)',#geoDetails_df['ObligorName'][0],
            'data': environment_df[0:1].values.tolist()[0],
            'borderColor': colors['primary'][0],
            'backgroundColor': colors['primary'][0],
            'pointBackgroundColor': colors['primary'][0],
            'borderWidth': 4,
            'fill': False
            },{
            'label': 'National Average',
            'data': environment_df[1:2].values.tolist()[0],
            'borderColor': colors['benchmark'][0],
            'backgroundColor': colors['benchmark'][0],
            'pointBackgroundColor': colors['benchmark'][0],
            'borderWidth': 4,
            'fill': False
            }]
        
    }
    public_transport_df = environment_df[0:2]
    
    return render_template('detailsenvironment.html'
                           ,geoDetails_df=geoDetails_df
                           ,public_transport_df=public_transport_df
                           ,esgDetailsTrendChart=esgDetailsTrendChart
                           ,CUSIP=CUSIP
                           ,portfolio_details=portfolio_details
                           )

@bp.route('/search/<slug>')
#@app.route('/search/<slug>')
def search(slug):
    
    sql = '''
    SELECT DISTINCT
    	LEFT(mpc.CUSIP9,6) AS 'CUSIP'
    	,ge.GeographyName AS 'Matched Issuer'
		,ge2.GeographyName AS 'State'
    FROM MuniPortfolioCUSIPMatch mpc 
    LEFT JOIN Komodo.GeoEntity ge ON mpc.GeoID = ge.GeoID 
    LEFT JOIN Komodo.GeoEntity ge2 ON ge2.StateCode = ge.StateCode AND ge2.SummaryLevel ='040'
    WHERE ge.GeographyName LIKE  "''' + slug + '''%"
    
    UNION 
    
    SELECT DISTINCT
    	LEFT(mpc.CUSIP9,6) AS 'CUSIP'
    	,ge.GeographyName AS 'Matched Issuer'
		,ge2.GeographyName 
    FROM Komodo.MuniPortfolioCUSIPMatch mpc 
    LEFT JOIN Komodo.GeoEntity ge ON mpc.GeoID = ge.GeoID 
    LEFT JOIN Komodo.GeoEntity ge2 ON ge2.StateCode = ge.StateCode AND ge2.SummaryLevel ='040'
    WHERE mpc.CUSIP9 LIKE "''' + slug + '''%"
    LIMIT 100;
    '''
    search_df = pymysqlQuery(sql)
    
    return render_template('search.html', search_df=search_df)
