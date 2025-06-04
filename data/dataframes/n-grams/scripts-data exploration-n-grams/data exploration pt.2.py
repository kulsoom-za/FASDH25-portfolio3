import pandas as pd
import plotly.express as px
import nltk
from nltk.corpus import stopwords

# Download stopwords if needed
nltk.download('stopwords')

# Load dataset
data_path = r"C:\Users\HP\Downloads\FASDH25-portfolio3\data\dataframes\n-grams\3-gram\3-gram.csv"
df = pd.read_csv(data_path)

# Lowercase all trigrams for consistency
df['3-gram'] = df['3-gram'].str.lower()

# Define stopwords set
stop_words = set(stopwords.words('english'))

# Keep trigrams that have at least one non-stopword
df = df[df['3-gram'].apply(lambda x: any(w not in stop_words for w in x.split()))]

# Create 'period' column from year and month
df['month_str'] = df['month'].astype(str).str.zfill(2)
df['period'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month_str'])

# List of trigrams to track
target_trigrams = [
    "the gaza strip",
    "told al jazeera",
    "the israeli army",
    "occupied west bank",
    "humanitarian aid"
]

# Filter dataset to these target trigrams
filtered = df[df['3-gram'].isin(target_trigrams)]

# Group by period and trigram, summing counts
monthly_counts = filtered.groupby(['period', '3-gram'], as_index=False)['count'].sum()

# Plot with plotly express
fig = px.line(
    monthly_counts,
    x="period",
    y="count",
    color="3-gram",
    markers=True,
    title="Narrative Framing in al-Jazeera Gaza Corpus (Selected 3-grams)",
    labels={"period": "Date", "count": "Monthly Frequency", "3-gram": "Trigram"}
)

fig.update_layout(hovermode="x unified")
fig.show()

# Save plot as HTML
fig.write_html("n-afreen-baig_3gram_framing_trends.html")
