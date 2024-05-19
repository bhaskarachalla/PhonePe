import streamlit as st 
import psycopg2
import pandas as pd
import json
import requests
import plotly.express as px
from PIL import Image
from streamlit_option_menu import option_menu

mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        database = "Phonepe_Data",
                        password = 'Space-time123')

cursor = mydb.cursor()

#aggre_transaction DF
cursor.execute('SELECT * FROM aggregated_transaction')
mydb.commit()
Table1 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(Table1, columns=('States','Years','Quartile','Transaction_type','Transaction_count','Transaction_amount'))


cursor.execute('SELECT * FROM aggregated_user')
mydb.commit()
Table2 = cursor.fetchall()

Aggre_user = pd.DataFrame(Table2, columns=('States','Years','Quartile','Brands','Transaction_count','Percentage'))

cursor.execute('SELECT * FROM map_transaction')
mydb.commit()
Table3 = cursor.fetchall()

Map_transaction = pd.DataFrame(Table3, columns=('States','Years','Quartile','Districts','Transaction_count','Transaction_amount'))


cursor.execute('SELECT * FROM map_users')
mydb.commit()
Table4 = cursor.fetchall()

Map_user = pd.DataFrame(Table4, columns=('States','Years','Quartile','Districts','RegisteredUsers','AppOpens'))


cursor.execute('SELECT * FROM top_transaction')
mydb.commit()
Table5 = cursor.fetchall()

Top_transaction = pd.DataFrame(Table5, columns=('States','Years','Quartile','Pincodes','Transaction_count','Transaction_amount'))


cursor.execute('SELECT * FROM top_user')
mydb.commit()
Table6 = cursor.fetchall()

Top_user = pd.DataFrame(Table6, columns=('States','Years','Quartile','Pincodes','RegisteredUsers'))



def Transaction_Amount_Count_Yearwise(df, year):
    
    
    Tramcoye = df[df['Years'] == year]
    Tramcoye.reset_index(drop = True, inplace = True)
    
    Tramcoye_Group = Tramcoye.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    Tramcoye_Group.reset_index(inplace= True)
    
    col1, col2 = st.columns(2)
    with col1:

        Amount_Plot = px.bar(Tramcoye_Group, x = 'States', y = 'Transaction_amount',title = f'{year}  Transaction Amount', height = 630, width=600)
        st.plotly_chart(Amount_Plot)
    with col2:   
        Count_Plot = px.bar(Tramcoye_Group, x = 'States', y = 'Transaction_count',title = f'{year}  Transaction Count', height = 630, width=600)
        st.plotly_chart(Count_Plot)
    
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response = requests.get(url)
    data1 = json.loads(response.content)

    states_name = []
    for feature in data1['features']:
        states_name.append((feature['properties']['ST_NM']))
        

    states_name.sort()

    India_map1 = px.choropleth(Tramcoye_Group, geojson = data1, 
                                locations = 'States', 
                                featureidkey = 'properties.ST_NM',
                                color = 'Transaction_amount', 
                                color_continuous_scale = 'Rainbow',
                                range_color = (Tramcoye_Group['Transaction_amount'].min(),
                                                Tramcoye_Group['Transaction_amount'].max()), 
                                hover_name = 'States', 
                                title = f'{year}  Transaction amount', fitbounds = 'locations',height = 600, width=600
                                ) 
    
    col3 , col4 = st.columns(2)
    with col3:
        India_map1.update_geos(visible = False)
        st.plotly_chart(India_map1)
    
    
    India_map2 = px.choropleth(Tramcoye_Group, geojson = data1, 
                                locations = 'States', 
                                featureidkey = 'properties.ST_NM',
                                color = 'Transaction_count', 
                                color_continuous_scale = 'Rainbow',
                                range_color = (Tramcoye_Group['Transaction_count'].min(),
                                                Tramcoye_Group['Transaction_count'].max()), 
                                hover_name = 'States', 
                                title = f'{year}  Transaction count', fitbounds = 'locations',height = 600, width=600
                                ) 
    with col4:
        India_map2.update_geos(visible = False)
        st.plotly_chart(India_map2)

    return Tramcoye


