#!/usr/bin/env python
# coding: utf-8

# 1 READ THE DATASETS
# 
# The very first step is to read the datasets that have already been generated
# We have already created two datasets, data_11_30_21 and data_12_1_21 from Nov 30th and Dec 1st. 
#     one was generated on Nov 30th, the other on Dec 1st
# We simply join the two datasets to create one large dataset for two days worth of daya, giving us a total of 30000 entries
# NOTE: PLEASE edit the path listed below to match your folder structure!!!!

# In[79]:


import plotly.graph_objects as go
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

# read the data from your designated folder
data_30 = pd.read_csv('https://raw.githubusercontent.com/bhullar5/CourseProject/main/data_11_30_21.csv')
data_01 = pd.read_csv('https://raw.githubusercontent.com/bhullar5/CourseProject/main/data_12_1_21.csv') 
data = data_30.append(data_01)
data = data.reset_index()

# state_abbrev contains a list of state abbreviations, we just want the code from this dataset
state_abbrev =  pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')['code']

# this contains the vaccination rates for each state, this was copied from https://www.mayoclinic.org/coronavirus-covid-19/vaccine-tracker 
vaccination = pd.read_csv('https://raw.githubusercontent.com/bhullar5/CourseProject/main/vaccinations.csv')
vaccination['state_abbrev'] = state_abbrev


# 2 WORD PROCESSING
# The goal is to create three different datasets.
#   1 Dataset will include only alphanumeric values
#   2 Dataset with no stop words
#   3 The null dataset, basically everything is just lower case
#   

# In[80]:


# the following dataset SHOULD only contain alphanumeric values

headlines_2 = data['Headline']

j =0

# this will hold the final dataset
headlines_final =[]

# for the length of the list replace alphanumeric values with space

for i in range(0, len(headlines_2)):
    headlines_2[i]= headlines_2[i].lower()
    ## Code to remove digit with word pattern
    remove_1 = re.sub(r'([\d]+[a-zA-Z]+)|([a-zA-Z]+[\d]+)', "", headlines_2[i])
    ## Code to remove only digit patter
    remove_2 = re.sub(r"(^|\s)(\-?\d+(?:\.\d)*|\d+|[\d]+[A-Za-z]+)"," ", remove_1)
    
    remove_3 = re.sub(r"'","",remove_2)
        
    string_remove = re.sub('[^A-Za-z\']+', " ", remove_3)
    headlines_final.append(string_remove)


# 3. NLTK
# We will now use NLTK to first look for stop words and replace them AND also to apply sentiment analysis to the datasets

# In[81]:


# download these specific packages from the NLTK library
nltk.download(["names","stopwords","state_union", "twitter_samples", "movie_reviews", 
               "averaged_perceptron_tagger", "vader_lexicon", "punkt"])


# Remove all the stop words from the headlines

# In[82]:


stopwords = nltk.corpus.stopwords.words("english")
split_headline = []  #this will hold the split words as a list, 
                    #not containing stop words and any random stuff
join_headline = []

for i in range(0, len(headlines_final)):
    split_headline_i = headlines_final[i].split() #split the headline into different words
    
    alphabet_words = [w for w in split_headline_i if w.isalpha()] #remove non-alphabet words
    words = [w for w in alphabet_words if w not in stopwords] #remove stopwords
    
    join_headline_i = ' '.join(words) #join with a space 
    
    join_headline.append(join_headline_i)
    split_headline.append(words) #append the new list of words onto the split_headline list


# We will now apply sentiment analysis to each one of the headlines. We will create the following new columns in each dataset:
#     Neutral= neutral, neutral value 
#     Positive= positive, positive value
#     Negative= negative, negative value
#     Sentiment= sentiment_null, is it pos, neg, neu
#     Sentiment_C= sentiment_null_c, is it pos, neg, neu
#     Compound= compound_null, compound value
#     Neutral_Num= neutral_num, 0 or 1 (0 means false 1 means true)
#     Positive_Num= positive_num, 0 or 1 (0 means false 1 means true)
#     Negative_Num= negative_num, 0 or 1 (0 means false 1 means true)
#     Neutral_Num_C = sent_neu_num, 0 or 1 (0 means false 1 means true)
#     Positive_Num_C = sent_pos_num, 0 or 1 (0 means false 1 means true)
#     Negative_Num_C= sent_neg_num, 0 or 1 (0 means false 1 means true)

# In[83]:


sia = SentimentIntensityAnalyzer()

# this removes any non alphabetic values
neutral_headline = []
positive_headline = []
negative_headline = []
neutral_headline_num = []
positive_headline_num = []
negative_headline_num = []
sent_negheadline_num = []
sent_posheadline_num = []
sent_neuheadline_num = []
sentiment_headline = []
compound_headline = []
sentiment_headline_c = []

