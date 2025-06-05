import pandas as pd
import os

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

# Load data
df = pd.read_csv('../outputs/Topic_model_and_tfidf_sorted_by_topic.csv')

# 2. Create the edges list (using original filenames)
edges = df[['filename-1', 'filename-2', 'similarity']]
edges.columns = ['Source', 'Target', 'Weight']

# 3. Create the nodes list
source_nodes = df[['filename-1', 'topic_1']]
source_nodes.columns = ['Id', 'topic']

target_nodes = df[['filename-2', 'topic_2']]
target_nodes.columns = ['Id', 'topic']

# Combine and remove duplicate nodes
nodes = pd.concat([source_nodes, target_nodes]).drop_duplicates(subset='Id')

# Add label column (same as Id)
nodes['Label'] = nodes['Id']

# 4. Save to CSV
edges.to_csv('../outputs/kulsoom-zaman-edges.csv', encoding='utf-8-sig', index=False)
nodes.to_csv('../outputs/kulsoom-zaman-nodes.csv', encoding='utf-8-sig', index=False)
