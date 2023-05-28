# Top 250 IMDB Movies Dashboard
This project provides a dashboard for exploring the top 250 movies on IMDB. It includes various visualizations and insights about the movies' ratings, release years, directors, and more.
## Requirements
To run this project, make sure you have the following dependencies installed:

* Dash
* Plotly
* Beautiful Soup
* Requests
* Pandas
You can install these dependencies using pip:
```bash
pip install dash plotly beautifulsoup4 requests pandas
```
## Getting Started
To use this dashboard, follow these steps:

1. Clone the repository from GitHub:
  ```bash
  git clone git@github.com:Ewins518/IMBD-with-Dash.git
  ```
2. Navigate to the project directory:
  ```bash
  cd IMBD-with-Dash 
  ```
3. Run the following command to start the application:
   ```bash
   python3 app.py
   ```
4. Open a web browser and go to http://localhost:8050 to access the dashboard.

## Features

The dashboard provides the following features and visualizations:

### Top Movies by IMDB Rating
Shows a dropdown to select the number of top movies to display (e.g., top 5, top 10, etc.).
Displays a horizontal bar chart of the selected number of top-rated movies.
The movies are categorized by rating, and the color indicates the release year.

![Screenshot](/screenshot/1.png)


### Distribution of the Variables
Shows a dropdown to select the attribute for distribution (e.g., rating, release date, etc.).
Displays a histogram with a box plot, representing the distribution of the selected attribute.

![Screenshot](/screenshot/2.png)

### Percentage Distribution of Movies by Decade
Displays a donut chart showing the percentage distribution of movies by decade.
The center hole size and label placement can be customized.
![Screenshot](/screenshot/3.png)

### Number of Films Grouped by Date
Shows a dropdown to select the number of top years to display (e.g., top 5, top 10, etc.).
Displays a pie chart with a large hole at the center, representing the number of films grouped by release year.
The percentage and labels are shown inside the sectors of the chart.
![Screenshot](/screenshot/4.png)

### Average Rating per Decade
Displays a bar chart showing the changes in average rating and the number of movies by decade.
The total average rating line is also included.
![Screenshot](/screenshot/5.png)

### Data Source
The data for this project is scraped from the IMDb website. The code fetches the top 250 movies from the IMDb website and extracts movie titles, directors, ratings, and release years.

