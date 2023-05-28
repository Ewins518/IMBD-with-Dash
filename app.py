import dash
from dash import dcc,html
from dash.dependencies import Input, Output
from bs4 import BeautifulSoup
import requests
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_data():

    # Scraping the IMDb website
    url = 'https://www.imdb.com/chart/top/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.select('td.titleColumn')
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.contents for b in soup.select('td.imdbRating strong')]

    # Extracting movie titles, directors, and ratings
    titles = [movie.text for movie in movies]
    directors = [title.split('(')[0].strip() for title in crew]
    ratings = [float(rating[0]) for rating in ratings]
     # Extract the release years
    movie_titles = soup.find_all("td", class_="titleColumn")

    release_years = [int(title.span.text.strip("()")) for title in movie_titles]

    import re

    clean_movies = []

    for movie in titles:
        clean_movie = re.sub(r'\n\s+\d+\.\n\s+', '', movie)  # Remove leading numbers and dots
        clean_movie = re.sub(r'\s+\(\d+\)\n', '', clean_movie)  # Remove year in parentheses
        clean_movies.append(clean_movie.strip())

    df = pd.DataFrame(clean_movies, columns=["Titles"])
    df["release_years"] = release_years
    df["Directors"] = directors
    df["Rating"] = ratings

    return df


def plot_distribution(x):
    # Build a histogram of the rating distribution with boxplot
    fig = px.histogram(
        data,
        x=x,
        nbins=20,
        color_discrete_sequence=['indianred'],
        marginal='box',
        text_auto=True,
        title='Rating distribution',
        width=1000,
        height=800    
    )

    return fig