def Transaction_Amount_Count_Quartilewise(df, quartile):
    Tramcoye = df[df['Quartile'] == quartile]
    Tramcoye.reset_index(drop = True, inplace = True)


    Tramcoye_Group = Tramcoye.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    Tramcoye_Group.reset_index(inplace= True)
    
    col5,col6 = st.columns(2)
    with col5:
        Amount_Plot = px.bar(Tramcoye_Group, x = 'States', y = 'Transaction_amount',title = f'  {Tramcoye["Years"].min()}  Year  {quartile} Quarter Transaction Amount' ,height = 630, width=600)
        st.plotly_chart(Amount_Plot)
    with col6:
        Count_Plot = px.bar(Tramcoye_Group, x = 'States', y = 'Transaction_count',title = f'  {Tramcoye["Years"].min()}  Year  {quartile} Quarter Transaction Count' ,height = 630, width=600)
        st.plotly_chart(Count_Plot)    
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    response = requests.get(url)
    data1 = json.loads(response.content)

    states_name = []
    for feature in data1['features']:
        states_name.append((feature['properties']['ST_NM']))
        

    states_name.sort()

    India_map1 = px.choropleth(Tramcoye_Group, geojson = data1, 
                                locations = 'States', 
                                featureidkey = 'properties.ST_NM',
                                color = 'Transaction_amount', 
                                color_continuous_scale = 'Rainbow',
                                range_color = (Tramcoye_Group['Transaction_amount'].min(),
                                                Tramcoye_Group['Transaction_amount'].max()), 
                                hover_name = 'States', 
                                title = f'{Tramcoye["Years"].min()}  Year {quartile} Quartrline Transaction amount', fitbounds = 'locations',height = 600, width=600
                                ) 
    col7, col8 = st.columns(2)
    with col7:
        India_map1.update_geos(visible = False)
        st.plotly_chart(India_map1)
    
    
    India_map2 = px.choropleth(Tramcoye_Group, geojson = data1, 
                                locations = 'States', 
                                featureidkey = 'properties.ST_NM',
                                color = 'Transaction_count', 
                                color_continuous_scale = 'Rainbow',
                                range_color = (Tramcoye_Group['Transaction_count'].min(),
                                                Tramcoye_Group['Transaction_count'].max()), 
                                hover_name = 'States', 
                                title = f'  {Tramcoye["Years"].min()}  Year  {quartile} Quarter Transaction Count' , fitbounds = 'locations',height = 600, width=600
                                ) 
    with col8:
        India_map2.update_geos(visible = False)
        st.plotly_chart(India_map2)

    return Tramcoye
    
    
    
def Aggre_Tran_Transaction_Type(df, state):

    Tramcoye = df[df['States'] == state]
    Tramcoye.reset_index(drop = True, inplace = True)

    Tramcoye_Group = Tramcoye.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    Tramcoye_Group.reset_index(inplace= True)
    
    col9, col10 = st.columns(2)
    
    Pie_Chart1 = px.pie(data_frame = Tramcoye_Group, names = 'Transaction_type', values = 'Transaction_amount', width = 600, title = f'{state}  Transaction amount', hole = 0.50 , )
    with col9:
        st.plotly_chart(Pie_Chart1)

    Pie_Chart2 = px.pie(data_frame = Tramcoye_Group, names = 'Transaction_type', values = 'Transaction_count', width = 600, title = f'{state}  Transaction count', hole = 0.50 , )
    with col10:
        st.plotly_chart(Pie_Chart2)  


def Aggre_User_plot1(df, year):
    
    
    AgUY = df[df['Years'] == year]
    AgUY.reset_index(drop = True, inplace = True)

    AgUY_Group = AgUY.groupby('Brands')[['Transaction_count']].sum()
    AgUY_Group.reset_index(inplace = True)

    
    Bar1 = px.bar(AgUY_Group, x = 'Brands', y = 'Transaction_count', title = f'{year} Brands and Transaction Count', width= 900)
    st.plotly_chart(Bar1)
    
    return AgUY

def Aggre_User_plot2(df, quartile):

    AgUYQ = df[df['Quartile'] == quartile]
    AgUYQ.reset_index(drop = True, inplace = True)

    AgUYQ_Group = AgUYQ.groupby(['Brands'])[['Transaction_count']].sum()
    AgUYQ_Group.reset_index(inplace = True)
    
   
    Bar2 = px.bar(AgUYQ_Group, x = 'Brands', y = 'Transaction_count',
                    title = f'{quartile} Quartile,Brands and Transaction Count Quartile', width= 900)
    st.plotly_chart(Bar2)
    
    return AgUYQ

