from model_pipeline import pipeline, disease_mapping
import pandas as pd
import re



def predict_disease(message_history):
    # Extract all user messages
    symptoms = " ".join([msg["content"] for msg in message_history if msg["role"] == "user"])
    
    # Create initial input for the pipeline
    initial_input = {'symptoms': symptoms}
    
    # Pass the input through the pipeline and make prediction
    result = pipeline.predict([initial_input])
    
    # Map the result to disease name
    disease_name = disease_mapping[result[0]]
    return disease_name


def get_drug_recommendations(predicted_disease, drugs_df):
    # Convert predicted disease to lowercase
    predicted_disease_lower = predicted_disease.lower()
    
    # Convert medical_condition column to lowercase and handle NaN values
    drugs_df['medical_condition_lower'] = drugs_df['medical_condition'].fillna('').str.lower()
    
    # Use regular expression to find matching conditions
    matching_drugs = drugs_df[drugs_df['medical_condition_lower'].apply(lambda x: bool(re.search(predicted_disease_lower, str(x))))]
    
    # Get unique drug names
    unique_drugs = matching_drugs['drug_name'].unique()
    
    return list(unique_drugs)