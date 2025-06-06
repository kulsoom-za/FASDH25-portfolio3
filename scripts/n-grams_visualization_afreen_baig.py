import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("../data/dataframes/n-grams/3-gram/3-gram.csv") #help taken from slide 13, DHFAS-13.2-plotly and Visualisation


# Define narrative phrases
phrases = [
    "the gaza strip",
    "occupied west bank",
    "the israeli army",
    "israeli air strikes",
    "palestinian health ministry",
    "officials told aljazeera"
]

# Filter data frame for these phrases
df = df[df['3-gram'].isin(phrases)] #help taken from slides, Exploring ngrams with pandas and plotly, DHFAS-14.1-ngrams

#See Solution No.3 in AI Documention in AI_Documnetation_Afreen_Baig
#Create a 'date' column with a default day (1st of each month)
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

#See Solution No.3 in AI Documention in AI_Documnetation_Afreen_Baig
#Define cutoff date
cutoff_date = pd.Timestamp('2023-10-01')

#see ChatGPT Solution No.3 in AI Documention in AI_Documnetation_Afreen_Baig
# Add period column: before vs after October 2023
df['period'] = df['date'].apply(lambda d: 'Before Oct 2023' if d < pd.Timestamp("2023-10-01") else 'After Oct 2023')

# Group by phrase and period and them sum the count
grouped = df.groupby(['3-gram', 'period'], as_index=False)['count'].sum()# taken help from slide, groupby, DHFAS-14.1-ngrams

# Plot bar chart
fig = px.bar(
    grouped,
    x='count',
    y='3-gram',           
    color='period',
    barmode='group',
    title='Media Framing of Gaza: Before vs After October 2023',
    labels={'3-gram':'Narrative Phrase','count':'Total Frequency','period':'Time Period'},
    text='count'
)#learned from the slides and lectures

#See ChatGPT respone No.4 in AI Documention in AI_Documnetation_Afreen_Baig
fig.update_layout(
    yaxis={'automargin':True},    # gives room for long labels
    legend_title='Period'
)
fig.show()

# Save to HTML
fig.write_html("../graphs/n-afreen-baig_before_after_oct2023.html")
# Save to png
fig.write_image("../graphs/n-afreen-baig_before_after_oct2023.png")
