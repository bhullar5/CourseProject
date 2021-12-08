#!/usr/bin/env python
# coding: utf-8

# The code below uses BeautifulSoup to web scrape a series of web pages. 
# Within the context of this project, these webpages contain Covid-19 related headlines for U.S. states
# For each state there are 300 headlines
# NOTE: Please change the path to match your laptops folder structure!!!!

# In[ ]:


import plotly.graph_objects as go
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

# countryList contains all 50 U.S. states
countryList = ["Alabama",
"Alaska",
"Arizona",
"Arkansas",
"California",
"Colorado",
"Connecticut",
"Delaware",
"Florida",
"Georgia",
"Hawaii",
"Idaho",
"Illinois",
"Indiana",
"Iowa",
"Kansas",
"Kentucky",
"Louisiana",
"Maine",
"Maryland",
"Massachusetts",
"Michigan",
"Minnesota",
"Mississippi",
"Missouri",
"Montana",
"Nebraska",
"Nevada",
"New Hampshire",
"New Jersey",
"New Mexico",
"New York",
"North Carolina",
"North Dakota",
"Ohio",
"Oklahoma",
"Oregon",
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee",
"Texas",
"Utah",
"Vermont",
"Virginia",
"Washington",
"West Virginia",
"Wisconsin",
"Wyoming"]

# headlines will contain all the headlines from the web scraping piece
# countries will contain the list of countries
# we will create a data frame from these lists
headlines = []
countries = []

# this is going to be the finL dataset containing headlines and countries
data = pd.DataFrame(columns = ['Headline', 'Country'])

for i in range(0, len(countryList)):
    
    # these are the three search queries
    
    # search: covid-19 state
    covid19URL = "https://news.google.com/search?q=covid-19+" + countryList[i].lower()
    
    # search: corona state
    covidURL = "https://news.google.com/search?q=corona+" + countryList[i].lower()
    
    # search: corona virus state
    coronaVirusURL = "https://news.google.com/search?q=corona+virus+" + countryList[i].lower()

    # get all the results for the specific queries with pauses between them 
    covid19URLpage = requests.get(covid19URL)
    time.sleep(3)
    covidURLpage = requests.get(covidURL)
    time.sleep(3)
    coronaVirusURLpage = requests.get(coronaVirusURL)
    time.sleep(3)

    # parse the returned json accordingly to get the text of interest, in this case thats the headlines
    covid19Soup = BeautifulSoup(covid19URLpage.content, "html.parser")
    covidSoup = BeautifulSoup(covidURLpage.content, "html.parser")
    coronaSoup = BeautifulSoup(coronaVirusURLpage.content, "html.parser")

    resultsCovid19 = covid19Soup.find(id="yDmH0d")
    job_elementsCovid19 = resultsCovid19.find("c-wiz", class_="zQTmif SSPGKf")
    h3_Covid19 = job_elementsCovid19.find_all("h3", class_="ipQwMb ekueJc RD0gLb")

    resultsCovid = covidSoup.find(id="yDmH0d")
    job_elementsCovid = resultsCovid.find("c-wiz", class_="zQTmif SSPGKf")
    h3_Covid = job_elementsCovid.find_all("h3", class_="ipQwMb ekueJc RD0gLb")

    resultsCorona = coronaSoup.find(id="yDmH0d")
    job_elementsCorona = resultsCorona.find("c-wiz", class_="zQTmif SSPGKf")
    h3_Corona = job_elementsCorona.find_all("h3", class_="ipQwMb ekueJc RD0gLb")

    x = list(map(lambda x: x.text, h3_Covid19))
    y = list(map(lambda y: y.text, h3_Corona))
    z = list(map(lambda z: z.text, h3_Covid))
    
    headlines = headlines + x
    headlines = headlines + y
    headlines = headlines + z
    len_headlines = len(x) + len(y) + len(z)

    countryValues = [countryList[i]] * len_headlines
    countries = countries + countryValues


# In[ ]:


import os

data_30 = pd.DataFrame(columns = ['Headline', 'Country'])
data_01 = pd.DataFrame(columns = ['Headline', 'Country'])
data = pd.DataFrame(columns = ['Headline', 'Country'])
data['Headline'] = headlines
data['Country'] = countries

path =r'C:\Users\sukhw\Desktop\CS 410\Final Project' # PLEASE change the path to match your
data.to_csv(os.path.join(path, 'data_12_1_21.csv'))  #you may change data_12_1_21 accordingly to match your date


# Now we will calculate the accuracy rates for each method. Since there isn't an actual test dataset available to us, I will simply be categorizing a subset of the data as positive, negative or neutral. Because our dataset is so small and I want to be able to properly categorize the data for the test dataset. Instead, we will take a subset of the data (3000 headlines) and then from the 3000 headlines, I will randomly sample 300 for the test set (300 headlines). 

# In[ ]:


from sklearn.model_selection import train_test_split

subset = data.sample(n=3000)

train, test = train_test_split(subset, test_size=0.1)
train = train.reset_index()
test = test.reset_index()

path =r'C:\Users\sukhw\Desktop\CS 410\Final Project'
train.to_csv(os.path.join(path, 'train.csv'))
test.to_csv(os.path.join(path, 'test.csv'))