def Aggre_User_plot3(df, state):
    AgU_Year_Q_S = df[df['States'] == state]
    AgU_Year_Q_S.reset_index(drop=True, inplace= True )
    
    Area1 = px.area(AgU_Year_Q_S, x= 'Brands', y= 'Transaction_count',hover_data='Percentage',
                    title=f'{state} Brands, Transaction count, Percentage',width=900, markers=True)
    st.plotly_chart(Area1)
    
    
def Map_Trans_District(df, state):
    Tacyd = df[df['States'] == state]
    Tacyd.reset_index(drop=True, inplace=True)
    
    Tacyd_Group = Tacyd.groupby('Districts')[['Transaction_count', 'Transaction_amount']].sum()
    Tacyd_Group.reset_index(inplace=True)
    
    Bar3 = px.bar(Tacyd_Group, x='Transaction_amount', y='Districts', orientation='h', 
                  title=f'{state} Districts and Transaction amount', width=900)
    st.plotly_chart(Bar3)
    
    Bar4 = px.bar(Tacyd_Group, x='Transaction_count', y='Districts', 
                  title=f'{state} Districts and Transaction count')
    st.plotly_chart(Bar4)   


def Map_User_Plot1(df, year):

    MUY = df[df['Years'] == year]
    MUY.reset_index(drop = True, inplace = True)

    MUY_Group = MUY.groupby('States')[['RegisteredUsers', 'AppOpens']].sum()
    MUY_Group.reset_index(inplace = True)

    Area2  = px.area(MUY_Group, x= 'States', y= ['RegisteredUsers', 'AppOpens'],
                     title=f'{year} MUY Registered Users & App Opens',
                     width=900, markers= True)
    st.plotly_chart(Area2)

    return MUY    

def Map_User_Plot2(df, quartile):

    MUY_Q = df[df['Quartile'] == quartile]
    MUY_Q.reset_index(drop = True, inplace = True)

    MUY_Q_Group = MUY_Q.groupby('States')[['RegisteredUsers', 'AppOpens']].sum()
    MUY_Q_Group.reset_index(inplace = True)

    Area2  = px.area(MUY_Q_Group, x= 'States', y= ['RegisteredUsers', 'AppOpens'],
                     title=f'{df['Years'].min()} Year {quartile} MUY Quartile Registered Users & App Opens',width=900, 
                     markers= True, color_discrete_sequence = px.colors.sequential.Rainbow_r)
    st.plotly_chart(Area2)
    
    return MUY_Q


def Map_User_plot3(df, states):
    MUYQS = df[df['States'] == states]
    MUYQS.reset_index(drop = True, inplace = True)
    
    col1,col2 = st.columns(2)
    
    with col1:

        Bar5 = px.bar(MUYQS, x = 'RegisteredUsers', y = 'Districts',orientation='h', 
                        title = f'{states} Registered User',
                        height=900, width= 900)
        st.plotly_chart(Bar5)
    with col2:
        Bar6 = px.bar(MUYQS, x = 'AppOpens', y = 'Districts',orientation='h', 
                        title = f'{states} App Opens',
                        height=900, width= 900)
        st.plotly_chart(Bar6)

def Top_Transaction_Plot1(df, states):
    
    col1, col2 = st.columns(2)

    TTY_Q = df[df['States'] == states]
    TTY_Q.reset_index(drop = True, inplace = True)

    TTY_Q_Group = TTY_Q.groupby('Pincodes')[['Transaction_count', 'Transaction_amount']].sum()
    TTY_Q_Group.reset_index(inplace = True)
    
    with col1:
        Line1  = px.area(TTY_Q, x= 'Pincodes', y= 'Transaction_amount',
                            title='Transaction Amount',width=600, 
                            markers= True, color_discrete_sequence = px.colors.sequential.YlGnBu)
        st.plotly_chart(Line1)
    with col2:
        Line2  = px.area(TTY_Q, x= 'Pincodes', y= 'Transaction_count',
                            title='Transaction Count',width=600, 
                            markers= True, color_discrete_sequence = px.colors.sequential.Sunsetdark_r)
        st.plotly_chart(Line2)

