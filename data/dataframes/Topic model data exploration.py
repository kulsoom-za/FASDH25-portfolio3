import pandas as pd

# === File paths to the data files ===
topic_model_path = r'topic-model\topic-model.csv'    # topic model output
tfidf_path = r'tfidf\tfidf-over-0.3.csv'             # tf-idf similarity data

# === Step 1: Load the CSV files ===
topic_df = pd.read_csv(topic_model_path)             # this has topic info for each article
tfidf_df_data = pd.read_csv(tfidf_path)              # this has similarity between article pairs

print("Columns in the topic-model data:", topic_df.columns.tolist())
print("First 5 rows of topic-model data:")
print(topic_df.head())
print("\nColumns in the tf-idf data:", tfidf_df_data.columns.tolist())
print("First 5 rows of tf-idf data:")
print(tfidf_df_data.head())

# === Step 2: Remove rows in the topic model that have no assigned topic (-1 means unassigned) ===
topic_df = topic_df[topic_df["Topic"] != -1].copy()

# === Step 3: Find the 5 most common topics by frequency (most articles assigned to them) ===
top_5_topic_numbers = topic_df['Topic'].value_counts().head(5).index.tolist()

# === Step 4: Filter the topic dataframe to include only those top 5 topics (for general overview prints) ===
filtered_topic_df = topic_df[topic_df['Topic'].isin(top_5_topic_numbers)]
print("\nTop 5 Topic Numbers:", top_5_topic_numbers)
print("Sample of Filtered Topic Data (for general overview):")
print(filtered_topic_df[['year', 'Topic', 'title']].head())

# === Step 5: Create readable labels for each topic by combining its 4 top keywords ===
topic_labels = topic_df[['Topic', 'topic_1', 'topic_2', 'topic_3', 'topic_4']].drop_duplicates().copy()
topic_labels['Label'] = topic_labels[['topic_1', 'topic_2', 'topic_3', 'topic_4']].agg(', '.join, axis=1)

print("\n--- Topic Number = Label Mapping for Top Topics ---")
print(topic_labels[topic_labels['Topic'].isin(top_5_topic_numbers)][['Topic', 'Label']])

# === Step 6: Loop through the top 5 topics and compute intra-topic similarity metrics ===
print("\n--- Intra-topic TF-IDF Similarity Analysis for Top 5 Topics ---")

for topic_num in top_5_topic_numbers:
    print(f"\n>> Analyzing Topic {topic_num}")
    
    # Get all articles that belong to this topic
    topic_articles_df = topic_df[topic_df['Topic'] == topic_num]
    topic_articles = topic_articles_df['file'].unique()
    n_articles = len(topic_articles)

    # Get the keyword label for this topic
    label_row = topic_labels[topic_labels['Topic'] == topic_num]
    label = ', '.join(label_row[['topic_1', 'topic_2', 'topic_3', 'topic_4']].values[0]) if not label_row.empty else "N/A"
    
    # Filter similarity pairs where BOTH articles belong to this topic
    topic_set = set(topic_articles)
    same_topic_pairs = tfidf_df_data[
        tfidf_df_data['filename-1'].isin(topic_set) &
        tfidf_df_data['filename-2'].isin(topic_set)
    ]

    # Metrics
    pair_count = len(same_topic_pairs)
    possible_pairs = n_articles * (n_articles - 1) / 2 if n_articles >= 2 else 0
    density = pair_count / possible_pairs if possible_pairs else 0
    avg_similarity = same_topic_pairs['similarity'].mean() if pair_count > 0 else 0

    # Print results for each topic
    print(f"- Label: {label}")
    print(f"- Articles in topic: {n_articles}")
    print(f"- Similar article pairs (similarity > 0.3): {pair_count}")
    print(f"- Possible article pairs: {int(possible_pairs)}")
    print(f"- Pair density: {density:.3f}")
    print(f"- Average similarity: {avg_similarity:.3f}")

# --------------------------------------------------------------------------------------
# Section for detailed processing of Specific Topics (Topic 3 and Topic 0)
# --------------------------------------------------------------------------------------

# Create a smaller mapping from filename to topic (used for merging)
topic_map = topic_df[['file', 'Topic']].drop_duplicates()

# Merge topic number for filename-1
tfidf_with_topics = tfidf_df_data.merge(topic_map, left_on='filename-1', right_on='file', how='left') \
                                 .rename(columns={'Topic': 'topic_1'}).drop(columns='file')

