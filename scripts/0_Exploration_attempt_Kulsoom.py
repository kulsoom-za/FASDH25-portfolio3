import pandas as pd

# Load the topic model CSV
topic_df = pd.read_csv(r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv')
topic_df = topic_df[['file', 'Topic']].rename(columns={'file': 'filename'})

# Load the TF-IDF similarity CSV
similarity_df = pd.read_csv(r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\tfidf\tfidf-over-0.3.csv')

# Merge topic info into similarity dataframe
similarity_df = similarity_df.merge(topic_df, left_on='filename-1', right_on='filename', how='left')
similarity_df = similarity_df.rename(columns={'Topic': 'topic-1'}).drop(columns=['filename'])

similarity_df = similarity_df.merge(topic_df, left_on='filename-2', right_on='filename', how='left')
similarity_df = similarity_df.rename(columns={'Topic': 'topic-2'}).drop(columns=['filename'])

# Filter: both documents are from Topic 0
topic_0_pairs = similarity_df[(similarity_df['topic-1'] == 0) & (similarity_df['topic-2'] == 0)]

# Show result
print(topic_0_pairs[['filename-1', 'filename-2', 'topic-1', 'topic-2', 'similarity']].head())



# Use the full topic_0_pairs DataFrame
# 1. Create edges CSV
edges = topic_0_pairs[['filename-1', 'filename-2', 'similarity']].copy()
edges.columns = ['Source', 'Target', 'Weight']

# 2. Create nodes CSV (source + target, deduplicated)
source_nodes = topic_0_pairs[['filename-1']].copy()
source_nodes.columns = ['Id']

target_nodes = topic_0_pairs[['filename-2']].copy()
target_nodes.columns = ['Id']

nodes = pd.concat([source_nodes, target_nodes]).drop_duplicates().reset_index(drop=True)
nodes['Label'] = nodes['Id']  # Set label same as Id
nodes['Group'] = 0  # Optional: same group (or you can later add topics/months)

# 3. Save to CSV
edges.to_csv('topic0_edges.csv', index=False, encoding='utf-8-sig')
nodes.to_csv('topic0_nodes.csv', index=False, encoding='utf-8-sig')
