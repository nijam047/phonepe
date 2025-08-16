import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import psycopg2
import requests
import json
from PIL import Image

#SQL CONNECTION

mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        password='1234',
                        database='phonepe_data',
                        port='5432')
cursor=mydb.cursor()

#agg_insurance_df

cursor.execute('SELECT * FROM aggregate_insurance')
mydb.commit()
tabel1=cursor.fetchall()

agg_insurance=pd.DataFrame(tabel1,columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count',
       'Transaction_amount'))

#agg_transaction_df

cursor.execute('SELECT * FROM aggregate_transaction')
mydb.commit()
tabel2=cursor.fetchall()

agg_transaction=pd.DataFrame(tabel2,columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count',
       'Transaction_amount'))

#agg_user_df

cursor.execute('SELECT * FROM aggregate_user')
mydb.commit()
tabel3=cursor.fetchall()

agg_user=pd.DataFrame(tabel3,columns=('States', 'Years', 'Quarter', 'Brands', 'Transaction_count',
       'Percentage'))

#map_insurance_df

cursor.execute('SELECT * FROM map_insurance')
mydb.commit()
tabel4=cursor.fetchall()

map_insurance=pd.DataFrame(tabel4,columns=('States', 'Years', 'Quarter', 'Districts', 'Transaction_count',
       'Transaction_amount'))

#map_transaction_df

cursor.execute('SELECT * FROM map_transaction')
mydb.commit()
tabel5=cursor.fetchall()

map_transaction=pd.DataFrame(tabel5,columns=('States', 'Years', 'Quarter', 'Districts', 'Transaction_count',
       'Transaction_amount'))

#map_user_df

cursor.execute('SELECT * FROM map_user')
mydb.commit()
tabel6=cursor.fetchall()

map_user=pd.DataFrame(tabel6,columns=('States', 'Years', 'Quarter', 'Districts', 'RegisteredUsers',
       'AppOpens'))

#top_insurance_df

cursor.execute('SELECT * FROM top_insurance')
mydb.commit()
tabel7=cursor.fetchall()

top_insurance=pd.DataFrame(tabel7,columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count',
       'Transaction_amount'))

#top_transaction_df

cursor.execute('SELECT * FROM top_transaction')
mydb.commit()
tabel8=cursor.fetchall()

top_transaction=pd.DataFrame(tabel8,columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count',
       'Transaction_amount'))

#top_user_df

cursor.execute('SELECT * FROM top_user')
mydb.commit()
tabel9=cursor.fetchall()

top_user=pd.DataFrame(tabel9,columns=('States', 'Years', 'Quarter', 'Pincodes', 'RegisteredUsers'))

#Transaction State Based

