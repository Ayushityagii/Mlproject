from flask import Flask, request, render_template
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.exception import CustomException
import sys

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Extract form data
            gender = request.form.get('gender')
            race_ethnicity = request.form.get('ethnicity')
            parental_level_of_education = request.form.get('parental_level_of_education')
            lunch = request.form.get('lunch')
            test_preparation_course = request.form.get('test_preparation_course')
            reading_score = float(request.form.get('reading_score'))  # Correct field names
            writing_score = float(request.form.get('writing_score'))  # Correct field names

            # Create CustomData instance
            data = CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score
            )

            # Convert to DataFrame
            pred_df = data.get_data_as_data_frame()
            print(f"DataFrame for prediction: {pred_df}")

            # Initialize pipeline and make prediction
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            print(f"Prediction results: {results}")

            # Render result
            return render_template('home.html', results=results[0])

        except CustomException as ce:
            print(f"CustomException occurred: {ce}")
            return "A custom error occurred while processing your request.", 500
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while processing your request.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
       


      