# remove all the stop words, its called join because we split the headline -> removed the stop word and then joined them
neutral_join = []
positive_join = []
negative_join = []
neutral_join_num = []
positive_join_num = []
negative_join_num = []
sent_negjoin_num = []
sent_posjoin_num = []
sent_neujoin_num = []
sentiment_join = []
compound_join = []
sentiment_join_c = []

# this is the default headline
neutral = []
positive = []
negative = []
neutral_num = []
positive_num = []
negative_num = []
sent_neg_num = []
sent_pos_num = []
sent_neu_num = []
sentiment_null = []
compound_null = []
sentiment_null_c = []

threshold = .05

# for i in range(0, len(headlines)):
for i in range(0, len(data['Headline'])):
    #df: data_headline, apply polarity scores to the headline i 
    headlines_polarity = sia.polarity_scores(data['Headline'][i])
    
    # assign the values to the neutral, positive, negative and compound columns
    neutral_headline.append(headlines_polarity['neu'])
    positive_headline.append(headlines_polarity['pos'])
    negative_headline.append(headlines_polarity['neg'])
    compound_headline.append(headlines_polarity['compound'])
    
    # assign the sentiment, negative, positive and neutral headlines are assinged values accordingly
    if negative_headline[i]>neutral_headline[i] and negative_headline[i]>positive_headline[i]:
        sentiment_headline.append('neg')
        negative_headline_num.append(1)
        positive_headline_num.append(0)
        neutral_headline_num.append(0)
    elif positive_headline[i]>neutral_headline[i] and positive_headline[i]>negative_headline[i]:
        sentiment_headline.append('pos')
        negative_headline_num.append(0)
        positive_headline_num.append(1)
        neutral_headline_num.append(0)
    elif neutral_headline[i]>positive_headline[i] and neutral_headline[i]>negative_headline[i]:
        sentiment_headline.append('neu')
        negative_headline_num.append(0)
        positive_headline_num.append(0)
        neutral_headline_num.append(1)
    else:
        sentiment_headline.append('equal')
        negative_headline_num.append(0)
        positive_headline_num.append(0)
        neutral_headline_num.append(0)
        
    # assign the sentiment, negative, positive and neutral headlines are assinged values accordingly NOTE this is based on the
    # compound threshold value 
    if compound_headline[i] >= .05:# if the value is >= .05 then its positive
        sentiment_headline_c.append('pos')
        sent_negheadline_num.append(0)
        sent_posheadline_num.append(1)
        sent_neuheadline_num.append(0)
    elif compound_headline[i] <= -.05:
        sentiment_headline_c.append('neg') # if the value is <= -.05 then its negative
        sent_negheadline_num.append(1)
        sent_posheadline_num.append(0)
        sent_neuheadline_num.append(0)
    else:
        sentiment_headline_c.append('neu') # otherwise its neutral
        sent_negheadline_num.append(0)
        sent_posheadline_num.append(0)
        sent_neuheadline_num.append(1)
        
        
        
    # df: data_join
    join_polarity = sia.polarity_scores(join_headline[i])
    
    # assign the values to the neutral, positive, negative and compound columns
    neutral_join.append(join_polarity['neu'])
    positive_join.append(join_polarity['pos'])
    negative_join.append(join_polarity['neg'])
    compound_join.append(join_polarity['compound'])
    
    # assign the sentiment, negative, positive and neutral headlines are assinged values accordingly
    if negative_join[i]>neutral_join[i] and negative_join[i]>positive_join[i]:
        sentiment_join.append('neg')
        negative_join_num.append(1)
        positive_join_num.append(0)
        neutral_join_num.append(0)
    elif positive_join[i]>neutral_join[i] and positive_join[i]>negative_join[i]:
        sentiment_join.append('pos')
        negative_join_num.append(0)
        positive_join_num.append(1)
        neutral_join_num.append(0)
    elif neutral_join[i]>positive_join[i] and neutral_join[i]>negative_join[i]:
        sentiment_join.append('neu')
        negative_join_num.append(0)
        positive_join_num.append(0)
        neutral_join_num.append(1)
    else:
        sentiment_join.append('equal')
        negative_join_num.append(0)
        positive_join_num.append(0)
        neutral_join_num.append(0)
    
    # assign the sentiment, negative, positive and neutral headlines are assinged values accordingly NOTE this is based on the
    # compound threshold value 
    if compound_join[i] >= .05:
        sentiment_join_c.append('pos')
        sent_negjoin_num.append(0)
        sent_posjoin_num.append(1)
        sent_neujoin_num.append(0)
    elif compound_join[i] <= -.05:
        sentiment_join_c.append('neg')
        sent_negjoin_num.append(1)
        sent_posjoin_num.append(0)
        sent_neujoin_num.append(0)
    else:
        sentiment_join_c.append('neu')
        sent_negjoin_num.append(0)
        sent_posjoin_num.append(0)
        sent_neujoin_num.append(1)
    
    # df: data 
    polarity = sia.polarity_scores(data['Headline'][i])
    
    # assign the values to the neutral, positive, negative and compound columns
    neutral.append(polarity['neu'])
    positive.append(polarity['pos'])
    negative.append(polarity['neg'])
    compound_null.append(polarity['compound'])
    
    # assign the sentiment, negative, positive and neutral headlines are assinged values accordingly
    if negative[i]>neutral[i] and negative[i]>positive[i]:
        sentiment_null.append('neg')
        negative_num.append(1)
        positive_num.append(0)
        neutral_num.append(0)
    elif positive[i]>neutral[i] and positive[i]>negative[i]:
        sentiment_null.append('pos')
        negative_num.append(0)
        positive_num.append(1)
        neutral_num.append(0)
    elif neutral[i]>positive[i] and neutral[i]>negative[i]:
        sentiment_null.append('neu')
        negative_num.append(0)
        positive_num.append(0)
        neutral_num.append(1)
    else:
        sentiment_null.append('equal')
        negative_num.append(0)
        positive_num.append(0)
        neutral_num.append(0)
        
    # assign the sentiment, negative, positive and neutral headlines are assinged values accordingly NOTE this is based on the
    # compound threshold value     
    if compound_null[i] >= .05:
        sentiment_null_c.append('pos')
        sent_neg_num.append(0)
        sent_pos_num.append(1)
        sent_neu_num.append(0)
    elif compound_null[i] <= -.05:
        sentiment_null_c.append('neg')
        sent_neg_num.append(1)
        sent_pos_num.append(0)
        sent_neu_num.append(0)
    else:
        sentiment_null_c.append('neu')
        sent_neg_num.append(0)
        sent_pos_num.append(0)
        sent_neu_num.append(1)


