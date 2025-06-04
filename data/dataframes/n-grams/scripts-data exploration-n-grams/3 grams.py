import pandas as pd
import plotly.express as px
import nltk
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')

# Load dataset
data_path = r"../n-grams/3-gram/3-gram.csv"
df = pd.read_csv(data_path)

# Normalize trigrams
df['3-gram'] = df['3-gram'].str.lower()

# Remove trigrams made entirely of stopwords
stop_words = set(stopwords.words('english'))
df = df[df['3-gram'].apply(lambda x: any(word not in stop_words for word in x.split()))]

# Create a datetime column
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Define narrative phrases
phrases = [
    "the gaza strip",
    "told al jazeera",
    "the israeli army",
    "occupied west bank",
    "humanitarian aid",
    "palestinian health ministry",
    "the social media",
    "united nations says"
]

# Filter for these phrases
df_filtered = df[df['3-gram'].isin(phrases)]

# Define time period: before vs after October 2023
df_filtered['period'] = df_filtered['date'].apply(lambda d: 'Before Oct 2023' if d < pd.Timestamp("2023-10-01") else 'After Oct 2023')

# Group by phrase and period
grouped = df_filtered.groupby(['3-gram', 'period'], as_index=False)['count'].sum()

# Plot bar chart
fig = px.bar(
    grouped,
    x='3-gram',
    y='count',
    color='period',
    barmode='group',
    title='Media Framing of Gaza: Before vs After October 2023',
    labels={'3-gram': 'Phrase', 'count': 'Total Frequency', 'period': 'Time Period'},
    text='count'
)

fig.update_layout(
    xaxis_tickangle=45,
    xaxis_title='Narrative Phrase',
    yaxis_title='Total Frequency',
    legend_title='Period'
)

fig.show()

# Save to HTML
fig.write_html("n-afreen-baig_before_after_oct2023.html")
