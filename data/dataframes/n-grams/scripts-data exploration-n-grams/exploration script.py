import pandas as pd
import plotly.express as px
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already done
nltk.download('stopwords')

# --- Step 1: Load data ---
data_path = r"C:\Users\HP\Downloads\FASDH25-portfolio3\data\dataframes\n-grams\1-gram\1-gram.csv"
df = pd.read_csv(data_path)

# --- Step 2: Basic info and cleaning ---
print("Dataframe shape:", df.shape)
print("Columns:", df.columns)
print("\nSample data:")
print(df.head())

# Drop rows where the n-gram is missing
df = df.dropna(subset=['1-gram'])

# Convert 'count' column to numeric, drop invalid rows
df['count'] = pd.to_numeric(df['count'], errors='coerce')
df = df.dropna(subset=['count'])

# Combine date columns if available
if all(col in df.columns for col in ['year', 'month', 'day']):
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
else:
    df['date'] = None  # If date columns are not present

# --- Step 3: Frequency distribution of top n-grams ---

# Lowercase n-grams for consistency
df['1-gram_lower'] = df['1-gram'].str.lower()

# Filter out stopwords (English)
stop_words = set(stopwords.words('english'))
df_filtered = df[~df['1-gram_lower'].isin(stop_words)]

# Aggregate counts by n-gram
freq_dist = df_filtered.groupby('1-gram_lower')['count'].sum().reset_index()
freq_dist = freq_dist.sort_values('count', ascending=False).head(20)

print("\nTop 20 most frequent non-stopword 1-grams:")
print(freq_dist)

# Plot top 20 frequent n-grams
fig1 = px.bar(freq_dist, x='1-gram_lower', y='count', 
              title='Top 20 Most Frequent 1-grams (Excluding Stopwords)',
              labels={'1-gram_lower': '1-gram', 'count': 'Total Count'})
fig1.show()

# --- Step 4: Time series of overall frequency (if dates exist) ---

if df['date'].notnull().any():
    daily_counts = df.groupby('date')['count'].sum().reset_index()

    fig2 = px.line(daily_counts, x='date', y='count',
                   title='Daily Total N-gram Counts Over Time',
                   labels={'count': 'Total Count', 'date': 'Date'})
    fig2.show()
else:
    print("No date columns to plot time series.")

# --- Step 5: Optional - Word length analysis ---
df_filtered['word_length'] = df_filtered['1-gram_lower'].apply(len)

word_length_freq = df_filtered.groupby('word_length')['count'].sum().reset_index()

fig3 = px.bar(word_length_freq, x='word_length', y='count',
              title='Frequency of 1-grams by Word Length',
              labels={'word_length': 'Word Length (characters)', 'count': 'Total Count'})
fig3.show()