# In[84]:


# data: this is the default headline, 
# we will assign the lists accordingly from above to the data data frame
data['Neutral'] = neutral
data['Positive'] = positive
data['Negative'] = negative
data['Sentiment'] = sentiment_null
data['Sentiment_C'] = sentiment_null_c
data['Compound'] = compound_null
data['Neutral_Num'] = neutral_num
data['Positive_Num'] = positive_num
data['Negative_Num'] = negative_num
data['Neutral_Num_C'] = sent_neu_num
data['Positive_Num_C'] = sent_pos_num
data['Negative_Num_C'] = sent_neg_num
 
# data_headline: this removes any non alphabetic values, 
# we will assign the lists accordingly from above to the data data frame
data_headline = pd.DataFrame(columns = ['Headline', 'Country'])
data_headline['Headline'] = data['Headline']
data_headline['Country'] = data['Country']
data_headline['Neutral'] = neutral_headline
data_headline['Positive'] = positive_headline
data_headline['Negative'] = negative_headline
data_headline['Sentiment'] = sentiment_headline
data_headline['Sentiment_C'] = sentiment_headline_c
data_headline['Compound'] = compound_headline
data_headline['Neutral_Num'] = neutral_headline_num
data_headline['Positive_Num'] = positive_headline_num
data_headline['Negative_Num'] = negative_headline_num
data_headline['Neutral_Num_C'] = sent_neuheadline_num
data_headline['Positive_Num_C'] = sent_posheadline_num
data_headline['Negative_Num_C'] = sent_negheadline_num

# data_join: join concatenates all the words so that they do not contain any stop words, 
# we will assign the lists accordingly from above to the data data frame
data_join = pd.DataFrame(columns = ['Headline', 'Country'])
data_join['Headline'] = join_headline
data_join['Country'] = data['Country']
data_join['Neutral'] = neutral_join
data_join['Positive'] = positive_join
data_join['Negative'] = negative_join
data_join['Sentiment'] = sentiment_join
data_join['Sentiment_C'] = sentiment_join_c
data_join['Compound'] = compound_join
data_join['Neutral_Num'] = neutral_join_num
data_join['Positive_Num'] = positive_join_num
data_join['Negative_Num'] = negative_join_num
data_join['Neutral_Num_C'] = sent_neujoin_num
data_join['Positive_Num_C'] = sent_posjoin_num
data_join['Negative_Num_C'] = sent_negjoin_num


