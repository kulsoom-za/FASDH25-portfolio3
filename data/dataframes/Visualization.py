import pandas as pd
import plotly.express as px

# === Load high-similarity pairs for Topic 3 and Topic 0 ===
topic3_df = pd.read_csv('topic3-high-similarity.csv')
topic0_df = pd.read_csv('topic0-high-similarity.csv')

# === Load the full topic metadata (for dates) ===
topic_df = pd.read_csv(r'topic-model\topic-model.csv')
topic_df = topic_df[topic_df['Topic'] != -1]  # remove unassigned

# === Step: Create a mapping from file name to full date ===
topic_df['date'] = pd.to_datetime(topic_df[['year', 'month', 'day']])
file_date_map = topic_df.set_index('file')['date'].to_dict()

# === Step: Add 'date-1' and 'date-2' columns to each high similarity df ===
def add_dates(df):
    df['date-1'] = df['filename-1'].map(file_date_map)
    df['date-2'] = df['filename-2'].map(file_date_map)
    df['min_date'] = df[['date-1', 'date-2']].min(axis=1)  # use earliest date
    return df

topic3_df = add_dates(topic3_df)
topic0_df = add_dates(topic0_df)

# === Step: Group by month and count pairs ===
topic3_counts = topic3_df.groupby(topic3_df['min_date'].dt.to_period('M')).size().reset_index(name='pair_count')
topic3_counts['topic'] = 'Topic 3'

topic0_counts = topic0_df.groupby(topic0_df['min_date'].dt.to_period('M')).size().reset_index(name='pair_count')
topic0_counts['topic'] = 'Topic 0'

# Combine both
combined_counts = pd.concat([topic3_counts, topic0_counts])
combined_counts['min_date'] = combined_counts['min_date'].dt.to_timestamp()

# === Plotting ===
fig = px.line(
    combined_counts,
    x='min_date',
    y='pair_count',
    color='topic',
    title='Monthly Trend of High Similarity Article Pairs (Similarity > 0.5)',
    labels={'min_date': 'Month', 'pair_count': 'High Similarity Pairs'},
    markers=True
)

fig.update_layout(xaxis_title='Month', yaxis_title='Number of High-Similarity Pairs', title_x=0.5)
fig.show()
