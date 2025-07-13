import pandas as pd
import ast

df = pd.read_csv("./tmdb_5000_movies.csv")

df.drop_duplicates(inplace=True)

df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df.dropna(subset=["overview", "release_date"], inplace=True)

def replace_invalid (col_name, round_to_int = True):
    #Calculate the mean value for the column, from fields whose values are greater than 0
    mean_val = df.loc[df[col_name] > 0, col_name].mean()

    # Round the number if required
    if(round_to_int):
        mean_val = round(mean_val)
    
    # REplace the NA's with the mean value
    df.fillna({col_name: mean_val}, inplace=True)
    
    # If the value for that field in the column is 0, replace it with the mean value
    df.loc[df[col_name] == 0, col_name] = mean_val

    return mean_val

replace_invalid("budget")
replace_invalid("revenue")
replace_invalid("vote_count")
replace_invalid("vote_average", False)
mean_runtime = round(replace_invalid("runtime", False), 2)

# Remove rows that have a value of "[]"
for col in ["genres", "keywords", "production_companies"]:
    df = df[df[col] != "[]"]

# Converts a "stringed dictionary" to a proper dictionary and return the name property of the first item in the dictionary, if it's a dictionary and if the dictionary has any objects inside
def extract_first_value (str):
    try:
        new_list = ast.literal_eval(str)

        if isinstance(new_list, list) and new_list:
            return new_list[0]["name"]
    except(ValueError, SyntaxError):
        pass
    return None

# Create a new columns which have the first value from the "stringed-dictionaries"
df["main_genre"] = df["genres"].apply(extract_first_value)
df["main_company"] = df["production_companies"].apply(extract_first_value)


def max_value(column_name):
    value = df[column_name].max()
    id = df[column_name].idxmax()
    
    return value, id

def top_n_movies (column_name, limit=10):
    return df.nlargest(limit, column_name)[["original_title", column_name]]


# Most common genre
genre_count = df["main_genre"].value_counts()
most_common_genre = genre_count.idxmax()
most_common_count = genre_count.max()
print(f"The most common genre is {most_common_genre} which occurs a total of {most_common_count} times.\n")

# Movie with highest average rating
highest_rating, highest_rating_id = max_value("vote_average")
highest_rating_name = df.loc[highest_rating_id, "original_title"]
print(f"Top rated movie with a rating of {highest_rating} is \"{highest_rating_name}\".\n")

# Year with the most moive release
df["release_year"] = df["release_date"].dt.year
year_counts = df.groupby("release_year")["original_title"].count()
most_release_year = year_counts.idxmax()
most_release_count = year_counts.max()
print(f"The year with the most released movies is {most_release_year} with {most_release_count} movies in total.\n")

# Average runtime across all movies
print(f"The average runtime across all movies is {mean_runtime:.2f} minutes.\n")

# Most common languages
languages_count = df["original_language"].value_counts()
most_common_language = languages_count.idxmax()
most_common_count = languages_count.max()
print(f"The most common language was \"{most_common_language}\" with {most_common_count} entries.\n")

    
# Movies with the highest budget and revenue
max_budget, max_budget_id = max_value("budget")
max_budget_title = df.loc[max_budget_id, "original_title"]
print(f"The movie with the highest budget is \"{max_budget_title}\" with a budget of ${max_budget}.")

max_revenue, max_revenue_id = max_value("revenue")
max_revenue_title = df.loc[max_revenue_id, "original_title"]
print(f"The movie with the highest revenue is \"{max_revenue_title}\" with a revenue of ${max_revenue}.\n")

# Average rating for each genre
average_rating_per_genre = df.groupby("main_genre")["vote_average"].mean()
print("The average rating per genre are:")
print(average_rating_per_genre)

# Average rating for each language
average_rating_per_language = df.groupby("original_language")["vote_average"].mean()
print("The average rating per language are:")
print(average_rating_per_language)

# Average popularity per genre and language
average_popularity_per_genre = df.groupby("main_genre")["popularity"].mean()
average_popularity_per_language = df.groupby("main_genre")["popularity"].mean()
print("\nThe average popularity per language are:")
print(average_popularity_per_language)
print("\nThe average popularity per genre are:")
print(average_popularity_per_genre)

# Trend in ratings and runtimes over the years
print("\nBelow is the trend in runtime and ratings respectively, over the years:")
print(df.groupby("release_year")["runtime"].mean())
print(df.groupby("release_year")["vote_average"].mean())

# Correlation between budget and revenue
budget_revenue_correlation = df["budget"].corr(df["revenue"])
print(f"The correlation between budget and revenue is {budget_revenue_correlation:.2f} which indicates that higher-budget films are more likely to earn more revenue, but spending more doesn't guarantee success. The relationship is not perfectly linear.")

# Top-rated vs most-rated movie
most_rated_movie_count = df["vote_count"].max()
most_rated_movie_id = df["vote_average"].idxmax()
most_rated_movie_name = df.loc[most_rated_movie_id, "original_title"]
print(f"\nWe can see that the top rated movie \"{highest_rating_name}\" has an average rating of {highest_rating}, while the most rated movie {most_rated_movie_name} has an total rating count of {most_rated_movie_count}\n")

# Top 10 highest rated movies
top_ten_highest_rated = top_n_movies("vote_average")
print("The top 10 highest rated movies are:")
print(top_ten_highest_rated)

# Top 10 longest movies
top_ten_longest = top_n_movies("runtime")
print("\nThe top 10 movies with the longest runtimes are:")
print(top_ten_longest)

# Top 10 movies with the highest revenue
top_ten_highest_revenue = top_n_movies("revenue")
print("\nThe top 10 movies with highest revenues are:")
print(top_ten_highest_revenue)

# Top 10 movies with the highest budget
top_ten_highest_budget = top_n_movies("budget")
print("\nThe top 10 movies with highest budgets are:")
print(top_ten_highest_budget)

# Top recurring production companies
most_recurring_companies = df["main_company"].value_counts()
most_recurring_company = most_recurring_companies.idxmax()
print(f"The most recurring company is {most_recurring_company}.")

# Most successful genre financially
most_successful_genre = df.groupby("main_genre")["revenue"].median().idxmax()
most_successful_genre_average = df.groupby("main_genre")["revenue"].median().max()
print(f"\nOn average, {most_successful_genre} had the best revenue with ${round(most_successful_genre_average)}, making it the most successful genre financially.")


df.to_csv("cleaned_tmdb_movies.csv", index=False)
print("\nCleaned dataset saved as 'cleaned_tmdb_movies.csv'")