# Now we will group by state and calculate the percentage of negative, positive and neutral headlines. Also we'll include the number of headlines as well. 
# Along with this we'll add the vaccination rate.

# In[85]:


# DEFAULT DATA
# take the mean of the data df grouped by country
average_data = pd.DataFrame(data.groupby(by=["Country"]).mean())

# reset the index to 0-len(average_data)
average_data.reset_index(inplace=True)

# this is the default dataset, we simply 

avg_sentiment= []
avg_sentiment_c = []

# for i in range 0 to the length of average_data
for i in range(0, len(average_data)):
    
    # based on the grouped means for each country, assign negative, positive or neutral
    if average_data['Negative'][i]>average_data['Neutral'][i] and average_data['Negative'][i]>average_data['Positive'][i]:
        avg_sentiment.append('Negative')
    elif average_data['Positive'][i]>average_data['Neutral'][i] and average_data['Positive'][i]>average_data['Negative'][i]:
        avg_sentiment.append('Positive')
    elif average_data['Neutral'][i]>average_data['Positive'][i] and average_data['Neutral'][i]>average_data['Negative'][i]:
        avg_sentiment.append('Neutral')
    else:
        avg_sentiment.append('Equal')
        
    # based on the grouped mean value for the compound for each country, assign negative, positive or neutral    
    if average_data['Compound'][i] >= .05:
        avg_sentiment_c.append('Positive')
    elif average_data['Compound'][i] <= -.05:
        avg_sentiment_c.append('Negative')
    else:
        avg_sentiment_c.append('Neutral')

# data_sent_count sums the values in negative_num, neutral_num, positive_num, 
# negative_num_c, neutral_num_c, positive_num_c
data_sent_count = data[['Country','Negative_Num', 'Positive_Num', 'Neutral_Num', 
                        'Negative_Num_C', 'Positive_Num_C', 'Neutral_Num_C']].groupby(["Country"]).sum()
data_sent_count.reset_index(inplace=True)

# add all of the above lists to the average_data dataset
average_data['State_Abbrev'] = state_abbrev
average_data['Sentiment'] = avg_sentiment        
average_data['Sentiment_C'] = avg_sentiment_c
average_data['Negative_Total'] = data_sent_count['Negative_Num']
average_data['Positive_Total'] = data_sent_count['Positive_Num']
average_data['Neutral_Total'] = data_sent_count['Neutral_Num']
average_data['Negative_Total_C'] = data_sent_count['Negative_Num_C']
average_data['Positive_Total_C'] = data_sent_count['Positive_Num_C']
average_data['Neutral_Total_C'] = data_sent_count['Neutral_Num_C']
average_data['Vaccination'] = vaccination['vaccination_rate']

average_data['P_Negative_Total_C'] = round((data_sent_count['Negative_Num_C']/(data_sent_count['Positive_Num_C']
                                                                             +data_sent_count['Negative_Num_C']
                                                                             +data_sent_count['Neutral_Num_C']))*100,2)

average_data['P_Positive_Total_C'] = round((data_sent_count['Positive_Num_C']/(data_sent_count['Positive_Num_C']
                                                                             +data_sent_count['Negative_Num_C']
                                                                             +data_sent_count['Neutral_Num_C']))*100,2)

average_data['P_Neutral_Total_C'] = round((data_sent_count['Neutral_Num_C']/(data_sent_count['Positive_Num_C']
                                                                           +data_sent_count['Negative_Num_C']
                                                                           +data_sent_count['Neutral_Num_C']))*100,2)

average_data['P_Negative_Total'] = round((data_sent_count['Negative_Num']/(data_sent_count['Positive_Num']
                                                                             +data_sent_count['Negative_Num']
                                                                             +data_sent_count['Neutral_Num']))*100,2)

average_data['P_Positive_Total'] = round((data_sent_count['Positive_Num']/(data_sent_count['Positive_Num']
                                                                             +data_sent_count['Negative_Num']
                                                                             +data_sent_count['Neutral_Num']))*100,2)

average_data['P_Neutral_Total'] = round((data_sent_count['Neutral_Num']/(data_sent_count['Positive_Num']
                                                                           +data_sent_count['Negative_Num']
                                                                           +data_sent_count['Neutral_Num']))*100,2)

average_data['text'] = 'Sentiment Analysis<br>Negative: '+ average_data['P_Negative_Total_C'].apply(str) + '%' + '<br>' +                            'Positive: '+ average_data['P_Positive_Total_C'].apply(str) + '%' + '<br>' +                            'Neutral: '+ average_data['P_Neutral_Total_C'].apply(str) + '%' + '<br>'