def Top_User_P1(df, years):
    TUY = df[df['Years'] == years]
    TUY.reset_index(drop = True, inplace = True)

    TUY_Group = pd.DataFrame(TUY.groupby(['States', 'Quartile'])['RegisteredUsers'].sum())
    TUY_Group.reset_index(inplace = True)

    Top_User_Plot1 = px.bar(TUY_Group, x = 'States', y = 'RegisteredUsers', 
                            color = 'Quartile', width= 900, height = 900,
                            color_discrete_sequence=px.colors.sequential.algae_r,
                            title = f'{years} Registered Users')

    st.plotly_chart(Top_User_Plot1)
    
    return TUY


def Top_User_P2(df,states):

    TUYS = df[df['States'] == states]
    TUYS.reset_index(drop = True, inplace = True)

    StackedPlot1 = px.bar(TUYS, x= 'Quartile', y = 'RegisteredUsers', color='RegisteredUsers', 
                        title = 'Registered Users, Pincodes, Quarter', width=900, height = 600, 
                        hover_data='Pincodes',color_continuous_scale=px.colors.sequential.Magma)

    st.plotly_chart(StackedPlot1)


def top_chart_transaction_amount(table_name):

    mydb = psycopg2.connect(host = 'localhost',
                            user = 'postgres',
                            port = '5432',
                            database = "Phonepe_Data",
                            password = 'Space-time123')

    cursor = mydb.cursor()

    query_1 = f'''Select states, SUM(transaction_amount) as transaction_amount
                From {table_name}
                Group by States
                Order by transaction_amount DESC
                Limit 10;'''
    cursor.execute(query_1)   
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=('states','transaction_amount'))          
    fig_amount = px.bar(df_1,x='states', y = 'transaction_amount', title = 'Top 10 of Transaction Amount',hover_name='states',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl ,height=650, width=600)

    st.plotly_chart(fig_amount)

    query_2 = f'''Select states, SUM(transaction_amount) as transaction_amount
                From {table_name}
                Group by States
                Order by transaction_amount
                Limit 10;'''
    cursor.execute(query_2)   
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=('states','transaction_amount'))          
    fig_amount_2= px.bar(df_1,x='states', y = 'transaction_amount', title = 'Last 10 Transaction Amount',hover_name='states',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)

    st.plotly_chart(fig_amount_2)

    query_3 = f'''Select states, AVG(transaction_amount) as transaction_amount
                From {table_name}
                Group by States
                Order by transaction_amount;'''
    cursor.execute(query_3)   
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=('states','transaction_amount'))          
    fig_amount_3= px.bar(df_1,y='states', x = 'transaction_amount', title = 'Average Transaction Amount',hover_name='states', orientation='h',
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

    st.plotly_chart(fig_amount_3)


def top_chart_transaction_count(table_name):

    mydb = psycopg2.connect(host = 'localhost',
                            user = 'postgres',
                            port = '5432',
                            database = "Phonepe_Data",
                            password = 'Space-time123')

    cursor = mydb.cursor()

    query_1 = f'''Select states, SUM(transaction_count) as transaction_count
                From {table_name}
                Group by States
                Order by transaction_count DESC
                Limit 10;'''
    cursor.execute(query_1)   
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=('states','transaction_count'))          
    fig_amount = px.bar(df_1,x='states', y = 'transaction_count', title = 'Top 10 of Transaction Count',hover_name='states',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl ,height=650, width=600)

    st.plotly_chart(fig_amount)

    query_2 = f'''Select states, SUM(transaction_count) as transaction_count
                From {table_name}
                Group by States
                Order by transaction_count
                Limit 10;'''
    cursor.execute(query_2)   
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=('states','transaction_count'))          
    fig_amount_2= px.bar(df_1,x='states', y = 'transaction_count', title = 'Last 10 of Transaction Count',hover_name='states',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)

    st.plotly_chart(fig_amount_2)

    query_3 = f'''Select states, AVG(transaction_count) as transaction_count
                From {table_name}
                Group by States
                Order by transaction_count;'''
    cursor.execute(query_3)   
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=('states','transaction_count'))          
    fig_amount_3= px.bar(df_1,y='states', x = 'transaction_count', title = 'Average Transaction Count',hover_name='states', orientation='h',
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

    st.plotly_chart(fig_amount_3)


def top_chart_map_user(table_name,state):

    mydb = psycopg2.connect(host = 'localhost',
                            user = 'postgres',
                            port = '5432',
                            database = "Phonepe_Data",
                            password = 'Space-time123')

    cursor = mydb.cursor()

    query_1 = f'''select districts,sum(registeredusers) as registeredusers
                  from {table_name}
                  where states = '{state}'
                  group by districts
                  order by registeredusers desc
                  limit 10;'''
    cursor.execute(query_1)   
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=('districts','registeredusers'))          
    fig_amount = px.bar(df_1,x='districts', y = 'registeredusers', title = 'Top 10 of Registered User',hover_name='districts',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl ,height=650, width=600)

    st.plotly_chart(fig_amount)

    query_2 = f'''select districts,sum(registeredusers) as registeredusers
                  from {table_name}
                  where states = '{state}'
                  group by districts
                  order by registeredusers asc
                  limit 10;'''
    cursor.execute(query_2)   
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=('districts','registeredusers'))          
    fig_amount_2= px.bar(df_1,x='districts', y = 'registeredusers', title = 'Last 10 Registered User',hover_name='districts',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)

    st.plotly_chart(fig_amount_2)

    query_3 = f'''select districts,avg(registeredusers) as registeredusers
                  from {table_name}
                  where states = '{state}'
                  group by districts
                  order by registeredusers;'''
    cursor.execute(query_3)   
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=('districts','registeredusers'))          
    fig_amount_3= px.bar(df_1,y='districts', x = 'registeredusers', title = 'Average Registered User',hover_name='districts', orientation='h',
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

    st.plotly_chart(fig_amount_3)


def top_chart_map_user_appOpens(table_name,state):

    mydb = psycopg2.connect(host = 'localhost',
                            user = 'postgres',
                            port = '5432',
                            database = "Phonepe_Data",
                            password = 'Space-time123')

    cursor = mydb.cursor()

    query_1 = f'''select districts,sum(appopens) as appopens
                  from {table_name}
                  where states = '{state}'
                  group by districts
                  order by appopens desc
                  limit 10;'''
    cursor.execute(query_1)   
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=('districts','appopens'))          
    fig_amount = px.bar(df_1,x='districts', y = 'appopens', title = 'Top 10 of App Opens',hover_name='districts',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl ,height=650, width=600)

    st.plotly_chart(fig_amount)

    query_2 = f'''select districts,sum(appopens) as appopens
                  from {table_name}
                  where states = '{state}'
                  group by districts
                  order by appopens asc
                  limit 10;'''
    cursor.execute(query_2)   
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=('districts','appopens'))          
    fig_amount_2= px.bar(df_1,x='districts', y = 'appopens', title = 'Last 10 App Opens',hover_name='districts',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)

    st.plotly_chart(fig_amount_2)

    query_3 = f'''select districts,avg(appopens) as appopens
                  from {table_name}
                  where states = '{state}'
                  group by districts
                  order by appopens;'''
    cursor.execute(query_3)   
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=('districts','appopens'))          
    fig_amount_3= px.bar(df_1,y='districts', x = 'appopens', title = 'Average App Opens',hover_name='districts', orientation='h',
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

    st.plotly_chart(fig_amount_3)


def top_chart_top_user(table_name):

    mydb = psycopg2.connect(host = 'localhost',
                            user = 'postgres',
                            port = '5432',
                            database = "Phonepe_Data",
                            password = 'Space-time123')

    cursor = mydb.cursor()

    query_1 = f'''select states,sum(registeredusers) as registeredusers
                  from {table_name}
                  group by states
                  order by registeredusers desc
                  limit 10;'''
    cursor.execute(query_1)   
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=('states','registeredusers'))          
    fig_amount = px.bar(df_1,x='states', y = 'registeredusers', title = 'Top 10 of Registered Users in Top User',hover_name='states',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl ,height=650, width=600)

    st.plotly_chart(fig_amount)

    query_2 = f'''select states,sum(registeredusers) as registeredusers
                    from {table_name}
                    group by states
                    order by registeredusers
                    limit 10;'''
    cursor.execute(query_2)   
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=('states','registeredusers'))          
    fig_amount_2= px.bar(df_1,x='states', y = 'registeredusers', title = 'Last 10 Registered users in top user',hover_name='states',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)

    st.plotly_chart(fig_amount_2)

    query_3 = f'''select states,avg(registeredusers) as registeredusers
                    from {table_name}
                    group by states
                    order by registeredusers;'''
    cursor.execute(query_3)   
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=('states','registeredusers'))          
    fig_amount_3= px.bar(df_1,y='states', x = 'registeredusers', title = 'Average Registered Users in Top User'
                         ,hover_name='states', orientation='h',
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

    st.plotly_chart(fig_amount_3)
    
    
def total_count_Y(table_name):
    mydb = psycopg2.connect(host = 'localhost',
                            user = 'postgres',
                            port = '5432',
                            database = "Phonepe_Data",
                            password = 'Space-time123')

    cursor = mydb.cursor()
    
    query_1 = f'''Select years, sum(transaction_count) as total_count 
                        from {table_name} 
                        group by years 
                        order by years asc'''
    cursor.execute(query_1)   
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=('years','total_count'))          
    Pie_Chart = px.pie(data_frame = df_1, names = 'years', values = 'total_count', width = 600, title = 'Transactions Through Years', hole = 0.50 )


    st.plotly_chart(Pie_Chart)
    
    
        


