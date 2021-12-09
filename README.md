# Covid-19 News Headline Sentiment Analysis Goals

Goal 1: Use web scraping techniques discussed in class to generate a dataset that consists of Covid-19 related headlines for each state. \
Goal 2: Implement SentimentIntensityAnalyzer to apply sentiment analysis to each headline. \
Goal 3: Display the results for each state as a percentage of neutral, positive and negatives headlines. \
Tools: Python 3.9, SentimentIntensityAnalyzer (https://towardsdatascience.com/sentimental-analysis-using-vader-a3415fef7664)

# Files

There are a total of 7 files in this repository, but the news_sentiment_analysis.py is the main one of interest:  <br/>
  &nbsp; generate_dataset.py --> code that generates the datasets that contain Google news headlines for each U.S. state<br/>
  &nbsp; data_11_30_21.csv  --> dataset that contains Google news headlines for 11/30/21  <br/>
  &nbsp; data_12_1_21.csv --> dataset that contains Google news headlines for 12/1/21  <br/>
  &nbsp; news_sentiment_analysis.py --> code that applies sentiment analysis to each headline, generates a python dashboard displaying the results and calculates accuracy <br/>
  &nbsp; state_abbrev.csv --> file that contains state abbreviations, this will be used as a coordinate in the US map   <br/>
  &nbsp; test.csv --> test dataset consisting of radnomly selected 300 headlines, this is used to calculate our model's accuracy, precision and recall  <br/>
  &nbsp; vaccinations.csv --> contains vaccination rates for 50 U.S. states as of 12/6/21 <br/>
  
# Instructions 

1. Clone the repository in your directory of interest. To do this simply open the command line and enter:

 git clone https://github.com/bhullar5/CourseProject.git \
 Technically, you could simply just download the news_sentiment_analysis.py file since you don't need the others to run the analysis. 
 
2. Once you've cloned the repository into your directory of choice we want to make sure we have the necessary libraries to run this code. Please make sure you have the following packages/libraries installed:\
&nbsp; pandas\
&nbsp; beautifulsoup4\
&nbsp; numpy\
&nbsp; nltk\
&nbsp; plotly\
&nbsp; dash  \
&nbsp; dash-html-components\
&nbsp; dash-core-components\
&nbsp; openpyxl (this MAY need to be installed)

3. Once you've installed those files all you have to do is run the following script from the command line. Before your run the below code, make sure you specify the location of the file OR make you're already located in that specific folder that contains the file: \
&nbsp; python news_sentiment_analysis.py

4. After running the command in step 3, it will take a couple minutes for the analysis to work. Eventually you will get a series of warning messages, which can be ignored.

5. Finally, you will see a message towards the bottom: "Running on http://127.0.0.1:8050/". Copy paste http://127.0.0.1:8050/ (or whatever local server has been created) on your browser. This will then display the app. 

# Documentation Questions

This section will answer all of the questions mentioned in the course documentation portion of this project.

1) An overview of the function of the code (i.e., what it does and what it can be used for):\
There are two python files in the above repository:\
The generate_dataset.py file is used to generate a data by web scraping the Google news webpage. Once run, this code will import a csv file containing a series of Covid-19 related headlines for each U.S. state. The results are used in the actual sentiment analysis portion of this project. \
The news_sentiment_analysis.py file is used to analyze the results from the generate_dataset.py file. This file first goes through the csv file and creates three different variations of the original dataset (no stop words, only alphanumeric text and the default dataset). Once these datasets have been created, the SentimentIntensityAnalyzer is implemented to apply sentiment analysis to each dataset. The results of this analysis are used to aggregate percent values for the percentage of negative, positive and neutral headlines for each state and combine them with pre-existing vaccination rates for each state. Finally these values are displayed on a U.S. state map, so that users can see how vaccination rates and percent of positive/negative/neutral sentiments for each state. \
The main function of this project was to see how vaccination rates and the sentiments around Covid-19 (through Google news) vary across the various U.S. states. This can be extended to reflect counties or countries by simply changing the existing country dataset to a country or country dataset and then changing the choropleth map type.
----
2) Documentation of how the software is implemented with sufficient detail so that others can have a basic understanding of your code for future extension or any further improvement. \
&nbsp;Tools used: \
&nbsp;&nbsp;SentimentIntensityAnalyzer from nltk\
&nbsp;&nbsp;Python 3.9\
&nbsp;&nbsp;Python Dash\
&nbsp;&nbsp;The code has three stages.\
 \
Stage 1: In this stage we run the generate_dataset.py file to generate a new dataset that consists of the headlines for the 50 states for that given day. For example, if I run that file on 12/7/21, it will generate the dataset for that specific date. The code itself is fairly simple, and you can view the comments in the actual file to get a more detaield explanation. Basically, I used the package beautifulsoup that uses requests.get(some url) and returns the json for that specific url. The url itself is some varaition of "https://news.google.com/search?q=corona+virus+" with the state from the country dataset. We iterate through the country dataset by appending each state to the query that will be used in the request.get() request. We then store its results by parsing through the html to look for the headlines and finally creating a dataframe from it, which can be imported to your operating system. This code does take a very long time to generate, at least 1.5 hours. The expected outcome is a dataset consisting of 15,000 entries. I generated this dataset on 11/30/21 and 12/1/21 to get a total of 30,000 entires, these datasets were used in the analysis. \
 \
Stage 2: In this stage we go through the original dataset and create three datasets: one that removed stop words, one that only keeps alpha-numeric values and finally the default one. After this has been done, we simply apply the SentimentIntensityAnalyzer to each dataset. This will generate a tuple that consists of the sentiment intensity of positive, negative and neutral sentiments. It also contains a compound score, which is a normalized score of the previous three. I added multiple columns, one that classifies the headline with the sentiment intensity values, in which the highest intensity value from the three is used to determine the final classification. Another column uses the compound score for a similar classification, but instead it looks at the compound score and anything below -.05 is negative, above .05 is positive and between is neutral. Finally, the dataset is aggregated to group by each state and calculate the number/percent of positive headlines, negative headlines and netural headlines. \
 \
Stage 3: At this point we had enough data analysis on the sentiment, so it was time to calculate the accuracy rates. Since this was a brand new dataset, I had to create a test dataset myself by going through a subset of the data and classifying it as positive, negative or neutral. I ended up looking at a subset of 300 headlines randomly selected from the dataset and then going through each headline to categorize it as positive, negative or neutral. From this I calculated various different accuracy rates. Finally, the results from Stage 2 are displayed on a U.S. map using python's dash framework. I simply inputted the datasets created and then used the state abbreviation as a coordinate. The state avbbreviations were simply added to  When a user runs "python news_sentiment_analysis.py", they will be able to see this app on their local server. The user can then over the map to see what the vaccination rate, the positive/negativ/neutral percentages for headlines for a specific state.

----
3) Documentation of the usage of the software including either documentation of usages of APIs or detailed instructions on how to install and run a software, whichever is applicable.\
PLEASE LOOK AT THE INSTRUCTIONS SECTION FOR THIS
----
4) Brief description of contribution of each team member in case of a multi-person team.\
I was the only one on the team.