#----------------------------------------------------------------------------------------------------------------------

# ALPHANUMERIC HEADLINE
# take the mean of the data_headline df grouped by country
average_data_headline = pd.DataFrame(data_headline.groupby(by=["Country"]).mean())

# reset the index to 0-len(average_data_headline)
average_data_headline.reset_index(inplace=True)

headline_sentiment = []
headline_sentiment_c = []

# for i in range 0 to the length of average_data
for i in range(0, len(average_data)):
    if average_data_headline['Negative'][i]>average_data_headline['Neutral'][i] and average_data_headline['Negative'][i]>average_data_headline['Positive'][i]:
        headline_sentiment.append('Negative')
    elif average_data_headline['Positive'][i]>average_data_headline['Neutral'][i] and average_data_headline['Positive'][i]>average_data_headline['Negative'][i]:
        headline_sentiment.append('Positive')
    elif average_data_headline['Neutral'][i]>average_data_headline['Positive'][i] and average_data_headline['Neutral'][i]>average_data_headline['Negative'][i]:
        headline_sentiment.append('Neutral')
    else:
        headline_sentiment.append('Equal')
        
    if average_data_headline['Compound'][i] >= .05:
        headline_sentiment_c.append('Positive')
    elif average_data_headline['Compound'][i] <= -.05:
        headline_sentiment_c.append('Negative')
    else:
        headline_sentiment_c.append('Neutral')

# headline_sent_count sums the values in negative_num, neutral_num, positive_num, 
# negative_num_c, neutral_num_c, positive_num_c
headline_sent_count = data_headline[['Country','Negative_Num', 'Positive_Num', 'Neutral_Num',
                                    'Negative_Num_C', 'Positive_Num_C', 'Neutral_Num_C']].groupby(["Country"]).sum()
headline_sent_count.reset_index(inplace=True)

# add all of the above lists to the average_data_headline dataset
average_data_headline['State_Abbrev'] = state_abbrev
average_data_headline['Sentiment'] = headline_sentiment
average_data_headline['Sentiment_C'] = headline_sentiment_c
average_data_headline['Negative_Total'] = headline_sent_count['Negative_Num']
average_data_headline['Positive_Total'] = headline_sent_count['Positive_Num']
average_data_headline['Neutral_Total'] = headline_sent_count['Neutral_Num']
average_data_headline['Negative_Total_C'] = headline_sent_count['Negative_Num_C']
average_data_headline['Positive_Total_C'] = headline_sent_count['Positive_Num_C']
average_data_headline['Neutral_Total_C'] = headline_sent_count['Neutral_Num_C']
average_data_headline['Vaccination'] = vaccination['vaccination_rate']

average_data_headline['P_Negative_Total_C'] = round((headline_sent_count['Negative_Num_C']/(headline_sent_count['Positive_Num_C']
                                                                             +headline_sent_count['Negative_Num_C']
                                                                             +headline_sent_count['Neutral_Num_C']))*100,2)
average_data_headline['P_Positive_Total_C'] = round((headline_sent_count['Positive_Num_C']/(headline_sent_count['Positive_Num_C']
                                                                             +headline_sent_count['Negative_Num_C']
                                                                             +headline_sent_count['Neutral_Num_C']))*100,2)
average_data_headline['P_Neutral_Total_C'] = round((headline_sent_count['Neutral_Num_C']/(headline_sent_count['Positive_Num_C']
                                                                           +headline_sent_count['Negative_Num_C']
                                                                           +headline_sent_count['Neutral_Num_C']))*100,2)
average_data_headline['P_Negative_Total'] = round((headline_sent_count['Negative_Num']/(headline_sent_count['Positive_Num']
                                                                             +headline_sent_count['Negative_Num']
                                                                             +headline_sent_count['Neutral_Num']))*100,2)
average_data_headline['P_Positive_Total'] = round((headline_sent_count['Positive_Num']/(headline_sent_count['Positive_Num']
                                                                             +headline_sent_count['Negative_Num']
                                                                             +headline_sent_count['Neutral_Num']))*100,2)
average_data_headline['P_Neutral_Total'] = round((headline_sent_count['Neutral_Num']/(headline_sent_count['Positive_Num']
                                                                           +headline_sent_count['Negative_Num']
                                                                           +headline_sent_count['Neutral_Num']))*100,2)

average_data_headline['text'] = 'Sentiment Analysis<br>Negative: '+ average_data_headline['P_Negative_Total_C'].apply(str) + '%' + '<br>' +                            'Positive: '+ average_data_headline['P_Positive_Total_C'].apply(str) + '%' + '<br>' +                            'Neutral: '+ average_data_headline['P_Neutral_Total_C'].apply(str) + '%' + '<br>'

