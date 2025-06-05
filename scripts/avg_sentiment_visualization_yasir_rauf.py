"""This script is part of our Digital Humanities Mini Project 3, where we are exploring different ways of visualizing data using Python.
In this script, I first load the avg_sentiment_results.csv file located inside the data/sentiment_analysis folder of our repository
FASDH25-portfolio3 as a pandas DataFrame. Then, I defined a function to categorize numeric average sentiment into Negative, Neutral, or
Positive groups to simplify the analysis. Focusing on two specific months, October 2023 and January 2024, I then filtered the data accordingly.
Next, I grouped the data by month and sentiment category to count how many articles fell into each group, then calculated the percentage
distribution to compare relative sentiment changes between these two months. Finally, I used Plotly Express to create and display a grouped
bar chart. I also saved the bar chart as a html and png file in the graphs folder inside our repository FASDH25-portfolio3."""

# Help was taken from ChatGPT while creating this Visualization script see ChatGPT Solution No. 9 in in "AI_Documentation_yasir_rauf" document inside the AI Documentation folder

# importing the required libaries for visualization
import pandas as pd
import plotly.express as px

# Loading our avg_sentiment_results.csv file as a panda dataframe
df = pd.read_csv("../data/dataframes/sentiment-analysis/avg_sentiment_results.csv")

# Printing the head of the dataframe to explore columns and rows
print(df.head())

# Defining a function that converts numeric average sentiment into categorical sentiment labels: Negative, Neutral, and Positive. Grouping
# our average sentiment scores into categories will make it easier for us to analyze and visualize our sentiment distribution.
def label_sentiment(score):
    if 0 <= score < 0.5:
        return 'Negative'
    elif 0.5 <= score < 1.5:
        return 'Neutral'
    elif 1.5 <= score <= 2:
        return 'Positive'
    
# Applying the label_sentiment function to the avg_sentiment column and creating a new column sentiment_label in the DataFrame. It is essential because it prepares
# the data by categorizing sentiments for grouping and comparison.
df['sentiment_label'] = df['avg_sentiment'].apply(label_sentiment)

# Filtering the October 2023 and January 2024 articles to focus on our analysis on these two specific months to compare sentiment changes over time.
filtered_df = df[df['year_month'].isin(['2023-10', '2024-01'])]

# Grouping by year_month and sentiment_label to get counts. This aggregates data so we can see the distribution of sentiments per month.
grouped = filtered_df.groupby(['year_month', 'sentiment_label']).size().reset_index(name='count')

# Calculating percentage per sentiment per month. It normalizes the data to percentages, allowing for relative comparison between months regardless of different article volumes.
grouped['percentage'] = grouped.groupby('year_month')['count'].transform(lambda x: (x / x.sum()) * 100)

# Creating a grouped bar chart where the x-axis is the sentiment category, the y-axis is the percentage of articles, and bars are colored by month.
fig = px.bar(
    grouped,
    x='sentiment_label',
    y='percentage',
    color='year_month',
    barmode='group',
    title='Relative Sentiment Distribution: October 2023 vs January 2024',
    labels={
        'sentiment_label': 'Sentiment',
        'percentage': 'Percentage of Articles',
        'year_month': 'Month'})

# Display the bar chart
fig.show()

# Saving our graph as html and png file inside graphs folder of our repository FASDH25-portfolio3
fig.write_html("../graphs/sentiment_distribution_oct2023_jan2024.html")
fig.write_image("../graphs/sentiment_distribution_oct2023_jan2024.png")