# Merge topic number for filename-2
tfidf_with_topics = tfidf_with_topics.merge(topic_map, left_on='filename-2', right_on='file', how='left') \
                                     .rename(columns={'Topic': 'topic_2'}).drop(columns='file')

print("\n--- Merged TF-IDF Data with Topics (tfidf_with_topics) ---")
print("Sample of Merged TF-IDF Data with Topics:")
print(tfidf_with_topics.head())
print(f"Shape of tfidf_with_topics: {tfidf_with_topics.shape} (rows, columns)")
unique_articles_in_merged = pd.concat([tfidf_with_topics['filename-1'], tfidf_with_topics['filename-2']]).nunique()
print(f"Number of unique articles in tfidf_with_topics: {unique_articles_in_merged}")

# Filter out any rows where one of the topic values is missing (NaNs)
valid_pairs = tfidf_with_topics.dropna(subset=['topic_1', 'topic_2']).copy() # .copy() for safety
print("\n--- Valid Pairs (after dropping NaNs) ---")
print(valid_pairs.head())
print(f"Shape of valid_pairs: {valid_pairs.shape} (rows, columns)")
unique_articles_in_valid_pairs = pd.concat([valid_pairs['filename-1'], valid_pairs['filename-2']]).nunique()
print(f"Number of unique articles in valid_pairs: {unique_articles_in_valid_pairs}")


# =====================================================================================
# Detailed Exploration for TOPIC 3
# =====================================================================================
print("\n\n=============== DETAILED EXPLORATION FOR TOPIC 3 ===============")

# Filter pairs where both documents are in Topic 3 and similarity is strong (> 0.5)
topic3_df = valid_pairs[
    (valid_pairs['topic_1'] == 3) &
    (valid_pairs['topic_2'] == 3) &
    (valid_pairs['similarity'] > 0.5)
].copy() # .copy() for safety

print("\n--- Topic 3 Filtered Data (topic3_df) ---")
print(topic3_df.head())
print(f"Shape of topic3_df: {topic3_df.shape} (rows, columns)")
unique_articles_in_topic3 = pd.concat([topic3_df['filename-1'], topic3_df['filename-2']]).nunique()
print(f"Number of unique articles in topic3_df: {unique_articles_in_topic3}")

# Calculate and print the average similarity for topic3_df
average_similarity_topic3 = topic3_df['similarity'].mean()
print(f"Average similarity for Topic 3 (similarity > 0.5): {average_similarity_topic3:.3f}")

# Define the output path and file name for Topic 3
output_path_topic3 = r'topic3-high-similarity.csv'
# Save topic3_df to CSV
topic3_df.to_csv(output_path_topic3, index=False)
print(f"\nSaved Topic 3 high-similarity pairs to: {output_path_topic3}")


# =====================================================================================
# Detailed Exploration for TOPIC 0
# =====================================================================================
print("\n\n=============== DETAILED EXPLORATION FOR TOPIC 0 ===============")

# Filter pairs where both documents are in Topic 0 and similarity is strong (> 0.5)
topic0_df = valid_pairs[
    (valid_pairs['topic_1'] == 0) &
    (valid_pairs['topic_2'] == 0) &
    (valid_pairs['similarity'] > 0.5)
].copy() # .copy() for safety

print("\n--- Topic 0 Filtered Data (topic0_df) ---")
print(topic0_df.head())
print(f"Shape of topic0_df: {topic0_df.shape} (rows, columns)")
unique_articles_in_topic0 = pd.concat([topic0_df['filename-1'], topic0_df['filename-2']]).nunique()
print(f"Number of unique articles in topic0_df: {unique_articles_in_topic0}")

# Calculate and print the average similarity for topic0_df
average_similarity_topic0 = topic0_df['similarity'].mean()
print(f"Average similarity for Topic 0 (similarity > 0.5): {average_similarity_topic0:.3f}")

# Define the output path and file name for Topic 0
output_path_topic0 = r'topic0-high-similarity.csv'
# Save topic0_df to CSV
topic0_df.to_csv(output_path_topic0, index=False)
print(f"\nSaved Topic 0 high-similarity pairs to: {output_path_topic0}")

print("\n\n--- All specified data exploration complete ---")
# You now have 'topic3_df' and 'topic0_df' ready for further analysis or time-series plotting.
