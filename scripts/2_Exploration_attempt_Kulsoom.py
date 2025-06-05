import os
import re
import pandas as pd

def count_words_strict_filtering(directory, num_words=20):
    stop_words = {
        # Original stop words
        'the', 'of', 'to', 'and', 'in', 'a', 'on', 'that', 's', 'for',
        'is', 'said', 'it', 'as', 'with', 'was', 'has', 'at', 'by', 'from',
        # Expanded based on your last output
        'have', 'are', 'not', 'they', 'been', 'this', 'were', 'their', 'its',
        'but', 'his', 'more', 'or', 'which', 'an', 'who', 'what', 'when',
        'where', 'how', 'why', 'if', 'there', 'had', 'would', 'could', 'should',
        # New additions from this optimization
        'also', 'will', 'after', 'than', 'all', 'one', 'about', 'two', 'first',
        'last', 'over', 'into', 'during', 'before', 'such', 'other', 'most'
    }
    
    word_counts = {}
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                text = f.read().lower()
                words = re.findall(r'\b[a-z]+\b', text)
                
                for word in words:
                    if word not in stop_words and len(word) > 5:  # Now 5+ chars
                        word_counts[word] = word_counts.get(word, 0) + 1
    
    df = pd.DataFrame(list(word_counts.items()), columns=['Word', 'Count'])
    df = df.sort_values('Count', ascending=False).head(num_words)
    
    total_words = df['Count'].sum()
    df['Percentage'] = (df['Count'] / total_words * 100).round(2)
    
    return df

# 1. Load the data (no header since your file has none)
file_path = r"C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\n-grams\2-gram\2-gram.csv"
df = pd.read_csv(file_path, header=None, names=['year', 'month', 'day', '2-gram', 'count'])

# 2. Filter out empty rows and uninformative phrases
stop_phrases = {
    'of the', 'in the', 'to the', 'it is', 'as well', 'at the',
    'on the', 'for the', 'and the', 'that the', 'from the'
}
df = df[~df['2-gram'].isin(stop_phrases)]

# 3. Get top 20 phrases
top_phrases = df.groupby('2-gram')['count'].sum().reset_index()
top_phrases = top_phrases.sort_values('count', ascending=False).head(20)

# 4. Add percentage
total = top_phrases['count'].sum()
top_phrases['percentage'] = (top_phrases['count'] / total * 100).round(2)

# 5. Display results
print("Top 20 Most Frequent 2-Grams:")
print(top_phrases[['2-gram', 'count', 'percentage']].to_string(index=False))
