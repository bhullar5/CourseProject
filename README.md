# Covid-19 News Headline Sentiment Analysis Goals

Goal 1: Use web scraping techniques discussed in class to generate a dataset that consists of Covid-19 related headlines for each state.
Goal 2: Implement SentimentIntensityAnalyzer to apply sentiment analysis to each headline.
Goal 3: Display the results for each state as a percentage of neutral, positive and negatives headlines.
Tools: Python 3.9, SentimentIntensityAnalyzer (https://towardsdatascience.com/sentimental-analysis-using-vader-a3415fef7664) 

# Files

There are a total of 9 files in this repository:  <br/>
  generate_dataset.py --> code that generates the datasets that contain Google news headlines <br/>
  data_11_30_21.csv  --> dataset that contains Google news headlines for 11/30/21  <br/>
  data_12_1_21.csv --> dataset that contains Google news headlines for 12/1/21  <br/>
  news_sentiment_analysis.py --> code that applies sentiment analysis to each headline  <br/>
  state_abbrev.csv --> file that contains state abbreviations, this will be used as a coordinate in the US map   <br/>
  test.csv --> test dataset consisting of radnomly selected 300 headlines, this is used to calculate our model's accuracy, precision and recall  <br/>
  vaccinations.csv --> contains vaccination rates for 50 U.S. states as of 12/6/21 <br/>
  
# Instructions 

1. Clone the repository in your directory of interest. To do this simply open the command line and enter:

 git clone https://github.com/bhullar5/CourseProject.git 
 
2. Once you've cloned the repository into your directory of choice we want to make sure we have the necessary libraries to run this code. Please make sure you have the following packages/libraries installed:\
pandas\
beautifulsoup4\
numpy\
nltk\
plotly\
dash  \
dash-html-components\
dash-core-components

3. Once you've installed those files all you have to do is run the following script from the command line. Make sure you specify the location of the file OR make you're already located in that specific folder: \
python news_sentiment_analysis.py
