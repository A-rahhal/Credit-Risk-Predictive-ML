from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the model and columns
model = joblib.load('credit_risk_model.pkl')
model_columns = joblib.load('model_columns.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        input_data = {
            'person_age': int(request.form['person_age']),
            'person_income': float(request.form['person_income']),
            'person_emp_length': float(request.form['person_emp_length']),
            'loan_amnt': float(request.form['loan_amnt']),
            'loan_int_rate': float(request.form['loan_int_rate']),
            'loan_percent_income': float(request.form['loan_percent_income']),
            'person_home_ownership': request.form['person_home_ownership'],
            'loan_intent': request.form['loan_intent']
        }

        # Convert to DataFrame
        query_df = pd.DataFrame([input_data])
        
        # Encoding and aligning with model columns
        query_df = pd.get_dummies(query_df).reindex(columns=model_columns, fill_value=0)

        # Make prediction
        prediction = model.predict(query_df)[0]
        probability = model.predict_proba(query_df)[0][1]

        result = "High Risk (Default)" if prediction == 1 else "Low Risk (Safe)"
        color = "danger" if prediction == 1 else "success"

        return render_template('index.html', 
                               prediction_text=f'Result: {result}',
                               prob_text=f'Risk Probability: {probability:.2%}',
                               alert_class=color)
    
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}", alert_class="warning")

if __name__ == "__main__":
    app.run(debug=True)