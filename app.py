import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

import streamlit as st
# Define custom CSS with the provided image URL and transparent sidebar
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://i0.wp.com/elplanetaurbano.com/wp-content/uploads/2020/10/spotify-argentina.jpg?fit=640%2C430&ssl=1');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Sidebar Styling (transparent background) */
    .st-emotion-cache-6qob1r  {
        background: rgba(255, 255, 255, 0); /* Transparent background */
        color: white;
    }
    
    /* Optional: Adjust text color for readability */
    .css-1l02z6v .css-1v0mbdj {
        color: white; /* Adjust text color */
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
# # Define CSS styles for Argentina flag colors
# css = """
# <style>
# /* Background Gradient (light blue and white) */
# .stApp {
#     background: linear-gradient(135deg, #74b9ff, #ffffff);
# }

# /* Sidebar Styling (blue background with white text) */
# .css-1l02z6v {
#     background: linear-gradient(135deg, #3498db, #a2c2e6);
#     color: white;
# }

# /* Title Styling */
# .css-18e3f3m {
#     color: #0033a0;  /* Dark blue */
#     font-size: 2.5rem;
#     text-align: center;
# }

# /* Subheader Styling */
# .css-1co5ekb {
#     color: #0033a0;  /* Dark blue */
# }

# /* Bar Chart Styling */
# .css-1v6fa8r {
#     background-color: #ffffff;
#     border-radius: 10px;
# }
# </style>
# """

# Load CSS in Streamlit
# st.markdown(css, unsafe_allow_html=True)


# Assuming df_argentina is already loaded in your environment
df = pd.read_csv('data.csv')

# Title of the dashboard
st.title('Argentina Spotify Dashboard')

# Sidebar for selecting what to visualize
st.sidebar.title('Visualization Selector')
visualization = st.sidebar.radio('Select Visualization:', 
                                 ('DataFrame', 'Summary', 'Answer Questions'))

# Display the selected visualization
if visualization == 'DataFrame':
    st.subheader('DataFrame')
    st.dataframe(df)

elif visualization == 'Summary':
    st.subheader('Data Summary')
    st.write(df.describe())
  
# Extend the 'Answer Questions' section with more options
elif visualization == 'Answer Questions':
    st.subheader('Answer Questions')

    # Define the questions and their corresponding logic
    question = st.sidebar.selectbox('Select a Question:', 
                                    ('Top 10 most streamed songs',
                                     'Average streams per artist',
                                     'Trend of streams over time',
                                     'Top 5 artists by total streams',
                                     'Histogram of song ranks',
                                     'Comparison of streams between two artists',
                                     'Bar chart of trends',
                                     'Argentina streams over time',
                                     'Most monthly streams each year'))

    # Top 10 most streamed songs (code as previously fixed)
    if question == 'Top 10 most streamed songs':
        st.subheader('Top 10 Most Streamed Songs')
        top_10_songs = df.dropna(subset=['streams']).nlargest(10, 'streams')
        top_10_songs.set_index('title', inplace=True)
        st.bar_chart(top_10_songs['streams'])

    # Average streams per artist
    elif question == 'Average streams per artist':
        st.subheader('Average Streams per Artist')
        if 'artist' in df.columns and 'streams' in df.columns:
            avg_streams = df.dropna(subset=['streams']).groupby('artist')['streams'].mean().sort_values(ascending=False)
            st.bar_chart(avg_streams)
        else:
            st.write('The required columns are not available in the dataset.')

    # Trend of streams over time
    elif question == 'Trend of streams over time':
        st.subheader('Trend of Streams Over Time')
        if 'date' in df.columns and 'streams' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            streams_over_time = df.dropna(subset=['streams']).groupby('date')['streams'].sum()
            st.line_chart(streams_over_time)
        else:
            st.write('The required columns are not available in the dataset.')

    # Top 5 artists by total streams
    elif question == 'Top 5 artists by total streams':
        st.subheader('Top 5 Artists by Total Streams')
        if 'artist' in df.columns and 'streams' in df.columns:
            top_artists = df.dropna(subset=['streams']).groupby('artist')['streams'].sum().nlargest(5)
            st.bar_chart(top_artists)
        else:
            st.write('The required columns are not available in the dataset.')

    # Histogram of song ranks
    elif question == 'Histogram of song ranks':
        st.subheader('Histogram of Song Ranks')
        if 'rank' in df.columns:
            bins = st.sidebar.slider('Number of Bins:', min_value=5, max_value=50, value=10)
            fig, ax = plt.subplots()
            ax.hist(df['rank'], bins=bins, edgecolor='black')
            ax.set_xlabel('Rank')
            ax.set_ylabel('Frequency')
            ax.set_title('Histogram of Song Ranks')
            st.pyplot(fig)
        else:
            st.write('The required column is not available in the dataset.')

    # Comparison of streams between two artists
    elif question == 'Comparison of streams between two artists':
        st.subheader('Comparison of Streams Between Two Artists')
        if 'artist' in df.columns and 'streams' in df.columns:
            artists = st.sidebar.multiselect('Select Two Artists:', df['artist'].unique(), default=df['artist'].unique()[:2])
            if len(artists) == 2:
                artist_data = df[df['artist'].isin(artists)].dropna(subset=['streams']).groupby(['artist', 'date'])['streams'].sum().unstack().fillna(0)
                st.line_chart(artist_data)
            else:
                st.write('Please select exactly two artists.')
        else:
            st.write('The required columns are not available in the dataset.')

    # New: Bar chart of trends (e.g., by artist or over time)
   # New: Bar chart of trends (counts from the 'trend' column)
    elif question == 'Bar chart of trends':
        st.subheader('Bar Chart of Trends')
        
        if 'trend' in df.columns:  # Ensure 'trend' column is available
            fig, ax = plt.subplots()
            df['trend'].value_counts().plot(kind='bar', ax=ax)  # Bar chart of 'trend' counts
            ax.set_title('Trend Counts')
            ax.set_xlabel('Trend')
            ax.set_ylabel('Count')
            
            st.pyplot(fig)  # Display the plot in Streamlit
        else:
            st.write('The "trend" column is not available in the dataset.')


    # New: Argentina streams over time
    # New: Line plot of streams over time
    elif question == 'Argentina streams over time':
      st.subheader('Argentina Streams Over Time')

      if 'date' in df.columns and 'streams' in df.columns:  # Ensure required columns are available
          df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format

          # Create the line plot
          fig, ax = plt.subplots()
          df.plot(x='date', y='streams', kind='line', ax=ax)  # Line plot of streams over time
          ax.set_title('Argentina Streams Over Time')
          ax.set_xlabel('Date')
          ax.set_ylabel('Streams')
          
          st.pyplot(fig)  # Display the plot in Streamlit
      else:
          st.write('The "date" and/or "streams" columns are not available in the dataset.')




    # New: Most monthly streams each year
    elif question == 'Most monthly streams each year':
        st.subheader('Most Monthly Streams Each Year')
        if 'date' in df.columns and 'streams' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month

            # Group by year and month, then find the month with the max streams each year
            monthly_streams = df.dropna(subset=['streams']).groupby(['year', 'month'])['streams'].sum().reset_index()
            max_monthly_streams = monthly_streams.loc[monthly_streams.groupby('year')['streams'].idxmax()]

            # Plot the results
            fig, ax = plt.subplots()
            ax.bar(max_monthly_streams['year'], max_monthly_streams['streams'], color='orange')
            ax.set_xlabel('Year')
            ax.set_ylabel('Streams')
            ax.set_title('Most Monthly Streams Each Year')
            st.pyplot(fig)
        else:
            st.write('The required columns are not available in the dataset.')


# Button to show data info
if st.sidebar.button('Show Data Info'):
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
