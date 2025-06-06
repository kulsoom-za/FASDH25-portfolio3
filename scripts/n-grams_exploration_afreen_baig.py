import pandas as pd
import plotly.express as px
import nltk
from nltk.corpus import stopwords

# Load dataset
data_path = r"../data/dataframes/n-grams/3-gram/3-gram.csv"
df = pd.read_csv(data_path)


#see ChatGPT Solution.1 in AI Documnetation
# Define stopwords set
stop_words = set(stopwords.words('english'))

#see ChatGPT Solution.2 in AI Documnetation
# Create 'period' column from year and month
df['period'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2))


# List of trigrams to track
target_trigrams = [
    "the gaza strip",
    "told al jazeera",
    "the israeli army",
    "occupied west bank",
    "humanitarian aid"
]

# Filter dataset to these target trigrams
filtered = df[df['3-gram'].isin(target_trigrams)]#help taken from slides and class lecture, DHFAS-14.1-ngrams

# Group by period and trigram, summing counts
monthly_counts = filtered.groupby(['period', '3-gram'], as_index=False)['count'].sum()# taken help from slide, groupby, DHFAS-14.1-ngrams

# Plot with plotly express
fig = px.line(
    monthly_counts,
    x="period",
    y="count",
    color="3-gram",
    title="Narrative Framing in al-Jazeera Gaza Corpus (Selected 3-grams)",
    labels={"period": "Date", "count": "Monthly Frequency", "3-gram": "Trigram"}
)#help taken from slides and class lecture, DHFAS-13.2-plotly and Visualisation

fig.show()

