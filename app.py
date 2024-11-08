import os
import psycopg2
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import pickle
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Connect to the PostgreSQL database using environment variables
conn = psycopg2.connect(
    dbname=os.getenv("PG_NAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT")
)
cursor = conn.cursor()

# Continue with the rest of your Flask setup and routes


# Load your trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Route to fetch symptoms from the database
@app.route('/get_symptoms', methods=['GET'])
def get_symptoms():
    cursor.execute("SELECT name FROM symptoms")
    symptoms = [row[0] for row in cursor.fetchall()]
    return jsonify(symptoms)

@app.route('/')
def index():
    return render_template('index.ejs')

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.json.get('symptoms', [])
    predicted_diseases = model.predict(symptoms)
    predictions = {'diseases': predicted_diseases[:5]}
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
