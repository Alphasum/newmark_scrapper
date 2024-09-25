import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd


st.set_page_config(
    page_title="My Streamlit App",
    layout="wide"  # Use 'wide' layout
)

# Custom CSS to control the width of the main content area
st.markdown(
    """
    <style>
    .reportview-container {
        width: 67% !important;  /* Set width to approximately 2/3 */
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def scrape_data(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the second table inside the 'panel-block'
        panel_blocks = soup.find_all('div', class_='panel-block')
        
        if len(panel_blocks) >= 2:
            second_panel_block = panel_blocks[1]
            
            # Find the h2 tag to get the second word for the 'source' column
            h2_tag = second_panel_block.find('h2')
            second_word = ''
            if h2_tag:
                h2_text = h2_tag.text.strip()
                second_word = h2_text.split()[1] if len(h2_text.split()) > 1 else ''
            
            # Find the table inside the second panel block
            second_table = second_panel_block.find('table', class_='typstable responsive')
            
            if second_table:
                # Create lists to store the table data
                headers = []
                rows = []

                # Extract table headers
                for header in second_table.find_all('th'):
                    headers.append(header.text.strip())
                
                # Extract table rows
                for row in second_table.find_all('tr'):
                    row_data = [td.text.strip() for td in row.find_all('td')]
                    if row_data:
                        rows.append(row_data)

                # Create a DataFrame from the scraped data
                df = pd.DataFrame(rows, columns=headers)

                # Add the 'source' column with the second word of the h2 tag
                df['source'] = second_word
                
                # Move 'source' column to the beginning
                df = df[['source'] + [col for col in df.columns if col != 'source']]

                # Add 'outcome' column based on score and tip
                df['outcome'] = df.apply(determine_outcome, axis=1)

                return df
            else:
                print("Table not found in the second panel-block.")
                return pd.DataFrame()  # Return an empty DataFrame
        else:
            print("Second panel-block not found.")
            return pd.DataFrame()  # Return an empty DataFrame
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame


# Function to determine the outcome based on score and tip
def determine_outcome(row):
    try:
        # Extract values
        score = row['SCORE']
        tip = row['TIP']

        # Check if score is valid
        if ':' in score:
            a, b = map(int, score.split(':'))
            # Outcome logic based on tip and score
            if tip == '1':
                return 'win' if a > b else 'loss' if a <= b else 'undefined'
            elif tip == '2':
                return 'win' if b > a else 'loss' if b <= a else 'undefined'
            elif tip == 'x':
                return 'win' if a == b else 'loss' if a != b else 'undefined'
        return 'undefined'
    except:
        return 'undefined'


# List of URLs to scrape
urls = [
    'https://typersi.com/typer,52146,Pignoufett.html',
    'https://typersi.com/typer,36030,BLX.hrml',
    'https://typersi.com/typer,45260,maer20.hrml',
    'https://typersi.com/typer,24813,kapsel007.html',
    'https://typersi.com/typer,26940,Vitpas.hrml',
    'https://typersi.com/typer,60957,vini1981.html',
    'https://typersi.com/typer,52724,marta81.html',
    'https://typersi.com/typer,47042,lech7321.html',
    'https://typersi.com/typer,31024,wp76.html',
    'https://typersi.com/typer,25116,wercia.html',
    'https://typersi.com/typer,36774,tomek3588.html',
    'https://typersi.com/typer,26439,Vinchenso.html',
    'https://typersi.com/typer,26896,Wilenma.html',
    'https://typersi.com/typer,40179,falandysza.html',
    'https://typersi.com/typer,26392,call911.html',
    'https://typersi.com/typer,58616,Recreza.html',
    'https://typersi.com/typer,51330,rbb7050.html',
    'https://typersi.com/typer,60735,Niki4.html',
    'https://typersi.com/typer,50752,Kolba1.html',
    'https://typersi.com/typer,25431,blacho4.html',
    'https://typersi.com/typer,60688,0758204499.html',
    'https://typersi.com/typer,60183,michuulol.html',
    'https://typersi.com/typer,30510,rafiar.html',
    'https://typersi.com/typer,55077,GOVERNOR.html',
    'https://typersi.com/typer,24695,Maczan88.html',
    'https://typersi.com/typer,50909,Giper13.html',
    'https://typersi.com/typer,60959,Koshin.html',
    'https://typersi.com/typer,58640,Volker.html',
    'https://typersi.com/typer,51361,DODONI.html',
    'https://typersi.com/typer,48000,BAYERN777.html',
    'https://typersi.com/typer,24999,Ruch1920.html',
    'https://typersi.com/typer,25633,andrus.html',
    'https://typersi.com/typer,51315,Fuji1978.html'
    
    # Add more URLs here
]


def run_scraper():
    final_df = pd.DataFrame()
    # Scrape each URL and append the data to final_df
    for url in urls:
        data = scrape_data(url)
        if not data.empty:
            final_df = pd.concat([final_df, data], ignore_index=True)
    # Write the final DataFrame to a CSV file
    final_df.to_csv('match_stakes_and_odds_with_source_and_outcome.csv', index=False)
    print("Data scraping and CSV creation complete.")

# Create buttons in the Streamlit app
if st.button("Get Data"):
    run_scraper()
    
csv_file = 'match_stakes_and_odds_with_source_and_outcome.csv'
# Create a download button
with open(csv_file, 'rb') as f:
    st.download_button(
        label="Download Match Stakes and Odds Data",
        data=f,
        file_name=csv_file,
        mime='text/csv'
    )
# Load the CSV file
data = pd.read_csv("match_stakes_and_odds_with_source_and_outcome.csv")

# Function to compute win rate by source
def compute_source_ranking(df):
    df_win = df[df['outcome'] == 'win'].groupby('source').size()
    df_total = df.groupby('source').size()
    win_rate = (df_win / df_total).fillna(0).sort_values(ascending=False).reset_index(name='win_rate')
    win_rate['rank'] = range(1, len(win_rate) + 1)
    return win_rate

# Function to filter games by day and source ranking
def filter_games_by_day(day, ranked_sources, df):
    filtered_df = df[df['DAY'] == day]
    filtered_df = filtered_df[filtered_df['source'].isin(ranked_sources['source'])]
    return filtered_df.merge(ranked_sources[['source', 'rank']], on='source').sort_values('rank')

# Function to group similar matches by match with different sources
def similar_matches_by_day(day, df):
    filtered_df = df[df['DAY'] == day]
    similar_matches = filtered_df.groupby('MATCH / LEAGUE').filter(lambda x: len(x['source'].unique()) > 1)
    grouped = similar_matches.sort_values('MATCH / LEAGUE')
    return grouped

# Function to plot wins, losses, and undefined outcomes per day
def plot_wins_losses(df):
    df_day_outcome = df.groupby(['DAY', 'outcome']).size().unstack(fill_value=0)

    fig, ax = plt.subplots()  # Create figure and axes
    df_day_outcome.plot(kind='bar', stacked=True, color={'win': 'green', 'loss': 'red', 'undefined': 'gray'}, ax=ax)
    ax.set_title('Wins, Losses, and Undefined Outcomes by Day')
    ax.set_xlabel('Day')
    ax.set_ylabel('Count')
    st.pyplot(fig)  # Pass the figure to st.pyplot()

# Function to plot pie chart of total wins, losses, and undefined outcomes
def plot_pie_chart(df):
    df_outcome = df['outcome'].value_counts()

    fig, ax = plt.subplots(figsize=(5,5))  # Create figure and axes
    ax.pie(df_outcome, labels=df_outcome.index, colors=['green', 'red', 'gray'], autopct='%1.1f%%', startangle=90)
    ax.set_title('Total Wins, Losses, and Undefined Outcomes')
    st.pyplot(fig)  # Pass the figure to st.pyplot()

# Streamlit App Layout
st.title('Sports Betting Analysis')

st.subheader('Download CSV File of data')



# Compute source ranking by win rate
source_ranking = compute_source_ranking(data)

# 1. Ranking of sources by winning rate
st.subheader('1. Ranking of Sources by Winning Rate')
st.dataframe(source_ranking[['rank', 'source', 'win_rate']])

# Prompt the user for the day (default is current day)
from datetime import datetime
default_day = datetime.now().day
selected_day = st.number_input('Select the day to filter games', min_value=1, max_value=31, value=default_day)

# 2. List of games filtered by day and ordered by source ranking
st.subheader(f'2. Games for Day {selected_day}, Ordered by Source Ranking')
filtered_games = filter_games_by_day(selected_day, source_ranking, data)
st.dataframe(filtered_games)

# 3. Similar Matches with Different Sources grouped by match
st.subheader(f'3. Similar Matches for Day {selected_day} Grouped by Match')
similar_matches = similar_matches_by_day(selected_day, data)
st.dataframe(similar_matches)

# 4. Graph of similar matches wins, losses, and undefined outcomes by day
st.subheader('4. Wins, Losses, and Undefined Outcomes by Day')
plot_wins_losses(data)

# 5. Pie chart of total similar match wins, losses, and undefined outcomes
st.subheader('5. Total Similar Match Wins, Losses, and Undefined Outcomes')
plot_pie_chart(data)
