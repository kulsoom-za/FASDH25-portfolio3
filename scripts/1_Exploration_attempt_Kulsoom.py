import pandas as pd

# --- Load the topic model CSV ---
topic_model_path = r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv'
topic_df = pd.read_csv(topic_model_path)

# Just keep the necessary columns and rename for merging
topic_df = topic_df[['file', 'Topic']].rename(columns={'file': 'filename'})
print("Total documents in Topic 0:", topic_df[topic_df['Topic'] == 0].shape[0])


# --- Load the TF-IDF similarity CSV ---
similarity_df = pd.read_csv(r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\tfidf\tfidf-over-0.3.csv')

# --- Merge topic info into similarity dataframe ---
# Merge topic for filename-1
similarity_with_topics = similarity_df.merge(topic_df, left_on='filename-1', right_on='filename', how='left')
similarity_with_topics = similarity_with_topics.rename(columns={'Topic': 'topic-1'}).drop(columns=['filename'])

# Merge topic for filename-2
similarity_with_topics = similarity_with_topics.merge(topic_df, left_on='filename-2', right_on='filename', how='left')
similarity_with_topics = similarity_with_topics.rename(columns={'Topic': 'topic-2'}).drop(columns=['filename'])
# One side is Topic 0
topic_0_any = similarity_with_topics[
    (similarity_with_topics['topic-1'] == 0) | 
    (similarity_with_topics['topic-2'] == 0)
]
print("TF-IDF pairs involving Topic 0 on either side:", topic_0_any.shape[0])


# --- Filter only Topic 0 vs Topic 0 ---
topic_0_pairs = similarity_with_topics[
    (similarity_with_topics['topic-1'] == 0) & 
    (similarity_with_topics['topic-2'] == 0)
]

# --- Show result ---
print("TF-IDF pairs where both documents are from Topic 0:")
print(topic_0_pairs[['filename-1', 'filename-2', 'topic-1', 'topic-2', 'similarity']].head())


# --- Define your correct paths ---
tfidf_path = r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\tfidf\tfidf-over-0.3.csv'  # Update filename if needed
topic_model_path = r'C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv'

# --- Load data with absolute paths ---
df = pd.read_csv(tfidf_path, index_col=0).reset_index()  # Fixed path
topic_df = pd.read_csv(topic_model_path)  # Fixed path

# --- Rest of your code remains the same ---
# Merge topics for filename-1
df = df.merge(topic_df, left_on='filename-1', right_on='file', how='left')
df = df.rename(columns={'Topic': 'topic-1'}).drop(columns=['file'])

# Merge topics for filename-2
df = df.merge(topic_df, left_on='filename-2', right_on='file', how='left')
df = df.rename(columns={'Topic': 'topic-2'}).drop(columns=['file'])

# Filter for Topic 0 pairs
topic_0_pairs = df[(df['topic-1'] == 0) & (df['topic-2'] == 0)]

# --- Export nodes and edges for Topic 0 ---
# Edges
edges = topic_0_pairs[['filename-1', 'filename-2', 'similarity']]
edges.columns = ['Source', 'Target', 'Weight']
edges.to_csv(r'C:\Users\DELL\Downloads\topic_0_edges.csv', encoding='utf-8-sig', index=False)

# Nodes
source_nodes = topic_0_pairs[['filename-1', 'title-1', 'month-1']]
source_nodes.columns = ['Id', 'Label', 'month']
target_nodes = topic_0_pairs[['filename-2', 'title-2', 'month-2']]
target_nodes.columns = ['Id', 'Label', 'month']
nodes = pd.concat([source_nodes, target_nodes]).drop_duplicates('Id')
nodes.to_csv(r'C:\Users\DELL\Downloads\topic_0_nodes.csv', encoding='utf-8-sig', index=False)

print("Files saved successfully!")
