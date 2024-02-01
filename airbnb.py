# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_lottie import st_lottie
import json
import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns


#setting Streamlit 


st.set_page_config(page_title="Airbnb Data",layout= "wide")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
col1,col2=st.columns(2)
with col1:
        img=Image.open("ab.jpg")
        st.image(img,width=100)
        
with col2:
    st.markdown("<h1 style='text-align:right; color:white;'>Airbnb</h1>", unsafe_allow_html=True)

selected=option_menu(
        menu_title="Main Menu",
        options=["HOME","EXPLORE DATA","Insights","ADDITIONAL INFORMATION"],
        icons=["house-fill","box-fill","back","book-half"],
        menu_icon="wallet-fill",
        orientation="horizontal",
        styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "15px"},
                               "container" : {"max-width": "14000px"},
                               "nav-link-selected": {"background-color": "#121010"}})



if selected=="HOME":
    col1,col2=st.columns(2)
    with col1:
        st.header(":white[**About AirBNB**]")
        st.markdown(":white[**Airbnb is an online marketplace that connects people who want to rent out their property with people who are looking for accommodations. The name Airbnb is short for Air Bed and Breakfast**]")
        st.markdown(":white[**Airbnb offers hosts a way to earn income from their property. Guests can rent a space for multiple people to share, a shared space with private rooms, or the entire property for themselves. Airbnb is known for providing vacation homes, but you can also book private rooms, shared rooms, and even hotel rooms.**]")
        st.markdown(":white[**Airbnb acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.**]")
        st.markdown(":white[**Airbnb has listings all over the world, with more than 5.6 million listings in roughly 220 countries.**]")
    with col2:
        
        filepath=load_lottiefile("E:\data science\Airbnb Data Analysis\A2.json")
        st.lottie(filepath,speed=1,reverse=False,loop=True,height=500,width=700,quality="highest")

if selected=="EXPLORE DATA":
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding="ISO-8859-1")
    else:
        os.chdir(r"E:\data science\Airbnb Data Analysis")
        df = pd.read_csv("Airbnb_data.csv", encoding="ISO-8859-1")
    filepath=load_lottiefile("E:\data science\Airbnb Data Analysis\C.json")
    st.lottie(filepath,speed=1,reverse=False,loop=True,height=200,width=150,quality="highest")

    selected=option_menu( menu_title="",
        options=["View Data","Information"],
        icons=["distribute-vertical","postcard-fill"],
        orientation="horizontal",
        styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "15px"},
                               "container" : {"max-width": "800px"},
                               "nav-link-selected": {"background-color": "#121010"}})

    
    if selected=="View Data":
        if st.button("click to view Dataframe"):
            st.write(df)
    if selected=="Information":
        country = st.sidebar.multiselect('Select a Country',sorted(df['Country'].unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
         
        # TOP 10 PROPERTY TYPES BAR CHART
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                        title='Top 10 Property Types',
                        x='Listings',
                        y='Property_type',
                        orientation='h',
                        color='Property_type',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True) 
    
        # TOP 10 HOSTS BAR CHART
        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df2,
                        title='Top 10 Hosts with Highest number of Listings',
                        x='Listings',
                        y='Host_name',
                        orientation='h',
                        color='Host_name',
                        color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        
        
            
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1,
                        title='Total Listings in each Room_types',
                        names='Room_type',
                        values='counts',
                        color_discrete_sequence=px.colors.sequential.Rainbow
                    )
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)
        
        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='Country',
                            locationmode='country names',
                            color='Total_Listings',
                            color_continuous_scale=px.colors.sequential.Plasma,
                           
                            )
        fig.update_layout(height=1000,
                  width=1000)
 
        st.plotly_chart(fig,use_container_width=True)
