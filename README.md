# TMDb Movies Data Analysis

This project analyzes and visualizes the TMDb 5000 Movie Dataset. The dataset contains metadata about movies including their budget, revenue, genres, production companies, release dates, ratings, and popularity.

The goal of the project is to clean the dataset, extract meaningful insights, and provide a summary of trends and statistics that can be used for further exploration or reporting.

## Dataset

Source: [Kaggle - TMDb Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)
File used: `tmdb_5000_movies.csv`

## Features and Analyses

1. **Data Cleaning**

   * Handled missing and zero values by replacing them with the mean of valid entries
   * Removed duplicate entries
   * Converted stringified dictionaries (e.g., genres, keywords, production companies) to Python objects
   * Extracted the main genre and primary production company for each movie
   * Removed rows with unusable or empty JSON-style fields

2. **Exploratory Analysis**

   * Most common genres and production companies
   * Movies with the highest budget, revenue, and ratings
   * Year with the most movie releases
   * Average runtime and language distributions
   * Average ratings by genre and language
   * Average popularity by genre and language
   * Correlation between budget and revenue
   * Comparison of top-rated vs most-voted movies
   * Top 10 movies by:

     * Rating
     * Revenue
     * Budget
     * Runtime

3. **Trend Analysis**

   * Trends in movie runtime over the years
   * Trends in ratings over the years

## Project Structure

* `tmdb_5000_movies.csv`: Raw dataset from Kaggle
* `cleaned_tmdb_movies.csv`: Cleaned version of the dataset after preprocessing
* `analysis.py`: Python script containing data cleaning and exploratory logic

## Tools Used

* Python
* Pandas
* ast (for parsing structured strings)

## Getting Started

1. Clone this repository or download the files
2. Install dependencies (see below)
3. Run `analysis.py` to execute the full pipeline
4. Review the printed results or load the cleaned CSV for further analysis or visualization

## Installation

You only need a few core packages:

```bash
pip install pandas
```

## Output

The script prints key insights directly to the terminal and exports a cleaned dataset (`cleaned_tmdb_movies.csv`) for additional exploration or dashboarding.

## License

This project is open-source and free to use for educational or non-commercial purposes.
