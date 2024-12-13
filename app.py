from flask import Flask, jsonify, request
from flask import Flask, render_template
from pymongo import MongoClient
import random
import pandas as pd

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["prime_clone"]
collection = db["my_list"]

@app.route("/")
def home():
    return render_template("Recommended.html")

# Fetch all movies in the list
@app.route("/movies", methods=["GET"])
def get_movies():
    movies = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id field
    return jsonify(movies)

# Add a movie to the list
@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Movie added successfully!"}), 201

# Update a movie in the list
@app.route("/movies/<title>", methods=["PUT"])
def update_movie(title):
    data = request.json
    result = collection.update_one({"title": title}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Movie updated successfully!"})
    return jsonify({"message": "Movie not found!"}), 404

# Delete a movie from the list
@app.route("/movies/<title>", methods=["DELETE"])
def delete_movie(title):
    result = collection.delete_one({"title": title})
    if result.deleted_count:
        return jsonify({"message": "Movie deleted successfully!"})
    return jsonify({"message": "Movie not found!"}), 404

# Recommendation system
@app.route("/recommendations", methods=["GET"])
def recommendations():
    movies = list(collection.find({}, {"_id": 0}))
    recommendations = random.sample(movies, min(5, len(movies)))  # Return up to 5 random recommendations
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["prime_clone"]
collection = db["my_list"]

# Load CSV data
data = pd.read_csv("amazon_prime_titles.csv")
records = data.to_dict(orient="records")

# Insert records into MongoDB
collection.insert_many(records)
print("Data imported successfully!")
