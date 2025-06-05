"""This script is a part of our Digital Humanities Mini Project No. 3, where we are learning different ways to visualize data using Python.
In this script, I am exploring different methods to visualize my own created DataFrame named "avg_sentiment_results.csv", which is located inside the
data/sentiment analysis folder of FASDH25-portfolio3 repository. I start by creating a bar chart using absolute counts, then move on to relative counts,
and finally, we makea scatter plot.

All the visualization code blocks are currently commented out because running them all together can cause errors — one visualization might interfere
with another. If you want to explore a specific visualization, just remove the comment (i.e., the #) from the line of code you’re interested in and run
it. This way, you’ll get the exact visualization you want to see."""

# importing the required libaries for visualization
import pandas as pd
import plotly.express as px

# Loading our avg_sentiment_results.csv file as a panda dataframe
df = pd.read_csv("../data/dataframes/sentiment-analysis/avg_sentiment_results.csv")

# Printing the head of the dataframe to explore columns and rows
print(df.head())

# Visualization Exploration 1: Creating a Bar Chart
# Help was taken from ChatGPT while creating this Visualization see ChatGPT Solution No. 6 in in "AI_Documentation_yasir_rauf" document inside the AI Documentation folder
# Creating a new column  named Sentiment to group articles by "Negative", "Neutral", and "Positive" sentiment
#def get_sentiment(score):
    #if score < 0.5:
        #return "Negative"
    #elif score < 1.5:
        #return "Neutral"
    #else:
        #return "Positive"

#df["Sentiment"] = df["avg_sentiment"].apply(get_sentiment)

# Filtering October 2023 and January 2024 articles because we are interested in comparing articles from these two months.
#df = df[df["year_month"].isin(["2023-10", "2024-01"])]

# Counting articles for each sentiment in each month because we want to know how many articles are Negative, Neutral, or
# Positive in each of the two months. Grouping and counting helps us prepare for the chart.
#counts = df.groupby(["Sentiment", "year_month"]).size().reset_index(name="Count")

# Making a bar chart using plotly express
#fig1 = px.bar(counts,
             #x="Sentiment",
             #y="Count",
             #color="year_month",
             #barmode="group",
             #title="Sentiment of Articles in Oct 2023 and Jan 2024")

# Show the chart
#fig1.show()

# Visualization Exploration 2: Creating a Bar Chart Using Relative Percentages
# Note: In this Visualization we will be creating a separate bar plot with relative numbers (percentage of the positive/neutral/negative articles per month), to make the two months more comparable
# given the difference in number of articles
# Help was taken from ChatGPT while creating this Visualization see ChatGPT Solution No. 7 in in "AI_Documentation_yasir_rauf" document inside the AI Documentation folder
# Creating sentiment labels based on avg_sentiment to group articles by "Negative", "Neutral", and "Positive" sentiment
#def label_sentiment(score):
    #if 0 <= score < 0.5:
        #return 'Negative'
    #elif 0.5 <= score < 1.5:
        #return 'Neutral'
    #elif 1.5 <= score <= 2:
        #return 'Positive'

#df['sentiment_label'] = df['avg_sentiment'].apply(label_sentiment)

# Filtering the October 2023 and January 2024 articles
#filtered_df = df[df['year_month'].isin(['2023-10', '2024-01'])]

# Grouping by year_month and sentiment_label to get counts
#grouped = filtered_df.groupby(['year_month', 'sentiment_label']).size().reset_index(name='count')

# Calculating percentage per sentiment per month
#grouped['percentage'] = grouped.groupby('year_month')['count'].transform(lambda x: (x / x.sum()) * 100)

# Ploting with Plotly Express
#fig2 = px.bar(
    #grouped,
    #x='sentiment_label',
    #y='percentage',
    #color='year_month',
    #barmode='group',
    #title='Relative Sentiment Distribution: October 2023 vs January 2024',
    #labels={
        #'sentiment_label': 'Sentiment',
        #'percentage': 'Percentage of Articles',
        #'year_month': 'Month'})

#fig2.show()

# Visualization Exploration No. 3: Creating a Scatterplot
# Help was taken from ChatGPT while creating this Visualization see ChatGPT Solution No. 8 in in "AI_Documentation_yasir_rauf" document inside the AI Documentation folder
# Classify sentiment into categories so that each text is tagged as Positive / Neutral / Negative.
#def classify_sentiment(score):
    #if score < 0.5:
        #return "Negative"
    #elif score < 1.5:
        #return "Neutral"
    #else:
        #return "Positive"

#df["sentiment_category"] = df["avg_sentiment"].apply(classify_sentiment)

# Map months to human-readable labels because 2023-10 lablled as a month does not looks good for me
#month_map = {
    #"2023-10": "October 2023",
    #"2024-01": "January 2024"}
#df["month_label"] = df["year_month"].map(month_map)

# Create a linear numeric x-axis for spacing because plotly can't space points on the x-axis if they're strings like "October 2023", so we map them to numbers
#month_to_num = {
    #"October 2023": 0,
    #"January 2024": 1}
#df["month_num"] = df["month_label"].map(month_to_num)

# Plot scatter using numeric x-axis and label ticks manually
#fig3 = px.scatter(
    #df,
    #x="month_num",
    #y="avg_sentiment",
    #color="sentiment_category",
    #hover_data={"title": True, "month_num": False},
    #labels={"avg_sentiment": "Average Sentiment"},
    #title="Sentiment of Articles: October 2023 (War) vs January 2024 (Ceasefire)",
    #opacity=0.5 # Incorporated the feedback given by Peter # Help was taken from this website: https://plotly.com/python/marker-style/)

# Fix x-axis to show labels instead of numbers
#fig3.update_layout(
    #xaxis=dict(
        #tickmode='array',
        #tickvals=[0, 1],
        #ticktext=["October 2023", "January 2024"],
        #title="Month"),
    #yaxis=dict(title="Average Sentiment (0-0.5 = Negative, 0.5-1.5 = Neutral, 1.5-2 = Positive)", range=[0, 2]),
    #legend_title="Sentiment Category")

#fig3.show()






