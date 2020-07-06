# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 08:18:36 2019

@author: M_TASGETIREN
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
df = pd.read_csv(url)
df_cntry=df.groupby("Country/Region").sum()
df_cntry = df_cntry.drop(['Lat','Long'], 1)
df_cntry=df_cntry.T
df_cntry.reset_index(inplace=True)
df_cntry['index']=df_cntry['index'].apply(pd.to_datetime)
#,'China':"2/2/20",'Japan':"2/2/20",'Korea, South':"2/2/20",'France':"2/6/20",
firstday_cntry={'Italy':"2/19/20",'Iran':"2/18/20",'Germany':"2/18/20",'Turkey':"3/13/20",'US':"2/23/20",'Spain':"2/25/20"}
cntry_names=firstday_cntry.keys()

numbers=[]
for i in range(45):
    numbers.append(i)
yeni_listeler=[]
for k,v in firstday_cntry.items():
    yeni_listeler.append(df_cntry[df_cntry['index']>v][k].tolist())

df_new = pd.DataFrame(yeni_listeler)
df_new=df_new.T
df_new.columns=cntry_names
df_new['Day']=pd.Series(numbers)

#kac gune bakmak istiyoruz?
df_new=df_new[df_new['Day']<15]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


traces = []
labels=[]

for i in cntry_names:
    # df_by_continent = df_cntry[df_cntry['continent'] == i]
    traces.append(dict(
        x=df_new['Day'],
        y=df_new[i],
        text=i,
        opacity=0.7,

        name=i
    ))
    labels.append(dict(
        { 'label' : i,
          'value' : i}
    ))

app.layout = html.Div([
    html.Div(

    dcc.Graph(id="barplot",
                                    figure={
                                        "data": traces,
                                        "layout": go.Layout(
                                            title="Covid-19",

                                            )}
)),
html.Div(
dcc.Dropdown(
    options=labels
)
)])

if __name__ == "__main__":
    app.run_server()