def avg_rating_per_decades():
    data['Decade'] = 10 * (data['release_years'] // 10) 
    # Let's group the rating by decade
    decade_rating = round(data.groupby(by='Decade', as_index=False)['Rating'].mean(), 2)

    # Grouping the number of movies by decade
    decade_movie_count = data.groupby(by='Decade', as_index=False)['Titles'].count()

    # Merge the resulting tables
    merged = decade_rating.merge(decade_movie_count)
    merged = merged.rename(columns={'Titles' : 'Movie_count', 'Rating' : 'Mean_rating'})

    return merged


def plot_avg_rating_per_decades():
    # Let's build a bar chart showing the changes in the average rating and 
    # number of movies by decade with a total average rating line
    fig = go.Figure()

    merged = avg_rating_per_decades()
    # 1. The bar chart of average rating by decade
    fig.add_trace(trace=go.Bar(
        x=merged['Decade'],
        y=merged['Mean_rating'],
        text=merged['Mean_rating'],
        marker_color='red',
        name='Averege rating'
    ))
    # Specify the angle of rotation of the text for its identical vertical display
    fig.update_traces(textangle = 0)

    # 2. The bar chart of movies quantity by decade
    fig.add_trace(trace=go.Bar(
        x=merged['Decade'],
        y=merged['Movie_count'],
        text=merged['Movie_count'],
        marker_color='blue',
        name='Count of movies'
    ))
    # Specify the angle of rotation of the text for identical vertical display of text
    fig.update_traces(textangle = 0)

    # 3. The line graph showing the total average rating
    fig.add_trace(trace=go.Scatter(
        x=[1915, 2025],
        y=[8.25, 8.25],
        mode='lines',
        marker_color='green',
        name='Total averege rating line = 8.25'
         ))

    # Title and size of the chart field
    fig.update_layout(title='Average rating and number of movies by decade',
                      height=600,
                      width=1000)

    # X-axis title and slope angle for decades
    fig.update_xaxes(title='Decade', tickangle = 60)

    return fig

def percentage_movies_by_decades():

    merged = avg_rating_per_decades()

    merged['Movie_percent'] = merged['Movie_count'] * 100 / sum(merged['Movie_count'])
    # Let's create a donut chart showing the percentage of movies by decade
    fig = go.Figure()

    # The donut chart
    fig.add_trace(trace=go.Pie(
        labels=merged['Decade'],
        values=merged['Movie_percent'],
        pull=[0, 0, 0, 0.08, 0, 0, 0.1, 0.12, 0.17, 0.15, 0], # At the list, we set the values for the share 
                                                              # of the output of the sectors of the circle
        hole=0.1 # Center hole size
    ))

    # Set the location of the text within the sector
    # and in the information we combine the display of percent and decade
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Title and size of the chart field
    fig.update_layout(title='Percentage distribution of movies by decade',
                      height=800,
                      width=1000)
    return fig

def top_n_movies(n):
    # Sort movies by rating and release date
    top = data.sort_values(by=['Rating', 'release_years'], ascending=[False, True]).nlargest(n, columns='Rating')
    # Let's build a horizontal bar chart. 
    # Films are categorized by rating. 
    # The color highlights the release year.
    fig = px.bar(
        top,
        x='Rating',
        y='Titles',
        color='release_years',
        text_auto=True,
        title=f'Top {n} movies by IMDB rating',
        labels={'Movie_Name' : 'Name of movie',
                'Rating' : 'Rating of movie',
                'Release_date' : 'Date of movie release'},
        width=800,
        height=600    
    )

    # Specify the angle of rotation of the text for its identical vertical display
    fig.update_traces(textangle = 0)
    return fig 

def number_of_films_group_date(n):
    # Count the number of films and group by release date. 
    # Sort by movie title and year of release/
    top_n_years = data.groupby(by='release_years',
                                   as_index=False)['Titles'].count().sort_values(
                                                                                by=['Titles', 'release_years'],
                                                                                ascending=False
                                                                               )
    # Take the first 10 rows of the table
    top_data = top_n_years.head(n).rename(columns={'release_years' : 'Release year',
                                                 'Titles' : 'Movie count'}) 


    # Let's build a pie chart showing the percentage of movies by year
    fig = go.Figure()

    # Pie chart with a big hole at the centre
    fig.add_trace(go.Pie(
       values=top_data['Movie count'],
       labels=top_data['Release year'].sort_values(ascending=False),
       hole=0.8,
       textinfo='label+percent'     
    ))

    # Title, text at the centre and size of the chart field
    fig.update_layout(title=f'Top {n} years by movies quantity',
                      margin=dict(l=0, r=0, t=30, b=0),
                      annotations=[dict(text='IMDB Rating <br> Years with movie hits', x=0.5, y=0.5, font_size=20, showarrow=False)],
                      height=800,
                      width=1000)
    return fig


def init_figure():
    "This function initiate all the needed figure to start the app."
    return top_n_movies(10),plot_distribution("Rating"), percentage_movies_by_decades(), number_of_films_group_date(5), plot_avg_rating_per_decades()

data = get_data()

init_top_n_movies, init_plot_distribution, init_percentage_movies_by_decades, init_number_of_films_group_date, init_plot_avg_rating_per_decades = init_figure()

"""Building the app"""
# ---------------------------------------------------------------------------

# Initializing the app
app = dash.Dash(__name__)
server = app.server



# Building the app layout
app.layout = html.Div([
    html.H1("Top 250 IMDB Movies DashBoard", style={"text-align": "center"}),
    html.Br(),
    html.Div([
        html.Br(),
        html.H2("Top Movies by IMDB rating", style={"text-align": "center"}),
        html.Br(),
        dcc.Dropdown(id="select_keyword",
                     options=[
                         dict(label="Top 5", value=5),
                         dict(label="Top 10", value=10),
                         dict(label="Top 20", value=20),
                         dict(label="Top 50", value=50)],
                     multi=False,
                     value=10,
                     style={"width": "40%"}
                     ),
html.Div(
        dcc.Graph(id="top_n_movies_plot", figure=init_top_n_movies),
                style={"display": "flex", "justify-content": "center"}

)
    ]),

    html.Div([
        html.Br(),
        html.H2("Distribution of the variables", style={"text-align": "center"}),
        html.Br(),
        dcc.Dropdown(id="select_attribute",
                     options=[
                         dict(label="Rating", value='Rating'),
                         dict(label="Release Date", value='release_years'),
                         ],
                     multi=False,
                     value="Rating",
                     style={"width": "60%", 'display': 'inline-block'}
                     ),
        
html.Div(
        dcc.Graph(id="distribution_plot", figure=init_plot_distribution),
        style={"display": "flex", "justify-content": "center"}
)
    ]),

    html.Div([
        html.Br(),
        html.H2("Percentage distribution of movies by decade", style={"text-align": "center"}),
        html.Br(),
        
html.Div(
        dcc.Graph(id="movies_by_decade", figure=init_percentage_movies_by_decades),
        style={"display": "flex", "justify-content": "center"}

)
    ]),

        html.Div([
        html.Br(),
        html.H2("Number of films group by date", style={"text-align": "center"}),
        dcc.Dropdown(id="select_keyword_2",
                     options=[
                         dict(label="Top 5", value=5),
                         dict(label="Top 10", value=10),
                         dict(label="Top 15", value=15),
                         ],
                     multi=False,
                     value=5,
                     style={"width": "40%"}
                     ),
        html.Br(),
html.Div(
        dcc.Graph(id="group_by_date", figure=init_number_of_films_group_date),
                style={"display": "flex", "justify-content": "center"}
        )
    ]),

    html.Div([
        html.Br(),
        html.H2("Average rating per decade", style={"text-align": "center"}),
        html.Br(),

html.Div(
        dcc.Graph(id="rating_per_decade", figure=init_plot_avg_rating_per_decades),
        style={"display": "flex", "justify-content": "center"}
    )

    ])
])

# Defining the application callbacks

@app.callback(
    Output("top_n_movies_plot", "figure"),
    Input("select_keyword", "value")
)
def update_top_n_movies_plot(value):
    return top_n_movies(value)


@app.callback(
    Output("distribution_plot", "figure"),
    Input("select_attribute", "value"),
)
def update_distribution_plot(value):
    return plot_distribution(value)


@app.callback(
    Output("group_by_date", "figure"),
    Input("select_keyword_2", "value")
)
def update_group_by_date_plot(value):
    return number_of_films_group_date(value)




if __name__ == "__main__":
    data = get_data()
    app.run_server()


