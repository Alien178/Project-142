# Import necessary modules
from flask import Flask, jsonify, request

# Import data and functions from other modules
from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

# Create a Flask app instance
app = Flask(__name__)

# Define a route to get the next article
@app.route("/get-article")
def get_article():
    # Prepare movie data from all_articles
    movie_data = {
        "url": all_articles[0][11],
        "title": all_articles[0][12],
        "text": all_articles[0][13],
        "lang": all_articles[0][14],
        "total_events": all_articles[0][15]
    }

    # Return the movie data as JSON response with a success status
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

# Define a route to mark an article as liked
@app.route("/liked-article", methods=["POST"])
def liked_article():
    # Get the first article in all_articles
    article = all_articles[0]
    
    # Append the article to the liked_articles list
    liked_articles.append(article)
    
    # Remove the article from all_articles
    all_articles.pop(0)
    
    # Return a success status as JSON response with HTTP status code 201
    return jsonify({
        "status": "success"
    }), 201

# Define a route to mark an article as not liked
@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    # Get the first article in all_articles
    article = all_articles[0]
    
    # Append the article to the not_liked_articles list
    not_liked_articles.append(article)
    
    # Remove the article from all_articles
    all_articles.pop(0)
    
    # Return a success status as JSON response with HTTP status code 201
    return jsonify({
        "status": "success"
    }), 201

# Define a route to get popular articles
@app.route("/popular-articles")
def popular_articles():
    # Prepare data for popular articles
    article_data = []
    for article in output:
        d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        article_data.append(d)
    
    # Return popular article data as JSON response with a success status
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

# Define a route to get recommended articles based on liked articles
@app.route("/recommended-articles")
def recommended_articles():
    # Initialize a list to store all recommended articles
    all_recommended = []

    # Loop through liked articles and get recommendations
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)

    # Remove duplicates from the recommended articles list
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))

    # Prepare data for recommended articles
    article_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(_d)

    # Return recommended article data as JSON response with a success status
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

# Run the Flask app if this script is the main entry point
if __name__ == "__main__":
    app.run()