#-----------------------------------------------------------------------------------------------

# 
# take the mean of the data_join df grouped by country
average_data_join = pd.DataFrame(data_join.groupby(by=["Country"]).mean())

# reset the index to 0-len(average_data_join)
average_data_join.reset_index(inplace=True)

join_sentiment = []
join_sentiment_c = []

# for i in range 0 to the length of average_data
for i in range(0, len(average_data)):
    # this just looks at the highest value from negative, positive and netural and assigns the sentiment value
    if average_data_join['Negative'][i]>average_data_join['Neutral'][i] and average_data_join['Negative'][i]>average_data_join['Positive'][i]:
        join_sentiment.append('Negative')
    elif average_data_join['Positive'][i]>average_data_join['Neutral'][i] and average_data_join['Positive'][i]>average_data_join['Negative'][i]:
        join_sentiment.append('Positive')
    elif average_data_join['Neutral'][i]>average_data_join['Positive'][i] and average_data_join['Neutral'][i]>average_data_join['Negative'][i]:
        join_sentiment.append('Neutral')
    else:
        join_sentiment.append('Equal')
    
    # this looks at the compound value and assigns accordingly
    if average_data_join['Compound'][i] >= .05:
        join_sentiment_c.append('Positive')
    elif average_data_join['Compound'][i] <= -.05:
        join_sentiment_c.append('Negative')
    else:
        join_sentiment_c.append('Neutral')

# join_sent_count sums the values in negative_num, neutral_num, positive_num, 
# negative_num_c, neutral_num_c, positive_num_c
join_sent_count = data_join[['Country', 'Negative_Num', 'Positive_Num', 'Neutral_Num',
                             'Negative_Num_C', 'Positive_Num_C', 'Neutral_Num_C']].groupby(["Country"]).sum()
join_sent_count.reset_index(inplace=True)

# add all of the above lists to the average_data_join dataset
average_data_join['State_Abbrev'] = state_abbrev
average_data_join['Sentiment'] = join_sentiment
average_data_join['Sentiment_C'] = join_sentiment_c
average_data_join['Negative_Total'] = join_sent_count['Negative_Num']
average_data_join['Positive_Total'] = join_sent_count['Positive_Num']
average_data_join['Neutral_Total'] = join_sent_count['Neutral_Num']
average_data_join['Negative_Total_C'] = join_sent_count['Negative_Num_C']
average_data_join['Positive_Total_C'] = join_sent_count['Positive_Num_C']
average_data_join['Neutral_Total_C'] = join_sent_count['Neutral_Num_C']
average_data_join['Vaccination'] = vaccination['vaccination_rate']

average_data_join['P_Negative_Total_C'] = round((join_sent_count['Negative_Num_C']/(join_sent_count['Positive_Num_C']
                                                                             +join_sent_count['Negative_Num_C']
                                                                             +join_sent_count['Neutral_Num_C']))*100,2)
average_data_join['P_Positive_Total_C'] = round((join_sent_count['Positive_Num_C']/(join_sent_count['Positive_Num_C']
                                                                             +join_sent_count['Negative_Num_C']
                                                                             +join_sent_count['Neutral_Num_C']))*100,2)
average_data_join['P_Neutral_Total_C'] = round((join_sent_count['Neutral_Num_C']/(join_sent_count['Positive_Num_C']
                                                                           +join_sent_count['Negative_Num_C']
                                                                           +join_sent_count['Neutral_Num_C']))*100,2)
average_data_join['P_Negative_Total'] = round((join_sent_count['Negative_Num']/(join_sent_count['Positive_Num']
                                                                             +join_sent_count['Negative_Num']
                                                                             +join_sent_count['Neutral_Num']))*100,2)
average_data_join['P_Positive_Total'] = round((join_sent_count['Positive_Num']/(join_sent_count['Positive_Num']
                                                                             +join_sent_count['Negative_Num']
                                                                             +join_sent_count['Neutral_Num']))*100,2)
average_data_join['P_Neutral_Total'] = round((join_sent_count['Neutral_Num']/(join_sent_count['Positive_Num']
                                                                           +join_sent_count['Negative_Num']
                                                                           +join_sent_count['Neutral_Num']))*100,2)
average_data_join['text'] = 'Sentiment Analysis<br>Negative: '+ average_data_join['P_Negative_Total_C'].apply(str) + '%' + '<br>' +                            'Positive: '+ average_data_join['P_Positive_Total_C'].apply(str) + '%' + '<br>' +                            'Neutral: '+ average_data_join['P_Neutral_Total_C'].apply(str) + '%' + '<br>'


