import os
import pandas as pd
import plotly.express as px

# -- Your existing article reading and theme detection code --
folder_path = r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\articles'

article_data = []
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
            text = f.read().lower()
            article_data.append({'filename': filename, 'text': text})

articles_df = pd.DataFrame(article_data)

articles_df['date'] = articles_df['filename'].str.extract(r'(\d{4}-\d{2}-\d{2})')
articles_df['year'] = pd.to_datetime(articles_df['date']).dt.year
articles_df['month'] = pd.to_datetime(articles_df['date']).dt.month

themes = {
    'Israel and Israeli Context': ['israel', 'israeli', 'military', 'forces', 'government', 'united', 'october'],
    'Palestinian Context and Population': ['palestinian', 'palestinians', 'palestine', 'people', 'children'],
    'Conflict and Violence': ['killed', 'attacks', 'attack', 'against'],
    'Territorial and Political Issues': ['occupied', 'international', 'jazeera']
}

def detect_theme(text):
    present_themes = []
    for theme, keywords in themes.items():
        if any(keyword in text for keyword in keywords):
            present_themes.append(theme)
    return present_themes

articles_df['themes'] = articles_df['text'].apply(detect_theme)

# -- Load similarity dataframe --
similarity_df = pd.read_csv(r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\tfidf\tfidf-over-0.3.csv')

# Convert years/months to numeric
similarity_df['year-1'] = pd.to_numeric(similarity_df['year-1'], errors='coerce')
similarity_df['month-1'] = pd.to_numeric(similarity_df['month-1'], errors='coerce')
similarity_df['year-2'] = pd.to_numeric(similarity_df['year-2'], errors='coerce')
similarity_df['month-2'] = pd.to_numeric(similarity_df['month-2'], errors='coerce')

# Create datetime for each doc
similarity_df['date-1'] = pd.to_datetime(dict(year=similarity_df['year-1'], month=similarity_df['month-1'], day=1))
similarity_df['date-2'] = pd.to_datetime(dict(year=similarity_df['year-2'], month=similarity_df['month-2'], day=1))

# Use earlier date for pair_date
similarity_df['pair_date'] = similarity_df[['date-1', 'date-2']].min(axis=1)
similarity_df['year'] = similarity_df['pair_date'].dt.year
similarity_df['month'] = similarity_df['pair_date'].dt.month

# --- Step 1: Create filename -> themes mapping ---
# Convert themes lists to dict for quick lookup
filename_to_themes = articles_df.set_index('filename')['themes'].to_dict()

# --- Step 2: For each row in similarity_df, find shared themes ---
def get_shared_themes(row):
    themes1 = filename_to_themes.get(row['filename-1'], [])
    themes2 = filename_to_themes.get(row['filename-2'], [])
    shared = list(set(themes1).intersection(set(themes2)))
    return shared

similarity_df['shared_themes'] = similarity_df.apply(get_shared_themes, axis=1)

# --- Step 3: Explode so each row is one theme cluster ---
similarity_expanded = similarity_df.explode('shared_themes')

# Filter out pairs with no shared themes
similarity_expanded = similarity_expanded[similarity_expanded['shared_themes'].notnull()]

# --- Step 4: Group by theme, year, month and calculate average similarity ---
theme_similarity_trends = similarity_expanded.groupby(['shared_themes', 'year', 'month'])['similarity'].mean().reset_index()
theme_similarity_trends.rename(columns={'shared_themes': 'theme', 'similarity': 'avg_similarity'}, inplace=True)

fig = px.scatter(
    theme_similarity_trends,
    x='month',
    y='avg_similarity',
    color='theme',
    facet_row='year',
    title='Similarity Trends Within Theme Clusters Over Time (Scatter Plot)',
    labels={'avg_similarity': 'Average Similarity', 'month': 'Month'},
    opacity=0.7,  # optional: makes overlapping points easier to see
    size_max=10
)

fig.update_layout(height=800)
fig.show()