#Streamlit Part

st.set_page_config(layout = 'wide')
st.title('PhonePe Data Exploration')


with st.sidebar:
    select = option_menu('Main Menu',['HOME','DATA EXPO','TOP LIST'])

if select == 'HOME':
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:/Users/Srinivasa Rao/OneDrive/Documents/PhonePe/Phone_Img.jpeg"),width= 600)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:/Users/Srinivasa Rao/OneDrive/Documents/PhonePe/PhonePe_img.png"),width=540)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

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
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video('C:/Users/Srinivasa Rao/OneDrive/Documents/PhonePe/One-Click Payment.mp4')


elif select == 'DATA EXPO':
    Tab1, Tab2, Tab3 = st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])
    
    with Tab1:
        Method1 = st.radio('Select The Method',['Transaction Details', 'User Details'])
        
        if Method1 == 'Transaction Details':
            
            
            years = st.selectbox( 'Select the year',(Aggre_transaction['Years'].unique()))
            Tram_y = Transaction_Amount_Count_Yearwise(Aggre_transaction, years)
            
            quartile = st.selectbox( 'Select the quartile',(Tram_y['Quartile'].unique()))
            Tram_y_q = Transaction_Amount_Count_Quartilewise(Tram_y, quartile)
            
            states = st.selectbox('Select the state', Tram_y_q['States'].unique())
            Aggre_Tran_Transaction_Type(Tram_y_q, states)
        
            
        elif Method1 == 'User Details':
            
            
            years = st.selectbox( 'Select the year',(Aggre_user['Years'].unique()))
            AgU_Year = Aggre_User_plot1(Aggre_user, years)
            
            
            quartile = st.selectbox( 'Select the quartile',(AgU_Year['Quartile'].unique()))
            AgU_Year_Q = Aggre_User_plot2(AgU_Year, quartile)

            states = st.selectbox('Select the state', AgU_Year_Q['States'].unique())
            Aggre_User_plot3(AgU_Year_Q, states)
            
            
    with Tab2:
        Method2 = st.radio('Select The Method',['Map Transaction', 'Map User'])
        
        if Method2 == 'Map Transaction':
                
                years = st.selectbox('Select the year_mt',Map_transaction['Years'].unique())
                Map_TY = Transaction_Amount_Count_Yearwise(Map_transaction, years)
                
                states = st.selectbox('Select the state_mt',Map_TY['States'].unique())
                Map_Trans_District(Map_TY, states)
                
                quartile = st.selectbox( 'Select the quartile_mt',(Map_TY['Quartile'].unique()))
                Map_TY_Q = Transaction_Amount_Count_Quartilewise(Map_TY, quartile)
                
                states = st.selectbox('Select the state_mts',Map_TY_Q['States'].unique())
                Map_Trans_District(Map_TY_Q, states)
            
        elif Method2 == 'Map User':
             
             years = st.selectbox('Select the years_MU',Map_user['Years'].unique())
             Map_User_Y = Map_User_Plot1(Map_user, years)
             
             quartile = st.selectbox( 'Select the quartile_MU',(Map_User_Y['Quartile'].unique()))
             Map_User_Year_Q = Map_User_Plot2(Map_User_Y, quartile)
             
             states = st.selectbox('Select the state_MUS',Map_User_Year_Q['States'].unique())
             Map_User_plot3(Map_User_Year_Q, states)
            
    
    with Tab3:
        Method3 = st.radio('Select The Method',['Top Transaction', 'Top User'])
        
        if Method3 == 'Top Transaction':
            years = st.selectbox('Select the year_tt',Top_transaction['Years'].unique())
            Top_TY = Transaction_Amount_Count_Yearwise(Top_transaction, years)
            
            states = st.selectbox('Select the state_tts',Top_TY['States'].unique())
            Top_Transaction_Plot1(Top_TY,states)
            
            quartile = st.selectbox('Select the quartile_ttq',(Top_TY['Quartile'].unique()))
            Top_Transaction_Year_Q =  Transaction_Amount_Count_Quartilewise(Top_TY, quartile)
            
        elif Method3 == 'Top User':
             years = st.selectbox('Select the year_tu',Top_user['Years'].unique())
             Top_UY = Top_User_P1(Top_user, years)
             
             states = st.selectbox('Select the state_tts',Top_UY['States'].unique())
             Top_User_P2(Top_UY,states)
             
             
            
            
            
            