# The code chunk below has been commented out, but its purpose is to display the interactive plotly maps for each dataset. This is an alternative to the dash portion, just in case the dash portion doesn't work

# In[20]:


# ----------------------------------------------------------------------------------------------------------------------

# import plotly.graph_objects as go

# import pandas as pd

# # the join dataset concatenates all the words that do not contain any stop words

# fig = go.Figure(data=go.Choropleth(
#     locations=average_data_join['State_Abbrev'], # Spatial coordinates
#     z = average_data_join['Vaccination'].astype(float), # Data to be color-coded
#     text = average_data_join['text'],
#     locationmode = 'USA-states', # set of locations match entries in `locations`
#     colorscale = 'Greens',
#     colorbar_title = "% Vaccination",
# ))

# fig.update_layout(
#     title_text = 'Sentiment Analysis of Dataset Containing No Stop Words',
#     geo_scope='usa', # limite map scope to USA
# )

# fig.show()


# In[21]:


# # average_data_headline contains headlines that have no non-alphabetic characters

# fig2 = go.Figure(data=go.Choropleth(
#     locations=average_data_headline['State_Abbrev'], # Spatial coordinates
#     z = average_data_headline['Vaccination'].astype(float), # Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries in `locations`,
#     text = average_data_headline['text'],
#     colorscale = 'Blues',
#     colorbar_title = "% Vaccination",
# ))

# fig2.update_layout(
#     title_text = 'Sentiment Analysis of Dataset Containing Only Alphabet Characters',
#     geo_scope='usa', # limite map scope to USA
# )

# fig2.show()


# In[42]:


# # the average_data contains the default headlines, just lowercased

# fig3 = go.Figure(data=go.Choropleth(
#     locations=average_data['State_Abbrev'], # Spatial coordinates
#     z = average_data['Vaccination'].astype(float), # Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries in `locations`,
#     text = average_data['text'],
#     colorscale = 'Reds',
#     colorbar_title = "% Vaccination",
# ))

# fig3.update_layout(
#     title_text = 'Sentiment Analysis of the Default Dataset',
#     geo_scope='usa', # limite map scope to USA
# )

# fig3.show()


# ----------------------------------------------------------------------------------------------------------------------


# I implemented the following tutorial: https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4
# The code below generates the dashboard that will display the results from the datasets generated above.

# Calculate precision and recall:
#  
#  Accuracy = (True Positive)/ Total 
#  
#  Precision = (True Positive)/(True Positive + False Positive)
#  
#  Recall = (True Positive)/(True Positive + False Negative)
#  
# We will also look at overall accuracy, accuracy of negative, positive and neutral predictions against the actual values.

# In[91]:


test = pd.read_csv('https://raw.githubusercontent.com/bhullar5/CourseProject/main/test.csv') 

true_positive = []
true_positive_neu = []
false_positive = []
false_positive_neu = []
false_negative = []
false_negative_neu = []
accuracy = []

for i in range(0, len(test)):
    
    if test['Actual'][i] == 1 and test['Sentiment_C'][i] == 'pos':
        true_positive.append(1)
    else:
        true_positive.append(0)
        
    if test['Actual'][i] == -1 and test['Sentiment_C'][i] == 'pos':
        false_positive.append(1)
    else:
        false_positive.append(0)
     
    if test['Actual'][i] == 1 and test['Sentiment_C'][i] == 'neg':
        false_negative.append(1)
    else:
        false_negative.append(0)
        
    if test['Actual'][i] == 1 and test['Sentiment_C'][i] == 'pos':
        accuracy.append(1)
    elif test['Actual'][i] == -1 and test['Sentiment_C'][i] == 'neg':
        accuracy.append(1)
    elif test['Actual'][i] == 0 and test['Sentiment_C'][i] == 'neu':
        accuracy.append(1)
    else:
        accuracy.append(0)
        
    if test['Actual'][i] == 0 and test['Sentiment_C'][i] == 'neu':
        true_positive_neu.append(1)
    else:
        true_positive_neu.append(1)
    
    if test['Actual'][i] == -1 and test['Sentiment_C'][i] == 'neu':
        false_positive_neu.append(1)
    else:
        false_positive_neu.append(0)
        
    if test['Actual'][i] == 0 and test['Sentiment_C'][i] == 'neg':
        false_negative_neu.append(1)
    else:
        false_negative_neu.append(0)
        
test['TP'] = true_positive
test['FP'] = false_positive
test['FN'] = false_negative

test['TP_neu'] = true_positive_neu
test['FP_neu'] = false_positive_neu
test['FN_neu'] = false_negative_neu

test['Accuracy'] = accuracy