def transaction_amount_count_Y(df,year):
    tacy=df[df['Years'] == year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg,x='States',y='Transaction_amount',title=f'{year} TRANSACTION AMOUNT',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)
    
    with col2:
    
        fig_count=px.bar(tacyg,x='States',y='Transaction_count',title=f'{year} TRANSACTION COUNT',
                        color_discrete_sequence=px.colors.sequential.Turbo, height=650, width=600)
        st.plotly_chart(fig_count)

    url='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1['features']:
        states_name.append(feature['properties']['ST_NM'])
    states_name.sort()

    col1,col2=st.columns(2)

    with col1:

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations='States',featureidkey='properties.ST_NM',color='Transaction_amount',
                                color_continuous_scale='Rainbow',range_color=(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].min()),
                                hover_name='States',title=f'{year} TRANSACTION AMOUNT',fitbounds='locations',height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:   

        fig_india_2=px.choropleth(tacyg,geojson=data1,locations='States',featureidkey='properties.ST_NM',color='Transaction_count',
                                color_continuous_scale='Rainbow',range_color=(tacyg['Transaction_count'].min(),tacyg['Transaction_count'].min()),
                                hover_name='States',title=f'{year} TRANSACTION COUNT',fitbounds='locations',height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

#Transaction Quarter Based

def transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df['Quarter'] == quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg,x='States',y='Transaction_amount',title=f'{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)
    
    with col2:
    
        fig_count=px.bar(tacyg,x='States',y='Transaction_count',title=f'{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT',
                        color_discrete_sequence=px.colors.sequential.Turbo, height=650, width=600)
        st.plotly_chart(fig_count)

    url='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1['features']:
        states_name.append(feature['properties']['ST_NM'])
    states_name.sort()

    col1,col2=st.columns(2)

    with col1:

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations='States',featureidkey='properties.ST_NM',color='Transaction_amount',
                                color_continuous_scale='Rainbow',range_color=(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].min()),
                                hover_name='States',title=f'{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT',fitbounds='locations',height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:   

        fig_india_2=px.choropleth(tacyg,geojson=data1,locations='States',featureidkey='properties.ST_NM',color='Transaction_count',
                                color_continuous_scale='Rainbow',range_color=(tacyg['Transaction_count'].min(),tacyg['Transaction_count'].min()),
                                hover_name='States',title=f'{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT',fitbounds='locations',height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

#Transaction TYPE

def Agg_Transaction_Type(df,state):
    tacy=df[df['States'] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.pie(data_frame=tacyg, names='Transaction_type', values='Transaction_amount',
                          width=600, title=f'{state.upper()} TRANSACTION AMOUNT', hole=0.5)
        st.plotly_chart(fig_amount)
    
    with col2:
    
        fig_count=px.pie(data_frame=tacyg, names='Transaction_type', values='Transaction_count',
                          width=600, title=f'{state.upper()} TRANSACTION COUNT', hole=0.5)
        st.plotly_chart(fig_count)

#Agg_User_Analyziz_1

def Agg_User_Plot_1(df,year):
    aguy=df[df['Years'] == year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby('Brands')['Transaction_count'].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg, x='Brands', y= 'Transaction_count', title=f'{year} BRANDS AND TRANSACTION COUNT',
                     width= 1000, color_discrete_sequence=px.colors.sequential.haline_r,hover_name='Brands')
    
    st.plotly_chart(fig_bar_1)

    return aguy

#Agg_User_Analyziz_2

def Agg_User_Plot_2(df,quarter):
    aguyg=df[df['Quarter'] == quarter]
    aguyg.reset_index(drop=True,inplace=True)

    aguygq=pd.DataFrame(aguyg.groupby('Brands')['Transaction_count'].sum())
    aguygq.reset_index(inplace=True)

    fig_bar_1=px.bar(aguygq, x='Brands', y= 'Transaction_count', title=f'{quarter} QUARTER, BRANDS AND TRANSACTION COUNT',
                     width= 1000, color_discrete_sequence=px.colors.sequential.haline_r, hover_name='Brands')
    
    st.plotly_chart(fig_bar_1)

    return aguyg

#Agg_User_Analyziz_3

def Agg_User_Plot_3(df,state):
    auyqs=df[df['States'] == state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs, x='Brands', y= 'Transaction_count', title=f'{state.upper()} TRANSACTION COUNT, BRANDS AND PERCENTAGE',
                     width= 1000, hover_name='Percentage', markers=True)
    
    st.plotly_chart(fig_line_1)

#Map_Insurance_district

def map_insurance_district(df,state):
    tacy=df[df['States'] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby('Districts')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg,x='Transaction_amount',y='Districts',orientation='h',title=f'{state.upper()} DISTRICTS AND TRANSACTION AMOUNT',
                            color_discrete_sequence=px.colors.sequential.Mint_r, height=600)
        st.plotly_chart(fig_amount)
    
    with col2:
    
        fig_count=px.bar(tacyg,x='Transaction_count',y='Districts',orientation='h',title=f'{state.upper()} DISTRICTS AND TRANSACTION COUNT',
                            color_discrete_sequence=px.colors.sequential.Mint_r, height=600)
        st.plotly_chart(fig_count)

#Map_User_Analysis_1

def map_User_Plot_1(df,year):
    muy=df[df['Years'] == year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby('States')[['RegisteredUsers','AppOpens']].sum()
    muyg.reset_index(inplace=True)

    fig_bar_1=px.line(muyg, x='States', y= ['RegisteredUsers','AppOpens'], title=f'{year} REGISTERED USER AND APP OPENS',
                     width= 1000,height=600, markers=True)
    
    st.plotly_chart(fig_bar_1)

    return muy

#Map User Plot 2

def map_User_Plot_2(df,quarter):
    muyq=df[df['Quarter'] == quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby('States')[['RegisteredUsers','AppOpens']].sum()
    muyqg.reset_index(inplace=True)

    fig_bar_1=px.line(muyqg, x='States', y= ['RegisteredUsers','AppOpens'], title=f'{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER AND APP OPENS',
                     width= 1000,height=600, markers=True, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    
    st.plotly_chart(fig_bar_1)

    return muyq

#Map User Plot 3

def map_user_plot_3(df,state):
    muyqs=df[df['States'] == state]
    muyqs.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_map_user_bar_1=px.bar(muyqs, x='RegisteredUsers', y= 'Districts', orientation='h',
                                  title=f'{state.upper()} REGISTERED USER', height=800, color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_map_user_bar_1)
    
    with col2:
    
        fig_map_user_bar_2=px.bar(muyqs, x='AppOpens', y= 'Districts', orientation='h',
                                  title=f'{state.upper()} APPOPENS', height=800, color_discrete_sequence=px.colors.sequential.Brwnyl_r)
        st.plotly_chart(fig_map_user_bar_2)

#Map User Plot 3

def top_insur_plot_1(df,state):
    tiy=df[df['States'] == state]
    tiy.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_top_insur_bar_1=px.bar(tiy, x='Quarter', y= 'Transaction_amount', hover_data='Pincodes',
                                  title=f'{state.upper()} TRANSACTION AMOUNT', height=650,width=600, color_discrete_sequence=px.colors.sequential.amp)
        st.plotly_chart(fig_top_insur_bar_1)
    
    with col2:

        fig_top_insur_bar_2=px.bar(tiy, x='Quarter', y= 'Transaction_count', hover_data='Pincodes',
                                  title=f'{state.upper()} TRANSACTION COUNT', height=650,width=600, color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_top_insur_bar_2)

#top_User_plot_1

def top_User_Plot_1(df,year):
    tuy=df[df['Years'] == year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(['States','Quarter'])['RegisteredUsers'].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg, x='States', y= 'RegisteredUsers', title=f'{year} REGISTERED USER',
                     width= 1000, height=800, color_discrete_sequence=px.colors.sequential.Blugrn_r,hover_name='States',color='Quarter')
    
    st.plotly_chart(fig_top_plot_1)

    return tuy

#top_User__plot_2

def top_User_Plot_2(df,state):
    tuys=df[df['States'] == state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_=px.bar(tuys, x='Quarter', y= 'RegisteredUsers', title=f'{state} REGISTERED USER, PINCODES AND QUARTER',
                     width= 1000, height=800, color_discrete_sequence=px.colors.sequential.Magenta_r,hover_data='Pincodes',color='RegisteredUsers')
    
    st.plotly_chart(fig_top_plot_)

#SQL CONNECTION
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host='localhost',
                            user='postgres',
                            password='1234',
                            database='phonepe_data',
                            port='5432')
    cursor=mydb.cursor()

    #plot_1

    col1,col2=st.columns(2)
    
    with col1:

        query1=f''' SELECT states, SUM(transaction_amount) AS  transaction_amount FROM {table_name} GROUP BY states
                    ORDER BY transaction_amount DESC LIMIT 10;'''

        cursor.execute(query1)
        tabel1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(tabel1, columns=('states','transaction_amount'))

        fig_amount_1=px.bar(df1,x='states',y='transaction_amount', title='TOP 10 OF TRANSACTION AMOUNT',hover_name='states', color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            height=650, width=600)

        st.plotly_chart(fig_amount_1)

    #plot_2

    with col2:

        query2=f''' SELECT states, SUM(transaction_amount) AS  transaction_amount FROM {table_name} GROUP BY states
                    ORDER BY transaction_amount LIMIT 10;'''

        cursor.execute(query2)
        tabel2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(tabel2, columns=('states','transaction_amount'))

        fig_amount_2=px.bar(df2,x='states',y='transaction_amount', title='LAST 10 OF TRANSACTION AMOUNT',hover_name='states', color_discrete_sequence= px.colors.sequential.Aggrnyl_r,
                            height=650, width=600)

        st.plotly_chart(fig_amount_2)

    #plot_3 

    query3=f''' SELECT states, AVG(transaction_amount) AS  transaction_amount FROM {table_name} GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    tabel3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(tabel3, columns=('states','transaction_amount'))

    fig_amount_3=px.bar(df3,x='transaction_amount',y='states', title='AVERAGE OF TRANSACTION AMOUNT',hover_name='states', color_discrete_sequence= px.colors.sequential.Bluered_r,
                        height=1000, width=800, orientation='h')

    st.plotly_chart(fig_amount_3)

def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host='localhost',
                            user='postgres',
                            password='1234',
                            database='phonepe_data',
                            port='5432')
    cursor=mydb.cursor()

    #plot_1

    col1,col2=st.columns(2)
    
    with col1:

        query1=f''' SELECT states, SUM(transaction_count) AS  transaction_count FROM {table_name} GROUP BY states
                    ORDER BY transaction_count DESC LIMIT 10;'''

        cursor.execute(query1)
        tabel1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(tabel1, columns=('states','transaction_count'))

        fig_amount_1=px.bar(df1,x='states',y='transaction_count', title='TOP 10 OF TRANSACTION COUNT',hover_name='states', color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            height=650, width=600)

        st.plotly_chart(fig_amount_1)

    #plot_2

    with col2:

        query2=f''' SELECT states, SUM(transaction_count) AS  transaction_count FROM {table_name} GROUP BY states
                    ORDER BY transaction_count LIMIT 10;'''

        cursor.execute(query2)
        tabel2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(tabel2, columns=('states','transaction_count'))

        fig_amount_2=px.bar(df2,x='states',y='transaction_count', title='LAST 10 OFTRANSACTION COUNT',hover_name='states', color_discrete_sequence= px.colors.sequential.Aggrnyl_r,
                            height=650, width=600)

        st.plotly_chart(fig_amount_2)

    #plot_3 

    query3=f''' SELECT states, AVG(transaction_count) AS  transaction_count FROM {table_name} GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    tabel3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(tabel3, columns=('states','transaction_count'))

    fig_amount_3=px.bar(df3,x='transaction_count',y='states', title='AVERAGE TRANSACTION COUNT',hover_name='states', color_discrete_sequence= px.colors.sequential.Bluered_r,
                        height=1000, width=800, orientation='h')

    st.plotly_chart(fig_amount_3)

def top_chart_registered_user(table_name,state):
    mydb=psycopg2.connect(host='localhost',
                            user='postgres',
                            password='1234',
                            database='phonepe_data',
                            port='5432')
    cursor=mydb.cursor()

    #plot_1

    col1,col2=st.columns(2)
    
    with col1:

        query1=f'''SELECT districts, SUM(registeredusers) AS  registeredusers FROM {table_name} WHERE states='{state}' 
                   GROUP BY districts ORDER BY registeredusers DESC LIMIT 10;'''

        cursor.execute(query1)
        tabel1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(tabel1, columns=('districts','registeredusers'))

        fig_amount_1=px.bar(df1,x='districts',y='registeredusers', title='TOP 10 OF REGISTERED USER',hover_name='districts', color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            height=650, width=600)

        st.plotly_chart(fig_amount_1)

    #plot_2

    with col2:

        query2=f'''SELECT districts, SUM(registeredusers) AS  registeredusers FROM {table_name} WHERE states='{state}' 
                   GROUP BY districts ORDER BY registeredusers LIMIT 10;'''

        cursor.execute(query2)
        tabel2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(tabel2, columns=('districts','registeredusers'))

        fig_amount_2=px.bar(df2,x='districts',y='registeredusers', title='LAST 10 REGISTERED USER',hover_name='districts', color_discrete_sequence= px.colors.sequential.Aggrnyl_r,
                            height=650, width=600)

        st.plotly_chart(fig_amount_2)

    #plot_3 

    query3=f'''SELECT districts, AVG(registeredusers) AS  registeredusers FROM {table_name} WHERE states='{state}' 
                    GROUP BY districts ORDER BY registeredusers DESC;'''

    cursor.execute(query3)
    tabel3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(tabel3, columns=('districts','registeredusers'))

    fig_amount_3=px.bar(df3,x='registeredusers',y='districts', title='AVERAGE OF REGISTERED USER',hover_name='districts', color_discrete_sequence= px.colors.sequential.Bluered_r,
                        height=1000, width=800, orientation='h')

    st.plotly_chart(fig_amount_3)

def top_chart_appopens(table_name,state):
    mydb=psycopg2.connect(host='localhost',
                            user='postgres',
                            password='1234',
                            database='phonepe_data',
                            port='5432')
    cursor=mydb.cursor()

    #plot_1

    col1,col2=st.columns(2)
    
    with col1:

        query1=f'''SELECT districts, SUM(appopens) AS  appopens FROM {table_name} WHERE states='{state}' 
                   GROUP BY districts ORDER BY appopens DESC LIMIT 10;'''

        cursor.execute(query1)
        tabel1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(tabel1, columns=('districts','appopens'))

        fig_amount_1=px.bar(df1,x='districts',y='appopens', title='TOP 10 OF APPOPENS',hover_name='districts', color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            height=650, width=600)

        st.plotly_chart(fig_amount_1)

    #plot_2

    with col2:

        query2=f'''SELECT districts, SUM(appopens) AS  appopens FROM {table_name} WHERE states='{state}' 
                   GROUP BY districts ORDER BY appopens LIMIT 10;'''

        cursor.execute(query2)
        tabel2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(tabel2, columns=('districts','appopens'))

        fig_amount_2=px.bar(df2,x='districts',y='appopens', title='LAST 10 APPOPENS',hover_name='districts', color_discrete_sequence= px.colors.sequential.Aggrnyl_r,
                            height=650, width=600)

        st.plotly_chart(fig_amount_2)

    #plot_3 

    query3=f'''SELECT districts, AVG(appopens) AS  appopens FROM {table_name} WHERE states='{state}' 
                    GROUP BY districts ORDER BY appopens DESC;'''

    cursor.execute(query3)
    tabel3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(tabel3, columns=('districts','appopens'))

    fig_amount_3=px.bar(df3,x='appopens',y='districts', title='AVERAGE OF APPOPENS',hover_name='districts', color_discrete_sequence= px.colors.sequential.Bluered_r,
                        height=1000, width=800, orientation='h')

    st.plotly_chart(fig_amount_3)

def top_chart_TOP_user(table_name):
    mydb=psycopg2.connect(host='localhost',
                            user='postgres',
                            password='1234',
                            database='phonepe_data',
                            port='5432')
    cursor=mydb.cursor()

    #plot_1

    col1,col2=st.columns(2)
    
    with col1:

        query1=f'''SELECT states, SUM(registeredusers) AS  registeredusers FROM {table_name} 
                   GROUP BY states ORDER BY registeredusers DESC LIMIT 10;'''

        cursor.execute(query1)
        tabel1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(tabel1, columns=('states','registeredusers'))

        fig_amount_1=px.bar(df1,x='states',y='registeredusers', title='TOP 10 OF REGISTERED USER',hover_name='states', color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            height=650, width=600)

        st.plotly_chart(fig_amount_1)

    #plot_2

    with col2:

        query2=f'''SELECT states, SUM(registeredusers) AS  registeredusers FROM {table_name} 
                   GROUP BY states ORDER BY registeredusers LIMIT 10;'''

        cursor.execute(query2)
        tabel2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(tabel2, columns=('states','registeredusers'))

        fig_amount_2=px.bar(df2,x='states',y='registeredusers', title='LAST 10 REGISTERED USER',hover_name='states', color_discrete_sequence= px.colors.sequential.Aggrnyl_r,
                            height=650, width=600)

        st.plotly_chart(fig_amount_2)

    #plot_3 

    query3=f'''SELECT states, AVG(registeredusers) AS  registeredusers FROM {table_name} 
               GROUP BY states ORDER BY registeredusers;'''

    cursor.execute(query3)
    tabel3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(tabel3, columns=('states','registeredusers'))

    fig_amount_3=px.bar(df3,x='registeredusers',y='states', title='AVERAGE OF REGISTERED USER',hover_name='states', color_discrete_sequence= px.colors.sequential.Bluered_r,
                        height=1000, width=800, orientation='h')

    st.plotly_chart(fig_amount_3)

#streamlit Part


st.set_page_config(page_title="PhonePe: UPI Payments, Investment, Insurance, Recharges, DTH &amp; More", page_icon=r'D:\Phonepe\PhonePe4.png',layout='wide')

# Apply custom CSS
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #7432FF;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #7432FF;
            color: #FFFFFF;
        }
        .stDownloadButton>button {
            background-color: #7432FF;
            color: #FFFFFF;
        }
        .stRadio label {
            color: white;
        }
        .stSelectbox, .stSlider {
            color: white;
        }
        .stTextInput input {
            color: #7432FF;
        }
        .stApp {
            background-image: url('https://www.codesign.in/codesign/wp-content/uploads/2021/03/Codesign-PhonePe-Beam-Construction.jpg');
            background-size: cover;
            background-position: center;
            height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)

col1,col2= st.columns([3,9])
with col1:
    st.image(r"https://cdn.freelogovectors.net/wp-content/uploads/2023/11/phonepelogo-freelogovectors.net_.png", width=300)
with col2:
    st.markdown(
        """
        <h1 style="text-align: center;color: white;font-family: 'Roboto', sans-serif;text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.4)">PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION</h1>
        """,
        unsafe_allow_html=True
    )

main_tab1, main_tab2, main_tab3 = st.tabs(["***HOME***","***EXPLORE DATA***","***TOP CHARTS***"])

with main_tab1:
    col1,col2= st.columns(2)

    with col1:
        st.markdown('<h1 style="color:#FFFFFF">PHONEPE</h1>', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#FFFFFF">INDIA\'S BEST TRANSACTION APP</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">PhonePe is an Indian digital payments and financial technology company</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 24px;">FEATURES</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> Credit & Debit Card Linking</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> Bank Balance Check</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> Money Storage</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> PIN Authorization</p>', unsafe_allow_html=True)


        
        image=Image.open(r'D:\Phonepe\phonepe1.png')
        st.image(image,width=200)
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.video("https://youtu.be/Yy03rjSUIB8?si=HAOpw_bNFRaLsuCK") 

    col3,col4= st.columns(2)
    
    with col3:
        
        st.video("https://www.phonepe.com/webstatic/8541/videos/page/home-fast-secure-v3.mp4")
                        
    with col4:

        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> Easy Transactions</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> One App For All Your Payments</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> Your Bank Account Is All You Need</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> Multiple Payment Modes</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> PhonePe Merchants</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> Multiple Ways To Pay</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-  1. Direct Transfer & More</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-  2. QR Code</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; font-weight: bold; font-size: 18px;">-> Earn Great Rewards</p>', unsafe_allow_html=True)

        image=Image.open(r'D:\Phonepe\phonepe2.webp')
        st.image(image,width=200)

    col5,col6= st.columns(2)
    

    with col5:

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> No Wallet Top-Up Required</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> Pay Directly From Any Bank To Any Bank A/C</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#FFFFFF; font-weight: bold; font-size: 18px;">-> Instantly & Free</p>', unsafe_allow_html=True)



        image=Image.open(r'D:\Phonepe\phonepe3.webp')
        st.image(image,width=200)
    with col6:
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        video_url = "https://youtu.be/aXnNA4mv1dU?si=WYA0iMunvWvwxS4j"
        st.video(video_url)


with main_tab2:
    
    sub_tab1,sub_tab2,sub_tab3=st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

    with sub_tab1:

        method1=st.radio('Select The method',['Aggregated Insurance','Aggregated Transaction','Aggregated User'])

        if method1 == 'Aggregated Insurance':
            
            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',agg_insurance['Years'].min(),agg_insurance['Years'].max(),agg_insurance['Years'].min(),key='slider1')
            tac_y=transaction_amount_count_Y(agg_insurance,years)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',tac_y['Quarter'].min(),tac_y['Quarter'].max(),tac_y['Quarter'].min(),key='slider2')
            transaction_amount_count_Y_Q(tac_y,quarters)

        elif method1 == 'Aggregated Transaction':

            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',agg_transaction['Years'].min(),agg_insurance['Years'].max(),agg_insurance['Years'].min(),key='slider3')
            Agg_tran_tac_y=transaction_amount_count_Y(agg_transaction,years)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',Agg_tran_tac_y['States'].unique(), key='selectbox_1')
            Agg_Transaction_Type(Agg_tran_tac_y,states)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',Agg_tran_tac_y['Quarter'].min(),Agg_tran_tac_y['Quarter'].max(),Agg_tran_tac_y['Quarter'].min(),key='slider4')
            Agg_tran_tac_y_q = transaction_amount_count_Y_Q(Agg_tran_tac_y,quarters)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State for Quarter View',Agg_tran_tac_y_q['States'].unique(), key='selectbox_2')
            Agg_user_Y=Agg_Transaction_Type(Agg_tran_tac_y_q,states)


        elif method1 == 'Aggregated User':

            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',agg_user['Years'].min(),agg_user['Years'].max(),agg_user['Years'].min(),key='slider5')
            Agg_User_Y=Agg_User_Plot_1(agg_user,years)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',Agg_User_Y['Quarter'].min(),Agg_User_Y['Quarter'].max(),Agg_User_Y['Quarter'].min(),key='slider6')
            Agg_user_Y_Q = Agg_User_Plot_2(Agg_User_Y,quarters)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',Agg_user_Y_Q['States'].unique(), key='selectbox_3')
            Agg_User_Plot_3(Agg_user_Y_Q,states)
    
    with sub_tab2:

        method2=st.radio('Select The method',['Map Insurance','Map Transaction','Map User'])

        if method2 == 'Map Insurance':
            
            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',map_insurance['Years'].min(),map_insurance['Years'].max(),map_insurance['Years'].min(),key='slider7')
            map_insur_y=transaction_amount_count_Y(map_insurance,years)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',map_insur_y['States'].unique(), key='selectbox_4')
            map_insurance_district(map_insur_y,states)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',map_insur_y['Quarter'].min(),map_insur_y['Quarter'].max(),map_insur_y['Quarter'].min(),key='slider8')
            map_insur_y_q = transaction_amount_count_Y_Q(map_insur_y,quarters)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State for District Quarter View ',map_insur_y_q['States'].unique(), key='selectbox_5')
            map_insurance_district(map_insur_y_q,states)

        elif method2 == 'Map Transaction':

            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',map_transaction['Years'].min(),map_transaction['Years'].max(),map_transaction['Years'].min(),key='slider9')
            map_trans_y=transaction_amount_count_Y(map_transaction,years)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',map_trans_y['States'].unique(), key='selectbox_6')
            map_insurance_district(map_trans_y,states)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',map_trans_y['Quarter'].min(),map_trans_y['Quarter'].max(),map_trans_y['Quarter'].min(),key='slider10')
            map_trans_y_q = transaction_amount_count_Y_Q(map_trans_y,quarters)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State for District Quarter View ',map_trans_y_q['States'].unique(), key='selectbox_7')
            map_insurance_district(map_trans_y_q,states)

        elif method2 == 'Map User':
            
            col1,col2=st.columns(2)

            with col1:

                states= st.slider('Select the Year',map_user['Years'].min(),map_user['Years'].max(),map_user['Years'].min(),key='slider11')
            map_user_y= map_User_Plot_1(map_user,states)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',map_user_y['Quarter'].min(),map_user_y['Quarter'].max(),map_user_y['Quarter'].min(),key='slider12')
            map_user_y_q = map_User_Plot_2(map_user_y,quarters)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State for District Quarter View ',map_user_y_q['States'].unique(), key='selectbox_8')
            map_user_plot_3(map_user_y_q,states)

    with sub_tab3:

        method3=st.radio('Select The method',['Top Insurance','Top Transaction','Top User'])

        if method3 == 'Top Insurance':
            
            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',top_insurance['Years'].min(),top_insurance['Years'].max(),top_insurance['Years'].min(),key='slider13')
            top_insur_y=transaction_amount_count_Y(top_insurance,years)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',top_insur_y['States'].unique(), key='selectbox_9')
            top_insur_plot_1(top_insur_y,states)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',top_insur_y['Quarter'].min(),top_insur_y['Quarter'].max(),top_insur_y['Quarter'].min(),key='slider14')
            transaction_amount_count_Y_Q(top_insur_y,quarters)

        elif method3 == 'Top Transaction':

            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',top_transaction['Years'].min(),top_transaction['Years'].max(),top_transaction['Years'].min(),key='slider15')
            top_trans_y=transaction_amount_count_Y(top_transaction,years)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',top_trans_y['States'].unique(), key='selectbox_10')
            top_insur_plot_1(top_trans_y,states)

            col1,col2=st.columns(2)

            with col1:

                quarters= st.slider('Select the Quarter',top_trans_y['Quarter'].min(),top_trans_y['Quarter'].max(),top_trans_y['Quarter'].min(),key='slider16')
            transaction_amount_count_Y_Q(top_trans_y,quarters)

        elif method3 == 'Top User':
            
            col1,col2=st.columns(2)

            with col1:

                years= st.slider('Select the year',top_user['Years'].min(),top_user['Years'].max(),top_user['Years'].min(),key='slider17')
            top_user_y=top_User_Plot_1(top_user,years)

            col1,col2=st.columns(2)

            with col1:

                states=st.selectbox('Select the State',top_user_y['States'].unique(), key='selectbox_11')
            top_User_Plot_2(top_user_y,states)

with main_tab3:

    question=st.selectbox('Select the Questions',['1. Transaction Amount and Count of Aggregated Insurance',
                                                  '2. Transaction Amount and Count of Map Insurance',
                                                  '3. Transaction Amount and Count of Top Insurance',
                                                  '4. Transaction Amount and Count of Aggregated Transaction',
                                                  '5. Transaction Amount and Count of Map Transaction',
                                                  '6. Transaction Amount and Count of Top Transaction',
                                                  '7. Transaction Count of Aggregated User',
                                                  '8. Registered User of Map User',
                                                  '9. AppOpens of Map User',
                                                  '10. Registered User of Top User'])
    
    if question=='1. Transaction Amount and Count of Aggregated Insurance':

        st.subheader('TRANSACTION AMOUNT')
        top_chart_transaction_amount('aggregate_insurance')

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('aggregate_insurance')

    elif question=='2. Transaction Amount and Count of Map Insurance':

        st.subheader('TRANSACTION AMOUNT')
        top_chart_transaction_amount('map_insurance')

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('map_insurance')
    
    elif question=='3. Transaction Amount and Count of Top Insurance':

        st.subheader('TRANSACTION AMOUNT')
        top_chart_transaction_amount('top_insurance')

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('top_insurance')

    elif question=='4. Transaction Amount and Count of Aggregated Transaction':

        st.subheader('TRANSACTION AMOUNT')
        top_chart_transaction_amount('aggregate_transaction')

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('aggregate_transaction')

    elif question=='5. Transaction Amount and Count of Map Transaction':

        st.subheader('TRANSACTION AMOUNT')
        top_chart_transaction_amount('map_transaction')

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('map_transaction')

    elif question=='6. Transaction Amount and Count of Top Transaction':

        st.subheader('TRANSACTION AMOUNT')
        top_chart_transaction_amount('top_transaction')

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('top_transaction')

    elif question=='7. Transaction Count of Aggregated User':

        st.subheader('TRANSACTION COUNT')
        top_chart_transaction_count('aggregate_user')

    elif question=='8. Registered User of Map User':

        state=st.selectbox('Select the State', map_user['States'].unique(),key='selectbox_12')
        st.subheader('REGISTERED USER')
        top_chart_registered_user('map_user',state)

    elif question=='9. AppOpens of Map User':

        state=st.selectbox('Select the State', map_user['States'].unique(),key='selectbox_13')
        st.subheader('APPOPENS')
        top_chart_appopens('map_user',state)

    elif question=='10. Registered User of Top User':

        st.subheader('REGISTERED USER')
        top_chart_TOP_user('top_user')
