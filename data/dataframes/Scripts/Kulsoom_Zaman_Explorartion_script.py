import pandas as pd

# Loading TF-IDF similarity data and topic model results
tfidf_df = pd.read_csv('tfidf/tfidf-over-0.3.csv')

#EXPLORING TF-IDF

#single column
print("Selected 'similarity' column:")
similarity_column = tfidf_df['similarity']
print(similarity_column.head())

#Selecting the first row
print("First row:")
first_row = tfidf_df.iloc[0]
print(first_row)

#Selecting the first 5 rows
print("First 5 rows:")
first_five_rows = tfidf_df.head(5)
print(first_five_rows)

#Selecting multiple columns
print("Selected 'filename-1' and 'topic_1' columns:")
specific_cols_df = tfidf_df[['filename-1', 'title-1']]
print(specific_cols_df.head())

#Filtering the dataframe (greater than, less than, equal to, with a list)
# Filter for similarity greater than 0.9
print("Filtered: Similarity > 0.9")
high_similarity_df = tfidf_df[tfidf_df['similarity'] > 0.9]
print(high_similarity_df.head())

#Summary statistics (max and sum)
#Find the maximum similarity score
print(f"Maximum similarity score: {tfidf_df['similarity'].max()}")

#EXPLORING TOPIC-MODELING DATAFRAME

#Topic model
topics_df = pd.read_csv('topic-model/topic-model.csv').rename(columns={'Topic': 'topic'})
print(topics_df.head())
print(topics_df.columns)

# Filter for a specific topic_2 (e.g., topic 7)
print("\nFiltered: topic_2 == 7")
topic_7_df = topics_df[topics_df['topic_2'] == 7]
print(topic_7_df.head())

# Filter where topic_1 is in a list of topics (e.g., topics 0, 1, or 2)
print("Filtered: topic_1 in [0, 1, 2]")
favorite_topics_df = topics_df[topics_df['topic_1'].isin([0, 1, 2])]
print(favorite_topics_df.head())

#MERGING BOTH DATAFRAMES
# Merging topic info for filename-1
tfidf_df = tfidf_df.merge(
    topics_df[['file', 'topic']].rename(columns={'file': 'filename-1', 'topic': 'topic_1'}),
    on='filename-1', how='left'
)
print("After merging topic_1:")
print(tfidf_df.head())
print(tfidf_df.columns)

# Merging topic info for filename-2 (Code1, help from Chatbbt, mentioned in the AI_doc)
tfidf_df = tfidf_df.merge(
    topics_df[['file', 'topic']].rename(columns={'file': 'filename-2', 'topic': 'topic_2'}), 
    on='filename-2', how='left'
)
print("After merging topic_2:")
print(tfidf_df.head())
print(tfidf_df.columns)

# Keeping only the relevant columns (Code2, help from Chatgbt, mentioned in the AI_doc)
columns_to_keep = ['filename-1', 'topic_1', 'filename-2', 'topic_2', 'similarity']
filtered_df = tfidf_df[columns_to_keep].dropna(subset=['topic_1', 'topic_2'])
print("After keeping required columns:")
print(filtered_df.head())
print(filtered_df.columns)

# Filtering rows with similarity between 0.8 and 1.0 and same topic
filtered_df = filtered_df[
    (filtered_df['similarity'] > 0.6) &  
    (filtered_df['topic_1'] != filtered_df['topic_2'])
]

filtered_df = filtered_df[(filtered_df['topic_1'] != -1) & (filtered_df['topic_2'] != -1)]

print("After filtering for similarity 0.8–1.0 and matching topics:")
print(filtered_df.head())
print(filtered_df.columns)


# Sorting by similarity, topic_1, and topic_2
filtered_df = filtered_df.sort_values(by=['topic_1', 'topic_2', 'similarity'])
print("After sorting:")
print(filtered_df.head())
print(filtered_df.columns)

# Saving the final filtered and sorted DataFrame to CSV
filtered_df.to_csv('Topic_model_and_tfidf_sorted_by_topic.csv', index=False)
print("Saved")