neutral_df = test[test['Actual']==0]
neutral_predict = neutral_df[neutral_df['Sentiment_C'] == 'neu']

positive_df = test[test['Actual']==1]
positive_predict = positive_df[positive_df['Sentiment_C'] == 'pos']

negative_df = test[test['Actual']==-1]
negative_predict = negative_df[negative_df['Sentiment_C'] == 'neg']


# In[92]:


precision = test['TP'].sum()/(test['FP'].sum() + test['TP'].sum())
recall = test['TP'].sum()/(test['FN'].sum() + test['TP'].sum())
accuracy = test['Accuracy'].sum()/len(test)

precision_neu = test['TP_neu'].sum()/(test['FP_neu'].sum() + test['TP_neu'].sum())
recall_neu = test['TP_neu'].sum()/(test['FN_neu'].sum() + test['TP_neu'].sum())

neutral_accuracy = round((len(neutral_predict)/len(neutral_df))*100,2)
positive_accuracy = round((len(positive_predict)/len(positive_df))*100,2)
negative_accuracy = round((len(negative_predict)/len(negative_df))*100,2)

print("\nWhen calculating the precision and recall between positive and negative values, we get these results: ")
print("Precision is: ", round(precision*100,2), "%")
print("Recall is: ", round(recall*100,2), "%")

print("\nWhen calculating the precision and recall between neutral and negative values, we get these results: ")
print("Precision (Neutral) is: ", round(precision_neu*100,2), "%")
print("Recall (Neutral) is: ", round(recall_neu*100,2), "%")

print("\nWhen can calculate the overall accuracy where we calculate how many overall matches, we get these results: ")
print("Accuracy is: ", round(accuracy*100,2), "%")
print("Neutral Accuracy is: ", neutral_accuracy, "%")
print("Positive Accuracy is: ", positive_accuracy, "%")
print("Negative Accuracy is: ", negative_accuracy, "%")


# The code below uses the dash to generate a dashboard that will display the results of the three variations of the sentiment analysis on the datasets. 
# The following tutorial was implemented to make this work: https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4

# In[ ]:



app = dash.Dash()

df = px.data.stocks()

# citation: https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Covid-19 News Headline Sentiment Analysis by U.S. State', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
    html.Div(children='To view the vaccination rate and the corresponding sentiment analysis, please hover over the state.You will then be able to see the vaccination rate, state, and the percentage of negative, positive, or neutral headlines.', style={
        'textAlign': 'center'
    }),

        dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':'Headlines: No Stop Words', 'value':'GRAPH1' },
            {'label': 'Headlines: Non-alphabetic Characters Removed', 'value':'GRAPH2'},
            {'label': 'Headlines: Default Headlines-Lowercase', 'value':'GRAPH3'},
            ],
        value = 'GOOG'),
        dcc.Graph(id = 'bar_plot')
    ])

    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_value):

    if (dropdown_value == 'GRAPH1'):  # dataset that doesn't contain stop words
        fig = go.Figure([go.Choropleth(
            locations=average_data_join['State_Abbrev'], # Spatial coordinates
            z = average_data_join['Vaccination'].astype(float), # Data to be color-coded
            text = average_data_join['text'],
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Greens',
            colorbar_title = "% Vaccination"
        )])

        fig.update_layout(
            title_text = 'Sentiment Analysis of Dataset Containing No Stop Words',
            geo_scope='usa', # limite map scope to USA
        )
        
        description = "This dataset "

        fig = fig
    elif (dropdown_value == 'GRAPH2'): # datasest that doesn't contain any alphabetical letters
        fig2 = go.Figure([go.Choropleth(
            locations=average_data_headline['State_Abbrev'], # Spatial coordinates
            z = average_data_headline['Vaccination'].astype(float), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`,
            text = average_data_headline['text'],
            colorscale = 'Blues',
            colorbar_title = "% Vaccination"
        )])

        fig2.update_layout(
            title_text = 'Sentiment Analysis of Dataset Containing Only Alphabet Characters',
            geo_scope='usa', # limite map scope to USA
        )

        fig = fig2
        
    else: # the default dataset
        fig3 = go.Figure([go.Choropleth(
            locations=average_data['State_Abbrev'], # Spatial coordinates
            z = average_data['Vaccination'].astype(float), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`,
            text = average_data['text'],
            colorscale = 'Reds',
            colorbar_title = "% Vaccination",
        )])

        fig3.update_layout(
            title_text = 'Sentiment Analysis of the Default Dataset',
            geo_scope='usa', # limite map scope to USA
        )

        fig = fig3
        
    return fig



if __name__ == '__main__': 
    app.run_server()