elif select == 'TOP LIST':
    question = st.selectbox('Select question',['1.Transaction Amount and Count of Aggregated Transaction',
                                               '2.Transaction Amount and Count of Map Transaction',
                                               '3.Transaction Amount and Count of Top Transaction',
                                               '4.Transaction Count of Aggregated User',
                                               '5.Registered Users of Map Users',
                                               '6.App openings of Map User',
                                               '7.Registered Users of Top User',
                                               '8.Total aggregated transaction count for all years',
                                               '9.Total Top transaction count for all years',
                                               '10.Total Aggregated users  transaction count for all years'
                                               ])       
     
    
    
    if question ==  '1.Transaction Amount and Count of Aggregated Transaction':
        
        st.subheader('Transaction Amount')
        
        top_chart_transaction_amount('aggregated_transaction')
        
        st.subheader('Transaction Count')
        
        top_chart_transaction_count('aggregated_transaction')
        
    elif question ==  '2.Transaction Amount and Count of Map Transaction':
        
        st.subheader('Transaction Amount')
        
        top_chart_transaction_amount('map_transaction')
        
        st.subheader('Transaction Count')
        
        top_chart_transaction_count('map_transaction')
    
    elif question ==  '3.Transaction Amount and Count of Top Transaction':
        
        st.subheader('Transaction Amount')
        
        top_chart_transaction_amount('top_transaction')
        
        st.subheader('Transaction Count')
        
        top_chart_transaction_count('top_transaction')       
            
    elif question ==  '4.Transaction Count of Aggregated User':
        
        st.subheader('Transaction Count')
        
        top_chart_transaction_count('aggregated_user')
    
    elif question ==  '5.Registered Users of Map Users':
        
        
        states = st.selectbox('Select the state', Map_user['States'].unique())
        st.subheader('Registred User')
        top_chart_map_user('map_users',states)
       
    
    
    elif question ==  '6.App openings of Map User':
        
        
        states = st.selectbox('Select the state', Map_user['States'].unique())
        st.subheader('App Openings')
        top_chart_map_user_appOpens('map_users',states)
    
    elif question ==  '7.Registered Users of Top User':
        st.subheader('Registered Users in Top User')
        
        top_chart_top_user('top_user')
        
    elif question == '8.Total aggregated transaction count for all years':    
        st.subheader('Total Count of Transactions')
        
        total_count_Y('aggregated_transaction')
    
    elif question == '9.Total Top transaction count for all years':    
        st.subheader('Total Count of Transactions')
        
        total_count_Y('top_transaction')
    
    elif question == '10.Total Aggregated users  transaction count for all years':    
        st.subheader('Total Count of Transactions')
        
        total_count_Y('aggregated_user')
                                          
                                                #### Enjoy Coding #### Hello#