if selected=="Insights":
    filepath=load_lottiefile("E:\data science\Airbnb Data Analysis\B.json")
    st.lottie(filepath,speed=1,reverse=False,loop=True,height=200,width=150,quality="highest")
    
    os.chdir(r"E:\data science\Airbnb Data Analysis")
    df = pd.read_csv("Airbnb_data.csv", encoding="ISO-8859-1")
    selected=option_menu( menu_title="",
        options=["Price on the basis of Room Type"],
        icons=["distribute-vertical"],
        orientation="horizontal",
        styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "15px"},
                               "container" : {"max-width": "800px"},
                               "nav-link-selected": {"background-color": "#121010"}})
    if selected=="Price on the basis of Room Type":
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
        country_df = df.groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter(data_frame=country_df,
           x='Country',y='Price',
           color='Country',
           size='Price',
           opacity=1,
           size_max=35,
           title='Avg Listing Price in each Countries')
        st.plotly_chart(fig)
        # HEADING 1
        st.markdown("## Price Analysis")  
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                        x='Room_type',
                        y='Price',
                        color='Price',
                        title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)

        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                        locations='Country',
                                        color= 'Price', 
                                        hover_data=['Price'],
                                        locationmode='country names',
                                        size='Price',
                                        title= 'Avg Price in  Country',
                                        color_continuous_scale='agsunset'
                            )
        fig.update_layout(height=1000,
                  width=1000)
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                        x='Room_type',
                        y='Availability_365',
                        color='Room_type',
                        title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
         
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                        locations='Country',
                                        color= 'Availability_365', 
                                        hover_data=['Availability_365'],
                                        locationmode='country names',
                                        size='Availability_365',
                                        title= 'Avg Availability in  Country',
                                        color_continuous_scale='agsunset'
                            )
        fig.update_layout(height=1000,width=1000)
        st.plotly_chart(fig,use_container_width=True)

       
if selected=="ADDITIONAL INFORMATION":
    selected=option_menu( menu_title="",
        options=["About Project","Technologies Used"],
        icons=["distribute-vertical","code"],
        menu_icon="play-fill",
        orientation="horizontal",
        styles={"nav-link": {"font-size": "12px", "text-align": "centre", "margin": "0.5px"},
                              "icon": {"font-size": "4x"},
                               "container" : {"max-width": "800px"},
                               "nav-link-selected": {"background-color": "#121010"}})
    if selected =="About Project":
        st.header(":white[**Objective**]")
        st.markdown(":white[**This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.**]")
        st.header(":white[**Procedure**]")
        st.markdown(":white[**1. MongoDB Connection and Data Retrieval**]")
        st.markdown(":white[**2. Data Cleaning and Preparation**]")
        st.markdown(":white[**3. Geospatial Visualization using Streamlit**]")
        st.markdown(":white[**4. Price Analysis and Visualization**]")
        st.markdown(":white[**5. Availability Analysis by Season**]")
        st.markdown(":white[**6. Location-Based Insights**]")
        st.markdown(":white[**7. Interactive Visualizations**]")
        st.markdown(":white[**8. Dashboard Creation -Power BI OR Tableau**]")
    if selected=="Technologies Used":
        st.header(":white[**1.Python**]")
        st.markdown("Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured particularly, procedural and functional programming, object-oriented, and concurrent programming.Python is widely used for web development, software development, data science, machine learning and artificial intelligence, and more. It is free and open-source software.")
        st.header(":white[**2.Pandas**]")
        st.markdown(":white[**Pandas is a Python library used for working with data sets. It has functions for analyzing, cleaning, exploring, and manipulating data. The name Pandas has a reference to both Panel Data, and Python Data Analysis**]")
        st.header(":white[**3.Plotly**]")
        st.markdown(":white[**Plotly is a free and open-source Python library for creating interactive, scientific graphs and charts. It can be used to create a variety of different types of plots, including line charts, bar charts, scatter plots, histograms, and more. Plotly is a popular choice for data visualization because it is easy to use and produces high-quality graphs. It is also very versatile and can be used to create a wide variety of different types of plots.**]")
        st.header(":white[**4.MongoDB Atlas**]")
        st.markdown(":white[**MongoDB Atlas is a multi-cloud database service that helps simplify the deployment and management of databases. It's a fully-managed cloud database that handles the complexity of deploying and managing MongoDB database deployments on Google Cloud.**}")
        st.header(":white[**5.Tableau**]")
        st.markdown(":white[**Tableau is a visual analytics platform that helps people and organizations use data to solve problems. It allows users to connect, analyze, and share their data.**]")
        st.header(":white[**6.Streamlit**]")
        st.markdown(":white[**Streamlit is an open-source app framework in python language. It helps us create beautiful web apps for data science and machine learning in a little time. It is compatible with major python libraries such as scikit-learn, keras, PyTorch, latex, numpy, pandas, matplotlib, etc.**]")